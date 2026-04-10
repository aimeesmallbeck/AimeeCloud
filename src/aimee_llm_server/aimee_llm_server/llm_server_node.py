#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
ROS2 Node for LLM Server (Action Server)

This node wraps the LLMServerBrick and provides:
- ROS2 Action server for LLMGenerate action
- Streaming feedback during generation
- Preemption support for responsive interrupt handling

Usage:
    ros2 run aimee_llm_server llm_server_node
"""

import asyncio
import logging
import sys
import threading
from typing import Optional

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.action.server import ServerGoalHandle
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rcl_interfaces.msg import SetParametersResult

from aimee_msgs.action import LLMGenerate

# Import the brick
from aimee_llm_server.brick.llm_server import (
    LLMServerBrick, LLMRequest, LLMFeedback, LLMResult
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LLMServerNode(Node):
    """
    ROS2 Node for LLM Action Server.
    
    This node implements the LLMGenerate action server with:
    - Streaming feedback (partial responses)
    - Preemption support (cancel ongoing generation)
    - Session context management
    """
    
    def __init__(self):
        super().__init__('llm_server')
        
        # Declare parameters
        self.declare_parameters(namespace='', parameters=[
            ('backend', 'llama_cpp_server'),
            ('server_url', 'http://localhost:8080'),
            ('model_path', ''),
            ('default_max_tokens', 150),
            ('default_temperature', 0.7),
            ('timeout_seconds', 60.0),
            ('max_context_length', 2048),
            ('debug', False),
        ])
        
        # Get parameters
        backend = self.get_parameter('backend').value
        server_url = self.get_parameter('server_url').value
        model_path = self.get_parameter('model_path').value
        default_max_tokens = self.get_parameter('default_max_tokens').value
        default_temperature = self.get_parameter('default_temperature').value
        timeout_seconds = self.get_parameter('timeout_seconds').value
        max_context_length = self.get_parameter('max_context_length').value
        debug = self.get_parameter('debug').value
        
        # Create the brick
        self._brick = LLMServerBrick(
            backend=backend,
            server_url=server_url,
            model_path=model_path if model_path else None,
            default_max_tokens=default_max_tokens,
            default_temperature=default_temperature,
            timeout_seconds=timeout_seconds,
            max_context_length=max_context_length,
            debug=debug
        )
        
        # Async handling
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._shutdown_event = threading.Event()
        
        # State
        self._initialized = False
        
        # Action server (use ReentrantCallbackGroup for concurrent goals)
        self._action_server = ActionServer(
            self,
            LLMGenerate,
            '/llm/generate',
            execute_callback=self._execute_callback,
            goal_callback=self._goal_callback,
            cancel_callback=self._cancel_callback,
            callback_group=ReentrantCallbackGroup()
        )
        
        self.get_logger().info(
            f"LLMServerNode initialized:\n"
            f"  Backend: {backend}\n"
            f"  Server URL: {server_url}\n"
            f"  Max tokens: {default_max_tokens}\n"
            f"  Temperature: {default_temperature}"
        )
        
        # Start async thread
        self._start_async_thread()
    
    def _start_async_thread(self):
        """Start async event loop in background thread."""
        def run_async_loop():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            
            try:
                self._loop.run_until_complete(self._async_main())
            except Exception as e:
                self.get_logger().error(f"Async loop error: {e}")
            finally:
                self._loop.close()
        
        self._thread = threading.Thread(target=run_async_loop, daemon=True)
        self._thread.start()
    
    async def _async_main(self):
        """Main async coroutine."""
        try:
            await self._brick.initialize()
            self._initialized = True
            self.get_logger().info("Brick initialized successfully")
            
            # Keep running
            while not self._shutdown_event.is_set():
                await asyncio.sleep(0.1)
                
        except Exception as e:
            self.get_logger().error(f"Async main error: {e}")
    
    def _goal_callback(self, goal_request):
        """
        Accept or reject a goal.
        
        Called when a new goal is received.
        """
        self.get_logger().info(
            f"Received goal request: session={goal_request.session_id}, "
            f"max_tokens={goal_request.max_tokens}"
        )
        
        if not self._initialized:
            self.get_logger().error("Not initialized, rejecting goal")
            return GoalResponse.REJECT
        
        return GoalResponse.ACCEPT
    
    def _cancel_callback(self, goal_handle):
        """
        Accept or reject a cancel request.
        
        Called when a cancel request is received.
        """
        self.get_logger().info("Received cancel request")
        
        # Run preempt in async loop
        if self._loop:
            asyncio.run_coroutine_threadsafe(
                self._brick.preempt(),
                self._loop
            )
        
        return CancelResponse.ACCEPT
    
    async def _execute_callback(self, goal_handle: ServerGoalHandle):
        """
        Execute the LLM generation goal.
        
        This is the main execution function that:
        1. Creates LLMRequest from goal
        2. Generates text with streaming feedback
        3. Handles preemption
        4. Returns final result
        """
        goal = goal_handle.request
        self.get_logger().info(f"Executing goal: {goal.session_id}")
        
        # Create request
        request = LLMRequest(
            prompt=goal.prompt,
            system_context=goal.system_context,
            max_tokens=goal.max_tokens if goal.max_tokens > 0 else 150,
            temperature=goal.temperature if goal.temperature > 0 else 0.7,
            stream=goal.stream,
            session_id=goal.session_id
        )
        
        # Feedback helper
        def publish_feedback(feedback: LLMFeedback):
            """Publish streaming feedback."""
            if goal.stream:
                fb_msg = LLMGenerate.Feedback()
                fb_msg.partial_response = feedback.partial_response
                fb_msg.tokens_generated = feedback.tokens_generated
                fb_msg.tokens_total = feedback.tokens_total
                fb_msg.is_complete = feedback.is_complete
                fb_msg.current_word = feedback.current_word
                
                goal_handle.publish_feedback(fb_msg)
        
        try:
            if goal.stream:
                # Streaming generation
                final_text = ""
                final_tokens = 0
                
                async for feedback in self._brick.generate_stream(request):
                    publish_feedback(feedback)
                    final_text = feedback.partial_response
                    final_tokens = feedback.tokens_generated
                    
                    # Check for preemption
                    if goal_handle.is_cancel_requested:
                        self.get_logger().info("Goal preempted")
                        goal_handle.canceled()
                        
                        result = LLMGenerate.Result()
                        result.response = final_text
                        result.success = False
                        result.error_message = "Preempted"
                        result.tokens_generated = final_tokens
                        result.tokens_input = 0
                        return result
                
                # Build final result
                result = LLMGenerate.Result()
                result.response = final_text
                result.success = True
                result.tokens_generated = final_tokens
                result.tokens_input = len(goal.prompt.split())  # Rough estimate
                
                goal_handle.succeed()
                
            else:
                # Non-streaming generation
                llm_result = await self._brick.generate(request)
                
                result = LLMGenerate.Result()
                result.response = llm_result.response
                result.success = llm_result.success
                result.error_message = llm_result.error_message
                result.generation_time = llm_result.generation_time
                result.tokens_generated = llm_result.tokens_generated
                result.tokens_input = llm_result.tokens_input
                
                if llm_result.success:
                    goal_handle.succeed()
                else:
                    goal_handle.abort()
            
            self.get_logger().info(
                f"Goal completed: success={result.success}, "
                f"tokens={result.tokens_generated}"
            )
            
            return result
            
        except Exception as e:
            self.get_logger().error(f"Goal execution failed: {e}")
            
            result = LLMGenerate.Result()
            result.success = False
            result.error_message = str(e)
            
            goal_handle.abort()
            return result
    
    def destroy_node(self):
        """Clean shutdown."""
        self.get_logger().info("Shutting down LLMServerNode...")
        
        # Stop action server
        self._action_server.destroy()
        
        # Shutdown brick
        self._shutdown_event.set()
        
        if self._loop and self._initialized:
            future = asyncio.run_coroutine_threadsafe(
                self._brick.shutdown(),
                self._loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as e:
                self.get_logger().error(f"Error during brick shutdown: {e}")
        
        # Stop thread
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        
        super().destroy_node()
        self.get_logger().info("Shutdown complete")


def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)
    
    node = None
    executor = None
    
    try:
        node = LLMServerNode()
        
        # Use MultiThreadedExecutor for concurrent goal handling
        executor = MultiThreadedExecutor(num_threads=4)
        executor.add_node(node)
        
        executor.spin()
        
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        if executor:
            executor.shutdown()
        if node:
            node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
ROS2 Node for Skill Manager

This node provides:
- ExecuteSkill action server
- Subscribes to /intent/classified
- Executes skills and publishes results

Usage:
    ros2 run aimee_skill_manager skill_manager_node
"""

import asyncio
import json
import logging
import sys
import threading
from typing import Optional

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.action.server import ServerGoalHandle
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import String
from aimee_msgs.msg import Intent, RobotState
from aimee_msgs.action import ExecuteSkill

from aimee_skill_manager.brick.skill_manager import (
    SkillManagerBrick, SkillContext, SkillResult
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SkillManagerNode(Node):
    """
    ROS2 Node for Skill Manager.
    
    This node:
    - Provides ExecuteSkill action server
    - Subscribes to classified intents
    - Executes skills and reports results
    """
    
    def __init__(self):
        super().__init__('skill_manager')
        
        # Declare parameters
        self.declare_parameters(namespace='', parameters=[
            ('default_timeout', 30.0),
            ('enable_safety_checks', True),
            ('debug', False),
        ])
        
        # Get parameters
        default_timeout = self.get_parameter('default_timeout').value
        enable_safety_checks = self.get_parameter('enable_safety_checks').value
        debug = self.get_parameter('debug').value
        
        # Setup QoS
        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        
        # Publishers
        self._status_pub = self.create_publisher(
            String, '/skill/status', reliable_qos
        )
        self._tts_pub = self.create_publisher(
            String, '/tts/speak', reliable_qos
        )
        
        # Subscribers
        self._intent_sub = self.create_subscription(
            Intent,
            '/intent/classified',
            self._on_intent,
            10
        )
        
        self._robot_state_sub = self.create_subscription(
            RobotState,
            '/robot/state',
            self._on_robot_state,
            10
        )
        
        # Action server
        self._action_server = ActionServer(
            self,
            ExecuteSkill,
            '/skill/execute',
            execute_callback=self._execute_callback,
            goal_callback=self._goal_callback,
            cancel_callback=self._cancel_callback,
            callback_group=ReentrantCallbackGroup()
        )
        
        # Create the brick
        self._brick = SkillManagerBrick(
            default_timeout=default_timeout,
            enable_safety_checks=enable_safety_checks,
            debug=debug
        )
        
        # Register feedback callback
        self._brick.on_feedback(self._on_skill_feedback)
        
        # Async handling
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._shutdown_event = threading.Event()
        
        # State
        self._initialized = False
        self._current_robot_state: Optional[RobotState] = None
        
        self.get_logger().info(
            f"SkillManagerNode initialized:\n"
            f"  Timeout: {default_timeout}s\n"
            f"  Safety checks: {enable_safety_checks}"
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
            self.get_logger().info(f"Available skills: {self._brick.list_skills()}")
            
            # Keep running
            while not self._shutdown_event.is_set():
                await asyncio.sleep(0.1)
                
        except Exception as e:
            self.get_logger().error(f"Async main error: {e}")
    
    def _on_robot_state(self, msg: RobotState):
        """Receive robot state updates."""
        self._current_robot_state = msg
    
    def _on_intent(self, msg: Intent):
        """
        Callback when intent is classified.
        
        Automatically execute skill if required.
        """
        if not self._initialized:
            return
        
        if not msg.requires_skill:
            return
        
        skill_name = msg.skill_name
        if not skill_name:
            skill_name = msg.intent_type  # Fallback to intent type
        
        self.get_logger().info(f"Executing skill for intent: {skill_name}")
        
        # Create context
        context = SkillContext(
            user_input=msg.raw_text,
            skill_id=skill_name,
            session_id=msg.session_id,
            robot_state=self._current_robot_state
        )
        
        if self._loop and self._initialized:
            asyncio.run_coroutine_threadsafe(
                self._execute_skill_async(skill_name, context),
                self._loop
            )
    
    async def _execute_skill_async(self, skill_name: str, context: SkillContext):
        """Async skill execution."""
        result = await self._brick.execute_skill(skill_name, context)
        
        if result.success:
            # Send response to TTS
            if result.response_text:
                msg = String()
                msg.data = result.response_text
                self._tts_pub.publish(msg)
            
            self.get_logger().info(f"Skill {skill_name} executed successfully")
        else:
            self.get_logger().error(f"Skill {skill_name} failed: {result.error_message}")
            
            # Send error to TTS
            error_msg = String()
            error_msg.data = f"I couldn't do that. {result.error_message}"
            self._tts_pub.publish(error_msg)
    
    def _goal_callback(self, goal_request):
        """Accept or reject goal."""
        self.get_logger().info(
            f"Received skill execution request: {goal_request.skill_id}"
        )
        
        if not self._initialized:
            self.get_logger().error("Not initialized, rejecting goal")
            return GoalResponse.REJECT
        
        # Check if skill exists
        if goal_request.skill_id not in self._brick.list_skills():
            self.get_logger().warning(f"Unknown skill: {goal_request.skill_id}")
            return GoalResponse.REJECT
        
        return GoalResponse.ACCEPT
    
    def _cancel_callback(self, goal_handle):
        """Handle cancel request."""
        self.get_logger().info("Received cancel request")
        
        if self._loop:
            asyncio.run_coroutine_threadsafe(
                self._brick.cancel_current_skill(),
                self._loop
            )
        
        return CancelResponse.ACCEPT
    
    async def _execute_callback(self, goal_handle: ServerGoalHandle):
        """
        Execute skill action.
        """
        goal = goal_handle.request
        self.get_logger().info(f"Executing skill: {goal.skill_id}")
        
        # Parse user context
        user_context = {}
        if goal.user_context:
            try:
                user_context = json.loads(goal.user_context)
            except json.JSONDecodeError:
                pass
        
        # Create context
        context = SkillContext(
            user_input=goal.user_input,
            user_context=user_context,
            robot_state=goal.robot_state,
            session_id=goal.session_id,
            skill_id=goal.skill_id
        )
        
        # Report starting
        feedback = ExecuteSkill.Feedback()
        feedback.status = "starting"
        feedback.current_action = f"Starting {goal.skill_id}"
        feedback.progress = 0.0
        feedback.can_cancel = True
        goal_handle.publish_feedback(feedback)
        
        # Execute skill
        result = await self._brick.execute_skill(goal.skill_id, context)
        
        # Build result
        action_result = ExecuteSkill.Result()
        action_result.success = result.success
        action_result.response_text = result.response_text
        action_result.error_message = result.error_message
        
        # Convert actions to ROS messages
        # TODO: Convert result.actions_performed to MotorAction[], etc.
        
        if result.success:
            goal_handle.succeed()
            self.get_logger().info(f"Skill {goal.skill_id} completed")
        else:
            goal_handle.abort()
            self.get_logger().error(f"Skill {goal.skill_id} failed")
        
        return action_result
    
    def _on_skill_feedback(self, skill_name: str, status: str, progress: float):
        """Receive skill execution feedback."""
        status_msg = String()
        status_msg.data = f"{skill_name}: {status} ({progress*100:.0f}%)"
        self._status_pub.publish(status_msg)
    
    def destroy_node(self):
        """Clean shutdown."""
        self.get_logger().info("Shutting down SkillManagerNode...")
        
        self._action_server.destroy()
        self._shutdown_event.set()
        
        # Shutdown brick
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
    try:
        node = SkillManagerNode()
        rclpy.spin(node)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        if node:
            node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

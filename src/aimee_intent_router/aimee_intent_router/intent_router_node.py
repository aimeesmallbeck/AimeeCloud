#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
ROS2 Node for Intent Router

This node integrates:
- Subscribes to /voice/transcription
- Calls LLM via /llm/generate action for intent classification
- Routes to skills
- Publishes responses to /tts/speak

Usage:
    ros2 run aimee_intent_router intent_router_node
"""

import asyncio
import logging
import sys
import threading
from typing import Optional

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import String
from aimee_msgs.msg import Transcription, Intent as IntentMsg
from aimee_msgs.action import LLMGenerate

from aimee_intent_router.brick.intent_router import (
    IntentRouterBrick, IntentType
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class IntentRouterNode(Node):
    """
    ROS2 Node for Intent Router.
    
    This node:
    - Receives transcriptions from Voice Manager
    - Classifies intent using LLM Action Server
    - Routes to skills
    - Generates responses and sends to TTS
    """
    
    def __init__(self):
        super().__init__('intent_router')
        
        # Declare parameters
        self.declare_parameters(namespace='', parameters=[
            ('confidence_threshold', 0.6),
            ('enable_conversation_mode', True),
            ('conversation_timeout', 60.0),
            ('max_context_length', 10),
            ('fallback_to_chat', True),
            ('debug', False),
        ])
        
        # Get parameters
        confidence_threshold = self.get_parameter('confidence_threshold').value
        enable_conversation_mode = self.get_parameter('enable_conversation_mode').value
        conversation_timeout = self.get_parameter('conversation_timeout').value
        max_context_length = self.get_parameter('max_context_length').value
        fallback_to_chat = self.get_parameter('fallback_to_chat').value
        debug = self.get_parameter('debug').value
        
        # Setup QoS
        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        
        # Publishers
        self._tts_pub = self.create_publisher(
            String, '/tts/speak', reliable_qos
        )
        self._intent_pub = self.create_publisher(
            IntentMsg, '/intent/classified', reliable_qos
        )
        self._status_pub = self.create_publisher(
            String, '/intent/status', reliable_qos
        )
        
        # Subscribers
        self._transcription_sub = self.create_subscription(
            Transcription,
            '/voice/transcription',
            self._on_transcription,
            10
        )
        
        # Action client for LLM
        self._llm_client = ActionClient(
            self,
            LLMGenerate,
            '/llm/generate'
        )
        
        # Create the brick
        self._brick = IntentRouterBrick(
            confidence_threshold=confidence_threshold,
            enable_conversation_mode=enable_conversation_mode,
            conversation_timeout=conversation_timeout,
            max_context_length=max_context_length,
            fallback_to_chat=fallback_to_chat,
            debug=debug
        )
        
        # Register skill handlers (placeholder - will be extended)
        self._register_skills()
        
        # Async handling
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._shutdown_event = threading.Event()
        
        # State
        self._initialized = False
        self._llm_available = False
        
        self.get_logger().info(
            f"IntentRouterNode initialized:\n"
            f"  Confidence threshold: {confidence_threshold}\n"
            f"  Conversation mode: {enable_conversation_mode}\n"
            f"  Fallback to chat: {fallback_to_chat}"
        )
        
        # Start async thread
        self._start_async_thread()
        
        # Wait for LLM action server
        self._wait_for_llm()
    
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
    
    def _wait_for_llm(self):
        """Wait for LLM action server."""
        self.get_logger().info("Waiting for LLM action server...")
        if not self._llm_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().warning(
                "LLM action server not available. "
                "Will use fallback classification."
            )
            self._llm_available = False
        else:
            self._llm_available = True
            self.get_logger().info("LLM action server connected")
    
    def _register_skills(self):
        """Register skill handlers."""
        # Movement skill
        self._brick.register_skill_handler(
            "movement",
            self._handle_movement_skill
        )
        
        # Arm control skill
        self._brick.register_skill_handler(
            "arm_control",
            self._handle_arm_skill
        )
        
        # Camera skill
        self._brick.register_skill_handler(
            "camera",
            self._handle_camera_skill
        )
        
        # Response handler
        self._brick.on_response(self._on_response)
    
    def _handle_movement_skill(self, intent, context):
        """Handle movement skill."""
        self.get_logger().info(f"Executing movement: {intent.action}")
        # TODO: Publish to movement controller
        # self._movement_pub.publish(...)
        return f"Executed {intent.action}"
    
    def _handle_arm_skill(self, intent, context):
        """Handle arm control skill."""
        self.get_logger().info(f"Executing arm control: {intent.action}")
        # TODO: Publish to arm controller
        return f"Executed arm {intent.action}"
    
    def _handle_camera_skill(self, intent, context):
        """Handle camera skill."""
        self.get_logger().info(f"Executing camera: {intent.action}")
        # TODO: Publish to camera controller
        return f"Camera {intent.action}"
    
    def _on_response(self, response: str, intent):
        """Send response to TTS."""
        msg = String()
        msg.data = response
        self._tts_pub.publish(msg)
        self.get_logger().info(f"Sent to TTS: {response[:50]}...")
    
    def _on_transcription(self, msg: Transcription):
        """
        Callback when transcription is received.
        
        This is the main entry point for intent processing.
        """
        if not self._initialized:
            self.get_logger().warning("Not initialized, ignoring transcription")
            return
        
        # Only process commands (post-wake-word)
        if not msg.is_command:
            self.get_logger().debug("Not a command, ignoring")
            return
        
        text = msg.text.strip()
        if not text:
            return
        
        self.get_logger().info(f"Processing: '{text}'")
        
        if self._loop and self._initialized:
            asyncio.run_coroutine_threadsafe(
                self._process_async(text, msg.session_id),
                self._loop
            )
    
    async def _process_async(self, text: str, session_id: str):
        """Async processing task."""
        # Create LLM function wrapper
        llm_func = None
        if self._llm_available:
            llm_func = self._call_llm
        
        # Process through intent router
        result = await self._brick.process_text(
            text=text,
            session_id=session_id,
            llm_generate_func=llm_func
        )
        
        if result.success:
            # Publish intent message
            intent_msg = IntentMsg()
            intent_msg.intent_type = result.intent.intent_type.value
            intent_msg.action = result.intent.action
            intent_msg.confidence = result.intent.confidence
            intent_msg.raw_text = text
            intent_msg.requires_skill = result.intent.requires_skill
            intent_msg.skill_name = result.intent.skill_name
            intent_msg.session_id = session_id
            
            # Convert parameters to JSON string
            try:
                import json
                intent_msg.parameters_json = json.dumps(result.intent.parameters)
            except:
                intent_msg.parameters_json = "{}"
            
            self._intent_pub.publish(intent_msg)
            
            self.get_logger().info(
                f"Intent classified: {result.intent.intent_type.value} "
                f"(confidence: {result.intent.confidence:.2f})"
            )
        else:
            self.get_logger().error(f"Intent processing failed: {result.error_message}")
            
            # Send error response
            error_msg = String()
            error_msg.data = "I'm sorry, I didn't understand that."
            self._tts_pub.publish(error_msg)
    
    async def _call_llm(
        self,
        prompt: str,
        system_context: str = "",
        max_tokens: int = 150,
        temperature: float = 0.7
    ) -> dict:
        """
        Call LLM via action client.
        
        This is the bridge between the brick and ROS2 LLM action server.
        """
        if not self._llm_available:
            raise Exception("LLM not available")
        
        # Create goal
        goal = LLMGenerate.Goal()
        goal.prompt = prompt
        goal.system_context = system_context
        goal.max_tokens = max_tokens
        goal.temperature = temperature
        goal.stream = False  # Non-streaming for classification
        goal.session_id = "intent_router"
        
        # Send goal
        future = self._llm_client.send_goal_async(goal)
        
        # Wait for result
        rclpy.spin_until_future_complete(self, future)
        goal_handle = future.result()
        
        if not goal_handle.accepted:
            raise Exception("LLM goal rejected")
        
        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        result = result_future.result().result
        
        if not result.success:
            raise Exception(f"LLM generation failed: {result.error_message}")
        
        return {
            'response': result.response,
            'tokens_generated': result.tokens_generated
        }
    
    def destroy_node(self):
        """Clean shutdown."""
        self.get_logger().info("Shutting down IntentRouterNode...")
        
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
        node = IntentRouterNode()
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

#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
ROS2 Node for Cloud Bridge

Connects AIMEE robot to AimeeCloud via MQTT.
Subscribes to local ROS2 topics, forwards to cloud.
Receives cloud responses, dispatches to local topics/skills.

Usage:
    ros2 run aimee_cloud_bridge cloud_bridge_node
"""

import asyncio
import json
import logging
import sys
import threading
import time
from typing import Optional

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import String, Bool
from geometry_msgs.msg import Twist
from aimee_msgs.msg import Intent, CloudIntent, ArmCommand

from aimee_cloud_bridge.brick.cloud_bridge import CloudBridgeBrick

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CloudBridgeNode(Node):
    """
    ROS2 Node for AimeeCloud Bridge.
    """
    
    def __init__(self):
        super().__init__('cloud_bridge')
        
        # Declare parameters
        self.declare_parameters(namespace='', parameters=[
            ('device_id', 'arduino-uno-q-001'),
            ('broker_host', 'aimeecloud.com'),
            ('broker_port', 443),
            ('use_websocket', True),
            ('websocket_path', '/aimeecloud-mqtt'),
            ('user_name', 'Scott'),
            ('user_location', 'home'),
            ('user_language', 'en-US'),
            ('reconnect_interval_sec', 5.0),
            ('ping_interval_sec', 60.0),
            ('session_file', '/home/arduino/.config/aimee_session.json'),
        ])
        
        # Get parameters
        device_id = self.get_parameter('device_id').value
        broker_host = self.get_parameter('broker_host').value
        broker_port = self.get_parameter('broker_port').value
        use_websocket = self.get_parameter('use_websocket').value
        websocket_path = self.get_parameter('websocket_path').value
        user_name = self.get_parameter('user_name').value
        user_location = self.get_parameter('user_location').value
        user_language = self.get_parameter('user_language').value
        reconnect_interval_sec = self.get_parameter('reconnect_interval_sec').value
        ping_interval_sec = self.get_parameter('ping_interval_sec').value
        session_file = self.get_parameter('session_file').value
        
        # Setup QoS
        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        
        # Publishers
        self._tts_pub = self.create_publisher(String, '/tts/speak', reliable_qos)
        self._session_id_pub = self.create_publisher(String, '/cloud/session_id', reliable_qos)
        self._connected_pub = self.create_publisher(Bool, '/cloud/connected', reliable_qos)
        self._cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', reliable_qos)
        self._arm_cmd_pub = self.create_publisher(ArmCommand, '/arm/command', reliable_qos)
        
        # Subscribers
        self._intent_sub = self.create_subscription(
            Intent,
            '/intent/classified',
            self._on_intent,
            10
        )
        self._cloud_game_move_sub = self.create_subscription(
            CloudIntent,
            '/cloud/game_move',
            self._on_cloud_game_move,
            10
        )
        self._cloud_raw_text_sub = self.create_subscription(
            String,
            '/cloud/raw_text',
            self._on_cloud_raw_text,
            10
        )
        
        # Create the brick with callbacks
        self._brick = CloudBridgeBrick(
            device_id=device_id,
            broker_host=broker_host,
            broker_port=broker_port,
            use_websocket=use_websocket,
            websocket_path=websocket_path,
            user_name=user_name,
            user_location=user_location,
            user_language=user_language,
            reconnect_interval_sec=reconnect_interval_sec,
            ping_interval_sec=ping_interval_sec,
            session_file=session_file,
            on_chat_response=self._on_chat_response,
            on_game_update=self._on_game_update,
            on_robot_command=self._on_robot_command,
            on_error=self._on_cloud_error,
            on_connected=self._on_cloud_connected,
            on_session_id=self._on_session_id_changed,
        )
        
        # Async handling
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._shutdown_event = threading.Event()
        
        # State
        self._initialized = False
        
        self.get_logger().info(
            f"CloudBridgeNode initialized:\n"
            f"  Device ID: {device_id}\n"
            f"  Broker: {broker_host}:{broker_port}\n"
            f"  WebSocket: {use_websocket} ({websocket_path})\n"
            f"  Session file: {session_file}"
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
            self.get_logger().info("Cloud bridge brick initialized successfully")
            
            while not self._shutdown_event.is_set():
                await asyncio.sleep(0.1)
                
        except Exception as e:
            self.get_logger().error(f"Async main error: {e}")
    
    def _on_intent(self, msg: Intent):
        """Callback when intent is classified. Route cloud intents to AimeeCloud."""
        if not self._initialized:
            return
        
        # Route cloud skills to AimeeCloud
        if msg.skill_name == "cloud_proxy" or msg.intent_type in [
            "weather", "news", "story", "game", "help", "chat",
            "storytelling", "math", "identity_check", "status_check"
        ]:
            intent_dict = None
            if msg.intent_type:
                intent_dict = {
                    "intent": msg.intent_type,
                    "category": "cloud_skill",
                    "confidence": msg.confidence,
                    "text": msg.raw_text,
                    "source": "ros2_intent_router"
                }
            
            if self._loop and self._initialized:
                self._loop.call_soon_threadsafe(
                    self._brick.send_intent, msg.raw_text, intent_dict
                )
    
    def _on_cloud_game_move(self, msg: CloudIntent):
        """Callback for game moves from local game manager."""
        if not self._initialized:
            return
        
        try:
            move = json.loads(msg.move_json) if msg.move_json else {}
        except json.JSONDecodeError:
            move = {}
        
        if self._loop and self._initialized:
            self._loop.call_soon_threadsafe(
                self._brick.send_game_move, msg.game_type, move
            )
    
    def _on_cloud_raw_text(self, msg: String):
        """Callback for raw text to send to cloud."""
        if not self._initialized:
            return
        
        if self._loop and self._initialized:
            self._loop.call_soon_threadsafe(
                self._brick.send_intent, msg.data, None
            )
    
    def _on_chat_response(self, text: str):
        """Handle chat response from cloud."""
        msg = String()
        msg.data = text
        self._tts_pub.publish(msg)
        self.get_logger().info(f"Cloud TTS: {text[:60]}...")
    
    def _on_game_update(self, state: dict, text: str):
        """Handle game update from cloud."""
        # Publish game state update (for any local game UI)
        # For now, just speak the TTS
        self._on_chat_response(text)
        self.get_logger().info(f"Game update: {state}")
    
    def _on_robot_command(self, intent: str, command: dict, text: str):
        """Handle robot command from cloud."""
        motor = command.get("motor")
        arm = command.get("arm")
        gripper = command.get("gripper")
        duration_ms = command.get("duration_ms", 0)
        
        if motor:
            twist = Twist()
            if motor == "forward":
                twist.linear.x = 0.5
            elif motor == "backward":
                twist.linear.x = -0.5
            elif motor == "left":
                twist.angular.z = 0.5
            elif motor == "right":
                twist.angular.z = -0.5
            elif motor == "stop":
                pass
            elif motor == "wave":
                # Wave is more of an arm action, but protocol maps it to motor
                pass
            
            self._cmd_vel_pub.publish(twist)
            
            # Auto-stop after duration
            if duration_ms > 0 and motor not in ("stop", "wave"):
                def stop_motors():
                    stop_twist = Twist()
                    self._cmd_vel_pub.publish(stop_twist)
                
                timer = threading.Timer(duration_ms / 1000.0, stop_motors)
                timer.daemon = True
                timer.start()
        
        if arm or gripper:
            arm_msg = ArmCommand()
            arm_msg.action = arm or gripper
            self._arm_cmd_pub.publish(arm_msg)
        
        # Speak TTS
        if text:
            self._on_chat_response(text)
        
        self.get_logger().info(f"Robot command executed: {intent}")
    
    def _on_cloud_error(self, error_code: str, text: str):
        """Handle error response from cloud."""
        if text:
            self._on_chat_response(text)
        self.get_logger().error(f"Cloud error: {error_code}")
    
    def _on_cloud_connected(self, connected: bool):
        """Handle cloud connection state change."""
        msg = Bool()
        msg.data = connected
        self._connected_pub.publish(msg)
        self.get_logger().info(f"Cloud connected: {connected}")
    
    def _on_session_id_changed(self, session_id: str):
        """Handle session ID change."""
        msg = String()
        msg.data = session_id
        self._session_id_pub.publish(msg)
        self.get_logger().info(f"Session ID updated: {session_id or 'cleared'}")
    
    def destroy_node(self):
        """Clean shutdown."""
        self.get_logger().info("Shutting down CloudBridgeNode...")
        
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
        node = CloudBridgeNode()
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

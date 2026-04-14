#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
ROS2 Node for Wake Word Detection using Edge Impulse

This node wraps the WakeWordEIBrick and provides ROS2 interfaces:
- Publishes WakeWordDetection messages on /wake_word/detected
- Subscribes to control commands on /wake_word/control
- Provides runtime parameter adjustment

Usage:
    ros2 run aimee_wake_word_ei wake_word_ei_node
"""

import asyncio
import json
import logging
import signal
import sys
import threading
from typing import Optional

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import String
from aimee_msgs.msg import WakeWordDetection

# Import the brick
from aimee_wake_word_ei.brick.wake_word_ei import WakeWordEIBrick, DetectionResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WakeWordEINode(Node):
    """
    ROS2 Node for wake word detection using Edge Impulse.
    
    This node wraps the WakeWordEIBrick and provides:
    - ROS2 topic interface for wake word events
    - Parameter server for runtime configuration
    - Control interface for start/stop/status
    """
    
    def __init__(self):
        super().__init__('wake_word_ei')
        
        # Declare parameters
        self.declare_parameters(namespace='', parameters=[
            ('model_path', '/home/arduino/.arduino-bricks/models/custom-ei/ei-model-953002-1/model.eim'),
            ('target_keyword', 'aimee'),
            ('confidence_threshold', 0.70),
            ('cooldown_seconds', 2.0),
            ('audio_device', 'default'),
            ('enabled', True),
            ('debug', False),
        ])
        
        # Get parameters
        model_path = self.get_parameter('model_path').value
        target_keyword = self.get_parameter('target_keyword').value
        confidence_threshold = self.get_parameter('confidence_threshold').value
        cooldown_seconds = self.get_parameter('cooldown_seconds').value
        audio_device = self.get_parameter('audio_device').value
        self._enabled = self.get_parameter('enabled').value
        debug = self.get_parameter('debug').value
        
        # Setup QoS profile for sensor data (best effort, high throughput)
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        
        # Publishers
        self._detection_pub = self.create_publisher(
            WakeWordDetection,
            '/wake_word/detected',
            sensor_qos
        )
        
        self._classification_pub = self.create_publisher(
            String,
            '/wake_word/classification',
            sensor_qos
        )
        
        # Subscribers
        self._control_sub = self.create_subscription(
            String,
            '/wake_word/control',
            self._on_control_command,
            10
        )
        
        # Parameter callback
        self.add_on_set_parameters_callback(self._on_parameters_changed)
        
        # Create the brick
        self._brick = WakeWordEIBrick(
            model_path=model_path,
            target_keyword=target_keyword,
            confidence_threshold=confidence_threshold,
            cooldown_seconds=cooldown_seconds,
            audio_device=audio_device,
            debug=debug
        )
        
        # Register callbacks
        self._brick.on_wake_word(self._on_wake_word_detected)
        self._brick.on_classification(self._on_classification)
        
        # Async loop handling
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._shutdown_event = threading.Event()
        
        # Node state
        self._initialized = False
        self._listening = False
        
        self.get_logger().info(
            f"WakeWordEINode initialized:\n"
            f"  Model: {model_path}\n"
            f"  Target: '{target_keyword}'\n"
            f"  Threshold: {confidence_threshold}\n"
            f"  Cooldown: {cooldown_seconds}s"
        )
        
        # Start async operations in background thread
        self._start_async_thread()
    
    def _start_async_thread(self):
        """Start the async event loop in a background thread."""
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
        """Main async coroutine for brick operations."""
        try:
            # Initialize brick
            await self._brick.initialize()
            self._initialized = True
            self.get_logger().info("Brick initialized successfully")
            
            # Start listening if enabled
            if self._enabled:
                await self._brick.start_listening()
                self._listening = True
                self.get_logger().info("Wake word listening started")
            
            # Keep running until shutdown
            while not self._shutdown_event.is_set():
                await asyncio.sleep(0.1)
                
        except Exception as e:
            self.get_logger().error(f"Async main error: {e}")
    
    def _on_wake_word_detected(self, result: DetectionResult):
        """
        Callback when wake word is detected.
        
        Publishes WakeWordDetection message to ROS2 topic.
        
        FUTURE ENHANCEMENT: This is the AUDIO wake word detection.
        Other wake word sources (gesture, touch) will have similar callbacks
        that publish to different topics or a unified /wake_word/all topic.
        
        FUTURE ENHANCEMENT: When conversation mode is active, this may
        be suppressed to allow follow-up commands without repeated wake word.
        """
  </parameter<SECRET_KEY>EY>dy detected: '{result.keyword}' "
                    f"(confidence: {result.confidence:.2f})"
                )
        # Create and populate ROS2 message
        msg = WakeWordDetection()
        msg.wake_word = result.keyword
        msg.confidence = result.confidence
        msg.source = "edge_impulse"
        msg.active = True
        msg.timestamp = self.get_clock().now().to_msg()
        msg.session_id = result.session_id
        
        # Publish
        self._detection_pub.publish(msg)
        
        self.get_logger().info(
            f"Published wake word detection: '{result.keyword}' "
            f"(confidence: {result.confidence:.2f})"
        )
    
    def _on_classification(self, classifications: dict):
        """
        Callback for classification results (for monitoring/debugging).
        """
        # Publish as JSON string
        msg = String()
        msg.data = json.dumps(classifications)
        self._classification_pub.publish(msg)
    
    def _on_control_command(self, msg: String):
        """
        Handle control commands via ROS2 topic.
        
        Commands:
        - 'start': Start listening
        - 'stop': Stop listening
        - 'status': Log current status
        """
        command = msg.data.lower().strip()
        self.get_logger().info(f"Received control command: {command}")
        
        if command == 'start':
            if not self._enabled:
                self._enabled = True
                if self._loop and self._initialized:
                    asyncio.run_coroutine_threadsafe(
                        self._brick.start_listening(), 
                        self._loop
                    )
                    self._listening = True
                    self.get_logger().info("Started listening")
                    
        elif command == 'stop':
            if self._enabled:
                self._enabled = False
                if self._loop and self._initialized:
                    asyncio.run_coroutine_threadsafe(
                        self._brick.stop_listening(), 
                        self._loop
                    )
                    self._listening = False
                    self.get_logger().info("Stopped listening")
                    
        elif command == 'status':
            status = self._brick.get_status()
            self.get_logger().info(f"Status: {json.dumps(status, indent=2, default=str)}")
            
        else:
            self.get_logger().warning(f"Unknown command: {command}")
    
    def _on_parameters_changed(self, params):
        """
        Handle parameter changes at runtime.
        """
        results = []
        
        for param in params:
            if param.name == 'confidence_threshold':
                self._brick.config.confidence_threshold = param.value
                self.get_logger().info(f"Updated confidence_threshold: {param.value}")
                results.append(SetParametersResult(successful=True))
                
            elif param.name == 'cooldown_seconds':
                self._brick.config.cooldown_seconds = param.value
                self.get_logger().info(f"Updated cooldown_seconds: {param.value}")
                results.append(SetParametersResult(successful=True))
                
            elif param.name == 'enabled':
                self._enabled = param.value
                if self._loop and self._initialized:
                    if self._enabled and not self._listening:
                        asyncio.run_coroutine_threadsafe(
                            self._brick.start_listening(), 
                            self._loop
                        )
                        self._listening = True
                    elif not self._enabled and self._listening:
                        asyncio.run_coroutine_threadsafe(
                            self._brick.stop_listening(), 
                            self._loop
                        )
                        self._listening = False
                results.append(SetParametersResult(successful=True))
                
            else:
                results.append(SetParametersResult(
                    successful=False,
                    reason=f"Parameter {param.name} is read-only"
                ))
        
        return results
    
    def destroy_node(self):
        """Clean shutdown of the node."""
        self.get_logger().info("Shutting down WakeWordEINode...")
        
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
        
        # Stop async thread
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        
        super().destroy_node()
        self.get_logger().info("Shutdown complete")


def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)
    
    node = None
    try:
        node = WakeWordEINode()
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

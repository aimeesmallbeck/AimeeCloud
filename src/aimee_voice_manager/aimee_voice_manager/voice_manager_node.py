#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
ROS2 Node for Voice Manager (Continuous STT)

This node wraps the VoiceManagerBrick and provides ROS2 interfaces:
- Publishes Transcription messages on /voice/transcription
- Supports streaming partial results on /voice/partial
- No wake word required - continuous listening mode

Usage:
    ros2 run aimee_voice_manager voice_manager_node
"""

import asyncio
import logging
import signal
import sys
import threading
from typing import Optional

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from rcl_interfaces.msg import SetParametersResult
from std_msgs.msg import String
from aimee_msgs.msg import Transcription

# Import the brick
from aimee_voice_manager.brick.voice_manager import (
    VoiceManagerBrick, TranscriptionResult
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VoiceManagerNode(Node):
    """
    ROS2 Node for Voice Manager (Continuous STT).
    """

    def __init__(self):
        super().__init__('voice_manager')

        # Declare parameters
        self.declare_parameters(namespace='', parameters=[
            ('engine', 'vosk'),
            ('model_path', '/home/arduino/vosk-models/vosk-model-small-en-us-0.15'),
            ('sample_rate', 16000),
            ('audio_device', 'plughw:2,0'),
            ('command_timeout', 10.0),
            ('min_command_length', 0.5),
            ('enabled', True),
            ('publish_partials', True),
            ('debug', False),
        ])

        # Get parameters
        engine = self.get_parameter('engine').value
        model_path = self.get_parameter('model_path').value
        sample_rate = self.get_parameter('sample_rate').value
        audio_device = self.get_parameter('audio_device').value
        command_timeout = self.get_parameter('command_timeout').value
        min_command_length = self.get_parameter('min_command_length').value
        self._enabled = self.get_parameter('enabled').value
        self._publish_partials = self.get_parameter('publish_partials').value
        debug = self.get_parameter('debug').value

        # Setup QoS
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # Publishers
        self._transcription_pub = self.create_publisher(
            Transcription,
            '/voice/transcription',
            reliable_qos
        )

        self._partial_pub = self.create_publisher(
            Transcription,
            '/voice/partial',
            sensor_qos
        )

        self._status_pub = self.create_publisher(
            String,
            '/voice/status',
            reliable_qos
        )

        # Subscribers
        self._control_sub = self.create_subscription(
            String,
            '/voice/control',
            self._on_control_command,
            10
        )

        # Parameter callback
        self.add_on_set_parameters_callback(self._on_parameters_changed)

        # Create the brick
        self._brick = VoiceManagerBrick(
            model_path=model_path if model_path else None,
            engine=engine,
            sample_rate=sample_rate,
            audio_device=audio_device,
            command_timeout=command_timeout,
            min_command_length=min_command_length,
            debug=debug
        )

        # Register callbacks
        self._brick.on_transcription(self._on_transcription)
        if self._publish_partials:
            self._brick.on_partial(self._on_partial)

        # Async handling
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._shutdown_event = threading.Event()

        # State
        self._initialized = False

        self.get_logger().info(
            f"VoiceManagerNode initialized:\n"
            f"  Engine: {engine}\n"
            f"  Model: {model_path or 'default'}\n"
            f"  Sample rate: {sample_rate}Hz\n"
            f"  Audio device: {audio_device}\n"
            f"  Continuous mode: True"
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

            # Start continuous listening if enabled
            if self._enabled:
                self._brick.start_listening()
                self.get_logger().info("Continuous listening started")

            # Keep running
            while not self._shutdown_event.is_set():
                await asyncio.sleep(0.1)

        except Exception as e:
            self.get_logger().error(f"Async main error: {e}")

    def _on_transcription(self, result: TranscriptionResult):
        """Callback for final transcription."""
        msg = Transcription()
        msg.text = result.text
        msg.confidence = result.confidence
        msg.source = result.engine
        msg.is_command = result.is_command
        msg.is_partial = False
        msg.wake_word_detected = False
        msg.wake_word = ""
        msg.timestamp = self.get_clock().now().to_msg()
        msg.session_id = result.session_id

        self._transcription_pub.publish(msg)

        self.get_logger().info(
            f"Published transcription: '{result.text[:50]}...' "
            f"(confidence: {result.confidence:.2f})"
        )

    def _on_partial(self, result: TranscriptionResult):
        """Callback for partial transcription results."""
        if not self._publish_partials:
            return

        msg = Transcription()
        msg.text = result.text
        msg.confidence = result.confidence
        msg.source = result.engine
        msg.is_command = result.is_command
        msg.is_partial = True
        msg.wake_word_detected = False
        msg.wake_word = ""
        msg.timestamp = self.get_clock().now().to_msg()
        msg.session_id = result.session_id

        self._partial_pub.publish(msg)

    def _on_control_command(self, msg: String):
        """
        Handle control commands.

        Commands:
        - 'start': Enable listening
        - 'stop': Disable listening
        - 'status': Log current status
        """
        command = msg.data.lower().strip()
        self.get_logger().info(f"Received control command: {command}")

        if command == 'start':
            self._enabled = True
            if self._initialized:
                self._brick.start_listening()
                self.get_logger().info("Listening started")

        elif command == 'stop':
            self._enabled = False
            if self._initialized:
                self._brick.stop_listening()
                self.get_logger().info("Listening stopped")

        elif command == 'status':
            status = self._brick.get_status()
            self.get_logger().info(f"Status: {status}")

        else:
            self.get_logger().warning(f"Unknown command: {command}")

    def _on_parameters_changed(self, params):
        """Handle parameter changes at runtime."""
        results = []

        for param in params:
            if param.name == 'enabled':
                self._enabled = param.value
                if self._initialized:
                    if self._enabled:
                        self._brick.start_listening()
                    else:
                        self._brick.stop_listening()
                self.get_logger().info(f"Updated enabled: {param.value}")
                results.append(SetParametersResult(successful=True))

            elif param.name == 'publish_partials':
                self._publish_partials = param.value
                self.get_logger().info(f"Updated publish_partials: {param.value}")
                results.append(SetParametersResult(successful=True))

            elif param.name == 'min_command_length':
                self._brick.min_command_length = param.value
                self.get_logger().info(f"Updated min_command_length: {param.value}")
                results.append(SetParametersResult(successful=True))

            else:
                results.append(SetParametersResult(
                    successful=False,
                    reason=f"Parameter {param.name} is read-only after initialization"
                ))

        return results

    def destroy_node(self):
        """Clean shutdown."""
        self.get_logger().info("Shutting down VoiceManagerNode...")

        self._shutdown_event.set()

        # Shutdown brick
        if self._initialized:
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
        node = VoiceManagerNode()
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

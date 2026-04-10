#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
ROS2 Node for Text-to-Speech

This node wraps the TTSBrick and provides:
- Subscribe to /tts/speak for text to speak
- Service for synchronous speech
- Preemption support
- Status reporting

Usage:
    ros2 run aimee_tts tts_node
"""

import asyncio
import logging
import os
import sys
import threading
from typing import Optional

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import String, Bool, Float32
from rcl_interfaces.msg import SetParametersResult

from aimee_tts.brick.tts import TTSBrick, TTSRequest

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TTSNode(Node):
    """
    ROS2 Node for Text-to-Speech.
    
    This node:
    - Subscribes to text to speak
    - Publishes status
    - Handles preemption
    """
    
    def __init__(self):
        super().__init__('tts')
        
        # Declare parameters
        self.declare_parameters(namespace='', parameters=[
            ('default_engine', 'gtts'),
            ('fallback_engine', 'pyttsx3'),
            ('auto_fallback', True),
            ('piper_model', ''),
            ('piper_config', ''),
            ('piper_speaker_id', 0),
            ('gtts_lang', 'en'),
            ('gtts_tld', 'com'),
            ('gtts_slow', False),
            ('volume', 1.0),
            ('speed', 1.0),
            ('use_pygame', True),
            ('debug', False),
        ])
        
        # Get parameters
        default_engine = self.get_parameter('default_engine').value
        fallback_engine = self.get_parameter('fallback_engine').value
        auto_fallback = self.get_parameter('auto_fallback').value
        piper_model = self.get_parameter('piper_model').value
        piper_config = self.get_parameter('piper_config').value
        piper_speaker_id = self.get_parameter('piper_speaker_id').value
        gtts_lang = self.get_parameter('gtts_lang').value
        gtts_tld = self.get_parameter('gtts_tld').value
        gtts_slow = self.get_parameter('gtts_slow').value
        volume = self.get_parameter('volume').value
        speed = self.get_parameter('speed').value
        use_pygame = self.get_parameter('use_pygame').value
        debug = self.get_parameter('debug').value
        
        # Expand user path for piper model
        if piper_model:
            piper_model = os.path.expanduser(piper_model)
        if piper_config:
            piper_config = os.path.expanduser(piper_config)
        
        # Setup QoS
        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        
        # Publishers
        self._status_pub = self.create_publisher(
            String, '/tts/status', reliable_qos
        )
        self._speaking_pub = self.create_publisher(
            Bool, '/tts/is_speaking', reliable_qos
        )
        
        # Subscribers
        self._speak_sub = self.create_subscription(
            String,
            '/tts/speak',
            self._on_speak,
            10
        )
        
        self._control_sub = self.create_subscription(
            String,
            '/tts/control',
            self._on_control,
            10
        )
        
        self._volume_sub = self.create_subscription(
            Float32,
            '/tts/volume',
            self._on_volume,
            10
        )
        
        # Create the brick
        self._brick = TTSBrick(
            default_engine=default_engine,
            fallback_engine=fallback_engine,
            auto_fallback=auto_fallback,
            piper_model=piper_model if piper_model else None,
            piper_config=piper_config if piper_config else None,
            piper_speaker_id=piper_speaker_id,
            gtts_lang=gtts_lang,
            gtts_tld=gtts_tld,
            gtts_slow=gtts_slow,
            volume=volume,
            speed=speed,
            use_pygame=use_pygame,
            debug=debug
        )
        
        # Async handling
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._shutdown_event = threading.Event()
        
        # State
        self._initialized = False
        
        # Status timer
        self._status_timer = self.create_timer(1.0, self._publish_status)
        
        self.get_logger().info(
            f"TTSNode initialized:\n"
            f"  Default engine: {default_engine}\n"
            f"  Fallback: {fallback_engine}\n"
            f"  Auto fallback: {auto_fallback}\n"
            f"  Piper model: {piper_model or 'None'}"
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
    
    def _on_speak(self, msg: String):
        """
        Callback to speak text.
        
        Format: "text" or "engine:text" or "priority:text"
        """
        text = msg.data.strip()
        if not text:
            return
        
        # Parse format: "engine:text" or just "text"
        engine = None
        if ':' in text:
            parts = text.split(':', 1)
            if parts[0] in ['gtts', 'piper', 'pyttsx3', 'auto']:
                engine = parts[0]
                text = parts[1]
        
        self.get_logger().info(f"Speaking (engine={engine or 'default'}): {text[:50]}...")
        
        if self._loop and self._initialized:
            asyncio.run_coroutine_threadsafe(
                self._speak_async(text, engine),
                self._loop
            )
    
    async def _speak_async(self, text: str, engine: Optional[str]):
        """Async speak task."""
        result = await self._brick.speak(text, engine=engine, block=True)
        
        if result.success:
            self.get_logger().info(f"Spoke successfully using {result.engine_used}")
        else:
            self.get_logger().error(f"Speak failed: {result.error_message}")
    
    def _on_control(self, msg: String):
        """
        Handle control commands.
        
        Commands:
        - 'stop': Stop current speech
        - 'preempt': Preempt current speech
        - 'clear': Clear speech queue
        - 'status': Publish status
        """
        command = msg.data.lower().strip()
        self.get_logger().info(f"Received control command: {command}")
        
        if command == 'stop' or command == 'preempt':
            if self._loop and self._initialized:
                asyncio.run_coroutine_threadsafe(
                    self._brick.preempt(),
                    self._loop
                )
                
        elif command == 'status':
            self._publish_status()
            
        else:
            self.get_logger().warning(f"Unknown command: {command}")
    
    def _on_volume(self, msg: Float32):
        """Handle volume change."""
        volume = max(0.0, min(1.0, msg.data))
        self._brick.volume = volume
        self.get_logger().info(f"Volume set to {volume}")
    
    def _publish_status(self):
        """Publish TTS status."""
        if not self._initialized:
            return
        
        status = self._brick.get_status()
        
        # Publish speaking state
        speaking_msg = Bool()
        speaking_msg.data = status['is_speaking']
        self._speaking_pub.publish(speaking_msg)
        
        # Publish status string
        status_str = (
            f"engine={status['default_engine']}, "
            f"online={status['is_online']}, "
            f"speaking={status['is_speaking']}, "
            f"count={status['speak_count']}"
        )
        
        msg = String()
        msg.data = status_str
        self._status_pub.publish(msg)
    
    def destroy_node(self):
        """Clean shutdown."""
        self.get_logger().info("Shutting down TTSNode...")
        
        self._status_timer.cancel()
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
        node = TTSNode()
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

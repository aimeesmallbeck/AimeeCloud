#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
ROS2 Node for Test Dashboard

This node runs the Flask web dashboard and integrates with ROS2:
- Monitors ROS2 topics
- Allows testing via web interface
- Publishes test commands

Usage:
    ros2 run aimee_test_dashboard dashboard_node
    
Then open browser to: http://localhost:5000
"""

import logging
import os
import signal
import sys
import threading
import time
from pathlib import Path

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import String, Bool
from aimee_msgs.msg import (
    WakeWordDetection, Transcription, Intent, RobotState
)

# Import Flask app
sys.path.insert(0, str(Path(__file__).parent / 'web'))
from app import app, _dashboard_state, _component_config, run_flask_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DashboardNode(Node):
    """
    ROS2 Node for Test Dashboard.
    
    This node:
    - Runs Flask web server
    - Subscribes to all relevant topics
    - Publishes test commands
    """
    
    def __init__(self):
        super().__init__('test_dashboard')
        
        # Declare parameters
        self.declare_parameters(namespace='', parameters=[
            ('host', '0.0.0.0'),
            ('port', 5000),
            ('debug', False),
        ])
        
        # Get parameters
        self._host = self.get_parameter('host').value
        self._port = self.get_parameter('port').value
        self._debug = self.get_parameter('debug').value
        
        self.get_logger().info(
            f"Dashboard will be available at http://{self._host}:{self._port}"
        )
        
        # Setup QoS
        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        
        # Publishers (for testing)
        self._wake_word_control_pub = self.create_publisher(
            String, '/wake_word/control', reliable_qos
        )
        self._voice_control_pub = self.create_publisher(
            String, '/voice/control', reliable_qos
        )
        self._tts_speak_pub = self.create_publisher(
            String, '/tts/speak', reliable_qos
        )
        self._tts_control_pub = self.create_publisher(
            String, '/tts/control', reliable_qos
        )
        
        # Subscribers (for monitoring)
        self._wake_word_sub = self.create_subscription(
            WakeWordDetection,
            '/wake_word/detected',
            self._on_wake_word,
            sensor_qos
        )
        
        self._transcription_sub = self.create_subscription(
            Transcription,
            '/voice/transcription',
            self._on_transcription,
            reliable_qos
        )
        
        self._intent_sub = self.create_subscription(
            Intent,
            '/intent/classified',
            self._on_intent,
            reliable_qos
        )
        
        self._tts_status_sub = self.create_subscription(
            String,
            '/tts/status',
            self._on_tts_status,
            reliable_qos
        )
        
        self._skill_status_sub = self.create_subscription(
            String,
            '/skill/status',
            self._on_skill_status,
            reliable_qos
        )
        
        self._robot_state_sub = self.create_subscription(
            RobotState,
            '/robot/state',
            self._on_robot_state,
            sensor_qos
        )
        
        # State
        self._topics_data = {
            'wake_word': None,
            'transcription': None,
            'intent': None,
            'tts_status': None,
            'skill_status': None,
            'robot_state': None,
        }
        
        # Flask thread
        self._flask_thread = None
        self._shutdown_event = threading.Event()
        
        # Update timer
        self._update_timer = self.create_timer(1.0, self._update_dashboard_state)
        
        self.get_logger().info("DashboardNode initialized")
    
    def start_flask(self):
        """Start Flask server in separate thread."""
        def run_server():
            try:
                # Disable Flask's default logging
                import logging
                werkzeug_logger = logging.getLogger('werkzeug')
                werkzeug_logger.setLevel(logging.ERROR)
                
                run_flask_app(
                    host=self._host,
                    port=self._port,
                    debug=self._debug
                )
            except Exception as e:
                self.get_logger().error(f"Flask server error: {e}")
        
        self._flask_thread = threading.Thread(target=run_server, daemon=True)
        self._flask_thread.start()
        
        self.get_logger().info(f"Flask server started on http://{self._host}:{self._port}")
    
    # ==================== Subscribers ====================
    
    def _on_wake_word(self, msg):
        """Handle wake word detection."""
        self._topics_data['wake_word'] = {
            'keyword': msg.wake_word,
            'confidence': msg.confidence,
            'timestamp': time.time()
        }
    
    def _on_transcription(self, msg):
        """Handle transcription."""
        self._topics_data['transcription'] = {
            'text': msg.text,
            'confidence': msg.confidence,
            'is_command': msg.is_command,
            'timestamp': time.time()
        }
    
    def _on_intent(self, msg):
        """Handle intent classification."""
        self._topics_data['intent'] = {
            'type': msg.intent_type,
            'action': msg.action,
            'confidence': msg.confidence,
            'skill_name': msg.skill_name,
            'timestamp': time.time()
        }
    
    def _on_tts_status(self, msg):
        """Handle TTS status."""
        self._topics_data['tts_status'] = {
            'status': msg.data,
            'timestamp': time.time()
        }
    
    def _on_skill_status(self, msg):
        """Handle skill status."""
        self._topics_data['skill_status'] = {
            'status': msg.data,
            'timestamp': time.time()
        }
    
    def _on_robot_state(self, msg):
        """Handle robot state."""
        self._topics_data['robot_state'] = {
            'status': msg.status,
            'timestamp': time.time()
        }
    
    def _update_dashboard_state(self):
        """Update global dashboard state with ROS2 data."""
        global _dashboard_state
        
        _dashboard_state['ros2_connected'] = True
        _dashboard_state['last_update'] = time.time()
        _dashboard_state['topics'] = self._topics_data
        
        # Build system health
        health = {}
        for name, data in self._topics_data.items():
            if data and 'timestamp' in data:
                age = time.time() - data['timestamp']
                health[name] = {
                    'active': age < 10.0,  # Active if updated in last 10s
                    'age_seconds': age
                }
            else:
                health[name] = {'active': False, 'age_seconds': None}
        
        _dashboard_state['system_health'] = health
    
    # ==================== Publishers for Testing ====================
    
    def publish_wake_word_trigger(self):
        """Simulate wake word detection."""
        msg = String()
        msg.data = 'start'
        self._wake_word_control_pub.publish(msg)
        self.get_logger().info("Published wake word trigger")
    
    def publish_tts(self, text: str, engine: str = None):
        """Publish TTS message."""
        msg = String()
        if engine:
            msg.data = f"{engine}:{text}"
        else:
            msg.data = text
        self._tts_speak_pub.publish(msg)
        self.get_logger().info(f"Published TTS: {text[:50]}...")
    
    def destroy_node(self):
        """Clean shutdown."""
        self.get_logger().info("Shutting down DashboardNode...")
        self._shutdown_event.set()
        super().destroy_node()


def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)
    
    node = None
    try:
        node = DashboardNode()
        node.start_flask()
        
        print("\n" + "="*60)
        print("🤖 AIMEE Robot Test Dashboard")
        print("="*60)
        print(f"\n📱 Dashboard URL: http://localhost:5000")
        print("📝 Open this URL in your browser to access the dashboard")
        print("\n💡 Features:")
        print("   • Test individual components")
        print("   • Toggle simulation/real mode")
        print("   • Monitor ROS2 topics")
        print("   • Run full pipeline tests")
        print("\n⚠️  Default simulation mode for SAFETY:")
        print("   • Skills (movement/arm) - SIMULATED")
        print("   • Toggle to REAL when ready to test hardware")
        print("\n" + "="*60 + "\n")
        
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

#!/usr/bin/env python3
"""
ROS2 Node for Intent Router (Standard ROS2 implementation)

- Subscribes to /voice/transcription
- Classifies intent via external JSON config (no rebuilds needed)
- Executes local skills (movement, arm, camera, system) directly
- Routes everything else to AimeeCloud as AimeeAgent
"""

import json
import logging
import os
import uuid

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from aimee_msgs.msg import Transcription, Intent as IntentMsg

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class IntentRouterNode(Node):
    """Standard ROS2 Intent Router Node."""

    def __init__(self):
        super().__init__('intent_router')

        # Parameters
        self.declare_parameters(namespace='', parameters=[
            ('confidence_threshold', 0.6),
            ('debug', False),
            ('intent_config_path', '/workspace/config/aimee_intent_config.json'),
        ])

        self._confidence_threshold = self.get_parameter('confidence_threshold').value
        self._debug = self.get_parameter('debug').value
        intent_config_path = self.get_parameter('intent_config_path').value

        if self._debug:
            logger.setLevel(logging.DEBUG)

        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # Publishers
        self._tts_pub = self.create_publisher(String, '/tts/speak', reliable_qos)
        self._intent_pub = self.create_publisher(IntentMsg, '/intent/classified', reliable_qos)
        self._status_pub = self.create_publisher(String, '/intent/status', reliable_qos)
        self._movement_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Subscribers
        self.create_subscription(
            Transcription,
            '/voice/transcription',
            self._on_transcription,
            10
        )

        # Load intent configuration
        self._intent_config = self._load_intent_config(intent_config_path)
        self._noise_words = set(self._intent_config.get('noise_words', []))
        self._local_only_skill_names = set(self._intent_config.get('local_only_skill_names', []))

        self.get_logger().info(
            f"Intent Router initialized: "
            f"confidence_threshold={self._confidence_threshold}, "
            f"config={intent_config_path}"
        )

    def _load_intent_config(self, path: str, silent: bool = False) -> dict:
        """Load intent configuration from external JSON file."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            if not silent:
                self.get_logger().info(f"Loaded intent config from {path}")
            return config
        except Exception as e:
            self.get_logger().error(f"Failed to load intent config from {path}: {e}")
            return {"intents": {}, "noise_words": [], "local_only_skill_names": []}

    # ─────────────────────────────── Intent Classification ───────────────────────────────

    def _classify_intent(self, text: str) -> dict:
        """Classify intent using external JSON configuration (reloaded each call)."""
        # Reload config each time so edits take effect immediately
        config = self._load_intent_config(self.get_parameter('intent_config_path').value, silent=True)
        noise_words = set(config.get('noise_words', []))

        text_lower = text.lower().strip()
        cleaned = text_lower.rstrip('.').rstrip('?').rstrip('!')
        words = set(text_lower.split())

        if len(cleaned) < 2 or cleaned in noise_words:
            return {'intent_type': 'unclassified', 'action': 'noise', 'confidence': 0.0, 'requires_skill': False, 'parameters': {}}

        intents = config.get('intents', {})
        for intent_name, intent_def in intents.items():
            matched = False

            # Check words
            intent_words = set(intent_def.get('words', []))
            if intent_words and any(w in words for w in intent_words):
                matched = True

            # Check phrases (exact match when intent has exact=true)
            if not matched:
                for phrase in intent_def.get('phrases', []):
                    if intent_def.get('exact', False):
                        if text_lower == phrase:
                            matched = True
                            break
                    else:
                        if phrase in text_lower:
                            matched = True
                            break

            if matched:
                confidence = intent_def.get('confidence', 0.6)
                skill_name = intent_def.get('skill_name', '')
                requires_skill = bool(skill_name)
                if not requires_skill:
                    skill_name = "AimeeCloud"
                return {
                    'intent_type': intent_name,
                    'action': intent_name,
                    'confidence': confidence,
                    'requires_skill': requires_skill,
                    'skill_name': skill_name,
                    'parameters': {}
                }

        # Fallback: route to AimeeCloud
        return {'intent_type': 'unclassified', 'action': 'chat', 'confidence': 0.5, 'requires_skill': False, 'skill_name': 'AimeeCloud', 'parameters': {}}

    def _is_local_skill(self, skill_name: str) -> bool:
        return skill_name in self._local_only_skill_names

    def _on_transcription(self, msg: Transcription):
        """Main entry point for incoming transcriptions."""
        if not msg.is_command:
            return

        text = msg.text.strip()
        if not text:
            return

        session_id = msg.session_id if msg.session_id else str(uuid.uuid4())[:8]
        self.get_logger().info(f"Processing: '{text}'")

        intent = self._classify_intent(text)
        intent_type = intent['intent_type']
        skill_name = intent.get('skill_name', '')

        # AimeeCloud routing: everything except local skills goes to AimeeCloud
        if not self._is_local_skill(skill_name):
            intent_msg = IntentMsg()
            intent_msg.intent_type = intent_type
            intent_msg.action = intent.get('action', '')
            intent_msg.confidence = intent.get('confidence', 0.0)
            intent_msg.raw_text = text
            intent_msg.requires_skill = False
            intent_msg.skill_name = "AimeeCloud"
            intent_msg.session_id = session_id
            try:
                intent_msg.parameters_json = json.dumps(intent.get('parameters', {}))
            except Exception:
                intent_msg.parameters_json = "{}"
            self._intent_pub.publish(intent_msg)
            self.get_logger().info(
                f"Processing: '{text}' -> {intent_type} (AimeeCloud routing, "
                f"confidence: {intent['confidence']:.2f})"
            )
            return

        # Local execution path
        self._execute_intent(text, intent, session_id)

    def _execute_intent(self, text: str, intent: dict, session_id: str):
        """Execute intent locally and generate response."""
        intent_type = intent['intent_type']
        action = intent.get('action', '')
        confidence = intent.get('confidence', 0.0)
        skill_name = intent.get('skill_name', '')
        parameters = intent.get('parameters', {})

        # Publish the classified intent
        intent_msg = IntentMsg()
        intent_msg.intent_type = intent_type
        intent_msg.action = action
        intent_msg.confidence = confidence
        intent_msg.raw_text = text
        intent_msg.requires_skill = True
        intent_msg.skill_name = skill_name
        intent_msg.session_id = session_id
        try:
            intent_msg.parameters_json = json.dumps(parameters)
        except Exception:
            intent_msg.parameters_json = "{}"
        self._intent_pub.publish(intent_msg)

        self.get_logger().info(
            f"Processing: '{text}' -> {intent_type} (local, confidence: {confidence:.2f})"
        )

        # Execute local skills with fallback TTS
        response = ""
        if skill_name == 'movement':
            self._handle_movement(action)
            response = self._get_local_response(intent_type)
        elif skill_name == 'arm_control':
            response = self._get_local_response(intent_type)
        elif skill_name == 'camera':
            response = "Camera adjusted."

        if response:
            self._tts_pub.publish(String(data=response))
            self.get_logger().info(f"Sent to TTS: {response[:50]}...")

    def _get_local_response(self, intent_type: str) -> str:
        """Return a predefined response for local intents."""
        response_map = {
            'robot_forward': "Moving forward.",
            'robot_backward': "Moving backward.",
            'robot_left': "Turning left.",
            'robot_right': "Turning right.",
            'robot_stop': "Stopping.",
            'arm_raise': "Raising arm.",
            'arm_lower': "Lowering arm.",
            'arm_wave': "Waving arm.",
            'gripper_open': "Opening gripper.",
            'gripper_close': "Closing gripper.",
            'camera': "Camera adjusted.",
        }
        return response_map.get(intent_type, "Done.")

    def _handle_movement(self, action: str):
        """Publish movement commands."""
        twist = Twist()
        if action == 'robot_forward':
            twist.linear.x = 0.3
        elif action == 'robot_backward':
            twist.linear.x = -0.3
        elif action == 'robot_left':
            twist.angular.z = 0.5
        elif action == 'robot_right':
            twist.angular.z = -0.5
        elif action == 'robot_stop':
            twist.linear.x = 0.0
            twist.angular.z = 0.0
        self._movement_pub.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = IntentRouterNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

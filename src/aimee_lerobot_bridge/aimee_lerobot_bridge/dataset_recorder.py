#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
Dataset Recorder Node for LeRobot

Records robot demonstrations in ROS2 bag format for later conversion
to LeRobot dataset format. Captures synchronized observations and actions.

Usage:
    ros2 run aimee_lerobot_bridge dataset_recorder
    
    # In another terminal:
    ros2 service call /start_recording std_srvs/srv/Trigger
    ros2 service call /stop_recording std_srvs/srv/Trigger
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import Image, JointState, CameraInfo
from geometry_msgs.msg import PoseStamped, Twist
from trajectory_msgs.msg import JointTrajectory
from std_msgs.msg import String, Bool
from cv_bridge import CvBridge
import rosbag2_py
from rclpy.serialization import serialize_message
import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional
import threading


class DatasetRecorderNode(Node):
    """
    Records robot demonstrations for LeRobot training.
    
    Captures:
    - Camera images (/camera/image_raw)
    - Joint states (/joint_states)
    - Arm commands (/arm/command)
    - Base commands (/cmd_vel)
    - Task description
    """

    def __init__(self):
        super().__init__('dataset_recorder')

        # Declare parameters
        self.declare_parameters(namespace='', parameters=[
            ('output_dir', '~/aimee_datasets'),
            ('dataset_name', 'pick_place_demo'),
            ('fps', 30),
            ('observation_topics', [
                '/camera/image_raw',
                '/joint_states',
                '/arm/joint_states',
            ]),
            ('action_topics', [
                '/arm/command',
                '/cmd_vel',
            ]),
            ('camera_topics', [
                '/camera/image_raw',
            ]),
            ('compress_images', True),
            ('record_tf', True),
            ('episode_prefix', 'episode'),
        ])

        # Get parameters
        self._output_dir = os.path.expanduser(
            self.get_parameter('output_dir').value
        )
        self._dataset_name = self.get_parameter('dataset_name').value
        self._fps = self.get_parameter('fps').value
        self._obs_topics = self.get_parameter('observation_topics').value
        self._action_topics = self.get_parameter('action_topics').value
        self._camera_topics = self.get_parameter('camera_topics').value
        self._compress = self.get_parameter('compress_images').value
        self._record_tf = self.get_parameter('record_tf').value
        self._episode_prefix = self.get_parameter('episode_prefix').value

        # Create output directory
        os.makedirs(self._output_dir, exist_ok=True)

        # Setup QoS
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        # CV Bridge
        self._cv_bridge = CvBridge()

        # State
        self._is_recording = False
        self._current_episode = 0
        self._current_task = ""
        self._bag_writer: Optional[rosbag2_py.SequentialWriter] = None
        self._bag_storage_options: Optional[rosbag2_py.StorageOptions] = None
        self._bag_converter_options: Optional[rosbag2_py.ConverterOptions] = None
        self._topic_types: Dict[str, str] = {}
        self._start_time = 0.0

        # Subscribers
        self._subscribers = []
        self._setup_subscribers(sensor_qos)

        # Services
        self._srv_start = self.create_service(
            Trigger, '/start_recording', self._on_start_recording
        )
        self._srv_stop = self.create_service(
            Trigger, '/stop_recording', self._on_stop_recording
        )
        self._srv_new_episode = self.create_service(
            NewEpisode, '/new_episode', self._on_new_episode
        )

        # Publishers for status
        self._status_pub = self.create_publisher(
            DatasetStatus, '/dataset_recorder/status', 10
        )
        self._image_preview_pub = self.create_publisher(
            Image, '/dataset_recorder/image_preview', sensor_qos
        )

        # Status timer
        self._status_timer = self.create_timer(1.0, self._publish_status)

        self.get_logger().info(
            f"Dataset Recorder initialized:\n"
            f"  Output: {self._output_dir}\n"
            f"  Dataset: {self._dataset_name}\n"
            f"  FPS: {self._fps}\n"
            f"  Obs topics: {self._obs_topics}\n"
            f"  Action topics: {self._action_topics}"
        )

    def _setup_subscribers(self, qos: QoSProfile):
        """Setup topic subscribers."""
        all_topics = list(set(self._obs_topics + self._action_topics))
        
        for topic in all_topics:
            if 'image' in topic or 'camera' in topic:
                sub = self.create_subscription(
                    Image, topic, 
                    lambda msg, t=topic: self._on_image(msg, t), 
                    qos
                )
            elif 'joint' in topic:
                sub = self.create_subscription(
                    JointState, topic,
                    lambda msg, t=topic: self._on_joint_state(msg, t),
                    qos
                )
            elif 'cmd_vel' in topic:
                sub = self.create_subscription(
                    Twist, topic,
                    lambda msg, t=topic: self._on_cmd_vel(msg, t),
                    qos
                )
            else:
                sub = self.create_subscription(
                    String, topic,
                    lambda msg, t=topic: self._on_string(msg, t),
                    qos
                )
            self._subscribers.append(sub)

    def _on_start_recording(self, request, response):
        """Start recording a new episode."""
        if self._is_recording:
            response.success = False
            response.message = "Already recording"
            return response

        self._start_recording()
        response.success = True
        response.message = f"Started recording episode {self._current_episode}"
        return response

    def _on_stop_recording(self, request, response):
        """Stop current recording."""
        if not self._is_recording:
            response.success = False
            response.message = "Not recording"
            return response

        self._stop_recording()
        response.success = True
        response.message = f"Stopped episode {self._current_episode}"
        return response

    def _on_new_episode(self, request, response):
        """Start a new episode with task description."""
        self._current_task = request.task
        
        # Stop previous if recording
        if self._is_recording:
            self._stop_recording()
        
        self._current_episode += 1
        self._start_recording()
        
        response.success = True
        response.message = f"Started episode {self._current_episode}: {self._current_task}"
        return response

    def _start_recording(self):
        """Initialize bag writer and start recording."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        bag_name = f"{self._episode_prefix}_{self._current_episode:03d}_{timestamp}"
        bag_path = os.path.join(self._output_dir, self._dataset_name, bag_name)
        
        os.makedirs(bag_path, exist_ok=True)

        # Setup bag writer
        self._bag_storage_options = rosbag2_py.StorageOptions(
            uri=bag_path,
            storage_id='mcap'  # or 'sqlite3'
        )
        self._bag_converter_options = rosbag2_py.ConverterOptions(
            input_serialization_format='cdr',
            output_serialization_format='cdr'
        )
        
        self._bag_writer = rosbag2_py.SequentialWriter()
        self._bag_writer.open(
            self._bag_storage_options,
            self._bag_converter_options
        )

        # Create topics
        self._create_bag_topics()

        # Write metadata
        self._write_metadata()

        self._is_recording = True
        self._start_time = time.time()
        
        self.get_logger().info(f"Started recording to {bag_path}")

    def _stop_recording(self):
        """Stop recording and finalize bag."""
        if self._bag_writer:
            # Write episode stats
            duration = time.time() - self._start_time
            stats = {
                'episode': self._current_episode,
                'task': self._current_task,
                'duration': duration,
                'frames': int(duration * self._fps),
            }
            self._write_stats(stats)
            
            self._bag_writer.close()
            self._bag_writer = None

        self._is_recording = False
        self.get_logger().info(f"Stopped episode {self._current_episode}")

    def _create_bag_topics(self):
        """Register topics with bag writer."""
        topic_types = {
            '/camera/image_raw': 'sensor_msgs/msg/Image',
            '/joint_states': 'sensor_msgs/msg/JointState',
            '/arm/joint_states': 'sensor_msgs/msg/JointState',
            '/arm/command': 'trajectory_msgs/msg/JointTrajectory',
            '/cmd_vel': 'geometry_msgs/msg/Twist',
            '/tf': 'tf2_msgs/msg/TFMessage',
        }

        for topic in self._obs_topics + self._action_topics:
            if topic in topic_types:
                topic_info = rosbag2_py.TopicMetadata(
                    name=topic,
                    type=topic_types[topic],
                    serialization_format='cdr'
                )
                self._bag_writer.create_topic(topic_info)
                self._topic_types[topic] = topic_types[topic]

    def _write_metadata(self):
        """Write dataset metadata to bag."""
        metadata = {
            'dataset_name': self._dataset_name,
            'episode': self._current_episode,
            'task': self._current_task,
            'fps': self._fps,
            'observation_topics': self._obs_topics,
            'action_topics': self._action_topics,
            'camera_topics': self._camera_topics,
            'timestamp': datetime.now().isoformat(),
        }
        
        # Write as string message
        msg = String()
        msg.data = json.dumps(metadata)
        self._write_message('/dataset_metadata', msg, 'std_msgs/msg/String')

    def _write_stats(self, stats: dict):
        """Write episode statistics."""
        msg = String()
        msg.data = json.dumps(stats)
        self._write_message('/episode_stats', msg, 'std_msgs/msg/String')

    def _write_message(self, topic: str, msg, msg_type: str):
        """Write a message to the bag."""
        if self._bag_writer is None:
            return

        timestamp = self.get_clock().now()
        
        # Convert to rosbag2 write format
        self._bag_writer.write(
            topic,
            serialize_message(msg),
            timestamp.nanoseconds
        )

    def _on_image(self, msg: Image, topic: str):
        """Handle image messages."""
        if not self._is_recording:
            # Still publish preview
            self._image_preview_pub.publish(msg)
            return

        # Optionally compress
        if self._compress:
            # Convert to compressed if needed
            pass

        self._write_message(topic, msg, 'sensor_msgs/msg/Image')

    def _on_joint_state(self, msg: JointState, topic: str):
        """Handle joint state messages."""
        if not self._is_recording:
            return

        self._write_message(topic, msg, 'sensor_msgs/msg/JointState')

    def _on_cmd_vel(self, msg: Twist, topic: str):
        """Handle velocity commands."""
        if not self._is_recording:
            return

        self._write_message(topic, msg, 'geometry_msgs/msg/Twist')

    def _on_string(self, msg: String, topic: str):
        """Handle string messages."""
        if not self._is_recording:
            return

        self._write_message(topic, msg, 'std_msgs/msg/String')

    def _publish_status(self):
        """Publish recorder status."""
        status = DatasetStatus()
        status.is_recording = self._is_recording
        status.episode_number = self._current_episode
        status.current_task = self._current_task
        
        if self._is_recording:
            status.duration = time.time() - self._start_time
        else:
            status.duration = 0.0
            
        self._status_pub.publish(status)

    def destroy_node(self):
        """Clean shutdown."""
        if self._is_recording:
            self._stop_recording()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = DatasetRecorderNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

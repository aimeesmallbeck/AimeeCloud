#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
Dataset Recorder Node for LeRobot

Records robot demonstrations in ROS2 bag format for later conversion
to LeRobot dataset format. Captures synchronized observations and actions.
Optimized to use native C++ ros2 bag record to prevent Python deserialization overhead.

Usage:
    ros2 run aimee_lerobot_bridge dataset_recorder
    
    # In another terminal:
    ros2 service call /start_recording std_srvs/srv/Trigger
    ros2 service call /stop_recording std_srvs/srv/Trigger
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import String, Bool
import subprocess
import os
import signal
import time
import json
from datetime import datetime
from typing import Dict, List, Optional
import threading

# Import service types
try:
    from std_srvs.srv import Trigger
    # Using generic Trigger since NewEpisode isn't standard, will mock string data for simplicity
except ImportError:
    pass

class DatasetStatus:
    pass # Mock or use the actual message type from aimee_msgs if available

class DatasetRecorderNode(Node):
    """
    Records robot demonstrations for LeRobot training using native ros2 bag record.
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
                '/arm/joint_trajectory',
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
        self._output_dir = os.path.expanduser(self.get_parameter('output_dir').value)
        self._dataset_name = self.get_parameter('dataset_name').value
        self._fps = self.get_parameter('fps').value
        self._obs_topics = self.get_parameter('observation_topics').value
        self._action_topics = self.get_parameter('action_topics').value
        self._camera_topics = self.get_parameter('camera_topics').value
        self._compress = self.get_parameter('compress_images').value
        self._record_tf = self.get_parameter('record_tf').value
        self._episode_prefix = self.get_parameter('episode_prefix').value

        os.makedirs(self._output_dir, exist_ok=True)

        self._is_recording = False
        self._current_episode = 0
        self._current_task = ""
        self._start_time = 0.0
        self._record_process: Optional[subprocess.Popen] = None

        # Publishers for metadata that the bag will record
        self._metadata_pub = self.create_publisher(String, '/dataset_metadata', 10)
        self._stats_pub = self.create_publisher(String, '/episode_stats', 10)

        # Services
        self._srv_start = self.create_service(Trigger, '/start_recording', self._on_start_recording)
        self._srv_stop = self.create_service(Trigger, '/stop_recording', self._on_stop_recording)
        
        self.get_logger().info(
            f"Dataset Recorder initialized:\n"
            f"  Output: {self._output_dir}\n"
            f"  Dataset: {self._dataset_name}\n"
            f"  Obs topics: {self._obs_topics}\n"
            f"  Action topics: {self._action_topics}"
        )

    def _on_start_recording(self, request, response):
        if self._is_recording:
            response.success = False
            response.message = "Already recording"
            return response

        self._start_recording()
        response.success = True
        response.message = f"Started recording episode {self._current_episode}"
        return response

    def _on_stop_recording(self, request, response):
        if not self._is_recording:
            response.success = False
            response.message = "Not recording"
            return response

        self._stop_recording()
        response.success = True
        response.message = f"Stopped episode {self._current_episode}"
        return response

    def _start_recording(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        bag_name = f"{self._episode_prefix}_{self._current_episode:03d}_{timestamp}"
        bag_path = os.path.join(self._output_dir, self._dataset_name, bag_name)
        
        os.makedirs(bag_path, exist_ok=True)

        # Write metadata to topics so the bag catches them
        self._write_metadata()

        topics_to_record = self._obs_topics + self._action_topics + ['/dataset_metadata', '/episode_stats']
        if self._record_tf:
            topics_to_record.append('/tf')
            topics_to_record.append('/tf_static')

        # Launch native ros2 bag record as subprocess
        cmd = ['ros2', 'bag', 'record', '-o', bag_path] + list(set(topics_to_record))
        
        self._record_process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid  # Put in own process group for clean shutdown
        )

        self._is_recording = True
        self._start_time = time.time()
        self.get_logger().info(f"Started recording to {bag_path} via C++ ros2 bag record")

    def _stop_recording(self):
        if self._record_process:
            # Write episode stats before killing bag process
            duration = time.time() - self._start_time
            stats = {
                'episode': self._current_episode,
                'task': self._current_task,
                'duration': duration,
                'frames': int(duration * self._fps),
            }
            self._write_stats(stats)
            
            # Allow time for stats to publish
            time.sleep(0.5)

            # Send SIGINT to gracefully close the bag
            try:
                os.killpg(os.getpgid(self._record_process.pid), signal.SIGINT)
                self._record_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(os.getpgid(self._record_process.pid), signal.SIGKILL)
            except ProcessLookupError:
                pass
            
            self._record_process = None

        self._is_recording = False
        self.get_logger().info(f"Stopped episode {self._current_episode}")

    def _write_metadata(self):
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
        msg = String()
        msg.data = json.dumps(metadata)
        self._metadata_pub.publish(msg)

    def _write_stats(self, stats: dict):
        msg = String()
        msg.data = json.dumps(stats)
        self._stats_pub.publish(msg)

    def destroy_node(self):
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

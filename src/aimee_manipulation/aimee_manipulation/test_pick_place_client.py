#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
Test client for PickPlace action server (test mode).

Sends pick/place goals to the action server without requiring vision.

Usage (inside ROS2 container):
    ros2 run aimee_manipulation test_pick_place_client \
        --ros-args -p object:=corner_1 -p enable_place:=true

Available test objects (23.5cm square, hand-taught positions):
    corner_1   - Front-left corner  (x=360, y=-112, z=-208)
    corner_2   - Front-right corner (x=370, y=+99,  z=-205)
    corner_3   - Back-right corner  (x=146, y=+95,  z=-207)
    corner_4   - Back-left corner   (x=123, y=-117, z=-210)

Place position (hand-taught):
    x=254, y=+162, z=-215  (to the right of the square)
"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from aimee_msgs.action import PickPlace
import sys


class TestPickPlaceClient(Node):
    """Simple client to test pick/place without vision."""

    def __init__(self):
        super().__init__('test_pick_place_client')

        self.declare_parameters(namespace='', parameters=[
            ('object', 'test_center'),
            ('enable_place', True),
            ('timeout', 60.0),
        ])

        self._object = self.get_parameter('object').value
        self._enable_place = self.get_parameter('enable_place').value
        self._timeout = self.get_parameter('timeout').value

        self._action_client = ActionClient(
            self, PickPlace, '/manipulation/pick_place'
        )
        self._done = False

        self.get_logger().info(
            f"Test client initialized:\n"
            f"  Object: {self._object}\n"
            f"  Enable place: {self._enable_place}\n"
            f"  Timeout: {self._timeout}s"
        )

    def send_goal(self):
        """Send pick/place goal."""
        self.get_logger().info("Waiting for action server...")
        if not self._action_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error("Action server not available!")
            return False

        goal_msg = PickPlace.Goal()
        goal_msg.object_class = self._object
        goal_msg.object_color = ""  # Not used in test mode
        goal_msg.enable_place = self._enable_place
        goal_msg.natural_language_request = f"pick up {self._object}"

        self.get_logger().info(
            f"Sending goal: pick '{self._object}' "
            f"(place={'yes' if self._enable_place else 'no'})"
        )

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self._feedback_callback
        )
        self._send_goal_future.add_done_callback(self._goal_response_callback)
        return True

    def _goal_response_callback(self, future):
        """Handle goal response."""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error("Goal rejected!")
            rclpy.shutdown()
            return

        self.get_logger().info("Goal accepted, waiting for result...")
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self._result_callback)

    def _result_callback(self, future):
        """Handle result."""
        result = future.result().result
        if result.success:
            self.get_logger().info(
                f"✅ SUCCESS: {result.message}\n"
                f"   Execution time: {result.execution_time:.1f}s\n"
                f"   Retries: {result.retry_count}"
            )
        else:
            self.get_logger().error(
                f"❌ FAILED: {result.failure_reason}\n"
                f"   Phase: {result.failure_phase}"
            )
        # Signal completion - main() will handle shutdown
        self._done = True

    def _feedback_callback(self, feedback_msg):
        """Handle feedback."""
        fb = feedback_msg.feedback
        self.get_logger().info(
            f"  Phase: {fb.current_phase} ({fb.phase_progress}%)"
        )


def main(args=None):
    rclpy.init(args=args)
    node = TestPickPlaceClient()

    if not node.send_goal():
        sys.exit(1)

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

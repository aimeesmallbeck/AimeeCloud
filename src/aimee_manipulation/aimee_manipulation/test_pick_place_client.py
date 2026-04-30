#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
Test client for GraspPose publisher (new workflow mode).

Sends pick goals to the new arm kinematics bridge over /manipulation/grasp_pose.

Usage (inside ROS2 container):
    ros2 run aimee_manipulation test_pick_place_client \
        --ros-args -p object:=corner_1

Available test objects (23.5cm square, hand-taught positions):
    corner_1   - Front-left corner  (x=0.360, y=-0.112, z=-0.208)
    corner_2   - Front-right corner (x=0.370, y=0.099,  z=-0.205)
    corner_3   - Back-right corner  (x=0.146, y=0.095,  z=-0.207)
    corner_4   - Back-left corner   (x=0.123, y=-0.117, z=-0.210)
"""

import rclpy
from rclpy.node import Node
from aimee_msgs.msg import GraspPose
from geometry_msgs.msg import Pose
import sys
import time

LOCATIONS = {
    'corner_1': (0.360, -0.112, -0.208),
    'corner_2': (0.370, 0.099, -0.205),
    'corner_3': (0.146, 0.095, -0.207),
    'corner_4': (0.123, -0.117, -0.210),
}

class TestGraspClient(Node):
    """Simple client to test pick using GraspPose without vision."""

    def __init__(self):
        super().__init__('test_pick_place_client')

        self.declare_parameters(namespace='', parameters=[
            ('object', 'corner_1'),
            ('timeout', 60.0),
        ])

        self._object = self.get_parameter('object').value
        self._timeout = self.get_parameter('timeout').value

        self._publisher = self.create_publisher(
            GraspPose, '/manipulation/grasp_pose', 10
        )

        self.get_logger().info(
            f"Test client initialized:\n"
            f"  Object: {self._object}\n"
        )
        
        # Give the publisher some time to connect to subscribers
        time.sleep(1.0)

    def send_goal(self):
        """Send grasp pose message."""
        if self._object not in LOCATIONS:
            self.get_logger().error(f"Unknown object location: {self._object}. Valid options: {list(LOCATIONS.keys())}")
            return False
            
        x, y, z = LOCATIONS[self._object]
        
        msg = GraspPose()
        msg.object_id = self._object
        msg.object_class = "test_object"
        
        # Pre-grasp: slightly higher than grasp
        msg.pre_grasp_pose = Pose()
        msg.pre_grasp_pose.position.x = x
        msg.pre_grasp_pose.position.y = y
        msg.pre_grasp_pose.position.z = z + 0.05
        
        # Grasp
        msg.grasp_pose = Pose()
        msg.grasp_pose.position.x = x
        msg.grasp_pose.position.y = y
        msg.grasp_pose.position.z = z
        
        # Lift: same height as pre-grasp
        msg.lift_pose = Pose()
        msg.lift_pose.position.x = x
        msg.lift_pose.position.y = y
        msg.lift_pose.position.z = z + 0.05
        
        msg.gripper_open_width = 0.05 # 5cm
        msg.gripper_close_width = 0.0 # fully closed
        
        self.get_logger().info(f"Sending GraspPose for '{self._object}' at ({x}, {y}, {z})")
        self._publisher.publish(msg)
        
        return True

def main(args=None):
    rclpy.init(args=args)
    node = TestGraspClient()

    if node.send_goal():
        node.get_logger().info("Goal sent! Exiting in 5 seconds to allow message to process...")
        time.sleep(5.0)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

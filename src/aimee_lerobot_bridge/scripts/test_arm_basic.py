#!/usr/bin/env python3
"""
Basic test script for RoArm-M3 via ROS2.

Moves the arm through a simple sequence:
1. Home position
2. Elbow down 45°
3. Base rotate 30°
4. Gripper close
5. Gripper open
6. Return home

Usage (inside the ROS2 container):
    ros2 run aimee_lerobot_bridge test_arm_basic

Or from outside the container:
    docker exec -it aimee-robot bash -c \
        "source /ros_entrypoint.sh && source /workspace/install/setup.bash && \
         ros2 run aimee_lerobot_bridge test_arm_basic"
"""

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import numpy as np
import time


JOINT_NAMES = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'gripper']

# Positions in radians
HOME = [0.0, 0.0, 1.57, 0.0, 0.0, 3.14]
ELBOW_DOWN = [0.0, 0.0, 0.78, 0.0, 0.0, 3.14]
BASE_RIGHT = [0.52, 0.0, 0.78, 0.0, 0.0, 3.14]
GRIPPER_CLOSE = [0.52, 0.0, 0.78, 0.0, 0.0, 0.0]
GRIPPER_OPEN = [0.52, 0.0, 0.78, 0.0, 0.0, 3.14]

SEQUENCE = [
    ("Home", HOME, 3.0),
    ("Elbow down 45°", ELBOW_DOWN, 3.0),
    ("Base rotate right 30°", BASE_RIGHT, 3.0),
    ("Gripper close", GRIPPER_CLOSE, 2.0),
    ("Gripper open", GRIPPER_OPEN, 2.0),
    ("Return home", HOME, 3.0),
]


class ArmTestNode(Node):
    def __init__(self):
        super().__init__('test_arm_basic')
        self._pub = self.create_publisher(
            JointTrajectory, '/arm/joint_trajectory', 10
        )
        self.get_logger().info("Arm Basic Test Node started")
        time.sleep(1.0)  # Wait for connections

    def move_to(self, name: str, positions: list, wait: float):
        self.get_logger().info(f"➡️  {name}")
        msg = JointTrajectory()
        msg.joint_names = JOINT_NAMES
        point = JointTrajectoryPoint()
        point.positions = positions
        point.time_from_start.sec = 1
        msg.points.append(point)
        self._pub.publish(msg)
        time.sleep(wait)

    def run(self):
        self.get_logger().info("=" * 50)
        self.get_logger().info("Starting RoArm-M3 basic movement test")
        self.get_logger().info("=" * 50)
        self.get_logger().info("")
        self.get_logger().info("Make sure the arm has clear space to move!")
        self.get_logger().info("Starting in 3 seconds...")
        time.sleep(3.0)

        for name, positions, wait in SEQUENCE:
            self.move_to(name, positions, wait)

        self.get_logger().info("")
        self.get_logger().info("=" * 50)
        self.get_logger().info("✅ Test sequence complete!")
        self.get_logger().info("=" * 50)


def main(args=None):
    rclpy.init(args=args)
    node = ArmTestNode()
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

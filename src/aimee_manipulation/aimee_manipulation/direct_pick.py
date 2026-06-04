#!/usr/bin/env python3
"""
Direct Pick/Place Script

Commands the arm to pick up at a specific (X,Y,Z) coordinate without
requiring vision detection. Useful for AimeeCloud-driven game moves.

Usage:
    ros2 run aimee_manipulation direct_pick --ros-args \
        -p target_x:=-0.245 -p target_y:=0.293 -p target_z:=-0.08 \
        -p surface_offset:=0.01 -p enable_place:=false

Safety:
    - Always ensure 12V power is on before running
    - Keep hand on emergency stop for first tests
    - Verify coordinates are within arm workspace before executing
"""

import rclpy
from rclpy.node import Node
from aimee_msgs.msg import ArmCommand, GraspPose
from geometry_msgs.msg import Pose, Point, Quaternion
import time
import numpy as np


class DirectPick(Node):
    def __init__(self):
        super().__init__('direct_pick')

        self.declare_parameters(namespace='', parameters=[
            ('target_x', 0.0),
            ('target_y', 0.0),
            ('target_z', -0.08),
            ('surface_offset', 0.01),   # meters above physical surface
            ('approach_offset', 0.10),  # meters above target for approach
            ('lift_height', 0.10),      # meters to lift after grasp
            ('gripper_open', 0.08),
            ('gripper_close', 0.02),
            ('move_duration_ms', 4000),
            ('grasp_duration_ms', 2000),
            ('enable_place', False),
            ('place_x', 0.0),
            ('place_y', 0.0),
            ('place_z', -0.08),
        ])

        self._target_x = self.get_parameter('target_x').value
        self._target_y = self.get_parameter('target_y').value
        self._target_z = self.get_parameter('target_z').value
        self._surface_offset = self.get_parameter('surface_offset').value
        self._approach_offset = self.get_parameter('approach_offset').value
        self._lift_height = self.get_parameter('lift_height').value
        self._gripper_open = self.get_parameter('gripper_open').value
        self._gripper_close = self.get_parameter('gripper_close').value
        self._move_dur = self.get_parameter('move_duration_ms').value
        self._grasp_dur = self.get_parameter('grasp_duration_ms').value
        self._enable_place = self.get_parameter('enable_place').value
        self._place_x = self.get_parameter('place_x').value
        self._place_y = self.get_parameter('place_y').value
        self._place_z = self.get_parameter('place_z').value

        self._pub = self.create_publisher(ArmCommand, '/arm/command', 10)
        time.sleep(1.0)  # Wait for publisher discovery

        self.get_logger().info(
            f"DirectPick initialized:\n"
            f"  Target: ({self._target_x:.3f}, {self._target_y:.3f}, {self._target_z:.3f})\n"
            f"  Surface offset: {self._surface_offset:.3f}m\n"
            f"  Approach offset: {self._approach_offset:.3f}m\n"
            f"  Place enabled: {self._enable_place}"
        )

    def _send_cartesian(self, x: float, y: float, z: float, gripper_w: float, duration_ms: int):
        cmd = ArmCommand()
        cmd.command_type = "cartesian"
        cmd.target_pose.position.x = x
        cmd.target_pose.position.y = y
        cmd.target_pose.position.z = z
        # Gripper pointing down (pitch = 90°)
        cmd.target_pose.orientation.x = 0.0
        cmd.target_pose.orientation.y = 0.7071067811865475
        cmd.target_pose.orientation.z = 0.0
        cmd.target_pose.orientation.w = 0.7071067811865475
        cmd.gripper_position = gripper_w
        cmd.cartesian_speed = float(duration_ms)
        self._pub.publish(cmd)
        self.get_logger().info(
            f"  → X={x:.3f} Y={y:.3f} Z={z:.3f} gripper={gripper_w:.3f} ({duration_ms}ms)"
        )

    def _send_grasp_sequence(self, grasp: GraspPose, duration_ms: int = 1500):
        cmd = ArmCommand()
        cmd.command_type = "grasp"
        cmd.grasp_pose = grasp
        self._pub.publish(cmd)
        self.get_logger().info("  → Grasp sequence sent")

    def _send_home(self):
        cmd = ArmCommand()
        cmd.command_type = "home"
        self._pub.publish(cmd)
        self.get_logger().info("  → Home command sent")

    def run(self):
        # Grasp Z = target Z + surface_offset (e.g., desk -0.09 + 0.01 = -0.08)
        grasp_z = self._target_z + self._surface_offset
        approach_z = grasp_z + self._approach_offset
        lift_z = grasp_z + self._lift_height

        self.get_logger().info("=" * 40)
        self.get_logger().info("DIRECT PICK SEQUENCE STARTING")
        self.get_logger().info("=" * 40)

        # 1. Approach with open gripper
        self.get_logger().info("Step 1/5: Approach (open gripper)")
        self._send_cartesian(
            self._target_x, self._target_y, approach_z,
            self._gripper_open, self._move_dur
        )
        time.sleep(self._move_dur / 1000.0 + 1.0)

        # 2. Lower to grasp position
        self.get_logger().info("Step 2/5: Lower to grasp")
        self._send_cartesian(
            self._target_x, self._target_y, grasp_z,
            self._gripper_open, self._move_dur
        )
        time.sleep(self._move_dur / 1000.0 + 1.0)

        # 3. Close gripper
        self.get_logger().info("Step 3/5: Close gripper")
        self._send_cartesian(
            self._target_x, self._target_y, grasp_z,
            self._gripper_close, self._grasp_dur
        )
        time.sleep(self._grasp_dur / 1000.0 + 1.0)

        # 4. Lift
        self.get_logger().info("Step 4/5: Lift")
        self._send_cartesian(
            self._target_x, self._target_y, lift_z,
            self._gripper_close, self._move_dur
        )
        time.sleep(self._move_dur / 1000.0 + 1.0)

        # 5. Place (optional) or Home
        if self._enable_place:
            self.get_logger().info("Step 5/5: Place")
            place_approach_z = self._place_z + self._approach_offset
            self._send_cartesian(
                self._place_x, self._place_y, place_approach_z,
                self._gripper_close, self._move_dur
            )
            time.sleep(self._move_dur / 1000.0 + 1.0)

            self._send_cartesian(
                self._place_x, self._place_y, self._place_z,
                self._gripper_close, self._grasp_dur
            )
            time.sleep(self._grasp_dur / 1000.0 + 1.0)

            self._send_cartesian(
                self._place_x, self._place_y, self._place_z,
                self._gripper_open, self._grasp_dur
            )
            time.sleep(self._grasp_dur / 1000.0 + 1.0)

            self._send_cartesian(
                self._place_x, self._place_y, place_approach_z,
                self._gripper_open, self._move_dur
            )
            time.sleep(self._move_dur / 1000.0 + 1.0)
        else:
            self.get_logger().info("Step 5/5: Return home")

        self._send_home()
        time.sleep(6.0)

        self.get_logger().info("=" * 40)
        self.get_logger().info("DIRECT PICK SEQUENCE COMPLETE")
        self.get_logger().info("=" * 40)


def main(args=None):
    rclpy.init(args=args)
    node = DirectPick()
    try:
        node.run()
    except KeyboardInterrupt:
        node.get_logger().info("Interrupted by user")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

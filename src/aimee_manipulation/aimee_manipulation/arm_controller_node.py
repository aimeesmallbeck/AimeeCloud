#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
Arm Controller Node (Simulated)

Controls the RoArm-M3 robotic arm.
Currently simulated - prints commands instead of executing.

Usage:
    ros2 run aimee_manipulation arm_controller_node
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Pose
from aimee_msgs.msg import ArmCommand
from typing import Optional, List
import time
import json


# RoArm-M3 joint limits (degrees)
JOINT_LIMITS = {
    'base': (-90, 90),
    'shoulder': (-90, 90),
    'elbow': (-150, 0),
    'wrist1': (-90, 90),
    'wrist2': (-90, 90),
    'gripper': (0, 90),
}

# Default joint positions (home)
HOME_POSITION = [0, 0, -90, 0, 0, 0]  # base, shoulder, elbow, wrist1, wrist2, gripper


class SimulatedArmController(Node):
    """
    Simulated RoArm-M3 controller.
    
    Subscribes to ArmCommand messages and simulates execution.
    Will be replaced with actual serial communication when arm arrives.
    """

    def __init__(self):
        super().__init__('arm_controller')

        # Declare parameters
        self.declare_parameters(namespace='', parameters=[
            ('serial_port', '/dev/ttyUSB0'),
            ('baud_rate', 115200),
            ('simulation_mode', True),
            ('motion_delay', 1.0),  # Simulated motion time
            ('default_speed', 50),  # 0-100
        ])

        self._simulation = self.get_parameter('simulation_mode').value
        self._motion_delay = self.get_parameter('motion_delay').value
        self._default_speed = self.get_parameter('default_speed').value

        # Setup QoS
        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # Publishers
        self._joint_state_pub = self.create_publisher(
            JointState, '/arm/joint_states', reliable_qos
        )
        self._status_pub = self.create_publisher(
            ArmCommand, '/arm/status', reliable_qos
        )

        # Subscribers
        self._command_sub = self.create_subscription(
            ArmCommand,
            '/arm/command',
            self._on_command,
            10
        )

        # State
        self._current_joints = HOME_POSITION.copy()
        self._current_pose = Pose()  # Forward kinematics (simplified)
        self._gripper_position = 0  # 0-100
        self._is_moving = False

        # Status timer
        self._status_timer = self.create_timer(0.1, self._publish_status)

        self.get_logger().info(
            f"Arm Controller initialized:\n"
            f"  Simulation mode: {self._simulation}\n"
            f"  Motion delay: {self._motion_delay}s"
        )

    def _on_command(self, msg: ArmCommand):
        """Handle arm command."""
        self.get_logger().info(f"Received command: {msg.command_type}")

        if self._is_moving and msg.command_type != 'stop':
            self.get_logger().warn("Arm is already moving, queueing command")
            # In real implementation, queue commands

        self._is_moving = True

        try:
            if msg.command_type == 'joint':
                self._execute_joint_command(msg)
            elif msg.command_type == 'cartesian':
                self._execute_cartesian_command(msg)
            elif msg.command_type == 'grasp':
                self._execute_grasp_command(msg)
            elif msg.command_type == 'home':
                self._execute_home_command(msg)
            elif msg.command_type == 'gripper':
                self._execute_gripper_command(msg)
            elif msg.command_type == 'stop':
                self._execute_stop_command(msg)
            else:
                self.get_logger().error(f"Unknown command type: {msg.command_type}")

        except Exception as e:
            self.get_logger().error(f"Command execution error: {e}")
        finally:
            self._is_moving = False

    def _execute_joint_command(self, msg: ArmCommand):
        """Execute joint space command."""
        if len(msg.joint_angles) != 6:
            self.get_logger().error(f"Expected 6 joint angles, got {len(msg.joint_angles)}")
            return

        speed = msg.joint_speed if msg.joint_speed > 0 else self._default_speed

        self._print_command("JOINT MOVE", {
            'joints': msg.joint_angles,
            'speed': speed
        })

        # Simulate motion
        self._simulate_motion()

        # Update state
        self._current_joints = list(msg.joint_angles)

    def _execute_cartesian_command(self, msg: ArmCommand):
        """Execute cartesian space command."""
        pose = msg.target_pose

        self._print_command("CARTESIAN MOVE", {
            'position': {
                'x': round(pose.position.x, 3),
                'y': round(pose.position.y, 3),
                'z': round(pose.position.z, 3)
            },
            'orientation': {
                'x': round(pose.orientation.x, 3),
                'y': round(pose.orientation.y, 3),
                'z': round(pose.orientation.z, 3),
                'w': round(pose.orientation.w, 3)
            },
            'speed': msg.cartesian_speed
        })

        # Simulate motion
        self._simulate_motion()

        # Update state (simplified IK - not real kinematics)
        self._current_pose = pose

    def _execute_grasp_command(self, msg: ArmCommand):
        """Execute grasp sequence."""
        if not msg.grasp_pose:
            self.get_logger().error("Grasp command missing grasp_pose")
            return

        grasp = msg.grasp_pose

        # Step 1: Move to pre-grasp
        self.get_logger().info("  Step 1: Moving to pre-grasp position")
        self._print_command("PRE-GRASP", {
            'position': {
                'x': round(grasp.pre_grasp_pose.position.x, 3),
                'y': round(grasp.pre_grasp_pose.position.y, 3),
                'z': round(grasp.pre_grasp_pose.position.z, 3)
            }
        })
        self._simulate_motion()

        # Step 2: Open gripper
        self.get_logger().info("  Step 2: Opening gripper")
        self._print_command("GRIPPER", {'position': grasp.gripper_open_width * 1000})  # mm
        self._simulate_motion(0.5)

        # Step 3: Move to grasp
        self.get_logger().info("  Step 3: Moving to grasp position")
        self._print_command("GRASP", {
            'position': {
                'x': round(grasp.grasp_pose.position.x, 3),
                'y': round(grasp.grasp_pose.position.y, 3),
                'z': round(grasp.grasp_pose.position.z, 3)
            }
        })
        self._simulate_motion()

        # Step 4: Close gripper
        self.get_logger().info("  Step 4: Closing gripper")
        self._print_command("GRIPPER", {'position': grasp.gripper_close_width * 1000})
        self._gripper_position = 0  # Closed
        self._simulate_motion(0.5)

        # Step 5: Lift
        self.get_logger().info("  Step 5: Lifting")
        self._print_command("LIFT", {
            'position': {
                'x': round(grasp.lift_pose.position.x, 3),
                'y': round(grasp.lift_pose.position.y, 3),
                'z': round(grasp.lift_pose.position.z, 3)
            }
        })
        self._simulate_motion()

        self.get_logger().info("  ✓ Grasp complete!")

    def _execute_home_command(self, msg: ArmCommand):
        """Move to home position."""
        self._print_command("HOME", {})
        self._simulate_motion()
        self._current_joints = HOME_POSITION.copy()

    def _execute_gripper_command(self, msg: ArmCommand):
        """Move gripper to position."""
        self._print_command("GRIPPER", {
            'position': msg.gripper_position,
            'force': msg.gripper_force
        })
        self._simulate_motion(0.5)
        self._gripper_position = msg.gripper_position

    def _execute_stop_command(self, msg: ArmCommand):
        """Emergency stop."""
        self._print_command("STOP", {})
        self.get_logger().info("EMERGENCY STOP executed")

    def _print_command(self, cmd_type: str, data: dict):
        """Print simulated command."""
        if self._simulation:
            self.get_logger().info(
                f"\n{'='*50}\n"
                f"  [SIMULATED ARM COMMAND: {cmd_type}]\n"
                f"  {json.dumps(data, indent=2)}\n"
                f"{'='*50}"
            )
        else:
            # In real mode, send to serial
            pass

    def _simulate_motion(self, duration: Optional[float] = None):
        """Simulate arm motion time."""
        time.sleep(duration or self._motion_delay)

    def _publish_status(self):
        """Publish current arm state."""
        # Joint states
        joint_msg = JointState()
        joint_msg.header.stamp = self.get_clock().now().to_msg()
        joint_msg.header.frame_id = 'arm_base'
        joint_msg.name = ['base', 'shoulder', 'elbow', 'wrist1', 'wrist2', 'gripper']
        joint_msg.position = [j * 3.14159 / 180 for j in self._current_joints]  # deg to rad
        joint_msg.velocity = [0.0] * 6
        joint_msg.effort = [0.0] * 6

        self._joint_state_pub.publish(joint_msg)


def main(args=None):
    rclpy.init(args=args)
    node = SimulatedArmController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down...")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

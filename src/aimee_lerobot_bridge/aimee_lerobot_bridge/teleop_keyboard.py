#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
Keyboard Teleoperation Node for RoArm-M3

Maps keyboard input to joint position commands for data collection.

Controls:
    1-6: Select joint (1-5 = arm, 6 = gripper)
    +/-: Increase/decrease joint angle
    r: Reset all joints to home position
    s: Save current pose
    p: Play saved pose
    space: Emergency stop
    q/ESC: Quit

Usage:
    ros2 run aimee_lerobot_bridge teleop_keyboard
"""

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState
from std_msgs.msg import Bool
import sys
import termios
import tty
import select
import threading
import numpy as np
from typing import List, Optional, Dict


class KeyboardTeleopNode(Node):
    """Keyboard teleoperation for RoArm-M3."""

    # Default joint limits for RoArm-M3 (degrees)
    JOINT_LIMITS = {
        'joint1': (-180, 180),  # Base rotation
        'joint2': (-90, 90),    # Shoulder
        'joint3': (-150, 0),    # Elbow
        'joint4': (-90, 90),    # Wrist 1
        'joint5': (-90, 90),    # Wrist 2
        'gripper': (0, 90),     # Gripper
    }

    # Default home position
    HOME_POSITION = [0.0, 0.0, -90.0, 0.0, 0.0, 0.0]

    def __init__(self):
        super().__init__('teleop_keyboard')

        # Declare parameters
        self.declare_parameters(namespace='', parameters=[
            ('joint_names', ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'gripper']),
            ('step_size', 5.0),  # degrees per keypress
            ('publish_rate', 10.0),  # Hz
            ('action_topic', '/arm/command'),
            ('joint_state_topic', '/joint_states'),
        ])

        # Get parameters
        self._joint_names = self.get_parameter('joint_names').value
        self._step_size = self.get_parameter('step_size').value
        self._publish_rate = self.get_parameter('publish_rate').value
        self._action_topic = self.get_parameter('action_topic').value
        self._joint_state_topic = self.get_parameter('joint_state_topic').value

        # Publishers
        self._action_pub = self.create_publisher(
            JointTrajectory, self._action_topic, 10
        )
        self._estop_pub = self.create_publisher(
            Bool, '/emergency_stop', 10
        )

        # Subscribers
        self._joint_sub = self.create_subscription(
            JointState, self._joint_state_topic,
            self._on_joint_state, 10
        )

        # State
        self._current_joint_pos = list(self.HOME_POSITION)
        self._target_joint_pos = list(self.HOME_POSITION)
        self._selected_joint = 0  # 0-5
        self._saved_poses: Dict[str, List[float]] = {}
        self._estop = False
        self._running = True

        # Terminal settings
        self._old_termios = termios.tcgetattr(sys.stdin)

        # Keyboard thread
        self._keyboard_thread = threading.Thread(target=self._keyboard_loop)
        self._keyboard_thread.daemon = True

        # Publish timer
        self._timer = self.create_timer(
            1.0 / self._publish_rate, self._publish_command
        )

        self._print_help()

    def _print_help(self):
        """Print control instructions."""
        help_text = """
╔══════════════════════════════════════════════════════════════╗
║           RoArm-M3 Keyboard Teleoperation                    ║
╠══════════════════════════════════════════════════════════════╣
║  Joint Selection:                                            ║
║    1 = Base Rotation    2 = Shoulder    3 = Elbow           ║
║    4 = Wrist 1          5 = Wrist 2     6 = Gripper         ║
║                                                              ║
║  Controls:                                                   ║
║    +/-  = Increase/decrease selected joint                  ║
║    r    = Reset all joints to home                          ║
║    s    = Save current pose                                 ║
║    p    = Play saved pose                                   ║
║    h    = Print this help                                   ║
║    space = Emergency stop                                   ║
║    q/ESC = Quit                                             ║
╚══════════════════════════════════════════════════════════════╝
"""
        self.get_logger().info(help_text)
        self._print_status()

    def _print_status(self):
        """Print current joint status."""
        status = "\nCurrent Joints (deg):\n"
        for i, (name, pos) in enumerate(zip(self._joint_names, self._current_joint_pos)):
            marker = " >>>" if i == self._selected_joint else "    "
            limits = self.JOINT_LIMITS.get(name, (-180, 180))
            status += f"{marker} {name}: {pos:6.1f}° (limits: {limits[0]} to {limits[1]})\n"
        self.get_logger().info(status)

    def _get_key(self) -> str:
        """Read single keypress."""
        tty.setcbreak(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_termios)
        return key

    def _keyboard_loop(self):
        """Background keyboard input loop."""
        while self._running and rclpy.ok():
            try:
                key = self._get_key()
                self._process_key(key)
            except Exception as e:
                self.get_logger().debug(f"Keyboard error: {e}")

    def _process_key(self, key: str):
        """Process keyboard input."""
        if key == '\x1b':  # ESC
            self._running = False
        elif key == 'q':
            self._running = False
        elif key in '123456':
            self._selected_joint = int(key) - 1
            self._print_status()
        elif key in ('+', '='):
            self._adjust_joint(self._selected_joint, self._step_size)
        elif key == '-':
            self._adjust_joint(self._selected_joint, -self._step_size)
        elif key == 'r':
            self._go_home()
        elif key == 's':
            self._save_pose()
        elif key == 'p':
            self._play_pose()
        elif key == 'h':
            self._print_help()
        elif key == ' ':
            self._toggle_estop()

    def _adjust_joint(self, joint_idx: int, delta: float):
        """Adjust a joint position."""
        if self._estop:
            return

        joint_name = self._joint_names[joint_idx]
        limits = self.JOINT_LIMITS.get(joint_name, (-180, 180))

        new_pos = self._target_joint_pos[joint_idx] + delta
        new_pos = np.clip(new_pos, limits[0], limits[1])
        
        self._target_joint_pos[joint_idx] = new_pos
        self.get_logger().info(
            f"{joint_name} → {new_pos:.1f}°"
        )

    def _go_home(self):
        """Move to home position."""
        self._target_joint_pos = list(self.HOME_POSITION)
        self.get_logger().info("Moving to home position")

    def _save_pose(self):
        """Save current target pose."""
        pose_name = f"pose_{len(self._saved_poses)}"
        self._saved_poses[pose_name] = list(self._target_joint_pos)
        self.get_logger().info(f"Saved pose: {pose_name}")

    def _play_pose(self):
        """Play a saved pose."""
        if not self._saved_poses:
            self.get_logger().warn("No saved poses")
            return
        
        # For now, play the last saved pose
        pose_name = list(self._saved_poses.keys())[-1]
        self._target_joint_pos = list(self._saved_poses[pose_name])
        self.get_logger().info(f"Playing pose: {pose_name}")

    def _toggle_estop(self):
        """Toggle emergency stop."""
        self._estop = not self._estop
        self._estop_pub.publish(Bool(data=self._estop))
        
        if self._estop:
            self.get_logger().warn("🛑 EMERGENCY STOP ACTIVATED!")
        else:
            self.get_logger().info("Emergency stop released")

    def _on_joint_state(self, msg: JointState):
        """Update current joint positions."""
        for i, name in enumerate(self._joint_names):
            if name in msg.name:
                idx = msg.name.index(name)
                self._current_joint_pos[i] = np.degrees(msg.position[idx])

    def _publish_command(self):
        """Publish joint command."""
        if not self._running:
            return

        if self._estop:
            return

        # Create trajectory message
        traj = JointTrajectory()
        traj.header.stamp = self.get_clock().now().to_msg()
        traj.joint_names = self._joint_names

        point = JointTrajectoryPoint()
        # Convert degrees to radians
        point.positions = [np.radians(p) for p in self._target_joint_pos]
        point.time_from_start.sec = 0
        point.time_from_start.nanosec = int(0.1 * 1e9)  # 100ms

        traj.points.append(point)
        self._action_pub.publish(traj)

    def run(self):
        """Run the teleop node."""
        self._keyboard_thread.start()
        
        try:
            while self._running and rclpy.ok():
                rclpy.spin_once(self, timeout_sec=0.1)
        except KeyboardInterrupt:
            pass
        finally:
            self._cleanup()

    def _cleanup(self):
        """Clean up."""
        self._running = False
        
        # Stop robot
        traj = JointTrajectory()
        self._action_pub.publish(traj)
        
        # Restore terminal
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_termios)
        
        if self._keyboard_thread.is_alive():
            self._keyboard_thread.join(timeout=1.0)


def main(args=None):
    rclpy.init(args=args)
    node = KeyboardTeleopNode()
    
    try:
        node.run()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
RoArm-M3 HTTP Driver Node

Connects to the RoArm-M3 robotic arm via HTTP/WiFi and exposes it as a
standard ROS2 JointTrajectory subscriber + JointState publisher.

Firmware API (discovered empirically from the arm's web interface):
    T:102   - All joints control in radians
              params: base, shoulder, elbow, wrist, roll, hand, spd, acc
    T:106   - Gripper (EOAT) control in radians
              params: cmd, spd, acc
    T:105   - Get joint feedback
              returns: {T:1051, b, s, e, t, r, g, x, y, z, ...}
    T:100   - Home position

Joint mapping (ROS → RoArm-M3):
    joint1   → base
    joint2   → shoulder
    joint3   → elbow
    joint4   → wrist
    joint5   → roll
    gripper  → hand (via T:106 for better precision)

Coordinate frame (firmware-native radians):
    base:      0 = centered, positive = counter-clockwise (top view)
    shoulder:  0 = horizontal, positive = up, negative = down
    elbow:     0 = straight up, π/2 = horizontal forward, π = straight down
               NOTE: negative values are clamped to 0 by firmware
    wrist:     0 = straight (aligned with forearm), positive = up, negative = down
    roll:      0 = neutral, full rotation [-π, π]
    gripper:   0 = fully open, π = fully closed
               NOTE: firmware clamps effective range to ~[1.1, 3.14] rad.
               Commands below ~1.1 rad result in ~1.1 rad (fully open).

Verified joint limits (empirical, firmware v3.x on RoArm-M3-Pro):
    | Joint   | Min (rad) | Max (rad) | Notes                          |
    |---------|-----------|-----------|--------------------------------|
    | joint1  |   -3.14   |   +3.14   | Full rotation                  |
    | joint2  |   -1.57   |   +1.57   | SDK claims ±1.9, but HW=±π/2   |
    | joint3  |    0.0    |   +3.14   | Negative clamped to 0          |
    | joint4  |   -1.57   |   +1.57   | SDK claims ±1.9, but HW=±π/2   |
    | joint5  |   -3.14   |   +3.14   | Full rotation                  |
    | gripper |    0.0    |   +3.14   | Effective min ~1.1 rad         |

Usage:
    ros2 run aimee_lerobot_bridge roarm_m3_http_driver \
        --ros-args -p arm_ip:=192.168.1.57 -p poll_rate:=5.0

Parameters:
    arm_ip          - IP address of the RoArm-M3 (default: 192.168.4.1)
    poll_rate       - Feedback poll rate in Hz (default: 5.0)
    command_topic   - JointTrajectory subscription topic (default: /arm/joint_trajectory)
    joint_state_topic - JointState publication topic (default: /joint_states)
    default_speed   - Movement speed 0-4096 (default: 1000)
    default_acc     - Acceleration 1-254 (default: 100)
    connection_timeout - HTTP timeout in seconds (default: 5.0)
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState
from std_msgs.msg import Bool
import requests
import json
import threading
import time
import numpy as np
from typing import Optional, List, Dict


class RoArmM3HttpDriver(Node):
    """
    HTTP driver for RoArm-M3 robotic arm.
    """

    # Joint name mapping: ROS name → RoArm-M3 parameter name
    JOINT_MAP = {
        'joint1': 'base',
        'joint2': 'shoulder',
        'joint3': 'elbow',
        'joint4': 'wrist',
        'joint5': 'roll',
    }

    # Feedback field mapping: RoArm-M3 → ROS joint name
    FEEDBACK_MAP = {
        'b': 'joint1',
        's': 'joint2',
        'e': 'joint3',
        't': 'joint4',
        'r': 'joint5',
        'g': 'gripper',
    }

    # Verified joint limits (radians), determined empirically on RoArm-M3-Pro.
    # These match the actual firmware behavior, which differs from the SDK docs
    # in some cases (e.g. shoulder/wrist are ±π/2, not ±1.9 rad).
    JOINT_LIMITS = {
        'joint1': (-np.pi, np.pi),          # base: full rotation
        'joint2': (-np.pi/2, np.pi/2),      # shoulder: empirically ±π/2
        'joint3': (0.0, 2.967),             # elbow: 0=up, ~1.57=horizontal forward
                                            # max=170° (2.967 rad). 180° hits base.
        'joint4': (-np.pi/2, np.pi/2),      # wrist: empirically ±π/2
        'joint5': (-np.pi, np.pi),          # roll: full rotation
        'gripper': (0.0, np.pi),            # 0=fully open, π=fully closed
    }

    def __init__(self):
        super().__init__('roarm_m3_http_driver')

        # Parameters
        self.declare_parameters(namespace='', parameters=[
            ('arm_ip', '192.168.1.57'),
            ('poll_rate', 5.0),
            ('command_topic', '/arm/joint_trajectory'),
            ('joint_state_topic', '/joint_states'),
            ('default_speed', 500),   # slower for smoother motion
            ('default_acc', 50),       # lower accel for soft start/stop
            ('connection_timeout', 5.0),
            ('auto_home_on_start', False),
            ('gripper_threshold', 1.0),  # rad: below this, use T:106
        ])

        self._arm_ip = self.get_parameter('arm_ip').value
        self._poll_rate = self.get_parameter('poll_rate').value
        self._command_topic = self.get_parameter('command_topic').value
        self._joint_state_topic = self.get_parameter('joint_state_topic').value
        self._default_speed = self.get_parameter('default_speed').value
        self._default_acc = self.get_parameter('default_acc').value
        self._timeout = self.get_parameter('connection_timeout').value
        self._auto_home = self.get_parameter('auto_home_on_start').value
        self._gripper_threshold = self.get_parameter('gripper_threshold').value

        self._base_url = f"http://{self._arm_ip}/js"

        # NOTE: We intentionally do NOT use requests.Session() because the
        # ESP32's built-in web server crashes on persistent connections.
        # Each request uses a fresh connection with Connection: close.
        self._session = None

        # State
        self._current_joints: Dict[str, float] = {}
        self._target_joints: Dict[str, float] = {}
        self._connected = False
        self._estop = False
        self._lock = threading.Lock()

        # HTTP rate limiting: serialize requests and skip polls after commands
        self._http_lock = threading.Lock()
        self._last_cmd_time = 0.0
        self._cmd_cooldown = 2.0  # seconds: skip polls for 2s after a command
        self._min_request_interval = 1.0  # minimum 1s between any HTTP requests
        self._motion_wait_timeout = 10.0  # max seconds to wait for motion
        self._motion_tolerance = 0.15  # rad (~9°) tolerance for motion complete

        # Publishers
        self._joint_state_pub = self.create_publisher(
            JointState, self._joint_state_topic, 10
        )

        # Subscribers
        self._command_sub = self.create_subscription(
            JointTrajectory,
            self._command_topic,
            self._on_trajectory,
            10
        )
        self._estop_sub = self.create_subscription(
            Bool, '/emergency_stop', self._on_estop, 10
        )

        # Timers - slow polling to avoid overwhelming ESP32
        poll_period = max(2.0, 1.0 / self._poll_rate)  # at least 2 seconds
        self._poll_timer = self.create_timer(
            poll_period, self._poll_feedback
        )

        # Initialize
        self.get_logger().info(
            f"RoArm-M3 HTTP Driver initialized:\n"
            f"  Arm IP: {self._arm_ip}\n"
            f"  Command topic: {self._command_topic}\n"
            f"  Joint state topic: {self._joint_state_topic}\n"
            f"  Poll rate: {self._poll_rate} Hz"
        )

        # Test connection
        self._test_connection()

        # Optional home on start
        if self._auto_home:
            self._send_home()

    def _test_connection(self):
        """Test connection to the arm."""
        try:
            resp = self._send_command({"T": 105})
            if resp and 'b' in resp:
                self._connected = True
                self.get_logger().info(
                    f"✓ Connected to RoArm-M3 at {self._arm_ip}\n"
                    f"  Position: x={resp.get('x', 0):.1f}, "
                    f"y={resp.get('y', 0):.1f}, z={resp.get('z', 0):.1f}"
                )
                # Store initial joint positions
                for field, name in self.FEEDBACK_MAP.items():
                    if field in resp:
                        self._current_joints[name] = float(resp[field])
            else:
                self.get_logger().warn(
                    f"Connected but unexpected response from {self._arm_ip}"
                )
        except Exception as e:
            self.get_logger().error(
                f"✗ Failed to connect to RoArm-M3 at {self._arm_ip}: {e}"
            )

    def _send_command(self, cmd: dict, is_command: bool = False) -> Optional[dict]:
        """Send a JSON command to the arm via HTTP GET.

        Uses a fresh HTTP connection each time (no keep-alive) because
        the ESP32 web server crashes on persistent connections.

        Args:
            cmd: JSON command dict
            is_command: True if this is a motion command (not a poll).
        """
        with self._http_lock:
            # Enforce minimum interval between HTTP requests
            elapsed = time.time() - self._last_cmd_time
            if elapsed < self._min_request_interval:
                time.sleep(self._min_request_interval - elapsed)

            try:
                params = {"json": json.dumps(cmd)}
                # Fresh connection each time - ESP32 can't handle keep-alive
                response = requests.get(
                    self._base_url,
                    params=params,
                    timeout=self._timeout,
                    headers={'Connection': 'close'}
                )
                response.raise_for_status()
                if is_command:
                    self._last_cmd_time = time.time()
                return response.json()
            except requests.exceptions.RequestException as e:
                if self._connected:
                    self.get_logger().warn(f"HTTP request failed: {e}")
                    self._connected = False
                return None
            except json.JSONDecodeError as e:
                self.get_logger().warn(f"Invalid JSON response: {e}")
                return None

    def _on_trajectory(self, msg: JointTrajectory):
        """Handle incoming joint trajectory command."""
        if self._estop:
            self.get_logger().warn("Emergency stop active, ignoring trajectory")
            return

        if not msg.points:
            self.get_logger().warn("Empty trajectory received")
            return

        point = msg.points[0]

        # Build joint position map
        joint_positions = {}
        for i, name in enumerate(msg.joint_names):
            if i < len(point.positions):
                joint_positions[name] = float(point.positions[i])

        # Validate and clamp
        clamped = {}
        for name, pos in joint_positions.items():
            if name in self.JOINT_LIMITS:
                lo, hi = self.JOINT_LIMITS[name]
                clamped[name] = float(np.clip(pos, lo, hi))
                if clamped[name] != pos:
                    self.get_logger().warn(
                        f"Clamped {name}: {np.degrees(pos):.1f}° → "
                        f"{np.degrees(clamped[name]):.1f}°"
                    )
            else:
                clamped[name] = pos

        with self._lock:
            self._target_joints = clamped.copy()

        # Send to arm
        self._execute_command(clamped)

    def _execute_command(self, joints: Dict[str, float]):
        """Send joint positions to the arm."""
        if not self._connected:
            self.get_logger().warn("Not connected to arm, command dropped")
            return

        # Build T:102 command for arm joints
        cmd_102 = {
            "T": 102,
            "spd": self._default_speed,
            "acc": self._default_acc,
        }

        # Map ROS joint names to RoArm-M3 parameters
        for ros_name, roarm_name in self.JOINT_MAP.items():
            if ros_name in joints:
                cmd_102[roarm_name] = joints[ros_name]

        # Always include hand in T:102 to prevent firmware from resetting gripper.
        with self._lock:
            if 'gripper' in joints:
                hand_pos = joints['gripper']
            elif 'gripper' in self._current_joints:
                hand_pos = self._current_joints['gripper']
            else:
                hand_pos = None

        if hand_pos is not None:
            cmd_102['hand'] = hand_pos

        # Send T:102 for arm joints (including hand to preserve gripper)
        arm_cmd = {k: v for k, v in cmd_102.items() if k not in ('spd', 'acc')}
        if len(arm_cmd) > 1:  # More than just "T"
            resp = self._send_command(cmd_102, is_command=True)
            if resp:
                self.get_logger().debug(
                    f"Arm joints sent: { {k: round(v, 3) for k, v in arm_cmd.items() if k != 'T'} }"
                )

        # Send T:106 for gripper if explicitly commanded (required for gripper to move)
        if 'gripper' in joints:
            cmd_106 = {
                "T": 106,
                "cmd": joints['gripper'],
                "spd": self._default_speed,
                "acc": self._default_acc,
            }
            resp = self._send_command(cmd_106, is_command=True)
            if resp:
                self.get_logger().debug(
                    f"Gripper → {np.degrees(joints['gripper']):.1f}°"
                )

    def _wait_for_motion(self, target_joints: Dict[str, float]):
        """Poll joint positions until arm reaches target or timeout."""
        start = time.time()
        # Build set of joints we're waiting for
        wait_joints = {name: pos for name, pos in target_joints.items()
                       if name in self.JOINT_LIMITS}
        if not wait_joints:
            return

        self.get_logger().debug(
            f"Waiting for motion: {list(wait_joints.keys())}"
        )

        while time.time() - start < self._motion_wait_timeout:
            # Skip if we're in cooldown
            if time.time() - self._last_cmd_time < self._min_request_interval:
                time.sleep(self._min_request_interval)
                continue

            resp = self._send_command({"T": 105})
            if not resp:
                time.sleep(0.5)
                continue

            # Check if all target joints are within tolerance
            all_reached = True
            for name, target in wait_joints.items():
                field = None
                for f, n in self.FEEDBACK_MAP.items():
                    if n == name:
                        field = f
                        break
                if field and field in resp:
                    actual = float(resp[field])
                    if abs(actual - target) > self._motion_tolerance:
                        all_reached = False
                        break
                else:
                    all_reached = False
                    break

            if all_reached:
                self.get_logger().debug(
                    f"Motion complete in {time.time() - start:.1f}s"
                )
                return

            time.sleep(1.5)  # slow poll to avoid ESP32 overload

        self.get_logger().warn(
            f"Motion timeout after {self._motion_wait_timeout}s"
        )

    def _poll_feedback(self):
        """Poll arm status and publish JointState."""
        # Skip polling if a command was recently sent (let ESP32 recover)
        if time.time() - self._last_cmd_time < self._cmd_cooldown:
            return
        resp = self._send_command({"T": 105})
        if resp is None:
            return

        if not self._connected:
            self._connected = True
            self.get_logger().info("Connection restored")

        # Parse feedback fields
        joint_msg = JointState()
        joint_msg.header.stamp = self.get_clock().now().to_msg()
        joint_msg.header.frame_id = 'arm_base_link'

        for field, name in self.FEEDBACK_MAP.items():
            if field in resp:
                joint_msg.name.append(name)
                joint_msg.position.append(float(resp[field]))
                joint_msg.velocity.append(0.0)
                joint_msg.effort.append(0.0)

                with self._lock:
                    self._current_joints[name] = float(resp[field])

        # Publish if we have joints
        if joint_msg.name:
            self._joint_state_pub.publish(joint_msg)

    def _on_estop(self, msg: Bool):
        """Handle emergency stop."""
        self._estop = msg.data
        if self._estop:
            self.get_logger().warn("🛑 Emergency stop activated!")
        else:
            self.get_logger().info("Emergency stop released")

    def _send_home(self):
        """Send home command."""
        self.get_logger().info("Sending home command...")
        resp = self._send_command({"T": 100})
        if resp:
            self.get_logger().info("Home command sent")
        else:
            self.get_logger().warn("Home command failed")

    def destroy_node(self):
        """Clean shutdown."""
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = RoArmM3HttpDriver()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down...")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

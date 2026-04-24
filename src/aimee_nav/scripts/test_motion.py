#!/usr/bin/env python3
"""Basic motion accuracy test for AimeeNav.

Tests pure rotation and forward motion, measuring actual response via IMU.
Usage:
    ros2 run aimee_nav test_motion.py
"""

import math
import sys
import time

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu


class MotionTest(Node):
    def __init__(self):
        super().__init__('motion_test')
        self._best_effort_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )
        self._cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self._goal_pub = self.create_publisher(PoseStamped, '/goal_pose', 10)

        self._start_yaw = None
        self._current_yaw = None
        self._odom_yaw = None

        self.create_subscription(Odometry, '/odom', self._odom_cb, self._best_effort_qos)

    def _odom_cb(self, msg):
        q = msg.pose.pose.orientation
        siny = 2.0 * (q.w * q.z + q.x * q.y)
        cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        self._odom_yaw = math.atan2(siny, cosy)

    def wait_for_odom(self, timeout=5.0):
        self.get_logger().info("Waiting for /odom...")
        start = time.time()
        while self._odom_yaw is None and time.time() - start < timeout:
            rclpy.spin_once(self, timeout_sec=0.1)
        if self._odom_yaw is None:
            self.get_logger().error("No odometry received!")
            return False
        return True

    def send_vel(self, linear, angular, duration):
        """Send constant velocity for a duration."""
        t_end = time.time() + duration
        rate = self.create_rate(20.0)
        while time.time() < t_end and rclpy.ok():
            msg = Twist()
            msg.linear.x = float(linear)
            msg.angular.z = float(angular)
            self._cmd_pub.publish(msg)
            rclpy.spin_once(self, timeout_sec=0.01)
        # Stop
        self._cmd_pub.publish(Twist())

    def test_spin(self, target_deg, angular_speed):
        """Test pure rotation."""
        self.get_logger().info(
            f"\n=== SPIN TEST: {target_deg}° at {angular_speed:.2f} rad/s ==="
        )
        if not self.wait_for_odom():
            return

        start_yaw = self._odom_yaw
        duration = abs(math.radians(target_deg) / angular_speed)
        direction = 1.0 if target_deg > 0 else -1.0

        self.get_logger().info(
            f"Start yaw: {math.degrees(start_yaw):.1f}° | "
            f"Commanding {angular_speed:.2f} rad/s for {duration:.1f}s"
        )

        self.send_vel(0.0, angular_speed * direction, duration)
        time.sleep(0.5)  # let settle

        # Read final yaw
        for _ in range(10):
            rclpy.spin_once(self, timeout_sec=0.05)

        end_yaw = self._odom_yaw
        actual_turn = end_yaw - start_yaw
        while actual_turn > math.pi:
            actual_turn -= 2.0 * math.pi
        while actual_turn < -math.pi:
            actual_turn += 2.0 * math.pi

        error_deg = math.degrees(actual_turn) - target_deg
        self.get_logger().info(
            f"End yaw: {math.degrees(end_yaw):.1f}° | "
            f"Actual turn: {math.degrees(actual_turn):.1f}° | "
            f"Error: {error_deg:.1f}°"
        )
        return error_deg

    def test_turn_to_goal(self, delta_deg):
        """Test heading PID by publishing a goal at delta_deg offset."""
        self.get_logger().info(
            f"\n=== PID TURN TEST: turn to {delta_deg}° offset ==="
        )
        if not self.wait_for_odom():
            return

        start_yaw = self._odom_yaw
        target_yaw = start_yaw + math.radians(delta_deg)

        qz = math.sin(target_yaw / 2.0)
        qw = math.cos(target_yaw / 2.0)

        msg = PoseStamped()
        msg.header.frame_id = 'map'
        msg.pose.position.x = 0.0
        msg.pose.position.y = 0.0
        msg.pose.orientation.z = qz
        msg.pose.orientation.w = qw

        self.get_logger().info(
            f"Current: {math.degrees(start_yaw):.1f}° | "
            f"Target: {math.degrees(target_yaw):.1f}°"
        )
        self._goal_pub.publish(msg)

        # Wait for robot to settle (goal reached or timeout)
        timeout = 10.0
        start_t = time.time()
        while time.time() - start_t < timeout:
            rclpy.spin_once(self, timeout_sec=0.1)
            if self._odom_yaw is not None:
                err = self._odom_yaw - target_yaw
                while err > math.pi:
                    err -= 2.0 * math.pi
                while err < -math.pi:
                    err += 2.0 * math.pi
                if abs(err) < math.radians(5.0):
                    self.get_logger().info(
                        f"Settled within 5° in {time.time()-start_t:.1f}s"
                    )
                    break
        else:
            self.get_logger().warn("Turn did not settle within timeout")

        final_err_deg = math.degrees(self._odom_yaw - target_yaw)
        while final_err_deg > 180:
            final_err_deg -= 360
        while final_err_deg < -180:
            final_err_deg += 360
        self.get_logger().info(f"Final heading error: {final_err_deg:.1f}°")

    def run_all(self):
        """Run the full motion test suite."""
        self.get_logger().info("=" * 50)
        self.get_logger().info("AIMEE MOTION ACCURACY TEST")
        self.get_logger().info("=" * 50)

        # Test 1: Spin 90° clockwise
        self.test_spin(-90, 0.5)
        time.sleep(1.0)

        # Test 2: Spin 90° counter-clockwise
        self.test_spin(90, 0.5)
        time.sleep(1.0)

        # Test 3: Spin 180°
        self.test_spin(180, 0.5)
        time.sleep(1.0)

        # Test 4: PID turn to 90° offset
        self.test_turn_to_goal(90)
        time.sleep(1.0)

        # Test 5: PID turn to -90° offset
        self.test_turn_to_goal(-90)

        self.get_logger().info("\n=== TESTS COMPLETE ===")


def main():
    rclpy.init()
    node = MotionTest()
    try:
        node.run_all()
    except KeyboardInterrupt:
        pass
    finally:
        # Ensure stop command is sent
        node._cmd_pub.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

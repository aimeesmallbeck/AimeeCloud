#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
UGV02 Teleop Node

Keyboard control for UGV02 rover.
Maps keyboard input to velocity commands.

Controls:
    w/s - Forward/Backward
    a/d - Rotate Left/Right
    q/e - Strafe (if supported)
    space - Stop
    r - Reset odometry
    l - Toggle LED
    ESC/q - Quit

Usage:
    ros2 run aimee_ugv02_controller ugv02_teleop_node
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
import sys
import termios
import tty
import select
import threading


class UGV02TeleopNode(Node):
    """Keyboard teleoperation for UGV02."""

    def __init__(self):
        super().__init__('ugv02_teleop')

        # Declare parameters
        self.declare_parameters(namespace='', parameters=[
            ('linear_speed', 0.3),      # m/s
            ('angular_speed', 0.5),     # rad/s
            ('ramp_rate', 0.1),         # speed change per keypress
            ('cmd_rate', 10.0),         # Hz
        ])

        self._linear_speed = self.get_parameter('linear_speed').value
        self._angular_speed = self.get_parameter('angular_speed').value
        self._ramp_rate = self.get_parameter('ramp_rate').value
        self._cmd_rate = self.get_parameter('cmd_rate').value

        # Publishers
        self._cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self._estop_pub = self.create_publisher(Bool, '/emergency_stop', 10)

        # State
        self._current_linear = 0.0
        self._current_angular = 0.0
        self._target_linear = 0.0
        self._target_angular = 0.0
        self._emergency_stop = False
        self._running = True

        # Timer for command publishing
        self._timer = self.create_timer(1.0 / self._cmd_rate, self._publish_cmd)

        # Keyboard reading thread
        self._keyboard_thread = threading.Thread(target=self._keyboard_loop)
        self._keyboard_thread.daemon = True

        self.get_logger().info(
            "\n" + "="*50 + "\n"
            "  UGV02 Keyboard Teleop\n"
            "="*50 + "\n"
            "  w/s - Forward/Backward\n"
            "  a/d - Rotate Left/Right\n"
            "  space - Stop\n"
            "  r - Reset speed\n"
            "  +/- - Increase/Decrease speed\n"
            "  l - Toggle LED\n"
            "  e - Emergency stop (toggle)\n"
            "  q/ESC - Quit\n"
            "="*50 + "\n"
        )

        # Save terminal settings
        self._old_termios = termios.tcgetattr(sys.stdin)

    def _get_key(self) -> str:
        """Read single keypress from stdin."""
        tty.setcbreak(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_termios)
        return key

    def _keyboard_loop(self):
        """Background thread for keyboard input."""
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
            return
        elif key == 'q':
            self._running = False
            return
        elif key == ' ':
            # Stop
            self._target_linear = 0.0
            self._target_angular = 0.0
            self.get_logger().info("Stop")
        elif key == 'w':
            self._target_linear = self._linear_speed
            self._target_angular = 0.0
        elif key == 's':
            self._target_linear = -self._linear_speed
            self._target_angular = 0.0
        elif key == 'a':
            self._target_linear = 0.0
            self._target_angular = self._angular_speed
        elif key == 'd':
            self._target_linear = 0.0
            self._target_angular = -self._angular_speed
        elif key == 'r':
            # Reset speed
            self._current_linear = 0.0
            self._current_angular = 0.0
            self._target_linear = 0.0
            self._target_angular = 0.0
            self.get_logger().info("Speed reset")
        elif key == '+':
            self._linear_speed += self._ramp_rate
            self._angular_speed += self._ramp_rate
            self.get_logger().info(f"Speed increased: {self._linear_speed:.2f} m/s")
        elif key == '-':
            self._linear_speed = max(0.1, self._linear_speed - self._ramp_rate)
            self._angular_speed = max(0.1, self._angular_speed - self._ramp_rate)
            self.get_logger().info(f"Speed decreased: {self._linear_speed:.2f} m/s")
        elif key == 'e':
            self._emergency_stop = not self._emergency_stop
            self._estop_pub.publish(Bool(data=self._emergency_stop))
            if self._emergency_stop:
                self.get_logger().warn("EMERGENCY STOP ACTIVATED!")
            else:
                self.get_logger().info("Emergency stop released")
        elif key == 'l':
            self.get_logger().info("LED toggle (not implemented)")

    def _publish_cmd(self):
        """Publish velocity command with ramping."""
        if not self._running:
            return

        # Ramp current speed toward target
        if abs(self._current_linear - self._target_linear) > self._ramp_rate:
            if self._current_linear < self._target_linear:
                self._current_linear += self._ramp_rate
            else:
                self._current_linear -= self._ramp_rate
        else:
            self._current_linear = self._target_linear

        if abs(self._current_angular - self._target_angular) > self._ramp_rate:
            if self._current_angular < self._target_angular:
                self._current_angular += self._ramp_rate
            else:
                self._current_angular -= self._ramp_rate
        else:
            self._current_angular = self._target_angular

        # Emergency stop overrides everything
        if self._emergency_stop:
            self._current_linear = 0.0
            self._current_angular = 0.0

        # Create and publish Twist message
        twist = Twist()
        twist.linear.x = self._current_linear
        twist.angular.z = self._current_angular
        self._cmd_vel_pub.publish(twist)

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
        """Clean up and stop robot."""
        self._running = False
        
        # Stop robot
        twist = Twist()
        self._cmd_vel_pub.publish(twist)
        
        # Restore terminal
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_termios)
        
        if self._keyboard_thread.is_alive():
            self._keyboard_thread.join(timeout=1.0)


def main(args=None):
    rclpy.init(args=args)
    node = UGV02TeleopNode()
    
    try:
        node.run()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

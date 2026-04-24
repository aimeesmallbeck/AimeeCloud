#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
WASD Keyboard Teleoperation for Wave Rover / UGV02

Maps keyboard input to /cmd_vel using the same key layout as the web teleop:
    W / UP     : Forward
    S / DOWN   : Backward
    A / LEFT   : Turn left (in-place)
    D / RIGHT  : Turn right (in-place)
    Q          : Forward + left
    E          : Forward + right
    Z          : Backward + left
    C          : Backward + right
    SPACE      : Stop
    + / =      : Increase speed
    - / _      : Decrease speed
    ESC / Ctrl+C : Quit

Publishes:
    - /cmd_vel (Twist): Velocity commands

Usage:
    ros2 run aimee_ugv02_controller wasd_teleop
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import termios
import tty
import select
import threading
import time


class WASDTeleopNode(Node):
    """WASD keyboard teleoperation for Wave Rover base."""

    # Key mapping: key -> (linear_x, angular_z) as fractions of max
    MOVE_BINDINGS = {
        'w': (1.0, 0.0),      # Forward
        'W': (1.0, 0.0),
        '\x1b[A': (1.0, 0.0),  # UP arrow
        's': (-1.0, 0.0),     # Backward
        'S': (-1.0, 0.0),
        '\x1b[B': (-1.0, 0.0), # DOWN arrow
        'a': (0.0, 1.0),      # Turn left (CCW)
        'A': (0.0, 1.0),
        '\x1b[D': (0.0, 1.0),  # LEFT arrow
        'd': (0.0, -1.0),     # Turn right (CW)
        'D': (0.0, -1.0),
        '\x1b[C': (0.0, -1.0), # RIGHT arrow
        'q': (1.0, 1.0),      # Forward-left
        'Q': (1.0, 1.0),
        'e': (1.0, -1.0),     # Forward-right
        'E': (1.0, -1.0),
        'z': (-1.0, 1.0),     # Backward-left
        'Z': (-1.0, 1.0),
        'c': (-1.0, -1.0),    # Backward-right
        'C': (-1.0, -1.0),
    }

    def __init__(self):
        super().__init__('wasd_teleop')

        # Parameters
        self.declare_parameters(namespace='', parameters=[
            ('speed', 0.05),        # Linear speed (m/s)
            ('turn', 0.5),          # Angular speed (rad/s)
            ('speed_step', 0.01),   # Speed increment per +/- key
            ('publish_rate', 10.0), # Hz
            ('cmd_vel_topic', '/cmd_vel'),
        ])

        self._speed = self.get_parameter('speed').value
        self._turn = self.get_parameter('turn').value
        self._speed_step = self.get_parameter('speed_step').value
        self._publish_rate = self.get_parameter('publish_rate').value
        self._cmd_vel_topic = self.get_parameter('cmd_vel_topic').value

        # Publisher
        self._cmd_vel_pub = self.create_publisher(Twist, self._cmd_vel_topic, 10)

        # State
        self._current_key = None
        self._running = True
        self._lock = threading.Lock()

        # Terminal setup
        self._old_settings = termios.tcgetattr(sys.stdin)

        # Start threads
        self._key_thread = threading.Thread(target=self._read_keys, daemon=True)
        self._pub_thread = threading.Thread(target=self._publish_loop, daemon=True)
        self._key_thread.start()
        self._pub_thread.start()

        self._print_help()

    def _print_help(self):
        """Print usage instructions."""
        help_text = """
╔══════════════════════════════════════════════════════════════╗
║           Wave Rover WASD Teleop                             ║
╠══════════════════════════════════════════════════════════════╣
║  W / ↑      : Forward        A / ←      : Turn left        ║
║  S / ↓      : Backward       D / →      : Turn right       ║
║  Q          : Forward-left   E          : Forward-right    ║
║  Z          : Backward-left  C          : Backward-right   ║
║  SPACE      : Stop                                         ║
║  + / =      : Speed up       - / _      : Speed down       ║
║  ESC / Ctrl+C : Quit                                       ║
╚══════════════════════════════════════════════════════════════╝
Current: speed={:.3f} m/s  turn={:.2f} rad/s
        """.format(self._speed, self._turn)
        print(help_text)

    def _read_keys(self):
        """Read keyboard input in a background thread."""
        tty.setcbreak(sys.stdin.fileno())
        while self._running:
            if select.select([sys.stdin], [], [], 0.1)[0]:
                try:
                    key = sys.stdin.read(1)
                    # Handle arrow keys (escape sequences)
                    if key == '\x1b':
                        seq = sys.stdin.read(2)
                        key = key + seq
                except Exception:
                    continue

                with self._lock:
                    if key in self.MOVE_BINDINGS:
                        self._current_key = key
                    elif key == ' ':
                        self._current_key = None  # Stop
                    elif key in ('+', '=', '-'):
                        if key in ('+', '='):
                            self._speed = min(1.0, self._speed + self._speed_step)
                            self._turn = min(2.0, self._turn + self._speed_step * 10)
                        else:
                            self._speed = max(0.01, self._speed - self._speed_step)
                            self._turn = max(0.1, self._turn - self._speed_step * 10)
                        print(f"  Speed: linear={self._speed:.3f}  angular={self._turn:.2f}")
                    elif key in ('\x03', '\x1b'):  # Ctrl+C or ESC
                        self._running = False
                        self._current_key = None
                    else:
                        # Unknown key — ignore (don't stop)
                        pass

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_settings)

    def _publish_loop(self):
        """Publish cmd_vel at a fixed rate."""
        period = 1.0 / self._publish_rate
        while self._running:
            with self._lock:
                key = self._current_key
                speed = self._speed
                turn = self._turn

            twist = Twist()
            if key is not None and key in self.MOVE_BINDINGS:
                lin_frac, ang_frac = self.MOVE_BINDINGS[key]
                twist.linear.x = lin_frac * speed
                twist.angular.z = ang_frac * turn
                # Log what we're sending
                self.get_logger().info(
                    f"KEY '{key[-1]}' → linear={twist.linear.x:.3f} angular={twist.angular.z:.3f}"
                )
            else:
                # Stop — already zero
                pass

            self._cmd_vel_pub.publish(twist)
            time.sleep(period)

    def destroy_node(self):
        """Cleanup terminal settings."""
        self._running = False
        self._key_thread.join(timeout=0.5)
        self._pub_thread.join(timeout=0.5)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_settings)
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = WASDTeleopNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Send stop command before exiting
        stop = Twist()
        node._cmd_vel_pub.publish(stop)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Publish a named waypoint goal to AimeeNav.

Usage:
    ros2 run aimee_nav go_to_waypoint.py <waypoint_name>
"""

import sys
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


def main():
    if len(sys.argv) < 2:
        print("Usage: go_to_waypoint.py <waypoint_name>")
        sys.exit(1)

    name = sys.argv[1]

    rclpy.init()
    node = Node('go_to_waypoint_cli')
    pub = node.create_publisher(String, '/go_to_waypoint_name', 10)

    # Wait for subscription
    timeout = 5.0
    start = node.get_clock().now().nanoseconds / 1e9
    while pub.get_subscription_count() == 0:
        rclpy.spin_once(node, timeout_sec=0.1)
        if node.get_clock().now().nanoseconds / 1e9 - start > timeout:
            print("Warning: no subscribers on /go_to_waypoint_name")
            break

    msg = String()
    msg.data = name
    pub.publish(msg)
    print(f"Sent waypoint: '{name}'")

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

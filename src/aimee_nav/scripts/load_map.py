#!/usr/bin/env python3
"""Trigger AimeeNav map load (loads most recent saved map).

Usage:
    ros2 run aimee_nav load_map.py
"""

import rclpy
from rclpy.node import Node
from std_srvs.srv import Empty


def main():
    rclpy.init()
    node = Node('load_map_cli')
    cli = node.create_client(Empty, '/load_map')

    if not cli.wait_for_service(timeout_sec=5.0):
        print("Service /load_map not available")
        return

    future = cli.call_async(Empty.Request())
    rclpy.spin_until_future_complete(node, future)

    if future.result() is not None:
        print("Map load triggered successfully")
    else:
        print(f"Service call failed: {future.exception()}")

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class CmdVelTest(Node):
    def __init__(self):
        super().__init__('cmdvel_test')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.sub = self.create_subscription(Twist, '/cmd_vel', self.on_cmd_vel, 10)
        self.received = 0
        
    def on_cmd_vel(self, msg):
        self.received += 1
        
    def send_once(self, linear, angular):
        twist = Twist()
        twist.linear.x = linear
        twist.angular.z = angular
        self.pub.publish(twist)
        self.get_logger().info(f"Published cmd_vel: linear={linear} angular={angular}")

rclpy.init(args=[])
node = CmdVelTest()

# Spin for 10 seconds to allow discovery
node.get_logger().info("Waiting 10 seconds for DDS discovery...")
for i in range(20):
    rclpy.spin_once(node, timeout_sec=0.5)
    if i % 4 == 0:
        node.get_logger().info(f"Waiting... {i*0.5}s elapsed")

node.get_logger().info("Publishing cmd_vel...")
node.send_once(0.3, 0.0)

# Spin a bit more to let message propagate
rclpy.spin_once(node, timeout_sec=1.0)
time.sleep(0.5)

node.get_logger().info(f"Done. Messages echoed back: {node.received}")
node.destroy_node()
rclpy.shutdown()

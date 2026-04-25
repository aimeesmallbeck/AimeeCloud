#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class SquareTest(Node):
    def __init__(self):
        super().__init__('square_test')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
    def send_cmd(self, linear, angular, duration_sec):
        twist = Twist()
        twist.linear.x = linear
        twist.angular.z = angular
        
        start = time.time()
        count = 0
        while time.time() - start < duration_sec:
            self.pub.publish(twist)
            count += 1
            time.sleep(0.1)
        
        # Stop
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.pub.publish(twist)
        self.get_logger().info(f"Sent {count} cmds | linear={linear} angular={angular} duration={duration_sec:.1f}s")
        return count

rclpy.init(args=[])
node = SquareTest()
rclpy.spin_once(node, timeout_sec=0.5)

# Square pattern: forward 1s, turn ~90° right, repeat 4 times
# Turning at 1.0 rad/s for 1.6s should be ~1.6 rad ≈ 92° (close to 90)
FORWARD_SPEED = 0.3   # m/s
FORWARD_TIME = 1.0    # seconds
TURN_SPEED = 1.0      # rad/s
TURN_TIME = 1.6       # seconds (~92°)

for i in range(4):
    node.get_logger().info(f"=== SIDE {i+1}/4 ===")
    
    node.get_logger().info(f"Moving forward for {FORWARD_TIME}s at {FORWARD_SPEED} m/s...")
    node.send_cmd(FORWARD_SPEED, 0.0, FORWARD_TIME)
    time.sleep(0.5)
    
    node.get_logger().info(f"Turning right for {TURN_TIME}s at {TURN_SPEED} rad/s...")
    node.send_cmd(0.0, -TURN_SPEED, TURN_TIME)
    time.sleep(0.5)

node.get_logger().info("=== SQUARE TEST COMPLETE ===")
node.destroy_node()
rclpy.shutdown()

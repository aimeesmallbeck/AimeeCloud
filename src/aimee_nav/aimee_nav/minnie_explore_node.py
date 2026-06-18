#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import OccupancyGrid, Odometry
from sensor_msgs.msg import LaserScan
import numpy as np
import math
import time

class ExploreNode(Node):
    def __init__(self):
        super().__init__('explore_node')
        
        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Subscribers
        self.map_sub = self.create_subscription(OccupancyGrid, '/map', self.map_callback, 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        
        # State
        self.map_data = None
        self.current_pose = None
        self.last_scan = None
        self.state = 'IDLE' # IDLE, EXPLORING, RETURNING
        
        # Parameters
        self.declare_parameter('explore_speed', 0.15)
        self.declare_parameter('rotation_speed', 0.4)
        self.declare_parameter('min_obstacle_dist', 0.3)
        
        self.get_logger().info("Explore Node Initialized")
        
        # Timer for control loop
        self.timer = self.create_timer(0.1, self.control_loop)

    def map_callback(self, msg):
        self.map_data = msg

    def odom_callback(self, msg):
        self.current_pose = msg.pose.pose

    def scan_callback(self, msg):
        self.last_scan = msg

    def control_loop(self):
        if self.current_pose is None or self.last_scan is None:
            return

        # Simple frontier exploration logic would go here
        # For now, let's implement a basic "wander and map" behavior
        
        twist = Twist()
        
        # Check for obstacles
        # Filter out inf and nan
        valid_ranges = [r for r in self.last_scan.ranges if not np.isinf(r) and not np.isnan(r)]
        if not valid_ranges:
            return
            
        min_dist = min(valid_ranges)
        
        if min_dist < self.get_parameter('min_obstacle_dist').value:
            # Obstacle ahead, rotate
            twist.linear.x = 0.0
            twist.angular.z = self.get_parameter('rotation_speed').value
            self.state = 'AVOIDING'
        else:
            # Path clear, move forward
            twist.linear.x = self.get_parameter('explore_speed').value
            twist.angular.z = 0.0
            self.state = 'EXPLORING'
            
        self.cmd_vel_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = ExploreNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Stop the robot
        stop_msg = Twist()
        node.cmd_vel_pub.publish(stop_msg)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

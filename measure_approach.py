#!/usr/bin/env python3
"""Move to approach position and hold for measurement."""
import rclpy
from rclpy.node import Node
from aimee_msgs.msg import ArmCommand
import time

class MeasureApproach(Node):
    def __init__(self):
        super().__init__('measure_approach')
        self.arm_pub = self.create_publisher(ArmCommand, '/arm/command', 10)
        time.sleep(1)
        
        target_x = 0.31
        target_y = 0.0
        approach_z = -0.05  # Current approach height
        safe_z = 0.05
        
        self.get_logger().info(f'Moving to approach position: X={target_x:.3f} Y={target_y:.3f} Z={approach_z:.3f}')
        
        # 1. Home first
        self._send_home()
        time.sleep(6)
        
        # 2. Move to safe height
        self._send_cartesian(target_x, target_y, safe_z, True, 6000)
        time.sleep(7)
        
        # 3. Lower to approach height and STOP
        self._send_cartesian(target_x, target_y, approach_z, True, 4000)
        time.sleep(5)
        
        self.get_logger().info('========================================')
        self.get_logger().info('ARM IS AT APPROACH POSITION. MEASURE NOW.')
        self.get_logger().info('Press Ctrl+C when done.')
        self.get_logger().info('========================================')
        
        # Hold position indefinitely
        while rclpy.ok():
            time.sleep(1)
    
    def _send_cartesian(self, x, y, z, open_gripper, time_ms):
        cmd = ArmCommand()
        cmd.command_type = 'cartesian'
        cmd.target_pose.position.x = x
        cmd.target_pose.position.y = y
        cmd.target_pose.position.z = z
        cmd.target_pose.orientation.x = 0.0
        cmd.target_pose.orientation.y = 0.707
        cmd.target_pose.orientation.z = 0.0
        cmd.target_pose.orientation.w = 0.707
        cmd.gripper_position = 0.08 if open_gripper else 0.02
        cmd.cartesian_speed = float(time_ms)
        self.arm_pub.publish(cmd)
        self.get_logger().info(f'Move: X={x:.3f} Y={y:.3f} Z={z:.3f}')
    
    def _send_home(self):
        cmd = ArmCommand()
        cmd.command_type = 'home'
        self.arm_pub.publish(cmd)
        self.get_logger().info('Home')

def main():
    rclpy.init()
    node = MeasureApproach()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

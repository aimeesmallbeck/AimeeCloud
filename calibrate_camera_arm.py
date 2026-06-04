#!/usr/bin/env python3
"""Non-blocking calibration: move arm to test positions, capture camera frames."""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from aimee_msgs.msg import ArmCommand
from cv_bridge import CvBridge
import cv2

class CalibrateCameraArm(Node):
    def __init__(self):
        super().__init__('calibrate_camera_arm')
        self.arm_pub = self.create_publisher(ArmCommand, '/arm/command', 10)
        self.bridge = CvBridge()
        self.latest_image = None
        self.create_subscription(Image, '/camera/color/image_raw', self._on_image, 10)
        
        self.positions = [
            ('home', 0.0, 0.0, None),
            ('fwd_10', 0.10, 0.00, -0.09),
            ('fwd_20', 0.20, 0.00, -0.09),
            ('fwd_30', 0.30, 0.00, -0.09),
            ('fwd_20_left_05', 0.20, 0.05, -0.09),
            ('fwd_20_right_05', 0.20, -0.05, -0.09),
            ('done', 0.0, 0.0, None),
        ]
        self.pos_idx = 0
        self.state = 'idle'  # idle -> lift -> move_xy -> lower -> capture -> next
        self.current_x, self.current_y = 0.0, 0.0
        self.safe_z = 0.05
        self.timer = self.create_timer(1.0, self._tick)
        self.get_logger().info('Calibration node ready. Starting in 3s...')
        self.start_time = self.get_clock().now()
        
    def _on_image(self, msg):
        try:
            self.latest_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        except:
            pass
    
    def _send_cartesian(self, x, y, z, dur=4000):
        cmd = ArmCommand()
        cmd.command_type = 'cartesian'
        cmd.target_pose.position.x = x
        cmd.target_pose.position.y = y
        cmd.target_pose.position.z = z
        cmd.target_pose.orientation.x = 0.0
        cmd.target_pose.orientation.y = 0.707
        cmd.target_pose.orientation.z = 0.0
        cmd.target_pose.orientation.w = 0.707
        cmd.cartesian_speed = 50.0
        self.arm_pub.publish(cmd)
        self.get_logger().info(f'Move to X={x:.3f} Y={y:.3f} Z={z:.3f}')
    
    def _send_home(self):
        cmd = ArmCommand()
        cmd.command_type = 'home'
        self.arm_pub.publish(cmd)
        self.get_logger().info('Home')
    
    def _save_frame(self, name):
        if self.latest_image is not None:
            path = f'/workspace/cal_{name}.jpg'
            cv2.imwrite(path, self.latest_image)
            self.get_logger().info(f'Saved {path}')
            return True
        return False
    
    def _tick(self):
        elapsed = (self.get_clock().now() - self.start_time).nanoseconds / 1e9
        if elapsed < 3.0:
            return
        
        if self.pos_idx >= len(self.positions):
            self.get_logger().info('Calibration complete')
            self.timer.cancel()
            return
        
        name, x, y, z = self.positions[self.pos_idx]
        
        if self.state == 'idle':
            if name == 'home' or name == 'done':
                self._send_home()
                self.state = 'wait_home'
                self.wait_start = elapsed
            else:
                self._send_cartesian(self.current_x, self.current_y, self.safe_z)
                self.state = 'wait_lift'
                self.wait_start = elapsed
                self.target_x, self.target_y, self.target_z = x, y, z
        
        elif self.state == 'wait_lift':
            if elapsed - self.wait_start >= 5.0:
                self._send_cartesian(self.target_x, self.target_y, self.safe_z)
                self.state = 'wait_move_xy'
                self.wait_start = elapsed
        
        elif self.state == 'wait_move_xy':
            if elapsed - self.wait_start >= 5.0:
                self._send_cartesian(self.target_x, self.target_y, self.target_z)
                self.state = 'wait_lower'
                self.wait_start = elapsed
        
        elif self.state == 'wait_lower':
            if elapsed - self.wait_start >= 5.0:
                self._save_frame(name)
                self.current_x, self.current_y = self.target_x, self.target_y
                self.pos_idx += 1
                self.state = 'idle'
        
        elif self.state == 'wait_home':
            if elapsed - self.wait_start >= 6.0:
                self._save_frame(name)
                if name == 'home':
                    self.current_x, self.current_y = 0.0, 0.0
                self.pos_idx += 1
                self.state = 'idle'

def main():
    rclpy.init()
    node = CalibrateCameraArm()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

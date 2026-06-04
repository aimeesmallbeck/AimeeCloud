#!/usr/bin/env python3
"""
Test new calibration: command arm to estimated marker positions,
capture images for visual verification.
Uses Z=0.0 so orange dot is visible and arm won't hit base.
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from aimee_msgs.msg import ArmCommand
from cv_bridge import CvBridge
import numpy as np
import time
import cv2

# New calibration (from sweep, orange dot at Z=+0.125, gripper at Z=0.0)
# X = -0.000662*v + 0.431758
# Y = -0.000598*u + 0.117395

def img_to_arm(u, v):
    x = -0.000662 * v + 0.431758
    y = -0.000598 * u + 0.117395
    return x, y

MARKERS = [
    ("marker_1", 159, 207),
    ("marker_2", 362, 218),
    ("marker_3", 428, 341),
    ("marker_4", 43, 390),
]

class TestCalib(Node):
    def __init__(self):
        super().__init__('test_calib')
        self.arm_pub = self.create_publisher(ArmCommand, '/arm/command', 10)
        self.bridge = CvBridge()
        self.latest_image = None
        self.create_subscription(Image, '/camera/color/image_raw', self._on_image, 10)
        
        for _ in range(30):
            rclpy.spin_once(self, timeout_sec=0.1)
            if self.latest_image is not None:
                break
        
        if self.latest_image is None:
            self.get_logger().error('No camera')
            return
        
        # Home first
        self._send_home()
        time.sleep(6)
        
        for name, u, v in MARKERS:
            x, y = img_to_arm(u, v)
            self.get_logger().info(f'{name}: img=({u},{v}) -> arm=({x:.3f},{y:+.3f})')
            
            # Safety limits
            if x < 0.12:
                self.get_logger().warn(f'  X={x:.3f} too close, clamping to 0.15')
                x = 0.15
            if abs(y) > 0.15:
                self.get_logger().warn(f'  Y={y:.3f} too wide, clamping')
                y = max(-0.15, min(0.15, y))
            
            # Approach at safe height
            self._send_cartesian(x, y, 0.05, True, 5000)
            time.sleep(6)
            # Lower to test height
            self._send_cartesian(x, y, 0.0, True, 4000)
            time.sleep(5)
            
            # Capture and save image
            img = self._capture()
            if img is not None:
                # Draw marker target and arm estimate
                cv2.circle(img, (u, v), 8, (255, 0, 0), 2)  # blue target
                cv2.putText(img, f'{name} target', (u+10, v), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
                cv2.putText(img, f'cmd=({x:.3f},{y:+.3f})', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
                fname = f'/workspace/calib_test_{name}.jpg'
                cv2.imwrite(fname, img)
                self.get_logger().info(f'  Saved {fname}')
            
            # Home
            self._send_home()
            time.sleep(6)
        
        self.get_logger().info('Done!')
    
    def _on_image(self, msg):
        try:
            self.latest_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        except:
            pass
    
    def _capture(self):
        self.latest_image = None
        for _ in range(20):
            rclpy.spin_once(self, timeout_sec=0.1)
            if self.latest_image is not None:
                break
        return self.latest_image.copy() if self.latest_image is not None else None
    
    def _send_cartesian(self, x, y, z, gripper_open, time_ms):
        cmd = ArmCommand()
        cmd.command_type = 'cartesian'
        cmd.target_pose.position.x = x
        cmd.target_pose.position.y = y
        cmd.target_pose.position.z = z
        cmd.target_pose.orientation.x = 0.0
        cmd.target_pose.orientation.y = 0.707
        cmd.target_pose.orientation.z = 0.0
        cmd.target_pose.orientation.w = 0.707
        cmd.gripper_position = 0.08 if gripper_open else 0.02
        cmd.cartesian_speed = float(time_ms)
        self.arm_pub.publish(cmd)
    
    def _send_home(self):
        cmd = ArmCommand()
        cmd.command_type = 'home'
        self.arm_pub.publish(cmd)

def main():
    rclpy.init()
    node = TestCalib()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Capture image and show orange detection attempts."""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import cv2

class CheckOrange(Node):
    def __init__(self):
        super().__init__('check_orange')
        self.bridge = CvBridge()
        self.latest_image = None
        self.create_subscription(Image, '/camera/color/image_raw', self._on_image, 10)
        
        for _ in range(30):
            rclpy.spin_once(self, timeout_sec=0.1)
            if self.latest_image is not None:
                break
        
        if self.latest_image is None:
            print('No frame')
            return
        
        img = self.latest_image
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, w = img.shape[:2]
        
        # Try multiple orange ranges and show results
        ranges = [
            ("orange_5_25", np.array([5, 80, 80]), np.array([25, 255, 255])),
            ("orange_5_20", np.array([5, 100, 100]), np.array([20, 255, 255])),
            ("orange_8_18", np.array([8, 120, 120]), np.array([18, 255, 255])),
            ("orange_10_20", np.array([10, 100, 100]), np.array([20, 255, 255])),
        ]
        
        for name, lower, upper in ranges:
            mask = cv2.inRange(hsv, lower, upper)
            # Exclude top area (likely skin/background)
            mask[:h//4, :] = 0
            
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            print(f'\n{name}: found {len(contours)} contours')
            
            for cnt in sorted(contours, key=cv2.contourArea, reverse=True)[:5]:
                area = cv2.contourArea(cnt)
                if area > 20:
                    M = cv2.moments(cnt)
                    if M['m00'] > 0:
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        # Sample color at centroid
                        b, g, r = img[cy, cx]
                        h_val, s_val, v_val = hsv[cy, cx]
                        print(f'  ({cx},{cy}) area={area:.0f} RGB=({r},{g},{b}) HSV=({h_val},{s_val},{v_val})')
    
    def _on_image(self, msg):
        try:
            self.latest_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        except:
            pass

def main():
    rclpy.init()
    node = CheckOrange()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

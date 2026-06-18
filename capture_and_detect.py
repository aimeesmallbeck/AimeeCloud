import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
import sys

from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

class DiceDetector(Node):
    def __init__(self):
        super().__init__('dice_detector')
        self.get_logger().info("DiceDetector starting up...")
        self.bridge = CvBridge()
        
        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )
        
        self.subscription = self.create_subscription(
            Image,
            '/vision/arm_camera/image_raw',
            self.image_callback,
            qos
        )
        self.found = False
        self.target_coords = None
        self.get_logger().info("Subscribed to /vision/arm_camera/image_raw")

    def image_callback(self, msg):
        if self.found:
            return
            
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        cv2.imwrite('/workspace/debug_raw_arm.jpg', cv_image)
        
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        
        # Very relaxed red ranges
        lower_red1 = np.array([0, 50, 40])
        upper_red1 = np.array([15, 255, 255])
        lower_red2 = np.array([160, 50, 40])
        upper_red2 = np.array([180, 255, 255])
        
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)
        
        cv2.imwrite('/workspace/debug_red_mask.jpg', mask)
        
        # Clean up mask
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_cnt = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_cnt)
            print(f"DEBUG: Largest contour area: {area}")
            if area > 50:
                M = cv2.moments(largest_cnt)
                if M["m00"] > 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    self.target_coords = (cx, cy)
                    self.found = True
                    cv2.drawContours(cv_image, [largest_cnt], -1, (0, 255, 0), 2)
                    cv2.circle(cv_image, (cx, cy), 5, (255, 0, 0), -1)
                    cv2.imwrite('/workspace/dice_detection.jpg', cv_image)
                    print(f"DETECTED:{cx},{cy}")
                    rclpy.shutdown()
        else:
            print("DEBUG: No contours found in mask")

def main():
    rclpy.init()
    detector = DiceDetector()
    try:
        rclpy.spin(detector)
    except SystemExit:
        pass
    except KeyboardInterrupt:
        rclpy.shutdown()

if __name__ == '__main__':
    main()

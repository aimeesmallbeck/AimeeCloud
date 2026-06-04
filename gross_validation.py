#!/usr/bin/env python3
"""
Gross validation: move arm to known positions, capture images,
detect orange dot in window around expected position, report actual location.
Saves annotated images for inspection.
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from aimee_msgs.msg import ArmCommand
from cv_bridge import CvBridge
import numpy as np
import time
import cv2
import os

# Dot calibration (from sweep, gripper at Z=0.0)
def arm_to_dot_img(x, y):
    """Given arm X,Y, predict orange dot image position."""
    v = int((0.431758 - x) / 0.000662)
    u = int((0.117395 - y) / 0.000598)
    return u, v

def detect_orange_in_window(img, cx, cy, window=60):
    """Search for orange dot in a window around (cx, cy)."""
    h, w = img.shape[:2]
    x1 = max(0, cx - window)
    y1 = max(0, cy - window)
    x2 = min(w, cx + window)
    y2 = min(h, cy + window)
    
    roi = img[y1:y2, x1:x2]
    if roi.size == 0:
        return None, None
    
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([0, 60, 80]), np.array([20, 255, 255]))
    
    # Morphological cleanup
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    best = None
    best_score = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 2 <= area <= 200:
            M = cv2.moments(cnt)
            if M["m00"] > 0:
                # Centroid relative to full image
                cu = int(M["m10"]/M["m00"]) + x1
                cv_pos = int(M["m01"]/M["m00"]) + y1
                dist_from_center = np.sqrt((cu - cx)**2 + (cv_pos - cy)**2)
                # Prefer contours near expected center, with decent area
                score = area / (1 + dist_from_center/10)
                if score > best_score:
                    best_score = score
                    best = (cu, cv_pos, area)
    
    return best[:2] if best else (None, None)

class GrossValidation(Node):
    def __init__(self):
        super().__init__('gross_validation')
        self.arm_pub = self.create_publisher(ArmCommand, '/arm/command', 10)
        self.bridge = CvBridge()
        self.color_img = None
        self.create_subscription(Image, '/camera/color/image_raw', self._on_color, 10)
        
        for _ in range(30):
            rclpy.spin_once(self, timeout_sec=0.1)
            if self.color_img is not None:
                break
        
        if self.color_img is None:
            self.get_logger().error('No camera')
            return
        
        # Test positions
        tests = []
        # X sweep at Y=0
        for x in [0.15, 0.20, 0.25, 0.30]:
            tests.append((f"X{x:.2f}_Y0", x, 0.0))
        # Y sweep at X=0.25
        for y in [-0.10, -0.05, 0.0, 0.05, 0.10]:
            tests.append((f"X0.25_Y{y:+.2f}", 0.25, y))
        
        out_dir = '/workspace/gross_validation'
        os.makedirs(out_dir, exist_ok=True)
        
        # Home first
        self._send_home()
        time.sleep(6)
        self._capture_and_save(f"{out_dir}/home.jpg", "home", None, None)
        
        for name, x, y in tests:
            self.get_logger().info(f"Testing {name}: arm=({x:.2f},{y:+.2f})")
            
            # Safety limits
            x_cmd = max(0.12, x)
            y_cmd = max(-0.15, min(0.15, y))
            
            # Move to position
            self._send_cartesian(x_cmd, y_cmd, 0.05, True, 5000)
            time.sleep(6)
            self._send_cartesian(x_cmd, y_cmd, 0.0, True, 4000)
            time.sleep(5)
            
            # Predict dot position
            pu, pv = arm_to_dot_img(x_cmd, y_cmd)
            
            # Detect dot in window around predicted position
            img = self._capture()
            du, dv = detect_orange_in_window(img, pu, pv, window=80)
            
            if du is not None:
                err = np.sqrt((du-pu)**2 + (dv-pv)**2)
                self.get_logger().info(f"  Predicted=({pu},{pv}), Detected=({du},{dv}), Error={err:.1f}px")
            else:
                self.get_logger().warn(f"  Predicted=({pu},{pv}), NO DOT DETECTED")
                du, dv = None, None
            
            self._capture_and_save(f"{out_dir}/{name}.jpg", name, (pu, pv), (du, dv))
            
            # Home
            self._send_home()
            time.sleep(6)
        
        self.get_logger().info(f"Done. Images saved to {out_dir}")
    
    def _on_color(self, msg):
        try:
            self.color_img = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        except:
            pass
    
    def _capture(self):
        self.color_img = None
        for _ in range(20):
            rclpy.spin_once(self, timeout_sec=0.1)
            if self.color_img is not None:
                break
        return self.color_img.copy() if self.color_img is not None else None
    
    def _capture_and_save(self, path, label, predicted, detected):
        img = self._capture()
        if img is None:
            return
        h, w = img.shape[:2]
        # Draw predicted position (green circle)
        if predicted:
            pu, pv = predicted
            cv2.circle(img, (pu, pv), 8, (0, 255, 0), 2)
            cv2.putText(img, f"pred ({pu},{pv})", (pu+10, pv), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
        # Draw detected position (red circle)
        if detected and detected[0] is not None:
            du, dv = detected
            cv2.circle(img, (du, dv), 8, (0, 0, 255), 2)
            cv2.putText(img, f"det ({du},{dv})", (du+10, dv+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
        # Label
        cv2.putText(img, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        cv2.imwrite(path, img)
    
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
    node = GrossValidation()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

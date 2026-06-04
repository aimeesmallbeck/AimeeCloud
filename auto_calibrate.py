#!/usr/bin/env python3
"""
Automated calibration using blue tape markers + orange dot on arm.
Detects orange dot position, commands arm to each blue marker,
measures error between orange dot and marker, corrects iteratively.
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from aimee_msgs.msg import ArmCommand
from cv_bridge import CvBridge
import numpy as np
import time
import cv2

class AutoCalibrate(Node):
    def __init__(self):
        super().__init__('auto_calibrate')
        self.arm_pub = self.create_publisher(ArmCommand, '/arm/command', 10)
        self.bridge = CvBridge()
        self.latest_image = None
        self.create_subscription(Image, '/camera/color/image_raw', self._on_image, 10)
        
        for _ in range(30):
            rclpy.spin_once(self, timeout_sec=0.1)
            if self.latest_image is not None:
                break
        
        if self.latest_image is None:
            self.get_logger().error('No camera frame')
            return
        
        # Detect blue markers
        markers = self._detect_blue_markers()
        if len(markers) < 4:
            self.get_logger().error(f'Found only {len(markers)} blue markers, need 4')
            return
        
        self.get_logger().info(f'Markers detected: {markers}')
        
        # Calibration model: robot_x = a*v + b*u + c, robot_y = d*v + e*u + f
        # Initial guess from earlier testing
        self.params = np.array([0.0013, 0.0, -0.25, 0.0, -0.0004, 0.13], dtype=np.float64)
        
        desk_z = -0.075
        # Orange dot is 12.5cm above surface, so arm Z when dot is at marker height
        # We command the arm so the ORANGE DOT is near the marker visually
        # If dot is 12.5cm above gripper tip, and gripper tip is at desk_z when picking,
        # then dot is at desk_z + 0.125 = -0.075 + 0.125 = +0.050
        # But camera sees the dot at that height. For calibration, let's command
        # the arm to a Z where the dot is clearly visible near the marker.
        # Safe test height: Z=0.0 puts the dot roughly 12.5cm above desk
        test_z = 0.0  # orange dot will be ~12.5cm above desk, clearly visible
        safe_z = 0.05
        
        # Home first
        self._send_home()
        time.sleep(6)
        
        # Capture background image with arm at home for motion masking
        bg_image = self._capture_image()
        ou, ov = self._detect_orange_dot(bg_image)
        if ou is None:
            self.get_logger().warn('Orange dot not detected at home position')
        else:
            self.get_logger().info(f'Orange dot visible at home: ({ou},{ov})')
        
        # Collect data points for final calibration fit
        correspondences = []  # (img_u, img_v, arm_x, arm_y)
        
        # Test each marker
        for i, (u, v) in enumerate(markers):
            self.get_logger().info(f'=== Marker {i+1}: image=({u},{v}) ===')
            
            success = False
            for attempt in range(4):
                x, y = self._image_to_arm(u, v)
                self.get_logger().info(f'  Attempt {attempt+1}: cmd=({x:.3f},{y:.3f})')
                
                # Move to target (gripper closed)
                self._send_cartesian(x, y, safe_z, True, 5000)
                time.sleep(6)
                self._send_cartesian(x, y, test_z, True, 4000)
                time.sleep(5)
                
                # Find orange dot on arm
                img = self._capture_image()
                tip_u, tip_v = self._detect_orange_dot(img, bg_image)
                
                if tip_u is None:
                    self.get_logger().warn('  Orange dot not detected, retrying...')
                    self._send_home()
                    time.sleep(6)
                    continue
                
                error_u = u - tip_u
                error_v = v - tip_v
                dist_px = np.sqrt(error_u**2 + error_v**2)
                self.get_logger().info(f'  Orange dot at ({tip_u},{tip_v}), error=({error_u:+.0f},{error_v:+.0f}), dist={dist_px:.1f}px')
                
                if dist_px < 20:
                    self.get_logger().info(f'  ✓ Marker {i+1} HIT')
                    correspondences.append((u, v, x, y))
                    success = True
                    break
                
                # Correction: adjust params based on pixel error
                # If tip is to the right of marker (error_u > 0), need to move arm left (+Y if image left = +Y)
                # If tip is below marker (error_v > 0), need to move arm forward (+X if image up = +X)
                dx = error_v * 0.001  # v error -> X correction
                dy = -error_u * 0.0003  # u error -> Y correction
                self.params[2] += dx
                self.params[5] += dy
                self.get_logger().info(f'  Adjusted: dx={dx:.4f}, dy={dy:.4f}')
                
                self._send_home()
                time.sleep(6)
            
            if not success:
                self.get_logger().warn(f'  ✗ Marker {i+1} failed after 4 attempts')
            
            self._send_home()
            time.sleep(6)
        
        # Final fit: solve for params using all correspondences
        if len(correspondences) >= 3:
            self._fit_calibration(correspondences)
        
        self._print_results()
    
    def _on_image(self, msg):
        try:
            self.latest_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        except:
            pass
    
    def _capture_image(self):
        self.latest_image = None
        for _ in range(20):
            rclpy.spin_once(self, timeout_sec=0.1)
            if self.latest_image is not None:
                break
        return self.latest_image.copy() if self.latest_image is not None else None
    
    def _detect_blue_markers(self):
        img = self.latest_image
        if img is None:
            return []
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([90, 60, 120]), np.array([120, 255, 255]))
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        markers = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 100:
                M = cv2.moments(cnt)
                if M['m00'] > 0:
                    markers.append((int(M['m10']/M['m00']), int(M['m01']/M['m00'])))
        markers.sort(key=lambda p: (p[1], p[0]))
        return markers
    
    def _detect_orange_dot(self, img, bg_image=None):
        """Detect orange dot using color + motion mask if bg_image provided."""
        if img is None:
            return None, None
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, w = img.shape[:2]
        
        # Orange dot: high saturation red-orange (sampled HSV=(7,151,174))
        color_mask = cv2.inRange(hsv, np.array([0, 100, 100]), np.array([15, 255, 255]))
        
        # If background available, restrict to changed regions (arm motion)
        if bg_image is not None:
            diff = cv2.absdiff(bg_image, img)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, motion_mask = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
            # Dilate to include dot area
            motion_mask = cv2.dilate(motion_mask, np.ones((20,20), np.uint8))
            color_mask = cv2.bitwise_and(color_mask, motion_mask)
        
        # Exclude edges where false positives lurk
        color_mask[:int(h*0.10), :] = 0
        color_mask[int(h*0.90):, :] = 0
        color_mask[:, int(w*0.70):] = 0
        
        kernel = np.ones((3,3), np.uint8)
        color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_OPEN, kernel)
        
        contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Prefer small high-saturation blobs (the dot) over large skin regions
        best = None
        best_score = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 3 <= area <= 100:
                # Score by area and circularity (dot is roughly circular)
                perimeter = cv2.arcLength(cnt, True)
                circ = 0
                if perimeter > 0:
                    circ = 4 * np.pi * area / (perimeter ** 2)
                score = area * (0.5 + circ)
                if score > best_score:
                    best_score = score
                    best = cnt
        
        if best is not None:
            M = cv2.moments(best)
            return int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        return None, None
    
    def _image_to_arm(self, u, v):
        a, b, c, d, e, f = self.params
        return a*v + b*u + c, d*v + e*u + f
    
    def _fit_calibration(self, points):
        """Solve affine transform from image to arm coordinates."""
        # robot_x = a*v + b*u + c
        # robot_y = d*v + e*u + f
        A = []
        bx, by = [], []
        for u, v, x, y in points:
            A.append([v, u, 1, 0, 0, 0])
            A.append([0, 0, 0, v, u, 1])
            bx.append(x)
            by.append(y)
        A = np.array(A)
        b = np.array(bx + by)
        try:
            sol = np.linalg.lstsq(A, b, rcond=None)[0]
            self.params = sol
            self.get_logger().info('Calibration refitted from correspondences')
        except Exception as e:
            self.get_logger().error(f'Fit failed: {e}')
    
    def _print_results(self):
        a, b, c, d, e, f = self.params
        self.get_logger().info('========================================')
        self.get_logger().info('FINAL CALIBRATION')
        self.get_logger().info(f'robot_x = {a:.6f}*v + {b:.6f}*u + {c:.6f}')
        self.get_logger().info(f'robot_y = {d:.6f}*v + {e:.6f}*u + {f:.6f}')
        self.get_logger().info('========================================')
    
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
    node = AutoCalibrate()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Systematic sweep calibration: move arm to known (X,Y) positions,
detect orange dot in image, build correspondence table for affine fit.
Uses Z=0.0 where dot is visible and arm won't hit base.
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from aimee_msgs.msg import ArmCommand
from cv_bridge import CvBridge
import numpy as np
import time
import cv2

class SweepCalibrate(Node):
    def __init__(self):
        super().__init__('sweep_calibrate')
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
        
        # Safe test positions (Z=0.0, dot clearly visible)
        test_z = 0.0
        safe_z = 0.05
        
        # X sweep at Y=0 (forward range that doesn't hit base)
        x_positions = [0.15, 0.20, 0.25, 0.30, 0.35]
        # Y sweep at X=0.25 (left/right range)
        y_positions = [-0.10, -0.05, 0.0, 0.05, 0.10]
        
        correspondences = []  # (img_u, img_v, robot_x, robot_y)
        
        # Home first
        self._send_home()
        time.sleep(6)
        
        # X sweep at Y=0
        self.get_logger().info('=== X SWEEP at Y=0 ===')
        for x in x_positions:
            self.get_logger().info(f'Commanding X={x:.2f}, Y=0.00')
            ok = self._test_position(x, 0.0, safe_z, test_z)
            if ok:
                u, v = ok
                correspondences.append((u, v, x, 0.0))
                self.get_logger().info(f'  Recorded: img=({u},{v}) -> arm=({x:.2f},0.00)')
            else:
                self.get_logger().warn(f'  Failed at X={x:.2f}')
            self._send_home()
            time.sleep(6)
        
        # Y sweep at X=0.25
        self.get_logger().info('=== Y SWEEP at X=0.25 ===')
        for y in y_positions:
            self.get_logger().info(f'Commanding X=0.25, Y={y:+.2f}')
            ok = self._test_position(0.25, y, safe_z, test_z)
            if ok:
                u, v = ok
                correspondences.append((u, v, 0.25, y))
                self.get_logger().info(f'  Recorded: img=({u},{v}) -> arm=(0.25,{y:+.2f})')
            else:
                self.get_logger().warn(f'  Failed at Y={y:+.2f}')
            self._send_home()
            time.sleep(6)
        
        # Fit affine transform
        if len(correspondences) >= 3:
            self._fit_and_print(correspondences)
        else:
            self.get_logger().error(f'Only {len(correspondences)} points, need at least 3')
    
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
    
    def _detect_orange_dot(self, img):
        if img is None:
            return None, None
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, w = img.shape[:2]
        # Relaxed orange range based on sampled dot
        mask = cv2.inRange(hsv, np.array([0, 60, 80]), np.array([20, 255, 255]))
        # Restrict to arm workspace (exclude top edge and right edge)
        mask[:int(h*0.10), :] = 0
        mask[:, int(w*0.70):] = 0
        kernel = np.ones((3,3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        best = None
        best_score = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 3 <= area <= 100:
                perimeter = cv2.arcLength(cnt, True)
                circ = 4 * np.pi * area / (perimeter ** 2) if perimeter > 0 else 0
                score = area * (0.5 + circ)
                if score > best_score:
                    best_score = score
                    best = cnt
        if best is not None:
            M = cv2.moments(best)
            return int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        return None, None
    
    def _test_position(self, x, y, safe_z, test_z):
        # Move to safe height first
        self._send_cartesian(x, y, safe_z, True, 5000)
        time.sleep(6)
        # Move to test height
        self._send_cartesian(x, y, test_z, True, 4000)
        time.sleep(5)
        # Capture and detect dot
        img = self._capture_image()
        u, v = self._detect_orange_dot(img)
        return (u, v) if u is not None else None
    
    def _fit_and_print(self, points):
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
            a, b, c, d, e, f = sol
            self.get_logger().info('========================================')
            self.get_logger().info('CALIBRATION RESULTS')
            self.get_logger().info(f'robot_x = {a:.6f}*v + {b:.6f}*u + {c:.6f}')
            self.get_logger().info(f'robot_y = {d:.6f}*v + {e:.6f}*u + {f:.6f}')
            # Validation
            for u, v, x_true, y_true in points:
                x_pred = a*v + b*u + c
                y_pred = d*v + e*u + f
                err = np.sqrt((x_pred-x_true)**2 + (y_pred-y_true)**2)
                self.get_logger().info(f'  img=({u},{v}): actual=({x_true:.3f},{y_true:.3f}) pred=({x_pred:.3f},{y_pred:.3f}) err={err:.4f}m')
            self.get_logger().info('========================================')
        except Exception as ex:
            self.get_logger().error(f'Fit failed: {ex}')
    
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
    node = SweepCalibrate()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

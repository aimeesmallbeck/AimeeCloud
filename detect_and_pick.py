#!/usr/bin/env python3
"""Detect pink character and pick with corrected Y mapping."""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from aimee_msgs.msg import ArmCommand
from cv_bridge import CvBridge
import numpy as np
import time

class DetectAndPick(Node):
    def __init__(self):
        super().__init__('detect_and_pick')
        self.arm_pub = self.create_publisher(ArmCommand, '/arm/command', 10)
        self.bridge = CvBridge()
        self.latest_image = None
        self.create_subscription(Image, '/camera/color/image_raw', self._on_image, 10)
        
        # Wait for frame
        for _ in range(30):
            rclpy.spin_once(self, timeout_sec=0.1)
            if self.latest_image is not None:
                break
        
        if self.latest_image is None:
            self.get_logger().error('No camera frame')
            return
        
        u, v = self._detect_character()
        if u is None:
            self.get_logger().error('Character not detected')
            return
        
        # CORRECTED empirical mapping:
        # X: base at v≈450, scale ≈ 0.0013 m/pixel (forward = up in image)
        # Y: base at u≈320, +Y = left in image, scale ≈ 0.0004 m/pixel
        target_x = (450 - v) * 0.0013
        target_y = (320 - u) * 0.0004
        
        # Clamp
        target_x = max(0.10, min(0.35, target_x))
        target_y = max(-0.15, min(0.15, target_y))
        
        desk_z = -0.075
        grasp_z = desk_z + 0.01
        safe_z = 0.05
        lift_z = grasp_z + 0.08
        
        self.get_logger().info(f'Detected at img=({u},{v}) → arm=({target_x:.3f},{target_y:.3f})')
        
        # 1. Home
        self._send_home()
        time.sleep(6)
        
        # 2. Transit to safe height
        self._send_cartesian(target_x, target_y, safe_z, True, 5000)
        time.sleep(6)
        
        # 3. Lower to grasp
        self._send_cartesian(target_x, target_y, grasp_z, True, 4000)
        time.sleep(5)
        
        # 4. Close
        self._send_cartesian(target_x, target_y, grasp_z, False, 2000)
        time.sleep(3)
        
        # 5. Lift
        self._send_cartesian(target_x, target_y, lift_z, False, 4000)
        time.sleep(5)
        
        # 6. Home
        self._send_home()
        time.sleep(6)
        
        self.get_logger().info('Pick complete')
    
    def _on_image(self, msg):
        try:
            self.latest_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        except:
            pass
    
    def _detect_character(self):
        img = self.latest_image
        h, w = img.shape[:2]
        rgb = img[:, :, ::-1]
        r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
        
        # Magenta/pink signature from earlier analysis
        mask = (r > 160) & (g < 140) & (b > 120) & (r > g + 30) & (b > g + 20)
        mask[int(h*0.8):, :] = False
        
        ys, xs = np.where(mask)
        if len(xs) >= 10:
            visited = np.zeros(len(xs), dtype=bool)
            best_cluster = []
            for i in range(len(xs)):
                if visited[i]: continue
                queue = [i]
                visited[i] = True
                cluster = [i]
                while queue:
                    j = queue.pop(0)
                    dists = np.abs(xs - xs[j]) + np.abs(ys - ys[j])
                    neighbors = np.where((dists < 25) & ~visited)[0]
                    for n in neighbors:
                        visited[n] = True
                        queue.append(n)
                        cluster.append(n)
                if len(cluster) > len(best_cluster):
                    best_cluster = cluster
            
            if len(best_cluster) >= 10:
                cx = int(np.median(xs[best_cluster]))
                cy = int(np.median(ys[best_cluster]))
                self.get_logger().info(f'Character at ({cx},{cy}), area={len(best_cluster)}')
                return cx, cy
        
        return None, None
    
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
        g = "open" if open_gripper else "close"
        self.get_logger().info(f'Cmd: X={x:.3f} Y={y:.3f} Z={z:.3f} {g} {time_ms}ms')
    
    def _send_home(self):
        cmd = ArmCommand()
        cmd.command_type = 'home'
        self.arm_pub.publish(cmd)
        self.get_logger().info('Home')

def main():
    rclpy.init()
    node = DetectAndPick()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

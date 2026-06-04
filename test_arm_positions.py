#!/usr/bin/env python3
"""Move arm to grid positions and capture frames for calibration mapping.
SAFETY: Always lifts to Z=0.05 before moving between positions."""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from aimee_msgs.msg import ArmCommand
from cv_bridge import CvBridge
import cv2
import time

LIFT_Z = 0.05     # Safe transit height above desk
DESK_Z = -0.09    # Grasp height at desk surface
TRANSIT_MS = 3000
GRASP_MS = 4000

class ArmCalibrator(Node):
    def __init__(self):
        super().__init__('arm_calibrator')
        self.bridge = CvBridge()
        self.latest_image = None
        self.pub = self.create_publisher(ArmCommand, '/arm/command', 10)
        self.create_subscription(Image, '/camera/color/image_raw', self.on_image, 10)
        time.sleep(2.0)

        self.positions = [
            (0.20,  0.00, 'forward'),
            (0.00,  0.20, 'left'),
            (0.00, -0.20, 'right'),
            (-0.20, 0.00, 'backward'),
            (0.15,  0.15, 'fwd_left'),
            (0.15, -0.15, 'fwd_right'),
            (-0.15, 0.15, 'back_left'),
            (-0.15, -0.15, 'back_right'),
            (0.10,  0.00, 'fwd_close'),
        ]
        self.idx = 0
        self.step = 0  # 0=lift, 1=move_xy, 2=lower, 3=capture
        self.timer = self.create_timer(6.0, self.tick)
        self.get_logger().info('Calibration ready. Waiting for first tick...')

    def on_image(self, msg):
        self.latest_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

    def send(self, x, y, z, gripper, dur_ms):
        cmd = ArmCommand()
        cmd.command_type = 'cartesian'
        cmd.target_pose.position.x = x
        cmd.target_pose.position.y = y
        cmd.target_pose.position.z = z
        cmd.target_pose.orientation.x = 0.0
        cmd.target_pose.orientation.y = 0.7071067811865475
        cmd.target_pose.orientation.z = 0.0
        cmd.target_pose.orientation.w = 0.7071067811865475
        cmd.gripper_position = gripper
        cmd.cartesian_speed = float(dur_ms)
        self.pub.publish(cmd)

    def tick(self):
        if self.idx >= len(self.positions):
            self.get_logger().info('Done. Returning home.')
            cmd = ArmCommand()
            cmd.command_type = 'home'
            self.pub.publish(cmd)
            raise SystemExit

        x, y, label = self.positions[self.idx]

        if self.step == 0:
            self.get_logger().info(f'{label}: LIFT to safe height')
            self.send(x, y, LIFT_Z, 0.08, TRANSIT_MS)
            self.step = 1
        elif self.step == 1:
            self.get_logger().info(f'{label}: MOVE XY')
            self.send(x, y, LIFT_Z, 0.08, TRANSIT_MS)
            self.step = 2
        elif self.step == 2:
            self.get_logger().info(f'{label}: LOWER to desk')
            self.send(x, y, DESK_Z, 0.08, GRASP_MS)
            self.step = 3
        else:
            if self.latest_image is not None:
                path = f'/workspace/arm_pos_{label}.jpg'
                cv2.imwrite(path, self.latest_image)
                self.get_logger().info(f'  Saved {path}')
            else:
                self.get_logger().warn('  No image!')
            self.step = 0
            self.idx += 1

def main():
    rclpy.init()
    node = ArmCalibrator()
    try:
        rclpy.spin(node)
    except SystemExit:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

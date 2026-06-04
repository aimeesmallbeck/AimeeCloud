#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CaptureFrame(Node):
    def __init__(self):
        super().__init__('capture_frame')
        self.sub = self.create_subscription(Image, '/camera/color/image_raw', self.on_image, 10)
        self.bridge = CvBridge()
        self.got = False
    
    def on_image(self, msg):
        if self.got:
            return
        try:
            img = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
            cv2.imwrite('/workspace/current_camera.jpg', img)
            self.get_logger().info('Saved /workspace/current_camera.jpg')
            self.got = True
        except Exception as e:
            self.get_logger().error(str(e))

def main():
    rclpy.init()
    node = CaptureFrame()
    while rclpy.ok() and not node.got:
        rclpy.spin_once(node, timeout_sec=0.5)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

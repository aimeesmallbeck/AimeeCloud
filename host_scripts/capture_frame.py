#!/usr/bin/env python3
"""Capture a camera frame and save it for review."""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from aimee_msgs.msg import ObjectDetection
from cv_bridge import CvBridge
import cv2
import time

class CaptureNode(Node):
    def __init__(self):
        super().__init__('capture_node')
        self.bridge = CvBridge()
        self.latest_image = None
        self.latest_detections = []
        self.create_subscription(Image, '/camera/color/image_raw', self.on_image, 10)
        self.create_subscription(ObjectDetection, '/vision/detections_3d', self.on_detection, 10)
        self.timer = self.create_timer(0.5, self.check)
        self.start_time = time.time()
        self.frame_count = 0

    def on_image(self, msg):
        self.latest_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        self.frame_count += 1

    def on_detection(self, msg):
        self.latest_detections.append(msg)
        if len(self.latest_detections) > 20:
            self.latest_detections = self.latest_detections[-20:]

    def check(self):
        if self.latest_image is None:
            self.get_logger().info(f'Waiting for image... ({self.frame_count} frames)')
            return
        elapsed = time.time() - self.start_time
        if elapsed < 3.0:
            self.get_logger().info(f'Collecting detections... ({len(self.latest_detections)} so far)')
            return

        img = self.latest_image.copy()
        h, w = img.shape[:2]
        self.get_logger().info(f'Saving frame ({w}x{h}) with {len(self.latest_detections)} detections')

        for det in self.latest_detections:
            cx = int(det.bbox_x * w)
            cy = int(det.bbox_y * h)
            bw = int(det.bbox_width * w)
            bh = int(det.bbox_height * h)
            x1 = cx - bw // 2
            y1 = cy - bh // 2
            x2 = x1 + bw
            y2 = y1 + bh
            color = (0, 255, 255)
            if det.color == 'red': color = (0, 0, 255)
            elif det.color == 'blue': color = (255, 0, 0)
            elif det.color == 'green': color = (0, 255, 0)
            elif det.color == 'yellow': color = (0, 255, 255)
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            label = f"{det.color} {det.object_class}: {det.confidence:.2f}"
            cv2.putText(img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            cv2.putText(img, f"3D: ({det.position_robot.x:.3f}, {det.position_robot.y:.3f}, {det.position_robot.z:.3f})", 
                        (x1, y2 + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

        cv2.imwrite('/home/arduino/frame_raw.jpg', self.latest_image)
        cv2.imwrite('/home/arduino/frame_with_detections.jpg', img)
        self.get_logger().info('Saved /home/arduino/frame_raw.jpg and frame_with_detections.jpg')
        raise SystemExit

def main():
    rclpy.init()
    node = CaptureNode()
    try:
        rclpy.spin(node)
    except SystemExit:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

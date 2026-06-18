#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
import cv2
import numpy as np
from cv_bridge import CvBridge
import os
import sys

class DirectGrabber(Node):
    def __init__(self, output_path):
        super().__init__('direct_grabber')
        self.output_path = output_path
        self.bridge = CvBridge()
        self.frames_to_skip = 10 # Drain the buffer
        self.frames_seen = 0
        self.subscription = self.create_subscription(
            CompressedImage,
            '/vision/arm_camera/image_raw/compressed',
            self.listener_callback,
            10
        )
        self.get_logger().info(f"Waiting to skip {self.frames_to_skip} frames and grab the fresh one...")

    def listener_callback(self, msg):
        self.frames_seen += 1
        if self.frames_seen <= self.frames_to_skip:
            if self.frames_seen % 5 == 0:
                self.get_logger().info(f"Skipped {self.frames_seen} frames...")
            return

        self.get_logger().info("Fresh frame received! Saving...")
        try:
            # The msg.data is already JPEG
            with open(self.output_path, 'wb') as f:
                f.write(msg.data.tobytes())
            self.get_logger().info(f"Saved to {self.output_path}")
            # Verify it's a valid image
            img = cv2.imread(self.output_path)
            if img is not None:
                self.get_logger().info(f"Verified image: {img.shape[1]}x{img.shape[0]}")
                sys.exit(0)
            else:
                self.get_logger().error("Saved file is not a valid image!")
                sys.exit(1)
        except Exception as e:
            self.get_logger().error(f"Error: {e}")
            sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 grab_frame.py <output_path>")
        return
        
    rclpy.init()
    grabber = DirectGrabber(sys.argv[1])
    try:
        rclpy.spin(grabber)
    except SystemExit:
        pass
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()

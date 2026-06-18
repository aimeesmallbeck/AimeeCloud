#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import struct
import cv2
import numpy as np
from sensor_msgs.msg import Image, CompressedImage
from aimee_msgs.msg import ObjectDetection
from cv_bridge import CvBridge
from .rpc import rpc_uart_master

class K210VisionNode(Node):
    def __init__(self):
        super().__init__('k210_vision_node')
        
        # Parameters
        self.declare_parameter('port', '/dev/ttyCH341USB0')
        self.declare_parameter('baud', 57600)
        self.declare_parameter('frame_id', 'arm_camera_link')
        self.declare_parameter('publish_image', True)
        self.declare_parameter('protocol', 'openmv_rpc') # 'wonder_mv' or 'openmv_rpc'
        
        self.port = self.get_parameter('port').value
        self.baud = self.get_parameter('baud').value
        self.frame_id = self.get_parameter('frame_id').value
        self.publish_image_flag = self.get_parameter('publish_image').value
        self.protocol = self.get_parameter('protocol').value
        
        # Publishers
        self.detection_pub = self.create_publisher(ObjectDetection, '/vision/k210/detections', 10)
        self.image_pub = self.create_publisher(CompressedImage, '/vision/k210/image_raw/compressed', 10)
        
        self.bridge = CvBridge()
        self.rpc = None
        
        if self.protocol == 'openmv_rpc':
            try:
                self.rpc = rpc_uart_master(self.port, self.baud)
                self.get_logger().info(f"Connected to K210 RPC on {self.port} at {self.baud}")
            except Exception as e:
                self.get_logger().error(f"Failed to connect to K210 RPC: {e}")
        else:
            # Fallback to WonderMV serial if needed (not implemented in this version for brevity)
            self.get_logger().error(f"Protocol {self.protocol} not fully implemented in RPC refactor")

        # Timer for requesting data
        self.create_timer(0.1, self.timer_callback) # 10Hz

    def timer_callback(self):
        if self.rpc is None:
            return

        # 1. Request Image
        if self.publish_image_flag:
            try:
                # Call 'get_image' on K210
                result = self.rpc.call("get_image")
                if result is not None:
                    # result is JPEG bytes
                    msg = CompressedImage()
                    msg.header.stamp = self.get_clock().now().to_msg()
                    msg.header.frame_id = self.frame_id
                    msg.format = "jpeg"
                    msg.data = list(result)
                    self.image_pub.publish(msg)
                    self.get_logger().debug(f"Published image of size {len(result)}")
                else:
                    self.get_logger().warn("get_image call returned None")
            except Exception as e:
                self.get_logger().warn(f"Error requesting image: {e}")

        # 2. Request Detections
        try:
            result = self.rpc.call("get_detections")
            if result is not None:
                self.process_detections(result)
        except Exception as e:
            self.get_logger().warn(f"Error requesting detections: {e}")

    def process_detections(self, data):
        """
        Processes detections returned as a byte array via RPC.
        Format expected: [x1, y1, w1, h1, id1, x2, y2, w2, h2, id2, ...]
        Each value is 2 bytes (unsigned short).
        """
        num_detections = len(data) // 10
        for i in range(num_detections):
            x, y, w, h, obj_id = struct.unpack('<HHHHH', data[i*10 : (i+1)*10])
            
            msg = ObjectDetection()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = self.frame_id
            msg.object_id = str(obj_id)
            msg.bbox_x = float(x)
            msg.bbox_y = float(y)
            msg.bbox_width = float(w)
            msg.bbox_height = float(h)
            msg.object_class = "unknown" # Could be refined
            msg.confidence = 1.0
            self.detection_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = K210VisionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node.rpc:
            node.rpc.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

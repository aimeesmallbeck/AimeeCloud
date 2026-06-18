#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CompressedImage
from aimee_msgs.srv import CaptureSnapshot
import cv2
from cv_bridge import CvBridge
import threading

class SnapshotServiceNode(Node):
    def __init__(self):
        super().__init__('snapshot_service_node')
        
        # Parameters
        self.declare_parameter('image_topic', '/vision/arm_camera/image_raw')
        self.declare_parameter('service_name', '/camera/capture_snapshot')
        
        self.image_topic = self.get_parameter('image_topic').value
        self.service_name = self.get_parameter('service_name').value
        
        self.bridge = CvBridge()
        self.latest_image = None
        self.image_lock = threading.Lock()
        
        # Publishers
        self.compressed_pub = self.create_publisher(
            CompressedImage,
            self.image_topic + '/compressed',
            10
        )
        
        # Subscriber
        self.image_sub = self.create_subscription(
            Image,
            self.image_topic,
            self.image_callback,
            10
        )
        
        # Service
        self.srv = self.create_service(
            CaptureSnapshot,
            self.service_name,
            self.capture_callback
        )
        
        self.get_logger().info(f"Snapshot service started on {self.service_name}, listening to {self.image_topic}")

    def image_callback(self, msg):
        with self.image_lock:
            self.latest_image = msg
            
        # Also publish compressed for monitor
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            _, buffer = cv2.imencode('.jpg', cv_image, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            
            c_msg = CompressedImage()
            c_msg.header = msg.header
            c_msg.format = 'jpeg'
            c_msg.data = buffer.tobytes()
            self.compressed_pub.publish(c_msg)
        except Exception as e:
            self.get_logger().error(f"Error compressing image: {e}")

    def capture_callback(self, request, response):
        self.get_logger().info("Snapshot requested")
        
        with self.image_lock:
            if self.latest_image is None:
                response.success = False
                response.message = "No image received yet"
                return response
            
            try:
                cv_image = self.bridge.imgmsg_to_cv2(self.latest_image, desired_encoding='bgr8')
                
                # Optional: resize or compress
                quality = request.quality if request.quality > 0 else 95
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
                _, buffer = cv2.imencode('.jpg', cv_image, encode_param)
                
                response.image = CompressedImage()
                response.image.header = self.latest_image.header
                response.image.format = 'jpeg'
                response.image.data = buffer.tobytes()
                
                response.success = True
                response.message = f"Successfully captured snapshot ({cv_image.shape[1]}x{cv_image.shape[0]})"
            except Exception as e:
                response.success = False
                response.message = f"Error capturing snapshot: {str(e)}"
        
        return response

def main(args=None):
    rclpy.init(args=args)
    node = SnapshotServiceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

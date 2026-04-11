#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
Pose Estimator Node

Estimates 3D position of detected objects using monocular camera
with known object sizes.

Usage:
    ros2 run aimee_perception pose_estimator_node
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from geometry_msgs.msg import Point, TransformStamped
from sensor_msgs.msg import CameraInfo
from aimee_msgs.msg import ObjectDetection
import tf2_ros
from tf2_ros import TransformBroadcaster
from typing import Dict, Optional
import numpy as np


# Known object dimensions (meters)
OBJECT_DIMENSIONS: Dict[str, Dict[str, float]] = {
    "ball": {
        "diameter": 0.065,      # Tennis ball
        "height": 0.065,
        "width": 0.065,
    },
    "cup": {
        "diameter": 0.08,       # Standard cup
        "height": 0.10,
        "width": 0.08,
    },
    "block": {
        "width": 0.05,          # 5cm cube
        "height": 0.05,
        "depth": 0.05,
        "diameter": 0.05,
    },
}

# Default dimensions for unknown objects
DEFAULT_DIMENSIONS = {
    "diameter": 0.05,
    "height": 0.05,
    "width": 0.05,
    "depth": 0.05,
}


class PoseEstimatorNode(Node):
    """
    Estimates 3D position of objects from 2D detections.
    
    Uses monocular depth estimation based on known object sizes.
    Publishes position in camera frame and transforms to robot frame.
    """

    def __init__(self):
        super().__init__('pose_estimator_node')

        # Declare parameters
        self.declare_parameters(namespace='', parameters=[
            ('camera_frame', 'obsbot_camera'),
            ('robot_frame', 'base_link'),
            ('publish_tf', True),
            ('assumed_object_distance', 0.5),  # meters (fallback)
        ])

        self._camera_frame = self.get_parameter('camera_frame').value
        self._robot_frame = self.get_parameter('robot_frame').value
        self._publish_tf = self.get_parameter('publish_tf').value

        # Setup QoS
        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # TF
        self._tf_broadcaster = TransformBroadcaster(self)
        self._tf_buffer = tf2_ros.Buffer()
        self._tf_listener = tf2_ros.TransformListener(self._tf_buffer, self)

        # Publishers
        self._detection_pub = self.create_publisher(
            ObjectDetection, '/vision/detections_3d', reliable_qos
        )

        # Subscribers
        self._detection_sub = self.create_subscription(
            ObjectDetection,
            '/vision/tracked_objects',
            self._on_detection,
            10
        )

        self._camera_info_sub = self.create_subscription(
            CameraInfo,
            '/camera/camera_info',
            self._on_camera_info,
            reliable_qos
        )

        # State
        self._camera_info: Optional[CameraInfo] = None
        self._fx = 600.0  # Default focal length (updated from camera_info)
        self._fy = 600.0
        self._cx = 320.0  # Default principal point
        self._cy = 240.0

        self.get_logger().info(
            f"PoseEstimatorNode initialized:\n"
            f"  Camera frame: {self._camera_frame}\n"
            f"  Robot frame: {self._robot_frame}\n"
            f"  Publish TF: {self._publish_tf}"
        )

    def _on_camera_info(self, msg: CameraInfo):
        """Store camera intrinsics."""
        self._camera_info = msg
        self._fx = msg.k[0]  # Focal length x
        self._fy = msg.k[4]  # Focal length y
        self._cx = msg.k[2]  # Principal point x
        self._cy = msg.k[5]  # Principal point y
        
        self.get_logger().debug(
            f"Camera intrinsics updated: fx={self._fx:.1f}, fy={self._fy:.1f}, "
            f"cx={self._cx:.1f}, cy={self._cy:.1f}"
        )

    def _on_detection(self, msg: ObjectDetection):
        """Process detection and estimate 3D pose."""
        try:
            # Estimate 3D position in camera frame
            position_camera = self._estimate_3d_position(msg)
            
            # Update message with camera frame position
            msg.position_camera = position_camera
            
            # Try to transform to robot frame
            try:
                position_robot = self._transform_to_robot_frame(position_camera)
                msg.position_robot = position_robot
            except Exception as e:
                self.get_logger().debug(f"Could not transform to robot frame: {e}")
                msg.position_robot = position_camera  # Fallback

            # Publish updated detection
            self._detection_pub.publish(msg)

            # Publish TF if enabled
            if self._publish_tf:
                self._publish_object_tf(msg.object_id, position_camera)

        except Exception as e:
            self.get_logger().error(f"Error processing detection: {e}")

    def _estimate_3d_position(self, detection: ObjectDetection) -> Point:
        """
        Estimate 3D position from 2D detection using known object size.
        
        For a sphere (ball):
        - Use the bounding box width to estimate distance
        - Z = (real_diameter * focal_length) / apparent_width
        
        For other objects:
        - Use the larger dimension (height or width)
        """
        # Get object dimensions
        obj_class = detection.object_class
        if obj_class in OBJECT_DIMENSIONS:
            dims = OBJECT_DIMENSIONS[obj_class]
        else:
            dims = DEFAULT_DIMENSIONS

        # Choose reference dimension
        if "diameter" in dims:
            # Spherical objects
            real_size = dims["diameter"]
        else:
            # Use larger of width/height
            real_size = max(dims.get("width", 0.05), dims.get("height", 0.05))

        # Convert normalized bbox width to pixels
        apparent_width = detection.bbox_width * 640  # Assuming 640px width
        
        if apparent_width > 0:
            # Estimate distance: Z = (real_size * focal_length) / apparent_size
            z = (real_size * self._fx) / apparent_width
        else:
            z = self.get_parameter('assumed_object_distance').value

        # Calculate X, Y using pinhole camera model
        # X = (u - cx) * Z / fx
        # Y = (v - cy) * Z / fy
        
        # Convert normalized coordinates to pixel coordinates
        u = detection.bbox_x * 640
        v = detection.bbox_y * 480
        
        x = (u - self._cx) * z / self._fx
        y = (v - self._cy) * z / self._fy

        # In ROS, camera frame is:
        # X: right, Y: down, Z: forward
        # Our camera might be oriented differently, so adjust:
        
        point = Point()
        point.x = z   # Forward
        point.y = -x  # Right (negative because image x increases right)
        point.z = -y  # Up (negative because image y increases down)

        self.get_logger().debug(
            f"Object {detection.object_id}: "
            f"2D=({detection.bbox_x:.3f}, {detection.bbox_y:.3f}), "
            f"3D=({point.x:.3f}, {point.y:.3f}, {point.z:.3f})"
        )

        return point

    def _transform_to_robot_frame(self, camera_point: Point) -> Point:
        """Transform point from camera frame to robot base frame."""
        # Look up transform from camera to robot
        try:
            transform = self._tf_buffer.lookup_transform(
                self._robot_frame,
                self._camera_frame,
                rclpy.time.Time()
            )
            
            # Apply transform (simplified - just translation for now)
            robot_point = Point()
            robot_point.x = camera_point.x + transform.transform.translation.x
            robot_point.y = camera_point.y + transform.transform.translation.y
            robot_point.z = camera_point.z + transform.transform.translation.z
            
            return robot_point
            
        except tf2_ros.LookupException:
            # If no transform available, assume camera is at robot origin
            return camera_point

    def _publish_object_tf(self, object_id: str, position: Point):
        """Publish TF frame for detected object."""
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = self._camera_frame
        t.child_frame_id = f"object_{object_id}"
        
        t.transform.translation.x = position.x
        t.transform.translation.y = position.y
        t.transform.translation.z = position.z
        
        # No rotation (objects are rotationally symmetric for now)
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0
        
        self._tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = PoseEstimatorNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down...")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
Pose Estimator Node

Estimates 3D position of detected objects using a registered depth map.
Falls back to monocular estimation if depth data is unavailable or invalid.

Usage:
    ros2 run aimee_perception pose_estimator_node
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from geometry_msgs.msg import Point, TransformStamped
from sensor_msgs.msg import CameraInfo, Image
from aimee_msgs.msg import ObjectDetection
import tf2_ros
from tf2_ros import TransformBroadcaster
from typing import Dict, Optional
import numpy as np
from cv_bridge import CvBridge
import cv2


# Known object dimensions (meters) - used for fallback monocular estimation
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
    Estimates 3D position of objects from 2D detections and Depth Maps.
    
    Uses registered depth data to find exact distance.
    Publishes position in camera frame and transforms to robot frame.
    """

    def __init__(self):
        super().__init__('pose_estimator_node')

        # Declare parameters
        self.declare_parameters(namespace='', parameters=[
            ('camera_frame', 'camera_color_frame'), # Changed to match usb_cam
            ('robot_frame', 'base_link'),
            ('publish_tf', True),
            ('assumed_object_distance', 0.5),  # meters (fallback)
            ('image_width', 640),   # pixels
            ('image_height', 480),  # pixels
            ('camera_pitch_deg', 0.0),  # degrees: positive = camera looks down
            ('camera_yaw_deg', 0.0),    # degrees: rotation around camera optical axis (Z). +90 = camera image top points to robot left
            ('depth_scale', 1000.0),  # divide raw depth by this to get meters (1000=mm, 100=cm)
            ('use_hardware_depth', True),
            ('min_depth', 0.05),   # meters
            ('max_depth', 1.0),    # meters
            ('fx_override', 0.0),  # pixels; if > 0, use instead of CameraInfo or default
            ('fy_override', 0.0),  # pixels
        ])

        self._camera_frame = self.get_parameter('camera_frame').value
        self._robot_frame = self.get_parameter('robot_frame').value
        self._publish_tf = self.get_parameter('publish_tf').value
        self._image_width = self.get_parameter('image_width').value
        self._image_height = self.get_parameter('image_height').value
        self._camera_pitch_deg = self.get_parameter('camera_pitch_deg').value
        self._camera_yaw_deg = self.get_parameter('camera_yaw_deg').value
        self._depth_scale = self.get_parameter('depth_scale').value
        self._use_hardware_depth = self.get_parameter('use_hardware_depth').value
        self._min_depth = self.get_parameter('min_depth').value
        self._max_depth = self.get_parameter('max_depth').value
        self._fx_override = self.get_parameter('fx_override').value
        self._fy_override = self.get_parameter('fy_override').value

        # Setup QoS
        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        # TF
        self._tf_broadcaster = TransformBroadcaster(self)
        self._tf_buffer = tf2_ros.Buffer()
        self._tf_listener = tf2_ros.TransformListener(self._tf_buffer, self)

        # CV Bridge
        self._cv_bridge = CvBridge()
        self._latest_depth_image: Optional[np.ndarray] = None

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
            '/camera/color/camera_info',
            self._on_camera_info,
            reliable_qos
        )
        
        self._depth_sub = self.create_subscription(
            Image,
            '/camera/depth/image_raw',
            self._on_depth_image,
            sensor_qos
        )

        # State
        self._camera_info: Optional[CameraInfo] = None
        # Astra Pro HD typical intrinsics for 640x480 (60° HFOV, 49° VFOV)
        self._fx = 554.0  # 320 / tan(30°)
        self._fy = 526.0  # 240 / tan(24.5°)
        self._cx = 320.0
        self._cy = 240.0
        # Apply overrides if set
        if self._fx_override > 0:
            self._fx = self._fx_override
        if self._fy_override > 0:
            self._fy = self._fy_override

        self.get_logger().info(
            f"PoseEstimatorNode initialized:\n"
            f"  Camera frame: {self._camera_frame}\n"
            f"  Robot frame: {self._robot_frame}\n"
            f"  Publish TF: {self._publish_tf}\n"
            f"  Image size: {self._image_width}x{self._image_height}\n"
            f"  Camera pitch: {self._camera_pitch_deg}°\n"
            f"  Camera yaw: {self._camera_yaw_deg}°\n"
            f"  Depth scale: {self._depth_scale} (raw/scale = meters)\n"
            f"  Hardware depth: {self._use_hardware_depth}\n"
            f"  Depth range: [{self._min_depth}, {self._max_depth}] m"
        )

    def _on_camera_info(self, msg: CameraInfo):
        """Store camera intrinsics."""
        self._camera_info = msg
        if msg.k[0] > 0.0:
            self._fx = msg.k[0]  # Focal length x
            self._fy = msg.k[4]  # Focal length y
            self._cx = msg.k[2]  # Principal point x
            self._cy = msg.k[5]  # Principal point y
        
        # Only log once
        if not hasattr(self, '_camera_info_logged'):
            self.get_logger().info(
                f"Camera intrinsics updated: fx={self._fx:.1f}, fy={self._fy:.1f}, "
                f"cx={self._cx:.1f}, cy={self._cy:.1f}"
            )
            self._camera_info_logged = True

    def _on_depth_image(self, msg: Image):
        """Cache the latest depth image."""
        try:
            # Astra depth is usually 16UC1 (millimeters)
            self._latest_depth_image = self._cv_bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
        except Exception as e:
            self.get_logger().error(f"Error converting depth image: {e}")

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

    def _get_depth_at_pixel(self, u: int, v: int) -> Optional[float]:
        """Safely get the median depth value around a pixel in meters."""
        if self._latest_depth_image is None:
            return None
            
        h, w = self._latest_depth_image.shape
        if not (0 <= u < w and 0 <= v < h):
            return None
            
        # Use a small 5x5 window around the center to avoid noisy single pixels
        window_size = 5
        half_w = window_size // 2
        
        u_min, u_max = max(0, u - half_w), min(w, u + half_w + 1)
        v_min, v_max = max(0, v - half_w), min(h, v + half_w + 1)
        
        window = self._latest_depth_image[v_min:v_max, u_min:u_max]
        
        # Filter out 0 depth values (invalid data)
        valid_depths = window[window > 0]
        
        if len(valid_depths) == 0:
            return None
            
        # Get median depth and apply scale to convert to meters
        median_depth_raw = np.median(valid_depths)
        depth_m = float(median_depth_raw) / self._depth_scale
        return depth_m

    def _estimate_3d_position(self, detection: ObjectDetection) -> Point:
        """
        Estimate 3D position from 2D detection.
        Prefers hardware depth map if available, falls back to monocular estimation.
        """
        # Convert normalized coordinates to pixel coordinates
        u = int(detection.bbox_x * self._image_width)
        v = int(detection.bbox_y * self._image_height)
        
        # 1. Try Hardware Depth
        z = None
        if self._use_hardware_depth:
            z = self._get_depth_at_pixel(u, v)
            if z is not None and (z < self._min_depth or z > self._max_depth):
                self.get_logger().debug(
                    f"Hardware depth {z:.3f}m out of range "
                    f"[{self._min_depth}, {self._max_depth}], falling back to monocular"
                )
                z = None
        
        if z is not None:
            method = "Hardware Depth"
        else:
            # 2. Fallback to Monocular Depth Estimation
            method = "Monocular Fallback"
            # Get object dimensions
            obj_class = detection.object_class
            if obj_class in OBJECT_DIMENSIONS:
                dims = OBJECT_DIMENSIONS[obj_class]
            else:
                dims = DEFAULT_DIMENSIONS

            # Choose reference dimension
            if "diameter" in dims:
                real_size = dims["diameter"]
            else:
                real_size = max(dims.get("width", 0.05), dims.get("height", 0.05))

            apparent_width = detection.bbox_width * self._image_width
            
            if apparent_width > 0:
                z = (real_size * self._fx) / apparent_width
            else:
                z = self.get_parameter('assumed_object_distance').value

        # Calculate X, Y using pinhole camera model
        # X = (u - cx) * Z / fx
        # Y = (v - cy) * Z / fy
        
        x = (u - self._cx) * z / self._fx
        y = (v - self._cy) * z / self._fy

        # In ROS, standard camera frame is:
        # X: right, Y: down, Z: forward
        
        point = Point()
        point.x = x   
        point.y = y   
        point.z = z   

        self.get_logger().debug(
            f"Object {detection.object_id} ({method}): "
            f"2D=({u}, {v}), "
            f"3D=({point.x:.3f}, {point.y:.3f}, {point.z:.3f})"
        )

        return point

    def _transform_to_robot_frame(self, camera_point: Point) -> Point:
        """Transform point from camera optical frame to robot base frame.
        
        Applies camera yaw (around Z) then pitch (around X), then the
        standard optical-to-robot axis reorientation, then translation.
        """
        # 1. Apply camera yaw rotation (around optical Z axis)
        yaw_rad = np.radians(self._camera_yaw_deg)
        cy = np.cos(yaw_rad)
        sy = np.sin(yaw_rad)
        
        x_yaw = cy * camera_point.x - sy * camera_point.y
        y_yaw = sy * camera_point.x + cy * camera_point.y
        z_yaw = camera_point.z
        
        # 2. Apply camera pitch rotation (positive pitch = camera looks down)
        pitch_rad = np.radians(self._camera_pitch_deg)
        cp = np.cos(pitch_rad)
        sp = np.sin(pitch_rad)
        
        # Rotate around camera X axis
        x_rot = x_yaw
        y_rot = cp * y_yaw + sp * z_yaw
        z_rot = -sp * y_yaw + cp * z_yaw
        
        # 3. Re-orient from optical frame to robot frame
        # Optical: X=Right, Y=Down, Z=Forward
        # Robot:   X=Forward, Y=Left, Z=Up
        robot_x = z_rot
        robot_y = -x_rot
        robot_z = -y_rot
        
        # 3. Apply translation from TF
        try:
            transform = self._tf_buffer.lookup_transform(
                self._robot_frame,
                self._camera_frame,
                rclpy.time.Time()
            )
            robot_point = Point()
            robot_point.x = robot_x + transform.transform.translation.x
            robot_point.y = robot_y + transform.transform.translation.y
            robot_point.z = robot_z + transform.transform.translation.z
            return robot_point
        except tf2_ros.LookupException:
            # Fallback: reorientation only, no translation
            point = Point()
            point.x = robot_x
            point.y = robot_y
            point.z = robot_z
            return point

    def _publish_object_tf(self, object_id: str, position: Point):
        """Publish TF frame for detected object."""
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = self._camera_frame
        t.child_frame_id = f"object_{object_id}"
        
        t.transform.translation.x = position.x
        t.transform.translation.y = position.y
        t.transform.translation.z = position.z
        
        # No rotation
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

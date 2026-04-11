#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
Color-based Object Detector Node

Detects objects by color using OpenCV HSV segmentation.
Publishes detections in normalized coordinates.

Usage:
    ros2 run aimee_vision_pipeline color_detector_node
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import Image, CameraInfo
from std_msgs.msg import Header
from cv_bridge import CvBridge
import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional

from aimee_msgs.msg import ObjectDetection


# Color ranges in HSV format
# Red wraps around in HSV, so it has two ranges
COLOR_RANGES: Dict[str, List[Tuple[np.ndarray, np.ndarray]]] = {
    "red": [
        (np.array([0, 100, 100]), np.array([10, 255, 255])),
        (np.array([160, 100, 100]), np.array([180, 255, 255])),
    ],
    "blue": [
        (np.array([100, 150, 50]), np.array([130, 255, 255])),
    ],
    "green": [
        (np.array([40, 100, 100]), np.array([80, 255, 255])),
    ],
    "yellow": [
        (np.array([20, 100, 100]), np.array([35, 255, 255])),
    ],
    "orange": [
        (np.array([10, 100, 100]), np.array([20, 255, 255])),
    ],
    "purple": [
        (np.array([130, 100, 100]), np.array([160, 255, 255])),
    ],
}

# Object shape/size heuristics
OBJECT_CONFIGS: Dict[str, Dict] = {
    "ball": {
        "aspect_ratio_range": (0.8, 1.2),  # Nearly circular
        "min_area": 100,
        "max_area": 50000,
        "circularity_threshold": 0.7,
    },
    "cup": {
        "aspect_ratio_range": (0.5, 0.9),  # Taller than wide
        "min_area": 500,
        "max_area": 50000,
        "circularity_threshold": 0.3,
    },
    "block": {
        "aspect_ratio_range": (0.7, 1.3),
        "min_area": 200,
        "max_area": 30000,
        "circularity_threshold": 0.5,
    },
}


class ColorDetectorNode(Node):
    """
    Detects colored objects in camera feed using HSV segmentation.
    
    Publishes ObjectDetection messages for downstream processing.
    """

    def __init__(self):
        super().__init__('color_detector_node')

        # Declare parameters
        self.declare_parameters(namespace='', parameters=[
            ('enabled_colors', ['red', 'blue', 'green', 'yellow']),
            ('detectable_objects', ['ball', 'cup', 'block']),
            ('confidence_threshold', 0.5),
            ('min_detection_area', 100),
            ('max_detection_area', 50000),
            ('camera_topic', '/camera/image_raw'),
            ('camera_info_topic', '/camera/camera_info'),
            ('publish_debug_image', True),
            ('debug_image_topic', '/vision/debug_image'),
            ('frame_id', 'obsbot_camera'),
        ])

        # Get parameters
        self._enabled_colors = self.get_parameter('enabled_colors').value
        self._detectable_objects = self.get_parameter('detectable_objects').value
        self._confidence_threshold = self.get_parameter('confidence_threshold').value
        self._min_area = self.get_parameter('min_detection_area').value
        self._max_area = self.get_parameter('max_detection_area').value
        self._camera_topic = self.get_parameter('camera_topic').value
        self._publish_debug = self.get_parameter('publish_debug_image').value
        self._frame_id = self.get_parameter('frame_id').value

        # Setup QoS
        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        
        best_effort_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        # CV Bridge
        self._cv_bridge = CvBridge()

        # Publishers
        self._detections_pub = self.create_publisher(
            ObjectDetection, '/vision/detections', reliable_qos
        )
        
        if self._publish_debug:
            self._debug_image_pub = self.create_publisher(
                Image, self.get_parameter('debug_image_topic').value, best_effort_qos
            )

        # Subscribers
        self._image_sub = self.create_subscription(
            Image,
            self._camera_topic,
            self._on_image,
            best_effort_qos
        )
        
        self._camera_info_sub = self.create_subscription(
            CameraInfo,
            self.get_parameter('camera_info_topic').value,
            self._on_camera_info,
            reliable_qos
        )

        # State
        self._camera_info: Optional[CameraInfo] = None
        self._image_width = 640  # Default, updated from actual images
        self._image_height = 480

        self.get_logger().info(
            f"ColorDetectorNode initialized:\n"
            f"  Colors: {self._enabled_colors}\n"
            f"  Objects: {self._detectable_objects}\n"
            f"  Min area: {self._min_area}, Max area: {self._max_area}"
        )

    def _on_camera_info(self, msg: CameraInfo):
        """Store camera calibration info."""
        self._camera_info = msg

    def _on_image(self, msg: Image):
        """Process incoming image."""
        try:
            # Convert to OpenCV format
            cv_image = self._cv_bridge.imgmsg_to_cv2(msg, 'bgr8')
            self._image_height, self._image_width = cv_image.shape[:2]

            # Detect objects
            detections = self._detect_objects(cv_image)

            # Publish detections
            for detection in detections:
                self._detections_pub.publish(detection)

            # Publish debug image if enabled
            if self._publish_debug:
                debug_image = self._draw_detections(cv_image.copy(), detections)
                debug_msg = self._cv_bridge.cv2_to_imgmsg(debug_image, 'bgr8')
                debug_msg.header = msg.header
                self._debug_image_pub.publish(debug_msg)

        except Exception as e:
            self.get_logger().error(f"Error processing image: {e}")

    def _detect_objects(self, image: np.ndarray) -> List[ObjectDetection]:
        """
        Detect colored objects in the image.
        
        Returns:
            List of ObjectDetection messages
        """
        detections = []
        
        # Convert to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Detect each color
        for color in self._enabled_colors:
            if color not in COLOR_RANGES:
                continue

            color_detections = self._detect_color(hsv, image, color)
            detections.extend(color_detections)

        return detections

    def _detect_color(self, hsv: np.ndarray, bgr: np.ndarray, 
                      color: str) -> List[ObjectDetection]:
        """Detect objects of a specific color."""
        detections = []
        
        # Create color mask
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for lower, upper in COLOR_RANGES[color]:
            mask |= cv2.inRange(hsv, lower, upper)

        # Morphological operations to clean up noise
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Find contours
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for contour in contours:
            detection = self._process_contour(contour, color)
            if detection:
                detections.append(detection)

        return detections

    def _process_contour(self, contour: np.ndarray, 
                         color: str) -> Optional[ObjectDetection]:
        """Process a single contour into an ObjectDetection message."""
        # Calculate area
        area = cv2.contourArea(contour)
        if area < self._min_area or area > self._max_area:
            return None

        # Get bounding box
        x, y, w, h = cv2.boundingRect(contour)
        
        # Calculate normalized center coordinates
        center_x = (x + w / 2) / self._image_width
        center_y = (y + h / 2) / self._image_height
        norm_width = w / self._image_width
        norm_height = h / self._image_height

        # Calculate circularity (for ball detection)
        perimeter = cv2.arcLength(contour, True)
        if perimeter > 0:
            circularity = 4 * np.pi * area / (perimeter ** 2)
        else:
            circularity = 0

        # Determine object class based on shape heuristics
        object_class = self._classify_object(contour, w, h, circularity)

        # Calculate confidence based on area and shape match
        confidence = min(1.0, area / 10000) * 0.5
        if object_class == "ball":
            confidence += circularity * 0.5
        else:
            confidence += 0.3

        if confidence < self._confidence_threshold:
            return None

        # Create detection message
        detection = ObjectDetection()
        detection.object_class = object_class
        detection.object_id = f"{color}_{object_class}_{id(contour)}"[:20]
        detection.color = color
        detection.confidence = float(confidence)
        
        # Bounding box (normalized)
        detection.bbox_x = float(center_x)
        detection.bbox_y = float(center_y)
        detection.bbox_width = float(norm_width)
        detection.bbox_height = float(norm_height)
        
        # Metadata
        detection.detection_method = "color"
        detection.camera_source = self._frame_id
        detection.timestamp = self.get_clock().now().to_msg()

        return detection

    def _classify_object(self, contour: np.ndarray, w: int, h: int, 
                         circularity: float) -> str:
        """Classify object type based on shape."""
        aspect_ratio = float(w) / h if h > 0 else 1.0

        # Check each object type
        for obj_type in self._detectable_objects:
            if obj_type not in OBJECT_CONFIGS:
                continue
            
            config = OBJECT_CONFIGS[obj_type]
            ar_min, ar_max = config["aspect_ratio_range"]
            
            if (ar_min <= aspect_ratio <= ar_max and
                circularity >= config["circularity_threshold"]):
                return obj_type

        # Default to generic "object"
        return "object"

    def _draw_detections(self, image: np.ndarray, 
                         detections: List[ObjectDetection]) -> np.ndarray:
        """Draw detection visualizations on image."""
        for det in detections:
            # Convert normalized to pixel coordinates
            cx = int(det.bbox_x * self._image_width)
            cy = int(det.bbox_y * self._image_height)
            w = int(det.bbox_width * self._image_width)
            h = int(det.bbox_height * self._image_height)
            
            x1 = cx - w // 2
            y1 = cy - h // 2
            x2 = x1 + w
            y2 = y1 + h

            # Color based on detected color
            color_map = {
                "red": (0, 0, 255),
                "blue": (255, 0, 0),
                "green": (0, 255, 0),
                "yellow": (0, 255, 255),
                "orange": (0, 128, 255),
                "purple": (255, 0, 255),
            }
            color = color_map.get(det.color, (255, 255, 255))

            # Draw rectangle
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            
            # Draw label
            label = f"{det.color} {det.object_class}: {det.confidence:.2f}"
            cv2.putText(image, label, (x1, y1 - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            # Draw center point
            cv2.circle(image, (cx, cy), 3, color, -1)

        # Add stats
        stats = f"Detections: {len(detections)}"
        cv2.putText(image, stats, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        return image


def main(args=None):
    rclpy.init(args=args)
    node = ColorDetectorNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down...")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

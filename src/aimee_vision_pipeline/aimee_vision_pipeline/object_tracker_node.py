#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
Object Tracker Node

Tracks detected objects across frames using simple temporal association.
Filters detections to provide stable object IDs.

Usage:
    ros2 run aimee_vision_pipeline object_tracker_node
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import Header
from aimee_msgs.msg import ObjectDetection
from typing import Dict, List, Optional, Tuple
from collections import deque
import numpy as np


class TrackedObject:
    """Represents a tracked object with temporal history."""
    
    def __init__(self, detection: ObjectDetection, track_id: int):
        self.track_id = track_id
        self.object_class = detection.object_class
        self.color = detection.color
        
        # Position history (for smoothing)
        self.position_history: deque = deque(maxlen=10)
        self.update(detection)
        
        # Tracking state
        self.missed_frames = 0
        self.total_frames = 1
        self.confidence = detection.confidence

    def update(self, detection: ObjectDetection):
        """Update with new detection."""
        self.position_history.append({
            'x': detection.bbox_x,
            'y': detection.bbox_y,
            'width': detection.bbox_width,
            'height': detection.bbox_height,
            'confidence': detection.confidence,
            'timestamp': detection.timestamp,
        })
        self.confidence = detection.confidence
        self.missed_frames = 0
        self.total_frames += 1

    def predict(self):
        """Increment missed frames (called when object not detected)."""
        self.missed_frames += 1

    def get_smoothed_position(self) -> Tuple[float, float, float, float]:
        """Get position smoothed over recent frames."""
        if len(self.position_history) < 2:
            p = self.position_history[0]
            return p['x'], p['y'], p['width'], p['height']
        
        # Simple moving average
        x = sum(p['x'] for p in self.position_history) / len(self.position_history)
        y = sum(p['y'] for p in self.position_history) / len(self.position_history)
        w = sum(p['width'] for p in self.position_history) / len(self.position_history)
        h = sum(p['height'] for p in self.position_history) / len(self.position_history)
        
        return x, y, w, h

    def to_detection_msg(self) -> ObjectDetection:
        """Convert to ObjectDetection message."""
        x, y, w, h = self.get_smoothed_position()
        
        msg = ObjectDetection()
        msg.object_class = self.object_class
        msg.object_id = f"{self.color}_{self.object_class}_{self.track_id:03d}"
        msg.color = self.color
        msg.confidence = self.confidence
        msg.bbox_x = float(x)
        msg.bbox_y = float(y)
        msg.bbox_width = float(w)
        msg.bbox_height = float(h)
        msg.detection_method = "tracked"
        msg.camera_source = "tracked"
        
        return msg


class ObjectTrackerNode(Node):
    """
    Tracks objects across frames to provide stable IDs.
    
    Uses simple distance-based association between frames.
    """

    def __init__(self):
        super().__init__('object_tracker_node')

        # Declare parameters
        self.declare_parameters(namespace='', parameters=[
            ('max_distance', 0.15),        # Max normalized distance for matching
            ('max_missed_frames', 5),      # Frames before track is lost
            ('min_frames_confirmed', 3),   # Frames before track is confirmed
            ('similarity_threshold', 0.7), # Color/class matching threshold
        ])

        self._max_distance = self.get_parameter('max_distance').value
        self._max_missed = self.get_parameter('max_missed_frames').value
        self._min_confirmed = self.get_parameter('min_frames_confirmed').value

        # Setup QoS
        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # Publishers
        self._tracked_pub = self.create_publisher(
            ObjectDetection, '/vision/tracked_objects', reliable_qos
        )
        
        # Subscribers
        self._detection_sub = self.create_subscription(
            ObjectDetection,
            '/vision/detections',
            self._on_detection,
            10
        )

        # State
        self._tracks: Dict[int, TrackedObject] = {}
        self._next_track_id = 1
        self._pending_detections: List[ObjectDetection] = []

        # Timer for track management
        self._track_timer = self.create_timer(0.033, self._update_tracks)  # ~30Hz

        self.get_logger().info(
            f"ObjectTrackerNode initialized:\n"
            f"  Max distance: {self._max_distance}\n"
            f"  Max missed: {self._max_missed}\n"
            f"  Min confirmed: {self._min_confirmed}"
        )

    def _on_detection(self, msg: ObjectDetection):
        """Buffer incoming detections."""
        self._pending_detections.append(msg)

    def _update_tracks(self):
        """Update tracks with pending detections."""
        if not self._pending_detections:
            # No new detections, increment missed frames
            for track in self._tracks.values():
                track.predict()
            self._cleanup_tracks()
            return

        # Match detections to existing tracks
        detections = self._pending_detections.copy()
        self._pending_detections.clear()

        # Mark all tracks as potentially missing
        for track in self._tracks.values():
            track.predict()

        # Match each detection to best track
        matched_tracks = set()
        matched_detections = set()

        for det in detections:
            best_track_id = None
            best_score = -1

            for track_id, track in self._tracks.items():
                if track_id in matched_tracks:
                    continue
                
                score = self._calculate_match_score(track, det)
                if score > best_score and score > 0.5:
                    best_score = score
                    best_track_id = track_id

            if best_track_id is not None:
                # Update existing track
                self._tracks[best_track_id].update(det)
                matched_tracks.add(best_track_id)
                matched_detections.add(id(det))
            else:
                # Create new track
                track = TrackedObject(det, self._next_track_id)
                self._tracks[self._next_track_id] = track
                self._next_track_id += 1

        # Publish confirmed tracks
        self._publish_tracks()

        # Cleanup old tracks
        self._cleanup_tracks()

    def _calculate_match_score(self, track: TrackedObject, 
                               detection: ObjectDetection) -> float:
        """Calculate match score between track and detection."""
        # Color must match
        if track.color != detection.color:
            return 0.0

        # Class must match (or one is "object")
        if track.object_class != detection.object_class:
            if track.object_class != "object" and detection.object_class != "object":
                return 0.0

        # Calculate position distance
        tx, ty, _, _ = track.get_smoothed_position()
        distance = np.sqrt((tx - detection.bbox_x) ** 2 + 
                          (ty - detection.bbox_y) ** 2)

        # Score based on distance (closer = higher score)
        if distance > self._max_distance:
            return 0.0

        distance_score = 1.0 - (distance / self._max_distance)
        
        # Combine with confidence
        score = distance_score * 0.7 + detection.confidence * 0.3
        
        return score

    def _cleanup_tracks(self):
        """Remove tracks that haven't been seen for too long."""
        to_remove = [
            track_id for track_id, track in self._tracks.items()
            if track.missed_frames > self._max_missed
        ]
        for track_id in to_remove:
            del self._tracks[track_id]

    def _publish_tracks(self):
        """Publish confirmed tracks."""
        for track in self._tracks.values():
            # Only publish confirmed tracks
            if track.total_frames >= self._min_confirmed:
                msg = track.to_detection_msg()
                msg.timestamp = self.get_clock().now().to_msg()
                self._tracked_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ObjectTrackerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down...")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

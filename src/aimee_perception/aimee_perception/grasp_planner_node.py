#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
Grasp Planner Node

Plans grasp poses for detected objects based on their 3D position
and object type.

Usage:
    ros2 run aimee_perception grasp_planner_node
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from geometry_msgs.msg import Pose, Point, Quaternion, Vector3
from aimee_msgs.msg import ObjectDetection, GraspPose
import numpy as np
from typing import Optional


# Grasp configuration by object type
GRASP_CONFIGS = {
    "ball": {
        "grasp_type": "top_down",
        "pre_grasp_offset": 0.15,  # meters above object
        "gripper_open": 0.08,      # meters
        "gripper_close": 0.02,     # meters
        "approach_vector": (0, 0, -1),  # Downward
    },
    "cup": {
        "grasp_type": "side",
        "pre_grasp_offset": 0.10,
        "gripper_open": 0.10,
        "gripper_close": 0.08,
        "approach_vector": (1, 0, 0),  # From side
    },
    "block": {
        "grasp_type": "top_down",
        "pre_grasp_offset": 0.12,
        "gripper_open": 0.06,
        "gripper_close": 0.00,
        "approach_vector": (0, 0, -1),
    },
    "object": {  # Default
        "grasp_type": "top_down",
        "pre_grasp_offset": 0.15,
        "gripper_open": 0.08,
        "gripper_close": 0.02,
        "approach_vector": (0, 0, -1),
    },
}


class GraspPlannerNode(Node):
    """
    Plans grasp strategies for detected objects.
    
    Given an object detection with 3D position, computes:
    - Pre-grasp pose (approach position)
    - Grasp pose (final gripper position)
    - Lift pose (position after grasping)
    """

    def __init__(self):
        super().__init__('grasp_planner_node')

        # Declare parameters
        self.declare_parameters(namespace='', parameters=[
            ('default_lift_height', 0.10),     # meters
            ('safety_clearance', 0.05),        # meters
            ('gripper_length', 0.08),          # meters (from wrist to fingers)
            ('approach_speed', 0.05),          # m/s
            ('grasp_speed', 0.02),             # m/s
        ])

        self._lift_height = self.get_parameter('default_lift_height').value
        self._safety_clearance = self.get_parameter('safety_clearance').value

        # Setup QoS
        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # Publishers
        self._grasp_pub = self.create_publisher(
            GraspPose, '/manipulation/grasp_pose', reliable_qos
        )

        # Subscribers
        self._detection_sub = self.create_subscription(
            ObjectDetection,
            '/vision/detections_3d',
            self._on_detection,
            10
        )

        # Services
        # Could add a service for on-demand grasp planning

        self.get_logger().info(
            f"GraspPlannerNode initialized:\n"
            f"  Default lift height: {self._lift_height}m\n"
            f"  Safety clearance: {self._safety_clearance}m"
        )

    def _on_detection(self, msg: ObjectDetection):
        """Plan grasp for detected object."""
        try:
            # Only plan for objects with valid 3D position
            if msg.position_camera.x == 0 and msg.position_camera.y == 0:
                return

            grasp_pose = self._plan_grasp(msg)
            if grasp_pose:
                self._grasp_pub.publish(grasp_pose)
                self.get_logger().info(
                    f"Planned grasp for {msg.object_id}: "
                    f"type={grasp_pose.grasp_type}, "
                    f"quality={grasp_pose.grasp_quality:.2f}"
                )

        except Exception as e:
            self.get_logger().error(f"Error planning grasp: {e}")

    def _plan_grasp(self, detection: ObjectDetection) -> Optional[GraspPose]:
        """Plan a grasp for the given object detection."""
        
        # Get grasp configuration for object type
        obj_class = detection.object_class
        if obj_class not in GRASP_CONFIGS:
            obj_class = "object"
        
        config = GRASP_CONFIGS[obj_class]
        
        # Object position in robot frame (or camera frame if no transform)
        obj_pos = detection.position_robot if detection.position_robot.x != 0 else detection.position_camera
        
        # Calculate grasp poses based on grasp type
        if config["grasp_type"] == "top_down":
            grasp = self._plan_top_down_grasp(obj_pos, config, detection)
        elif config["grasp_type"] == "side":
            grasp = self._plan_side_grasp(obj_pos, config, detection)
        else:
            grasp = self._plan_top_down_grasp(obj_pos, config, detection)
        
        # Fill in detection reference
        grasp.object_id = detection.object_id
        grasp.object_class = detection.object_class
        
        return grasp

    def _plan_top_down_grasp(self, obj_pos: Point, config: dict, 
                             detection: ObjectDetection) -> GraspPose:
        """Plan a top-down grasp (coming from above)."""
        
        grasp = GraspPose()
        
        # Pre-grasp: above the object
        pre_grasp = Pose()
        pre_grasp.position.x = obj_pos.x
        pre_grasp.position.y = obj_pos.y
        pre_grasp.position.z = obj_pos.z + config["pre_grasp_offset"]
        # Orientation: gripper pointing down
        pre_grasp.orientation = self._quaternion_from_euler(0, np.pi/2, 0)
        grasp.pre_grasp_pose = pre_grasp
        grasp.pre_grasp_offset = config["pre_grasp_offset"]
        
        # Grasp: at object position (minus gripper length consideration)
        grasp_pose = Pose()
        grasp_pose.position.x = obj_pos.x
        grasp_pose.position.y = obj_pos.y
        # Account for gripper finger thickness
        grasp_pose.position.z = obj_pos.z + 0.02
        grasp_pose.orientation = pre_grasp.orientation
        grasp.grasp_pose = grasp_pose
        
        # Lift: up from grasp position
        lift_pose = Pose()
        lift_pose.position.x = obj_pos.x
        lift_pose.position.y = obj_pos.y
        lift_pose.position.z = obj_pos.z + self._lift_height
        lift_pose.orientation = pre_grasp.orientation
        grasp.lift_pose = lift_pose
        grasp.lift_height = self._lift_height
        
        # Gripper settings
        grasp.gripper_open_width = config["gripper_open"]
        grasp.gripper_close_width = config["gripper_close"]
        
        # Approach direction
        grasp.approach_vector = Vector3()
        grasp.approach_vector.x = float(config["approach_vector"][0])
        grasp.approach_vector.y = float(config["approach_vector"][1])
        grasp.approach_vector.z = float(config["approach_vector"][2])
        
        # Metadata
        grasp.grasp_type = config["grasp_type"]
        grasp.grasp_quality = self._calculate_grasp_quality(detection)
        grasp.frame_id = "base_link"
        grasp.timestamp = self.get_clock().now().to_msg()
        
        return grasp

    def _plan_side_grasp(self, obj_pos: Point, config: dict,
                         detection: ObjectDetection) -> GraspPose:
        """Plan a side grasp (coming from the side)."""
        
        grasp = GraspPose()
        
        # Pre-grasp: to the side of the object
        pre_grasp = Pose()
        pre_grasp.position.x = obj_pos.x - config["pre_grasp_offset"]
        pre_grasp.position.y = obj_pos.y
        pre_grasp.position.z = obj_pos.z + 0.02  # Slightly above center
        # Orientation: gripper pointing forward
        pre_grasp.orientation = self._quaternion_from_euler(0, 0, 0)
        grasp.pre_grasp_pose = pre_grasp
        grasp.pre_grasp_offset = config["pre_grasp_offset"]
        
        # Grasp: at object position
        grasp_pose = Pose()
        grasp_pose.position.x = obj_pos.x
        grasp_pose.position.y = obj_pos.y
        grasp_pose.position.z = obj_pos.z + 0.02
        grasp_pose.orientation = pre_grasp.orientation
        grasp.grasp_pose = grasp_pose
        
        # Lift: up and slightly back
        lift_pose = Pose()
        lift_pose.position.x = obj_pos.x - 0.05
        lift_pose.position.y = obj_pos.y
        lift_pose.position.z = obj_pos.z + self._lift_height
        lift_pose.orientation = pre_grasp.orientation
        grasp.lift_pose = lift_pose
        grasp.lift_height = self._lift_height
        
        # Gripper settings
        grasp.gripper_open_width = config["gripper_open"]
        grasp.gripper_close_width = config["gripper_close"]
        
        # Approach direction
        grasp.approach_vector = Vector3()
        grasp.approach_vector.x = float(config["approach_vector"][0])
        grasp.approach_vector.y = float(config["approach_vector"][1])
        grasp.approach_vector.z = float(config["approach_vector"][2])
        
        # Metadata
        grasp.grasp_type = config["grasp_type"]
        grasp.grasp_quality = self._calculate_grasp_quality(detection)
        grasp.frame_id = "base_link"
        grasp.timestamp = self.get_clock().now().to_msg()
        
        return grasp

    def _calculate_grasp_quality(self, detection: ObjectDetection) -> float:
        """Calculate a quality score for the grasp."""
        # Factors:
        # - Detection confidence
        # - Distance to camera (closer is better for accuracy)
        # - Object type (balls are easier than irregular objects)
        
        quality = detection.confidence
        
        # Distance factor: prefer objects 0.3-1.0m away
        distance = np.sqrt(
            detection.position_camera.x ** 2 +
            detection.position_camera.y ** 2 +
            detection.position_camera.z ** 2
        )
        if 0.3 < distance < 1.0:
            quality *= 1.0
        elif distance < 0.2:
            quality *= 0.5  # Too close
        else:
            quality *= 0.7  # Far away
        
        # Object type factor
        if detection.object_class == "ball":
            quality *= 1.0  # Easy to grasp
        elif detection.object_class == "block":
            quality *= 0.9
        else:
            quality *= 0.8
        
        return min(1.0, quality)

    def _quaternion_from_euler(self, roll: float, pitch: float, yaw: float) -> Quaternion:
        """Convert Euler angles to quaternion."""
        cy = np.cos(yaw * 0.5)
        sy = np.sin(yaw * 0.5)
        cp = np.cos(pitch * 0.5)
        sp = np.sin(pitch * 0.5)
        cr = np.cos(roll * 0.5)
        sr = np.sin(roll * 0.5)
        
        q = Quaternion()
        q.w = cr * cp * cy + sr * sp * sy
        q.x = sr * cp * cy - cr * sp * sy
        q.y = cr * sp * cy + sr * cp * sy
        q.z = cr * cp * sy - sr * sp * cy
        
        return q


def main(args=None):
    rclpy.init(args=args)
    node = GraspPlannerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down...")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

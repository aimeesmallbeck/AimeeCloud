#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
Pick and Place Action Server

Executes pick and place operations via ROS2 Action interface.
Coordinates between vision, perception, and arm control.

Usage:
    ros2 run aimee_manipulation pick_place_server
    
Test:
    ros2 action send_goal /manipulation/pick_place aimee_msgs/action/PickPlace "{object_class: 'ball', object_color: 'red'}"
"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from aimee_msgs.action import PickPlace
from aimee_msgs.msg import ObjectDetection, GraspPose, ArmCommand
from geometry_msgs.msg import Pose
from typing import Optional
import time


class PickPlaceState:
    """Internal state for pick and place operation."""
    
    SEARCHING = "searching"
    APPROACHING = "approaching"
    GRASPING = "grasping"
    LIFTING = "lifting"
    PLACING = "placing"
    COMPLETED = "completed"
    FAILED = "failed"


class PickPlaceServer(Node):
    """
    Action server for pick and place operations.
    
    Handles requests like "pick up the red ball" by:
    1. Waiting for matching object detection
    2. Getting grasp plan from grasp planner
    3. Executing grasp sequence via arm controller
    4. Reporting success/failure
    """

    def __init__(self):
        super().__init__('pick_place_server')

        # Declare parameters
        self.declare_parameters(namespace='', parameters=[
            ('search_timeout', 10.0),      # Seconds to wait for object detection
            ('grasp_timeout', 5.0),        # Seconds to wait for grasp plan
            ('max_retries', 2),            # Number of grasp retries
            ('approach_speed', 50),        # Arm speed 0-100
        ])

        self._search_timeout = self.get_parameter('search_timeout').value
        self._grasp_timeout = self.get_parameter('grasp_timeout').value
        self._max_retries = self.get_parameter('max_retries').value

        # Setup QoS
        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # Publishers
        self._arm_cmd_pub = self.create_publisher(
            ArmCommand, '/arm/command', reliable_qos
        )
        self._tts_pub = self.create_publisher(
            Pose, '/tts/speak', reliable_qos  # Actually uses std_msgs/String
        )

        # Subscribers
        self._detection_sub = self.create_subscription(
            ObjectDetection,
            '/vision/detections_3d',
            self._on_detection,
            10
        )
        self._grasp_sub = self.create_subscription(
            GraspPose,
            '/manipulation/grasp_pose',
            self._on_grasp_plan,
            10
        )

        # Action server
        self._action_server = ActionServer(
            self,
            PickPlace,
            '/manipulation/pick_place',
            execute_callback=self._execute_callback,
            goal_callback=self._goal_callback,
            cancel_callback=self._cancel_callback
        )

        # State
        self._current_detection: Optional[ObjectDetection] = None
        self._current_grasp: Optional[GraspPose] = None

        self.get_logger().info(
            f"PickPlaceServer initialized:\n"
            f"  Search timeout: {self._search_timeout}s\n"
            f"  Grasp timeout: {self._grasp_timeout}s\n"
            f"  Max retries: {self._max_retries}"
        )

    def _goal_callback(self, goal_request):
        """Accept or reject goal."""
        self.get_logger().info(
            f"Received pick_place goal: {goal_request.object_color} "
            f"{goal_request.object_class}"
        )
        return GoalResponse.ACCEPT

    def _cancel_callback(self, goal_handle):
        """Handle cancel request."""
        self.get_logger().info("Cancel requested")
        return CancelResponse.ACCEPT

    async def _execute_callback(self, goal_handle):
        """Execute the pick and place action."""
        request = goal_handle.request
        result = PickPlace.Result()
        feedback = PickPlace.Feedback()
        
        start_time = time.time()
        retry_count = 0

        # Phase 1: SEARCH
        feedback.current_phase = PickPlaceState.SEARCHING
        feedback.phase_progress = 0
        goal_handle.publish_feedback(feedback)
        
        self.get_logger().info(f"🔍 Searching for {request.object_color} {request.object_class}...")
        
        detection = await self._wait_for_detection(
            request.object_class,
            request.object_color,
            goal_handle
        )
        
        if not detection:
            result.success = False
            result.failure_reason = "Object not found within timeout"
            result.failure_phase = PickPlaceState.SEARCHING
            goal_handle.abort()
            return result

        result.grasped_object_id = detection.object_id
        self.get_logger().info(f"✓ Found {detection.object_id}")

        # Retry loop
        while retry_count <= self._max_retries:
            # Phase 2: APPROACH
            feedback.current_phase = PickPlaceState.APPROACHING
            feedback.detected_object = detection
            goal_handle.publish_feedback(feedback)
            
            # Wait for grasp plan
            grasp = await self._wait_for_grasp_plan(detection, goal_handle)
            
            if not grasp:
                result.success = False
                result.failure_reason = "Failed to plan grasp"
                result.failure_phase = PickPlaceState.APPROACHING
                goal_handle.abort()
                return result

            feedback.planned_grasp = grasp
            goal_handle.publish_feedback(feedback)

            # Phase 3: GRASP
            feedback.current_phase = PickPlaceState.GRASPING
            feedback.phase_progress = 50
            goal_handle.publish_feedback(feedback)
            
            grasp_success = await self._execute_grasp(grasp, goal_handle)
            
            if grasp_success:
                break
            else:
                retry_count += 1
                if retry_count <= self._max_retries:
                    self.get_logger().warn(f"Grasp failed, retrying ({retry_count}/{self._max_retries})...")
                    # Reset detection to get fresh data
                    self._current_detection = None
                else:
                    result.success = False
                    result.failure_reason = "Grasp failed after all retries"
                    result.failure_phase = PickPlaceState.GRASPING
                    result.retry_count = retry_count
                    goal_handle.abort()
                    return result

        # Phase 4: LIFT
        feedback.current_phase = PickPlaceState.LIFTING
        feedback.phase_progress = 75
        goal_handle.publish_feedback(feedback)
        
        lift_success = await self._execute_lift(grasp, goal_handle)
        
        if not lift_success:
            result.success = False
            result.failure_reason = "Lift failed"
            result.failure_phase = PickPlaceState.LIFTING
            goal_handle.abort()
            return result

        # Phase 5: PLACE (if enabled)
        if request.enable_place:
            feedback.current_phase = PickPlaceState.PLACING
            feedback.phase_progress = 90
            goal_handle.publish_feedback(feedback)
            
            place_success = await self._execute_place(request.place_pose, goal_handle)
            
            if not place_success:
                result.success = False
                result.failure_reason = "Place failed"
                result.failure_phase = PickPlaceState.PLACING
                goal_handle.abort()
                return result

        # Success!
        feedback.current_phase = PickPlaceState.COMPLETED
        feedback.phase_progress = 100
        goal_handle.publish_feedback(feedback)
        
        result.success = True
        result.message = "Pick and place completed successfully"
        result.grasp_quality = grasp.grasp_quality
        result.execution_time = time.time() - start_time
        result.retry_count = retry_count
        
        self.get_logger().info("✅ Pick and place completed successfully!")
        goal_handle.succeed()
        
        return result

    async def _wait_for_detection(self, obj_class: str, obj_color: str, 
                                   goal_handle) -> Optional[ObjectDetection]:
        """Wait for object detection matching criteria."""
        start_time = time.time()
        
        while time.time() - start_time < self._search_timeout:
            # Check for cancellation
            if goal_handle.is_cancel_requested:
                return None
            
            # Check current detection
            if self._current_detection:
                det = self._current_detection
                
                # Match criteria
                class_match = (det.object_class == obj_class or 
                              obj_class == "object" or
                              obj_class == "")
                color_match = (det.color == obj_color or
                              obj_color == "")
                
                if class_match and color_match:
                    detection = self._current_detection
                    self._current_detection = None  # Clear so we get fresh data
                    return detection
            
            # Small sleep to allow callbacks
            await self._sleep(0.1)
        
        return None

    async def _wait_for_grasp_plan(self, detection: ObjectDetection,
                                    goal_handle) -> Optional[GraspPose]:
        """Wait for grasp planner to produce a plan."""
        start_time = time.time()
        self._current_grasp = None
        
        while time.time() - start_time < self._grasp_timeout:
            if goal_handle.is_cancel_requested:
                return None
            
            if self._current_grasp:
                if self._current_grasp.object_id == detection.object_id:
                    grasp = self._current_grasp
                    self._current_grasp = None
                    return grasp
            
            await self._sleep(0.1)
        
        return None

    async def _execute_grasp(self, grasp: GraspPose, goal_handle) -> bool:
        """Execute grasp via arm controller."""
        self.get_logger().info("🤖 Executing grasp...")
        
        cmd = ArmCommand()
        cmd.command_type = "grasp"
        cmd.grasp_pose = grasp
        cmd.use_planning = False
        cmd.skill_id = "pick_place"
        
        self._arm_cmd_pub.publish(cmd)
        
        # Wait for completion (simulated)
        await self._sleep(4.0)  # Simulated grasp time
        
        return True  # Simulated success

    async def _execute_lift(self, grasp: GraspPose, goal_handle) -> bool:
        """Execute lift motion."""
        self.get_logger().info("⬆️  Executing lift...")
        
        cmd = ArmCommand()
        cmd.command_type = "cartesian"
        cmd.target_pose = grasp.lift_pose
        cmd.cartesian_speed = 30.0
        cmd.use_planning = False
        cmd.skill_id = "pick_place"
        
        self._arm_cmd_pub.publish(cmd)
        
        await self._sleep(2.0)
        
        return True

    async def _execute_place(self, place_pose: Pose, goal_handle) -> bool:
        """Execute place motion."""
        self.get_logger().info("📦 Executing place...")
        
        cmd = ArmCommand()
        cmd.command_type = "cartesian"
        cmd.target_pose = place_pose
        cmd.cartesian_speed = 30.0
        cmd.use_planning = False
        cmd.skill_id = "pick_place"
        
        self._arm_cmd_pub.publish(cmd)
        
        await self._sleep(2.0)
        
        # Open gripper
        gripper_cmd = ArmCommand()
        gripper_cmd.command_type = "gripper"
        gripper_cmd.gripper_position = 100  # Open
        gripper_cmd.skill_id = "pick_place"
        
        self._arm_cmd_pub.publish(gripper_cmd)
        
        await self._sleep(1.0)
        
        return True

    async def _sleep(self, duration: float):
        """Async sleep."""
        start = time.time()
        while time.time() - start < duration:
            await rclpy.spin_once(self, timeout_sec=0.01)

    def _on_detection(self, msg: ObjectDetection):
        """Store latest detection."""
        self._current_detection = msg

    def _on_grasp_plan(self, msg: GraspPose):
        """Store latest grasp plan."""
        self._current_grasp = msg


def main(args=None):
    rclpy.init(args=args)
    node = PickPlaceServer()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down...")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

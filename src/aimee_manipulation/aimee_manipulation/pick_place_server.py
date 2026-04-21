#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
Pick and Place Action Server

Executes pick and place operations via ROS2 Action interface.

MODES:
  VISION mode (default): Uses /vision/detections_3d and /manipulation/grasp_pose
  TEST mode: Uses predefined joint configurations, no vision needed

TEST MODE:
  In test mode, objects are defined as joint angle presets.
  The server directly publishes JointTrajectory to /arm/joint_trajectory.

Workspace Safety:
  12x12 inches (305x305mm) directly in front of robot.
  Enforced via joint limits: base ±20°, shoulder -10° to +20°,
  elbow 70° to 110°, wrist ±20°.

Usage:
    ros2 run aimee_manipulation pick_place_server --ros-args -p test_mode:=true

Test:
    ros2 action send_goal /manipulation/pick_place aimee_msgs/action/PickPlace \
        "{object_class: 'test_center', enable_place: true}"
"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from rclpy.executors import MultiThreadedExecutor
from aimee_msgs.action import PickPlace
from aimee_msgs.msg import ObjectDetection, GraspPose, ArmCommand
from geometry_msgs.msg import Pose
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from typing import Optional, List, Dict
import time
import numpy as np


class PickPlaceState:
    """Internal state for pick and place operation."""
    SEARCHING = "searching"
    APPROACHING = "approaching"
    GRASPING = "grasping"
    LIFTING = "lifting"
    PLACING = "placing"
    COMPLETED = "completed"
    FAILED = "failed"


# Joint names in ROS trajectory order
JOINT_NAMES = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'gripper']

# Workspace safety limits (degrees)
# Empirically determined from hand-taught positions on 23.5cm square
WORKSPACE_LIMITS_DEG = {
    'joint1': (-50.0, 40.0),    # base: covers recorded positions
    'joint2': (50.0, 70.0),     # shoulder: covers recorded positions
    'joint3': (80.0, 125.0),    # elbow: covers recorded positions
    'joint4': (-20.0, 20.0),    # wrist: minimal deflection
    'joint5': (-10.0, 10.0),    # roll: small range
    'gripper': (0.0, 180.0),    # full range
}

# Recorded test object positions from hand-teaching (joint angles in DEGREES)
# 23.5cm square workspace, z ≈ -210mm (table height)
DEFAULT_TEST_OBJECTS = {
    'corner_1': {
        # x=360.5, y=-111.8, z=-207.5  (front-left)
        'joint_angles': [-17.23, 65.40, 83.68, 0.44, 0.18],
        'description': 'Front-left corner of 23.5cm square',
    },
    'corner_2': {
        # x=369.6, y=99.2, z=-205.3  (front-right)
        'joint_angles': [15.03, 66.01, 92.03, -18.11, 0.53],
        'description': 'Front-right corner of 23.5cm square',
    },
    'corner_3': {
        # x=145.8, y=95.2, z=-207.4  (back-right)
        'joint_angles': [33.14, 57.84, 118.05, 17.40, 0.62],
        'description': 'Back-right corner of 23.5cm square',
    },
    'corner_4': {
        # x=122.6, y=-117.1, z=-210.0  (back-left)
        'joint_angles': [-43.68, 58.72, 118.49, 17.05, 0.62],
        'description': 'Back-left corner of 23.5cm square',
    },
}

# Recorded place position (joint angles in DEGREES)
# x=253.7, y=161.8, z=-214.9  (outside the square, to the right)
DEFAULT_PLACE_JOINTS_DEG = [32.52, 60.74, 97.74, 8.09, 0.62]

# Top-down pick/place waypoints (hand-taught, joint angles in DEGREES)
TOP_DOWN_HOME_DEG =      [0.44,   27.34, 105.83, 43.60,  0.44]
TOP_DOWN_APPROACH_DEG =  [-15.65, 60.74, 55.90,  56.87, -19.34]
# Grasp: lowered 1cm from previous test (was 62/55/55)
TOP_DOWN_GRASP_DEG =     [-15.65, 65.00, 57.00,  52.00, -19.34]
TOP_DOWN_LIFT_DEG =      [-15.73, 61.70, 31.82,  84.21, -19.95]
# Place approach: same height as lift, but at place base/roll angle
TOP_DOWN_PLACE_APPROACH_DEG = [30.24, 61.70, 31.82,  84.21,  30.32]
# Place: raised 2cm from previous test (was 71.37/52.03/63.64)
TOP_DOWN_PLACE_DEG =     [30.24,  66.00, 48.00,  69.00,  30.32]

# Gripper positions (radians, firmware-native)
GRIPPER_OPEN = 0.0      # fully open
GRIPPER_CLOSED = np.pi  # fully closed

# Motion timing (seconds per phase)
# Conservative values: driver waits for motion completion, but ESP32 is slow
PHASE_TIMES = {
    'approach': 5.0,
    'grasp': 3.0,
    'lift': 4.0,
    'place_approach': 5.0,
    'place': 3.0,
    'home': 5.0,
}


class PickPlaceServer(Node):
    """
    Action server for pick and place operations.

    VISION mode: Coordinates between vision pipeline and arm controller
    TEST mode: Uses predefined joint configurations, drives arm directly
    """

    def __init__(self):
        super().__init__('pick_place_server')

        # Declare parameters
        self.declare_parameters(namespace='', parameters=[
            ('search_timeout', 10.0),
            ('grasp_timeout', 5.0),
            ('max_retries', 2),
            ('approach_speed', 50),
            ('test_mode', False),           # Enable test mode (no vision)
            ('place_joints_deg', DEFAULT_PLACE_JOINTS_DEG),
            ('command_topic', '/arm/joint_trajectory'),
            ('home_joints_deg', [0.0, 0.0, 90.0, 0.0, 0.0]),
            ('gripper_open_rad', float(GRIPPER_OPEN)),
            ('gripper_close_rad', float(GRIPPER_CLOSED)),
        ])

        self._search_timeout = self.get_parameter('search_timeout').value
        self._grasp_timeout = self.get_parameter('grasp_timeout').value
        self._max_retries = self.get_parameter('max_retries').value
        self._test_mode = self.get_parameter('test_mode').value
        self._command_topic = self.get_parameter('command_topic').value
        self._home_joints_deg = self.get_parameter('home_joints_deg').value
        self._place_joints_deg = self.get_parameter('place_joints_deg').value
        self._gripper_open = self.get_parameter('gripper_open_rad').value
        self._gripper_closed = self.get_parameter('gripper_close_rad').value

        # Load test objects (use defaults, can override via param file)
        self._test_objects = DEFAULT_TEST_OBJECTS

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
        self._traj_pub = self.create_publisher(
            JointTrajectory, self._command_topic, reliable_qos
        )

        # Subscribers (only used in vision mode)
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

        mode_str = "TEST MODE (no vision)" if self._test_mode else "VISION MODE"
        self.get_logger().info(
            f"PickPlaceServer initialized [{mode_str}]:\n"
            f"  Search timeout: {self._search_timeout}s\n"
            f"  Max retries: {self._max_retries}\n"
            f"  Command topic: {self._command_topic}\n"
            f"  Test objects: {list(self._test_objects.keys())}"
        )

    def _parse_test_objects(self, param_value) -> Dict:
        """Parse test objects from parameter."""
        objects = {}
        try:
            if isinstance(param_value, dict):
                for name, config in param_value.items():
                    if 'joint_angles' in config:
                        objects[name] = {
                            'joint_angles': list(config['joint_angles']),
                            'description': config.get('description', name),
                        }
            return objects if objects else DEFAULT_TEST_OBJECTS
        except Exception as e:
            self.get_logger().warn(f"Failed to parse test_objects param: {e}")
            return DEFAULT_TEST_OBJECTS

    def _goal_callback(self, goal_request):
        """Accept or reject goal."""
        obj = goal_request.object_class or "unknown"
        color = goal_request.object_color or ""
        self.get_logger().info(
            f"Received pick_place goal: {color} {obj} "
            f"(place={'yes' if goal_request.enable_place else 'no'})"
        )

        # In test mode, validate object exists
        if self._test_mode:
            if obj == 'top_down':
                # Top-down mode uses explicit waypoints, skip validation
                pass
            elif obj not in self._test_objects:
                self.get_logger().error(
                    f"Test object '{obj}' not found. Available: "
                    f"{list(self._test_objects.keys())}"
                )
                return GoalResponse.REJECT
            else:
                # Validate workspace safety for corner objects
                joints_deg = self._test_objects[obj]['joint_angles']
                if not self._validate_workspace(joints_deg):
                    self.get_logger().error(
                        f"Object '{obj}' joint angles violate workspace safety!"
                    )
                    return GoalResponse.REJECT

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

        if self._test_mode:
            return await self._execute_test_mode(request, goal_handle, result, feedback, start_time)
        else:
            return await self._execute_vision_mode(request, goal_handle, result, feedback, start_time)

    async def _execute_test_mode(self, request, goal_handle, result, feedback, start_time):
        """Execute pick/place using predefined joint configurations."""
        retry_count = 0
        obj_name = request.object_class

        # Phase 1: SEARCH (instant in test mode)
        feedback.current_phase = PickPlaceState.SEARCHING
        feedback.phase_progress = 0
        goal_handle.publish_feedback(feedback)
        await self._sleep(0.5)

        if obj_name == 'top_down':
            return await self._execute_top_down(request, goal_handle, result, feedback, start_time)

        # Legacy corner-based test mode
        obj_config = self._test_objects[obj_name]
        obj_joints_deg = obj_config['joint_angles']

        self.get_logger().info(
            f"🧪 TEST MODE: Picking '{obj_name}' at joints {obj_joints_deg}°"
        )

        # Compute joint angles in radians
        # NOTE: arm joints are in DEGREES, gripper values are already in RADIANS.
        obj_joints_rad = self._deg_to_rad(obj_joints_deg) + [self._gripper_open]
        place_joints_rad = self._deg_to_rad(self._place_joints_deg) + [self._gripper_closed]
        home_joints_rad = self._deg_to_rad(self._home_joints_deg) + [self._gripper_open]

        # Compute approach positions (1cm above surface = reduce elbow by ~6°)
        approach_offset_rad = np.radians(6.0)
        obj_approach_rad = obj_joints_rad.copy()
        obj_approach_rad[2] = max(0.0, obj_joints_rad[2] - approach_offset_rad)
        place_approach_rad = place_joints_rad.copy()
        place_approach_rad[2] = max(0.0, place_joints_rad[2] - approach_offset_rad)

        # Phase 2: APPROACH → 1cm above object, gripper open
        feedback.current_phase = PickPlaceState.APPROACHING
        feedback.phase_progress = 20
        goal_handle.publish_feedback(feedback)

        self.get_logger().info("➡️  Approach: moving to 1cm above object")
        self._send_joint_trajectory(obj_approach_rad, duration=PHASE_TIMES['approach'])
        await self._sleep(PHASE_TIMES['approach'] + 1.0)

        # Phase 3: GRASP → lower to surface, close gripper
        feedback.current_phase = PickPlaceState.GRASPING
        feedback.phase_progress = 50
        goal_handle.publish_feedback(feedback)

        self.get_logger().info("🤖 Grasp: lowering to surface and closing gripper")
        # First lower to surface
        grasp_lower = obj_joints_rad.copy()
        grasp_lower[5] = self._gripper_open
        self._send_joint_trajectory(grasp_lower, duration=1.0)
        await self._sleep(1.5)
        # Then close gripper
        grasp_close = obj_joints_rad.copy()
        grasp_close[5] = self._gripper_closed
        self._send_joint_trajectory(grasp_close, duration=PHASE_TIMES['grasp'])
        await self._sleep(PHASE_TIMES['grasp'] + 1.0)

        # Phase 4: LIFT → back to 1cm above
        feedback.current_phase = PickPlaceState.LIFTING
        feedback.phase_progress = 75
        goal_handle.publish_feedback(feedback)

        self.get_logger().info("⬆️  Lift: raising 1cm with object")
        lift_joints = obj_approach_rad.copy()
        lift_joints[5] = self._gripper_closed
        self._send_joint_trajectory(lift_joints, duration=PHASE_TIMES['lift'])
        await self._sleep(PHASE_TIMES['lift'] + 1.0)

        # Phase 5: PLACE (if enabled)
        if request.enable_place:
            feedback.current_phase = PickPlaceState.PLACING
            feedback.phase_progress = 90
            goal_handle.publish_feedback(feedback)

            self.get_logger().info("📦 Place: moving to place position")
            # Move to place approach (1cm above, gripper closed)
            self._send_joint_trajectory(place_approach_rad, duration=PHASE_TIMES['place_approach'])
            await self._sleep(PHASE_TIMES['place_approach'] + 1.0)

            # Lower to place position
            place_lower = place_joints_rad.copy()
            place_lower[5] = self._gripper_closed
            self._send_joint_trajectory(place_lower, duration=1.0)
            await self._sleep(1.5)

            # Open gripper
            place_release = place_joints_rad.copy()
            place_release[5] = self._gripper_open
            self._send_joint_trajectory(place_release, duration=PHASE_TIMES['place'])
            await self._sleep(PHASE_TIMES['place'] + 1.0)

            # Lift back to 1cm above
            self._send_joint_trajectory(place_approach_rad, duration=1.0)
            await self._sleep(1.5)

        # Return home
        self.get_logger().info("🏠 Returning home")
        self._send_joint_trajectory(home_joints_rad, duration=PHASE_TIMES['home'])
        await self._sleep(PHASE_TIMES['home'] + 1.0)

        # Success!
        feedback.current_phase = PickPlaceState.COMPLETED
        feedback.phase_progress = 100
        goal_handle.publish_feedback(feedback)

        result.success = True
        result.message = f"Test pick/place of '{obj_name}' completed"
        result.execution_time = time.time() - start_time
        result.retry_count = retry_count

        self.get_logger().info("✅ Pick and place completed successfully!")
        goal_handle.succeed()
        return result

    async def _execute_top_down(self, request, goal_handle, result, feedback, start_time):
        """Execute top-down pick/place using explicit hand-taught waypoints."""
        retry_count = 0

        self.get_logger().info("🧪 TOP-DOWN MODE: Using hand-taught waypoints")

        # Convert waypoints to radians.
        # NOTE: arm joints are in DEGREES, gripper values are already in RADIANS.
        # Do NOT pass gripper values through _deg_to_rad()!
        home_rad = self._deg_to_rad(TOP_DOWN_HOME_DEG) + [self._gripper_open]
        approach_rad = self._deg_to_rad(TOP_DOWN_APPROACH_DEG) + [self._gripper_open]
        grasp_rad = self._deg_to_rad(TOP_DOWN_GRASP_DEG) + [self._gripper_open]
        lift_rad = self._deg_to_rad(TOP_DOWN_LIFT_DEG) + [self._gripper_closed]
        place_approach_rad = self._deg_to_rad(TOP_DOWN_PLACE_APPROACH_DEG) + [self._gripper_closed]
        place_rad = self._deg_to_rad(TOP_DOWN_PLACE_DEG) + [self._gripper_closed]
        place_release_rad = self._deg_to_rad(TOP_DOWN_PLACE_DEG) + [self._gripper_open]
        place_retract_rad = self._deg_to_rad(TOP_DOWN_PLACE_APPROACH_DEG) + [self._gripper_open]

        # Phase 2: APPROACH (gripper open)
        feedback.current_phase = PickPlaceState.APPROACHING
        feedback.phase_progress = 20
        goal_handle.publish_feedback(feedback)

        self.get_logger().info("➡️  Approach: moving to top-down approach")
        self._send_joint_trajectory(approach_rad, duration=6.0)
        await self._sleep(8.0)

        # Phase 3: GRASP → lower to grasp, close gripper
        feedback.current_phase = PickPlaceState.GRASPING
        feedback.phase_progress = 50
        goal_handle.publish_feedback(feedback)

        # Small move: approach→grasp is only ~5°, use short duration
        self.get_logger().info("🤖 Grasp: lowering to grasp position")
        self._send_joint_trajectory(grasp_rad, duration=3.0)
        await self._sleep(5.0)

        # Close gripper
        self.get_logger().info("🤖 Closing gripper")
        grasp_closed = grasp_rad.copy()
        grasp_closed[5] = self._gripper_closed
        self._send_joint_trajectory(grasp_closed, duration=2.0)
        await self._sleep(3.0)

        # Phase 4: LIFT → raise with object
        feedback.current_phase = PickPlaceState.LIFTING
        feedback.phase_progress = 75
        goal_handle.publish_feedback(feedback)

        self.get_logger().info("⬆️  Lift: raising with object")
        self._send_joint_trajectory(lift_rad, duration=6.0)
        await self._sleep(8.0)

        # Phase 5: PLACE (if enabled)
        if request.enable_place:
            feedback.current_phase = PickPlaceState.PLACING
            feedback.phase_progress = 90
            goal_handle.publish_feedback(feedback)

            # Move to place approach (same height as lift, gripper closed)
            self.get_logger().info("📦 Place approach: moving to place at lift height")
            self._send_joint_trajectory(place_approach_rad, duration=6.0)
            await self._sleep(8.0)

            # Lower to place position (gripper still closed)
            self.get_logger().info("📦 Place: lowering to place position")
            self._send_joint_trajectory(place_rad, duration=3.0)
            await self._sleep(5.0)

            # Open gripper at place
            self.get_logger().info("📦 Releasing object")
            self._send_joint_trajectory(place_release_rad, duration=2.0)
            await self._sleep(3.0)

            # Retract to place approach (up, not back to pickup)
            self.get_logger().info("📦 Retracting up from place")
            self._send_joint_trajectory(place_retract_rad, duration=3.0)
            await self._sleep(5.0)

        # Return home
        self.get_logger().info("🏠 Returning home")
        self._send_joint_trajectory(home_rad, duration=6.0)
        await self._sleep(8.0)

        # Success!
        feedback.current_phase = PickPlaceState.COMPLETED
        feedback.phase_progress = 100
        goal_handle.publish_feedback(feedback)

        result.success = True
        result.message = "Top-down pick/place completed"
        result.execution_time = time.time() - start_time
        result.retry_count = retry_count

        self.get_logger().info("✅ Top-down pick and place completed successfully!")
        goal_handle.succeed()
        return result

    async def _execute_vision_mode(self, request, goal_handle, result, feedback, start_time):
        """Original vision-based execution (unchanged)."""
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
                    self.get_logger().warn(
                        f"Grasp failed, retrying ({retry_count}/{self._max_retries})..."
                    )
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

    def _validate_workspace(self, joints_deg: List[float]) -> bool:
        """Validate joint angles are within safe workspace limits."""
        limits = [
            ('joint1', joints_deg[0], WORKSPACE_LIMITS_DEG['joint1']),
            ('joint2', joints_deg[1], WORKSPACE_LIMITS_DEG['joint2']),
            ('joint3', joints_deg[2], WORKSPACE_LIMITS_DEG['joint3']),
            ('joint4', joints_deg[3], WORKSPACE_LIMITS_DEG['joint4']),
            ('joint5', joints_deg[4], WORKSPACE_LIMITS_DEG['joint5']),
        ]

        for name, value, (lo, hi) in limits:
            if not (lo <= value <= hi):
                self.get_logger().error(
                    f"Workspace violation: {name}={value}° outside [{lo}, {hi}]"
                )
                return False
        return True

    def _deg_to_rad(self, joints_deg: List[float]) -> List[float]:
        """Convert joint angles from degrees to radians."""
        return [np.radians(a) for a in joints_deg]

    def _send_joint_trajectory(self, positions_rad: List[float], duration: float = 3.0):
        """Publish a JointTrajectory command to the arm."""
        traj = JointTrajectory()
        traj.header.stamp = self.get_clock().now().to_msg()
        traj.joint_names = JOINT_NAMES

        point = JointTrajectoryPoint()
        point.positions = positions_rad
        point.time_from_start.sec = int(duration)
        point.time_from_start.nanosec = int((duration % 1) * 1e9)

        traj.points.append(point)
        self._traj_pub.publish(traj)

        self.get_logger().debug(
            f"Sent trajectory: {[np.degrees(p) for p in positions_rad]}° "
            f"in {duration:.1f}s"
        )

    async def _wait_for_detection(self, obj_class: str, obj_color: str,
                                   goal_handle) -> Optional[ObjectDetection]:
        """Wait for object detection matching criteria."""
        start_time = time.time()
        while time.time() - start_time < self._search_timeout:
            if goal_handle.is_cancel_requested:
                return None
            if self._current_detection:
                det = self._current_detection
                class_match = (det.object_class == obj_class or
                              obj_class == "object" or obj_class == "")
                color_match = (det.color == obj_color or obj_color == "")
                if class_match and color_match:
                    detection = self._current_detection
                    self._current_detection = None
                    return detection
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
        await self._sleep(4.0)
        return True

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

        gripper_cmd = ArmCommand()
        gripper_cmd.command_type = "gripper"
        gripper_cmd.gripper_position = 100
        gripper_cmd.skill_id = "pick_place"
        self._arm_cmd_pub.publish(gripper_cmd)
        await self._sleep(1.0)
        return True

    async def _sleep(self, duration: float):
        """Sleep for given duration."""
        time.sleep(duration)

    def _on_detection(self, msg: ObjectDetection):
        """Store latest detection."""
        self._current_detection = msg

    def _on_grasp_plan(self, msg: GraspPose):
        """Store latest grasp plan."""
        self._current_grasp = msg


def main(args=None):
    rclpy.init(args=args)
    node = PickPlaceServer()
    # Use MultiThreadedExecutor so action server can send responses
    # while execute_callback is blocked by time.sleep() during arm motion
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down...")
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

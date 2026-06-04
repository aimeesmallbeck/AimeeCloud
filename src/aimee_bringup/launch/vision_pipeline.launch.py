#!/usr/bin/env python3
"""
Vision Pipeline launch file for Aimee Robot
Launches complete vision-to-manipulation pipeline
"""

import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.conditions import IfCondition


def generate_launch_description():
    # Launch arguments
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time'
    )
    
    enable_camera_arg = DeclareLaunchArgument(
        'enable_camera',
        default_value='true',
        description='Enable Orbbec Astra Pro RGB+Depth node'
    )
    
    enable_detection_arg = DeclareLaunchArgument(
        'enable_detection',
        default_value='true',
        description='Enable color detection node'
    )
    
    enable_tracking_arg = DeclareLaunchArgument(
        'enable_tracking',
        default_value='true',
        description='Enable object tracking node'
    )
    
    enable_perception_arg = DeclareLaunchArgument(
        'enable_perception',
        default_value='true',
        description='Enable perception nodes (pose estimation, grasp planning)'
    )
    
    enable_manipulation_arg = DeclareLaunchArgument(
        'enable_manipulation',
        default_value='true',
        description='Enable manipulation nodes (arm controller, pick_place server)'
    )
    
    # Get launch configurations
    use_sim_time = LaunchConfiguration('use_sim_time')
    enable_camera = LaunchConfiguration('enable_camera')
    enable_detection = LaunchConfiguration('enable_detection')
    enable_tracking = LaunchConfiguration('enable_tracking')
    enable_perception = LaunchConfiguration('enable_perception')
    enable_manipulation = LaunchConfiguration('enable_manipulation')
    
    # === Vision Pipeline Nodes ===
    
    # Astra Pro RGB+Depth Camera Node
    astra_pro_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('aimee_bringup'), 
            'launch', 
            'astra_pro_rgbd.launch.py'
        )),
        condition=IfCondition(enable_camera)
    )
    
    # Color Detector Node
    color_detector_node = Node(
        package='aimee_vision_pipeline',
        executable='color_detector_node',
        name='color_detector',
        output='screen',
        parameters=[{
            'enabled': True,
            'enabled_colors': ['red', 'pink', 'blue', 'green', 'yellow', 'orange', 'purple'],
            'min_object_area': 100,
            'confidence_threshold': 0.1,
            'publish_debug_image': True,
            'camera_topic': '/camera/color/image_raw',
            'camera_info_topic': '/camera/color/camera_info',
            'frame_id': 'camera_color_frame',
        }],
        condition=IfCondition(enable_detection)
    )
    
    # Object Tracker Node
    object_tracker_node = Node(
        package='aimee_vision_pipeline',
        executable='object_tracker_node',
        name='object_tracker',
        output='screen',
        parameters=[{
            'enabled': True,
            'max_disappeared': 30,
            'max_distance': 100.0,
            'use_kalman': True,
        }],
        condition=IfCondition(enable_tracking)
    )
    
    # Pose Estimator Node
    pose_estimator_node = Node(
        package='aimee_perception',
        executable='pose_estimator_node',
        name='pose_estimator',
        output='screen',
        parameters=[{
            'enabled': True,
            'image_width': 640,
            'image_height': 480,
            'camera_pitch_deg': 90.0,  # Camera is directly overhead, perpendicular to desk
            'camera_yaw_deg': 0.0,      # Tune this if arm goes to wrong angle (90° = image top points to robot left)
            'robot_frame': 'arm_base_link',
            # Astra Pro depth units: observed raw values ~78 at 80cm height.
            # 100.0 treats values as centimeters (78 -> 0.78m).
            'depth_scale': 100.0,
            'use_hardware_depth': True,
            'min_depth': 0.10,
            'max_depth': 1.20,  # Increased to allow desk (0.78m) + margin for edges/floor
        }],
        condition=IfCondition(enable_perception)
    )
    
    # Grasp Planner Node
    grasp_planner_node = Node(
        package='aimee_perception',
        executable='grasp_planner_node',
        name='grasp_planner',
        output='screen',
        parameters=[{
            'enabled': True,
            'default_grasp_height': 0.15,
            'gripper_open_width': 0.08,
            'gripper_closed_width': 0.02,
        }],
        condition=IfCondition(enable_perception)
    )
    
    # === Manipulation Nodes ===
    
    # Arm Kinematics Bridge Node (Hardware)
    arm_controller_node = Node(
        package='aimee_manipulation',
        executable='arm_kinematics_bridge_rpc',
        name='arm_kinematics_bridge_rpc',
        output='screen',
        condition=IfCondition(enable_manipulation)
    )
    
    # PickPlace Action Server
    pick_place_server = Node(
        package='aimee_manipulation',
        executable='pick_place_server',
        name='pick_place_server',
        output='screen',
        parameters=[{
            'enabled': True,
            'default_timeout': 30.0,
            'approach_height': 0.1,
            'gripper_open_delay': 1.0,
            'gripper_close_delay': 1.0,
        }],
        condition=IfCondition(enable_manipulation)
    )
    
    # TF2 static transform for camera to arm base
    # NOTE: The translation [X, Y, Z] was calibrated on 2026-05-09.
    # Rotation is handled inside pose_estimator_node (camera_pitch_deg).
    # If you need full 6-DOF TF for other tools (RViz), add roll/pitch/yaw here.
    camera_tf_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='camera_to_arm_tf',
        arguments=[
            '-0.3088', '0.2370', '0.5000', # Translation X, Y, Z (meters) - Z: camera 60cm above desk, arm base ~10cm above desk
            '0.0', '0.0', '0.0', # Rotation Yaw, Pitch, Roll (radians)
            'arm_base_link', 'camera_color_frame'
        ],
        condition=IfCondition(enable_camera)
    )
    
    return LaunchDescription([
        # Arguments
        use_sim_time_arg,
        enable_camera_arg,
        enable_detection_arg,
        enable_tracking_arg,
        enable_perception_arg,
        enable_manipulation_arg,
        
        # Vision Pipeline
        astra_pro_node,
        color_detector_node,
        object_tracker_node,
        camera_tf_node,
        
        # Perception
        pose_estimator_node,
        grasp_planner_node,
        
        # Manipulation
        arm_controller_node,
        pick_place_server,
    ])

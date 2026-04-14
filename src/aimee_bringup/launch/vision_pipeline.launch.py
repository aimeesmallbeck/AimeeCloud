#!/usr/bin/env python3
"""
Vision Pipeline launch file for Aimee Robot
Launches complete vision-to-manipulation pipeline
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
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
        description='Enable OBSBOT camera node'
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
    
    # OBSBOT Camera Node
    obsbot_node = Node(
        package='aimee_vision_obsbot',
        executable='obsbot_node',
        name='obsbot_camera',
        output='screen',
        parameters=[{
            'host': '192.168.5.1',
            'osc_send_port': 16284,
            'control_mode': 'auto',
            'auto_reconnect': True,
            'tracking_sensitivity': 0.5,
            'publish_video': False,
            'enabled': True,
        }],
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
            'colors': ['red', 'blue', 'green', 'yellow', 'orange', 'purple'],
            'min_object_area': 500,
            'confidence_threshold': 0.7,
            'publish_debug_image': True,
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
            'focal_length': 800.0,
            'camera_height': 0.5,
            'camera_tilt': -0.3,
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
    
    # Arm Controller Node (Simulated)
    arm_controller_node = Node(
        package='aimee_manipulation',
        executable='arm_controller_node',
        name='arm_controller',
        output='screen',
        parameters=[{
            'enabled': True,
            'simulation_mode': True,
            'arm_type': 'roarm_m3',
            'joint_limits': {
                'j1': [-90, 90],
                'j2': [0, 90],
                'j3': [-90, 90],
                'j4': [-90, 90],
                'j5': [-90, 90],
                'j6': [-90, 90],
            },
            'max_velocity': 1.0,
        }],
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
    
    return LaunchDescription([
        # Arguments
        use_sim_time_arg,
        enable_camera_arg,
        enable_detection_arg,
        enable_tracking_arg,
        enable_perception_arg,
        enable_manipulation_arg,
        
        # Vision Pipeline
        obsbot_node,
        color_detector_node,
        object_tracker_node,
        
        # Perception
        pose_estimator_node,
        grasp_planner_node,
        
        # Manipulation
        arm_controller_node,
        pick_place_server,
    ])

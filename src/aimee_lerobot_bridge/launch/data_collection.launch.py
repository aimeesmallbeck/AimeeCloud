#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
Data Collection Launch File

Launches all nodes needed for recording robot demonstrations.

Usage:
    ros2 launch aimee_lerobot_bridge data_collection.launch.py
    
    # Then in another terminal:
    ros2 service call /start_recording std_srvs/srv/Trigger
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """Generate launch description for data collection."""
    
    # Launch arguments
    output_dir_arg = DeclareLaunchArgument(
        'output_dir',
        default_value='~/aimee_datasets',
        description='Directory to save dataset'
    )
    
    dataset_name_arg = DeclareLaunchArgument(
        'dataset_name',
        default_value='pick_place_demo',
        description='Dataset name'
    )
    
    use_teleop_arg = DeclareLaunchArgument(
        'use_teleop',
        default_value='true',
        description='Enable keyboard teleop'
    )

    # Configurations
    output_dir = LaunchConfiguration('output_dir')
    dataset_name = LaunchConfiguration('dataset_name')
    use_teleop = LaunchConfiguration('use_teleop')

    # Dataset Recorder Node
    recorder_node = Node(
        package='aimee_lerobot_bridge',
        executable='dataset_recorder',
        name='dataset_recorder',
        output='screen',
        parameters=[{
            'output_dir': output_dir,
            'dataset_name': dataset_name,
            'fps': 30,
            'observation_topics': [
                '/camera/image_raw',
                '/joint_states',
                '/arm/joint_states',
            ],
            'action_topics': [
                '/arm/command',
                '/cmd_vel',
            ],
            'camera_topics': [
                '/camera/image_raw',
            ],
            'compress_images': False,
            'record_tf': True,
        }]
    )

    # Keyboard Teleop Node (optional)
    teleop_node = Node(
        package='aimee_lerobot_bridge',
        executable='teleop_keyboard',
        name='teleop_keyboard',
        output='screen',
        condition=use_teleop,
        parameters=[{
            'joint_names': ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'gripper'],
            'step_size': 5.0,
            'publish_rate': 10.0,
            'action_topic': '/arm/command',
        }]
    )

    # Image viewer (optional, for monitoring)
    image_view_node = Node(
        package='rqt_image_view',
        executable='rqt_image_view',
        name='image_view',
        arguments=['/camera/image_raw'],
        condition=use_teleop,
    )

    return LaunchDescription([
        LogInfo(msg=["Starting Aimee Data Collection..."]),
        output_dir_arg,
        dataset_name_arg,
        use_teleop_arg,
        recorder_node,
        teleop_node,
        # image_view_node,  # Uncomment if rqt_image_view is available
    ])

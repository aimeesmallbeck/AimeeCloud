#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
Policy Inference Launch File

Launches the policy controller for autonomous execution.

Usage:
    ros2 launch aimee_lerobot_bridge policy_inference.launch.py \
        policy_repo_id:=aimee/pick_place_policy
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """Generate launch description for policy inference."""
    
    policy_repo_arg = DeclareLaunchArgument(
        'policy_repo_id',
        default_value='',
        description='Hugging Face policy repository ID'
    )
    
    policy_type_arg = DeclareLaunchArgument(
        'policy_type',
        default_value='act',
        description='Policy type: act, diffusion, vqbet'
    )
    
    device_arg = DeclareLaunchArgument(
        'device',
        default_value='cpu',
        description='Device: cpu or cuda'
    )

    # Configurations
    policy_repo_id = LaunchConfiguration('policy_repo_id')
    policy_type = LaunchConfiguration('policy_type')
    device = LaunchConfiguration('device')

    # Policy Controller Node
    policy_node = Node(
        package='aimee_lerobot_bridge',
        executable='policy_controller',
        name='policy_controller',
        output='screen',
        parameters=[{
            'policy_repo_id': policy_repo_id,
            'policy_type': policy_type,
            'device': device,
            'control_freq': 10.0,
            'action_chunk_size': 16,
            'temporal_ensemble': True,
            'ensemble_alpha': 0.1,
            'camera_topics': ['/camera/image_raw'],
            'joint_state_topic': '/joint_states',
            'action_topic': '/arm/command',
        }]
    )

    return LaunchDescription([
        LogInfo(msg=["Starting Policy Inference..."]),
        policy_repo_arg,
        policy_type_arg,
        device_arg,
        policy_node,
    ])

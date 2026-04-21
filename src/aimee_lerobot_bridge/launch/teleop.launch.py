#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
Teleoperation Launch File

Launches teleoperation nodes for RoArm-M3.

Usage:
    ros2 launch aimee_lerobot_bridge teleop.launch.py
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """Generate launch description for teleop."""
    
    teleop_type_arg = DeclareLaunchArgument(
        'teleop_type',
        default_value='keyboard',
        description='Teleop type: keyboard or gamepad'
    )
    
    teleop_type = LaunchConfiguration('teleop_type')

    # Keyboard teleop
    keyboard_teleop = Node(
        package='aimee_lerobot_bridge',
        executable='teleop_keyboard',
        name='teleop_keyboard',
        output='screen',
        parameters=[{
            'joint_names': ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'gripper'],
            'step_size': 5.0,
            'publish_rate': 10.0,
        }]
    )

    # Gamepad teleop (future)
    # gamepad_teleop = Node(...)

    return LaunchDescription([
        teleop_type_arg,
        keyboard_teleop,
    ])

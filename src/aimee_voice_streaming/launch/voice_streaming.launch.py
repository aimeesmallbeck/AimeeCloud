#!/usr/bin/env python3
"""Launch file for aimee_voice_streaming node."""

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument


def generate_launch_description():
    config_path = LaunchConfiguration('config_path')

    config_path_arg = DeclareLaunchArgument(
        'config_path',
        default_value=os.path.join(
            os.getenv('AIMEE_ROBOT_WS', '/workspace'),
            'src/aimee_voice_streaming/config/voice_streaming.yaml'
        ),
        description='Path to voice_streaming configuration YAML'
    )

    voice_streaming_node = Node(
        package='aimee_voice_streaming',
        executable='voice_streaming_node',
        name='voice_streaming',
        output='screen',
        parameters=[config_path],
    )

    return LaunchDescription([
        config_path_arg,
        voice_streaming_node,
    ])

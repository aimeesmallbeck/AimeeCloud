#!/usr/bin/env python3
"""
SLAM launch for Aimee robots using slam_toolbox.

Usage:
  ros2 launch aimee_bringup slam.launch.py
  ros2 launch aimee_bringup slam.launch.py use_sim_time:=true
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    bringup_dir = get_package_share_directory('aimee_bringup')
    slam_params_file = os.path.join(bringup_dir, 'config', 'slam_params.yaml')

    use_sim_time = LaunchConfiguration('use_sim_time')

    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation/Gazebo clock'
    )

    slam_node = Node(
        package='slam_toolbox',
        executable='sync_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[
            slam_params_file,
            {'use_sim_time': use_sim_time}
        ]
    )

    return LaunchDescription([
        LogInfo(msg=["Starting SLAM Toolbox (sync) — params: ", slam_params_file]),
        declare_use_sim_time,
        slam_node,
    ])

#!/usr/bin/env python3
"""
Launch file for AimeeNav integrated navigation node.

Usage:
    ros2 launch aimee_nav aimee_nav.launch.py

This launches AimeeNav as a standalone navigation stack.
No other navigation nodes (ldlidar_stl_ros2, slam_toolbox, nav2,
aimee_ugv02_controller) are required.
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_dir = get_package_share_directory('aimee_nav')
    params_file = os.path.join(pkg_dir, 'config', 'aimee_nav_params.yaml')

    use_sim_time = LaunchConfiguration('use_sim_time')
    robot_name = LaunchConfiguration('robot_name')

    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation/Gazebo clock'
    )
    declare_robot_name = DeclareLaunchArgument(
        'robot_name',
        default_value='aimee',
        description='Robot name for frame IDs'
    )

    aimee_nav_node = Node(
        package='aimee_nav',
        executable='aimee_nav_node',
        name='aimee_nav',
        output='screen',
        parameters=[params_file, {'use_sim_time': use_sim_time}],
    )

    return LaunchDescription([
        LogInfo(msg=["Starting AimeeNav — standalone integrated navigation"]),
        declare_use_sim_time,
        declare_robot_name,
        aimee_nav_node,
    ])

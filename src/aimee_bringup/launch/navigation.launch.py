#!/usr/bin/env python3
"""
Combined robot bringup + SLAM/Nav2 navigation for Aimee robots.

Usage:
  # Mapping mode (SLAM + Nav2)
  ros2 launch aimee_bringup navigation.launch.py slam:=true

  # Localization mode (existing map + Nav2)
  ros2 launch aimee_bringup navigation.launch.py slam:=false map:=/path/to/map.yaml

  # Disable base controller for lidar-only testing
  ros2 launch aimee_bringup navigation.launch.py slam:=true use_base:=false

  # Disable voice/LLM to save resources
  ros2 launch aimee_bringup navigation.launch.py slam:=true use_voice:=false use_llm:=false
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    bringup_dir = get_package_share_directory('aimee_bringup')

    slam = LaunchConfiguration('slam')
    map_yaml_file = LaunchConfiguration('map')
    use_sim_time = LaunchConfiguration('use_sim_time')

    declare_slam = DeclareLaunchArgument(
        'slam',
        default_value='True',
        description='Whether to run SLAM'
    )
    declare_map = DeclareLaunchArgument(
        'map',
        default_value='',
        description='Full path to map yaml file (required if slam:=false)'
    )
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation/Gazebo clock'
    )

    # Robot bringup (hardware + core software)
    robot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(bringup_dir, 'launch', 'robot.launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
        }.items()
    )

    # Nav2 bringup (includes SLAM or localization + navigation)
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(bringup_dir, 'launch', 'nav2.launch.py')
        ),
        launch_arguments={
            'slam': slam,
            'map': map_yaml_file,
            'use_sim_time': use_sim_time,
        }.items()
    )

    return LaunchDescription([
        declare_slam,
        declare_map,
        declare_use_sim_time,
        LogInfo(msg=["Aimee Navigation Bringup — slam: ", slam, " | map: ", map_yaml_file]),
        robot_launch,
        nav2_launch,
    ])

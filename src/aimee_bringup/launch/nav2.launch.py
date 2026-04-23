#!/usr/bin/env python3
"""
Nav2 navigation launch for Aimee robots.

Usage:
  # With SLAM (mapping + navigation)
  ros2 launch aimee_bringup nav2.launch.py slam:=True

  # With existing map (localization + navigation)
  ros2 launch aimee_bringup nav2.launch.py slam:=False map:=/path/to/map.yaml

  # Simulation clock
  ros2 launch aimee_bringup nav2.launch.py use_sim_time:=true
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, LogInfo
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node


def generate_launch_description():
    bringup_dir = get_package_share_directory('aimee_bringup')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    nav2_launch_dir = os.path.join(nav2_bringup_dir, 'launch')

    params_file = os.path.join(bringup_dir, 'config', 'nav2_params.yaml')

    slam = LaunchConfiguration('slam')
    map_yaml_file = LaunchConfiguration('map')
    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')
    use_composition = LaunchConfiguration('use_composition')
    use_respawn = LaunchConfiguration('use_respawn')

    declare_slam = DeclareLaunchArgument(
        'slam',
        default_value='False',
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
    declare_autostart = DeclareLaunchArgument(
        'autostart',
        default_value='True',
        description='Automatically startup the nav2 stack'
    )
    declare_use_composition = DeclareLaunchArgument(
        'use_composition',
        default_value='True',
        description='Use composed bringup'
    )
    declare_use_respawn = DeclareLaunchArgument(
        'use_respawn',
        default_value='False',
        description='Whether to respawn if a node crashes'
    )

    # Include nav2_bringup bringup_launch.py with our params
    nav2_bringup_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_launch_dir, 'bringup_launch.py')
        ),
        launch_arguments={
            'slam': slam,
            'map': map_yaml_file,
            'use_sim_time': use_sim_time,
            'params_file': params_file,
            'autostart': autostart,
            'use_composition': use_composition,
            'use_respawn': use_respawn,
        }.items()
    )

    return LaunchDescription([
        LogInfo(msg=["Starting Nav2 — params: ", params_file]),
        declare_slam,
        declare_map,
        declare_use_sim_time,
        declare_autostart,
        declare_use_composition,
        declare_use_respawn,
        nav2_bringup_launch,
    ])

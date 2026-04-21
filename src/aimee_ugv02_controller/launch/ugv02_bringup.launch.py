#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
UGV02 Bringup Launch File

Launches the UGV02 controller and related nodes.

Usage:
    ros2 launch aimee_ugv02_controller ugv02_bringup.launch.py
    
With params:
    ros2 launch aimee_ugv02_controller ugv02_bringup.launch.py serial_port:=/dev/ttyUSB0
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """Generate launch description for UGV02 bringup."""
    
    # Launch arguments
    serial_port_arg = DeclareLaunchArgument(
        'serial_port',
        default_value='/dev/ttyACM0',
        description='Serial port for UGV02 ESP32'
    )
    
    baud_rate_arg = DeclareLaunchArgument(
        'baud_rate',
        default_value='115200',
        description='Serial baud rate'
    )
    
    use_tf_arg = DeclareLaunchArgument(
        'publish_tf',
        default_value='true',
        description='Publish odom->base_link transform'
    )
    
    enable_teleop_arg = DeclareLaunchArgument(
        'enable_teleop',
        default_value='false',
        description='Enable keyboard teleop'
    )

    # Configurations
    serial_port = LaunchConfiguration('serial_port')
    baud_rate = LaunchConfiguration('baud_rate')
    publish_tf = LaunchConfiguration('publish_tf')
    enable_teleop = LaunchConfiguration('enable_teleop')

    # UGV02 Controller Node
    ugv02_controller = Node(
        package='aimee_ugv02_controller',
        executable='ugv02_controller_node',
        name='ugv02_controller',
        output='screen',
        parameters=[{
            'serial_port': serial_port,
            'baud_rate': baud_rate,
            'base_frame': 'base_link',
            'odom_frame': 'odom',
            'wheel_separation': 0.23,
            'wheel_radius': 0.04,
            'max_speed': 0.5,
            'cmd_timeout': 0.5,
            'heartbeat_interval': 0.1,
            'continuous_feedback': True,
            'publish_tf': publish_tf,
            'linear_scale': 1.0,
            'angular_scale': 1.0,
        }],
        remappings=[
            ('/cmd_vel', '/cmd_vel'),
            ('/odom', '/odom'),
            ('/imu', '/imu'),
        ]
    )

    # Teleop Node (conditional)
    teleop_node = Node(
        package='aimee_ugv02_controller',
        executable='ugv02_teleop_node',
        name='ugv02_teleop',
        output='screen',
        condition=enable_teleop,
        parameters=[{
            'linear_speed': 0.3,
            'angular_speed': 0.5,
            'ramp_rate': 0.1,
            'cmd_rate': 10.0,
        }],
    )

    return LaunchDescription([
        LogInfo(msg=["Starting UGV02 Bringup..."]),
        serial_port_arg,
        baud_rate_arg,
        use_tf_arg,
        enable_teleop_arg,
        ugv02_controller,
        teleop_node,
    ])

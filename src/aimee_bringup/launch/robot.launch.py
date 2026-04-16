#!/usr/bin/env python3
"""
Robot-specific launch file for Aimee Robot
Launches hardware-specific nodes based on robot type
"""

import os
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument, 
    IncludeLaunchDescription,
    SetEnvironmentVariable
)
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node


def generate_launch_description():
    # Launch arguments
    robot_arg = DeclareLaunchArgument(
        'robot',
        default_value='ron',
        description='Robot to launch (ron or wren)'
    )
    
    use_cloud_arg = DeclareLaunchArgument(
        'use_cloud',
        default_value='true',
        description='Enable AimeeCloud connection'
    )
    
    use_vision_arg = DeclareLaunchArgument(
        'use_vision',
        default_value='true',
        description='Enable vision/camera nodes'
    )
    
    # Get launch configurations
    robot = LaunchConfiguration('robot')
    use_cloud = LaunchConfiguration('use_cloud')
    use_vision = LaunchConfiguration('use_vision')
    
    # Check robot type
    is_ron = PythonExpression(["'", robot, "' == 'ron'"])
    is_wren = PythonExpression(["'", robot, "' == 'wren'"])
    
    # Include core launch
    core_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                os.getenv('AIMEE_ROBOT_WS', '~/aimee-robot-ws'),
                'src/aimee_bringup/launch/core.launch.py'
            )
        ]),
        launch_arguments={
            'robot_name': robot,
        }.items()
    )
    
    # Ron-specific nodes (UGV02 + RoArm-M3)
    ugv02_controller_node = Node(
        package='aimee_motion',
        executable='ugv02_controller',
        name='ugv02_controller',
        output='screen',
        parameters=[{
            'serial_port': '/dev/ttyACM0',
            'baud_rate': 115200,
        }],
        condition=IfCondition(is_ron)
    )
    
    roarm_controller_node = Node(
        package='aimee_arm',
        executable='roarm_controller',
        name='roarm_controller',
        output='screen',
        parameters=[{
            'serial_port': '/dev/ttyUSB0',
            'baud_rate': 115200,
        }],
        condition=IfCondition(is_ron)
    )
    
    # Wren-specific nodes (Wave Rover)
    wave_rover_controller_node = Node(
        package='aimee_motion',
        executable='wave_rover_controller',
        name='wave_rover_controller',
        output='screen',
        parameters=[{
            'serial_port': '/dev/ttyACM0',
            'baud_rate': 115200,
        }],
        condition=IfCondition(is_wren)
    )
    
    # Vision Manager (OBSBOT)
    vision_manager_node = Node(
        package='aimee_vision',
        executable='vision_manager',
        name='vision_manager',
        output='screen',
        parameters=[{
            'obsbot_host': '192.168.5.1',
            'obsbot_port': 16284,
            'enable_tracking': True,
        }],
        condition=IfCondition(use_vision)
    )
    
    # AimeeCloud Client (ACC)
    aimee_cloud_client_node = Node(
        package='aimee_cloud_bridge',
        executable='cloud_bridge_node',
        name='aimee_cloud_client',
        output='screen',
        parameters=[{
            'endpoint': 'http://209.38.147.67:8089',
            'reconnect_interval': 5.0,
        }],
        condition=IfCondition(use_cloud)
    )
    
    # State Manager (aggregates robot state)
    state_manager_node = Node(
        package='aimee_bringup',
        executable='state_manager',
        name='state_manager',
        output='screen',
        parameters=[{
            'robot_name': robot,
            'publish_rate': 10.0,  # Hz
        }]
    )
    
    return LaunchDescription([
        # Arguments
        robot_arg,
        use_cloud_arg,
        use_vision_arg,
        
        # Core
        core_launch,
        
        # Hardware Controllers
        ugv02_controller_node,
        roarm_controller_node,
        wave_rover_controller_node,
        
        # Vision
        vision_manager_node,
        
        # Cloud
        aimee_cloud_client_node,
        
        # State
        state_manager_node,
    ])

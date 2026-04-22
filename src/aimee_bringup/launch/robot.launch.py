#!/usr/bin/env python3
"""
Robot-specific launch file for Aimee Robot
Launches hardware-specific nodes based on robot type.
Includes core.launch.py for the intelligence/voice/cloud stack.
"""

import os
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
    LogInfo,
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

    use_arm_arg = DeclareLaunchArgument(
        'use_arm',
        default_value='true',
        description='Enable arm/manipulation nodes (Ron only)'
    )

    # Get launch configurations
    robot = LaunchConfiguration('robot')
    use_cloud = LaunchConfiguration('use_cloud')
    use_vision = LaunchConfiguration('use_vision')
    use_arm = LaunchConfiguration('use_arm')

    # Check robot type
    is_ron = PythonExpression(["'", robot, "' == 'ron'"])
    is_wren = PythonExpression(["'", robot, "' == 'wren'"])

    # ─── Include core launch (intelligence stack) ───
    core_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                os.getenv('AIMEE_ROBOT_WS', '/workspace'),
                'src/aimee_bringup/launch/core.launch.py'
            )
        ]),
        launch_arguments={
            'robot_name': robot,
            'use_cloud': use_cloud,
        }.items()
    )

    # ─── Ron-specific: UGV02 base controller ───
    ugv02_controller_node = Node(
        package='aimee_ugv02_controller',
        executable='ugv02_controller_node',
        name='ugv02_controller',
        output='screen',
        parameters=[{
            'serial_port': '/dev/ttyACM0',
            'baud_rate': 115200,
            'publish_tf': True,
        }],
        condition=IfCondition(is_ron)
    )

    # ─── Ron-specific: Arm controller ───
    # NOTE: aimee_manipulation contains arm_controller_node and pick_place_server.
    # If you need a dedicated RoArm-M3 HTTP driver, aimee_lerobot_bridge has
    # roarm_m3_http_driver as well.
    arm_controller_node = Node(
        package='aimee_manipulation',
        executable='arm_controller_node',
        name='arm_controller',
        output='screen',
        parameters=[{
            'simulation_mode': False,
            'arm_type': 'roarm_m3',
        }],
        condition=IfCondition(PythonExpression(["'", use_arm, "' == 'true' and '", robot, "' == 'ron'"]))
    )

    pick_place_server = Node(
        package='aimee_manipulation',
        executable='pick_place_server',
        name='pick_place_server',
        output='screen',
        parameters=[{
            'default_timeout': 30.0,
        }],
        condition=IfCondition(PythonExpression(["'", use_arm, "' == 'true' and '", robot, "' == 'ron'"]))
    )

    # ─── Wren-specific: Wave Rover controller ───
    # TODO: Add wave_rover_controller_node when aimee_wave_rover package is available.
    # For now, Wren launches only the core stack.

    # ─── Vision Pipeline ───
    vision_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                os.getenv('AIMEE_ROBOT_WS', '/workspace'),
                'src/aimee_bringup/launch/vision_pipeline.launch.py'
            )
        ]),
        condition=IfCondition(use_vision)
    )

    return LaunchDescription([
        LogInfo(msg=["Starting Aimee robot.launch.py for robot: ", robot]),
        robot_arg,
        use_cloud_arg,
        use_vision_arg,
        use_arm_arg,
        core_launch,
        ugv02_controller_node,
        arm_controller_node,
        pick_place_server,
        vision_launch,
    ])

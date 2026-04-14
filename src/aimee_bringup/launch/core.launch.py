#!/usr/bin/env python3
"""
Core launch file for Aimee Robot
Launches essential infrastructure nodes
"""

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.conditions import IfCondition


def generate_launch_description():
    # Launch arguments
    robot_name_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='ron',
        description='Robot name (ron or wren)'
    )
    
    config_path_arg = DeclareLaunchArgument(
        'config_path',
        default_value=os.path.join(
            os.getenv('AIMEE_ROBOT_WS', '~/aimee-robot-ws'),
            'config'
        ),
        description='Path to configuration files'
    )
    
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time'
    )
    
    enable_camera_arg = DeclareLaunchArgument(
        'enable_camera',
        default_value='true',
        description='Enable OBSBOT camera'
    )
    
    # Get launch configurations
    robot_name = LaunchConfiguration('robot_name')
    config_path = LaunchConfiguration('config_path')
    use_sim_time = LaunchConfiguration('use_sim_time')
    enable_camera = LaunchConfiguration('enable_camera')
    
    # Set environment variables
    set_ros_domain_id = SetEnvironmentVariable(
        'ROS_DOMAIN_ID',
        '42'  # Unique domain for Aimee robots
    )
    
    # === Voice Pipeline Nodes ===
    
    # Voice Manager Node (Continuous STT - no wake word)
    voice_manager_node = Node(
        package='aimee_voice_manager',
        executable='voice_manager_node',
        name='voice_manager',
        output='screen',
        parameters=[{
            'engine': 'vosk',
            'model_path': '/home/arduino/vosk-models/vosk-model-small-en-us-0.15',
            'sample_rate': 16000,
            'audio_device': 'plughw:2,0',
            'publish_partials': True,
            'enabled': True,
        }]
    )
    
    # TTS Node
    tts_node = Node(
        package='aimee_tts',
        executable='tts_node',
        name='tts',
        output='screen',
        parameters=[{
            'default_engine': 'gtts',
            'fallback_engine': 'pyttsx3',
            'auto_fallback': True,
            'volume': 1.0,
        }]
    )
    
    # === Intelligence Nodes ===
    
    # LLM Server Node (Action Server)
    llm_server_node = Node(
        package='aimee_llm_server',
        executable='llm_server_node',
        name='llm_server',
        output='screen',
        parameters=[{
            'backend': 'llama_cpp_server',
            'server_url': 'http://localhost:8080',
            'default_max_tokens': 150,
            'default_temperature': 0.7,
        }]
    )
    
    # Intent Router Node
    intent_router_node = Node(
        package='aimee_intent_router',
        executable='intent_router_node',
        name='intent_router',
        output='screen',
        parameters=[{
            'confidence_threshold': 0.6,
            'enable_conversation_mode': True,
            'fallback_to_chat': True,
        }]
    )
    
    # Skill Manager Node
    skill_manager_node = Node(
        package='aimee_skill_manager',
        executable='skill_manager_node',
        name='skill_manager',
        output='screen',
        parameters=[{
            'default_timeout': 30.0,
            'enable_safety_checks': True,
        }]
    )
    
    # === Vision Nodes ===
    
    # OBSBOT SDK Control Node (PTZ/Tracking only)
    obsbot_node = Node(
        package='aimee_vision_obsbot',
        executable='obsbot_node',
        name='obsbot_camera',
        output='screen',
        parameters=[{
            'host': '192.168.5.1',
            'osc_send_port': 16284,
            'control_mode': 'auto',
            'auto_reconnect': True,
            'tracking_sensitivity': 0.5,
            'enabled': True,
        }],
        condition=IfCondition(enable_camera)
    )
    
    # USB Camera Node (dedicated video streaming)
    usb_cam_node = Node(
        package='usb_cam',
        executable='usb_cam_node_exe',
        name='usb_camera',
        output='screen',
        parameters=[{
            'video_device': '/dev/video2',
            'frame_id': 'obsbot_camera',
            'camera_name': 'obsbot_camera',
            'image_width': 1280,
            'image_height': 720,
            'pixel_format': 'mjpeg2rgb',
            'io_method': 'mmap',
            'framerate': 30.0,
        }],
        remappings=[
            ('/image_raw', '/camera/image_raw'),
            ('/camera_info', '/camera/camera_info'),
        ],
        condition=IfCondition(enable_camera)
    )
    
    return LaunchDescription([
        # Arguments
        robot_name_arg,
        config_path_arg,
        use_sim_time_arg,
        enable_camera_arg,
        
        # Environment
        set_ros_domain_id,
        
        # Voice Pipeline
        voice_manager_node,
        tts_node,
        
        # Intelligence
        llm_server_node,
        intent_router_node,
        skill_manager_node,
        
        # Vision
        obsbot_node,
        usb_cam_node,
    ])

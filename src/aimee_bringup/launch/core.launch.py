#!/usr/bin/env python3
"""
Core launch file for Aimee Robot
Launches essential infrastructure nodes
"""

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, ExecuteProcess
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
    
    # Get launch configurations
    robot_name = LaunchConfiguration('robot_name')
    config_path = LaunchConfiguration('config_path')
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    # Set environment variables
    set_ros_domain_id = SetEnvironmentVariable(
        'ROS_DOMAIN_ID',
        '42'  # Unique domain for Aimee robots
    )
    set_pacific_tz = SetEnvironmentVariable(
        'TZ',
        'America/Los_Angeles'
    )
    
    # Ensure container timezone is Pacific (container has no persistent RTC)
    set_container_timezone = ExecuteProcess(
        cmd=[
            'bash', '-c',
            'rm -f /etc/localtime && ln -s /usr/share/zoneinfo/America/Los_Angeles /etc/localtime && echo America/Los_Angeles > /etc/timezone'
        ],
        name='set_pacific_timezone',
        output='log'
    )
    
    # === Vision Pipeline Nodes ===
    
    # USB Camera Node (OBSBOT video streaming)
    usb_camera_node = Node(
        package='usb_cam',
        executable='usb_cam_node_exe',
        name='usb_camera',
        output='screen',
        parameters=[{
            'video_device': '/dev/video2',
            'image_width': 1280,
            'image_height': 720,
            'pixel_format': 'mjpeg2rgb',
            'io_method': 'mmap',
            'camera_name': 'usb_camera',
        }],
        remappings=[('image_raw', '/camera/image_raw')]
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
            'audio_device': 'default',
            'publish_partials': True,
            'energy_threshold': 45.0,
            'enabled': True,
            'whisper_enabled': True,
            'whisper_api_base_url': 'https://api.lemonfox.ai/v1/audio/transcriptions',
            'whisper_api_key': os.getenv('LEMONFOX_API_KEY', ''),
            'default_voice': 'sarah',
        }]
    )
    
    # TTS Node
    tts_node = Node(
        package='aimee_tts',
        executable='tts_node',
        name='tts',
        output='screen',
        parameters=[{
            'default_engine': 'lemonfox',
            'fallback_engine': 'gtts',
            'auto_fallback': True,
            'default_voice': 'sarah',
            'lemonfox_api_key': os.getenv('LEMONFOX_API_KEY', ''),
            'lemonfox_api_base_url': 'https://api.lemonfox.ai/v1',
            'volume': 1.0,
        }]
    )
    
    # ROS2 Monitor Node (Web Dashboard)
    monitor_node = Node(
        package='aimee_ros2_monitor',
        executable='monitor_node',
        name='ros2_monitor',
        output='screen',
    )
    
    # === Intelligence Nodes ===
    
    # Local LLM Backend (llama.cpp server)
    llm_backend = ExecuteProcess(
        cmd=[
            'bash', '-c',
            'export LD_LIBRARY_PATH=/workspace/lib:$LD_LIBRARY_PATH && /workspace/lib/llama-server --host 127.0.0.1 --port 8080 -m /workspace/models/Qwen2.5-0.5B-Instruct-Q4_K_M.gguf --ctx-size 2048'
        ],
        name='llm_backend',
        output='screen',
    )
    
    # LLM Server Node (Action Server)
    llm_server_node = Node(
        package='aimee_llm_server',
        executable='llm_server_node',
        name='llm_server',
        output='screen',
        parameters=[{
            'backend': 'llama_cpp_server',
            'server_url': 'http://127.0.0.1:8080',
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
            'intent_config_path': '/workspace/config/aimee_intent_config.json',
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
    
    # AimeeCloud Client (ACC) Node
    aimee_cloud_client_node = Node(
        package='aimee_cloud_bridge',
        executable='cloud_bridge_node',
        name='aimee_cloud_client',
        output='screen',
        parameters=[os.path.join(
            os.getenv('AIMEE_ROBOT_WS', '/home/arduino/aimee-robot-ws'),
            'src/aimee_cloud_bridge/config/cloud_bridge.yaml'
        )]
    )
    
    return LaunchDescription([
        # Arguments
        robot_name_arg,
        config_path_arg,
        use_sim_time_arg,
        
        # Environment
        set_ros_domain_id,
        set_pacific_tz,
        set_container_timezone,
        
        # Vision Pipeline
        usb_camera_node,
        
        # Voice Pipeline
        voice_manager_node,
        tts_node,
        
        # Monitor
        monitor_node,
        
        # Intelligence
        llm_backend,
        llm_server_node,
        intent_router_node,
        skill_manager_node,
        aimee_cloud_client_node,
    ])

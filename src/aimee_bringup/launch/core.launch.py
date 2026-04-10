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
    
    # Core nodes (to be implemented in subsequent phases)
    
    # Voice Manager Node
    voice_manager_node = Node(
        package='aimee_voice',
        executable='voice_manager',
        name='voice_manager',
        output='screen',
        parameters=[{
            'robot_name': robot_name,
            'use_sim_time': use_sim_time,
            'wake_word_model': os.getenv('EI_MODEL_PATH', ''),
            'vosk_server_url': 'http://localhost:5000',
        }],
        condition=None  # Always launch
    )
    
    # Intent Router Node
    intent_router_node = Node(
        package='aimee_intent',
        executable='intent_router',
        name='intent_router',
        output='screen',
        parameters=[{
            'robot_name': robot_name,
            'use_sim_time': use_sim_time,
            'skills_config': os.path.join(config_path, 'skills_config.yaml'),
        }]
    )
    
    # Memory Manager Node
    memory_manager_node = Node(
        package='aimee_memory',
        executable='memory_manager',
        name='memory_manager',
        output='screen',
        parameters=[{
            'robot_name': robot_name,
            'use_sim_time': use_sim_time,
            'db_path': os.path.join(config_path, 'user_memory.db'),
        }]
    )
    
    # LLM Action Server Node
    llm_action_server_node = Node(
        package='aimee_intent',
        executable='llm_action_server',
        name='llm_action_server',
        output='screen',
        parameters=[{
            'model': 'Qwen2.5-0.5B-Instruct-Q4_K_M.gguf',
            'host': 'localhost',
            'port': 8080,
        }]
    )
    
    return LaunchDescription([
        # Arguments
        robot_name_arg,
        config_path_arg,
        use_sim_time_arg,
        
        # Environment
        set_ros_domain_id,
        
        # Core Infrastructure Nodes
        # Note: These nodes will be available once their packages are built
        # voice_manager_node,
        # intent_router_node,
        # memory_manager_node,
        # llm_action_server_node,
    ])

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import launch.conditions

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    run_explore = LaunchConfiguration('run_explore')

    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )

    declare_run_explore = DeclareLaunchArgument(
        'run_explore',
        default_value='false',
        description='Whether to run the explore node'
    )

    nav_node = Node(
        package='aimee_nav',
        executable='minnie_nav_node.py',
        name='minnie_nav_node',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}]
    )

    slam_node = Node(
        package='aimee_nav',
        executable='minnie_slam_node.py',
        name='minnie_slam_node',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}]
    )

    explore_node = Node(
        package='aimee_nav',
        executable='minnie_explore_node.py',
        name='minnie_explore_node',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        condition=launch.conditions.IfCondition(run_explore)
    )

    return LaunchDescription([
        declare_use_sim_time,
        declare_run_explore,
        nav_node,
        slam_node,
        explore_node
    ])

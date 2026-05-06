#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    orbbec_launch_dir = os.path.join(get_package_share_directory('orbbec_camera'), 'launch')
    
    # 1. Orbbec Node for Depth & IR ONLY (Astra Pro crashes if color is initialized via OpenNI)
    orbbec_depth_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(orbbec_launch_dir, 'astra.launch.py')),
        launch_arguments={
            'camera_name': 'camera',
            'enable_color': 'false', # Critical for Astra Pro!
            'depth_fps': '30',       # Default 10fps fails on Astra Pro
            'enable_ir': 'false',
            'enable_point_cloud': 'false',
            'depth_registration': 'true'
        }.items(),
    )
    
    # 2. USB Cam Node for RGB Color (Astra Pro exposes color via standard UVC)
    usb_cam_node = Node(
        package='usb_cam',
        executable='usb_cam_node_exe',
        name='camera_color',
        namespace='camera/color',
        parameters=[{
            'video_device': '/dev/video0',
            'framerate': 30.0,
            'image_width': 640,
            'image_height': 480,
            'pixel_format': 'yuyv',
            'camera_frame_id': 'camera_color_frame'
        }],
        output='screen'
    )
    
    return LaunchDescription([
        orbbec_depth_node,
        usb_cam_node
    ])

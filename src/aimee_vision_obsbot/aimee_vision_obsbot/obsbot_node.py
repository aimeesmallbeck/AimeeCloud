#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
ROS2 Node for OBSBOT Camera Control

This node wraps the ObsbotBrick and provides ROS2 interfaces:
- Subscribes to /camera/tracking_command for AI tracking
- Subscribes to /camera/ptz_command for manual PTZ
- Publishes camera status on /camera/status

Usage:
    ros2 run aimee_vision_obsbot obsbot_node
"""

import asyncio
import logging
import os
import subprocess
import sys
import tempfile
import threading
import time
from typing import Optional

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from rcl_interfaces.msg import SetParametersResult
from sensor_msgs.msg import CompressedImage, Image
from std_msgs.msg import String, Bool, Header
from geometry_msgs.msg import Twist

from aimee_msgs.msg import TrackingCommand, CameraAction, RobotState
from aimee_msgs.srv import CaptureSnapshot

from aimee_vision_obsbot.brick.obsbot_brick import (
    ObsbotBrick, ObsbotStatus, TrackingMode
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ObsbotNode(Node):
    """
    ROS2 Node for OBSBOT Camera Control.
    
    This node:
    - Controls PTZ (Pan/Tilt/Zoom)
    - Manages AI tracking modes
    - Handles presets
    - Publishes camera status
    """
    
    def __init__(self):
        super().__init__('obsbot_camera')
        
        # Declare parameters
        self.declare_parameters(namespace='', parameters=[
            ('host', '192.168.5.1'),
            ('osc_send_port', 16284),
            ('osc_recv_port', 9000),
            ('control_mode', 'auto'),
            ('auto_reconnect', True),
            ('tracking_sensitivity', 0.5),
            ('default_tracking_mode', 'normal'),
            ('enabled', True),
            ('debug', False),
            ('video_device', '/dev/video2'),
            ('snapshot_default_resolution', '640x480'),
        ])
        
        # Get parameters
        host = self.get_parameter('host').value
        osc_send_port = self.get_parameter('osc_send_port').value
        osc_recv_port = self.get_parameter('osc_recv_port').value
        control_mode = self.get_parameter('control_mode').value
        auto_reconnect = self.get_parameter('auto_reconnect').value
        tracking_sensitivity = self.get_parameter('tracking_sensitivity').value
        default_tracking_mode = self.get_parameter('default_tracking_mode').value
        self._enabled = self.get_parameter('enabled').value
        debug = self.get_parameter('debug').value
        self._video_device = self.get_parameter('video_device').value
        self._snapshot_default_resolution = self.get_parameter('snapshot_default_resolution').value
        
        # Setup QoS
        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        
        # Publishers
        self._status_pub = self.create_publisher(
            String, '/camera/status', reliable_qos
        )
        self._connected_pub = self.create_publisher(
            Bool, '/camera/connected', reliable_qos
        )
        self._tracking_mode_pub = self.create_publisher(
            String, '/camera/tracking_mode', reliable_qos
        )
        self._robot_state_pub = self.create_publisher(
            RobotState, '/robot/state', reliable_qos
        )
        
        # Subscribers
        self._ptz_sub = self.create_subscription(
            Twist,
            '/camera/cmd_ptz',
            self._on_ptz_command,
            10
        )
        
        self._tracking_sub = self.create_subscription(
            TrackingCommand,
            '/camera/tracking',
            self._on_tracking_command,
            10
        )
        
        self._action_sub = self.create_subscription(
            CameraAction,
            '/camera/action',
            self._on_camera_action,
            10
        )
        
        self._control_sub = self.create_subscription(
            String,
            '/camera/control',
            self._on_control_command,
            10
        )
        
        # Snapshot service
        self._snapshot_srv = self.create_service(
            CaptureSnapshot,
            '/camera/capture_snapshot',
            self._on_capture_snapshot
        )
        
        # Subscribe to streaming camera feed for zero-contention snapshots
        self._latest_frame: Optional[Image] = None
        self._latest_frame_lock = threading.Lock()
        self._frame_count = 0
        self._image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self._on_camera_image,
            1  # Keep only latest frame to minimize memory
        )
        
        # Parameter callback
        self.add_on_set_parameters_callback(self._on_parameters_changed)
        
        # Create the brick with SDK path
        self._brick = ObsbotBrick(
            sdk_path="/workspace/libdev_v2.1.0_8/linux/arm64-release/libdev.so",
            auto_reconnect=auto_reconnect,
            tracking_sensitivity=tracking_sensitivity,
            debug=debug
        )
        
        # Register callbacks
        self._brick.on_status_change(self._on_status_change)
        self._brick.on_tracking_update(self._on_tracking_update)
        
        # Async handling
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._shutdown_event = threading.Event()
        
        # State
        self._initialized = False
        self._current_status: Optional[ObsbotStatus] = None
        
        # Status publishing timer
        self._status_timer = self.create_timer(1.0, self._publish_status)
        
        self.get_logger().info(
            f"ObsbotNode initialized:\n"
            f"  Host: {host}:{osc_send_port}\n"
            f"  Control mode: {control_mode}\n"
            f"  Auto reconnect: {auto_reconnect}"
        )
        
        # Start async thread
        self._start_async_thread()
    
    def _start_async_thread(self):
        """Start async event loop in background thread."""
        def run_async_loop():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            
            try:
                self._loop.run_until_complete(self._async_main())
            except Exception as e:
                self.get_logger().error(f"Async loop error: {e}")
            finally:
                self._loop.close()
        
        self._thread = threading.Thread(target=run_async_loop, daemon=True)
        self._thread.start()
    
    async def _async_main(self):
        """Main async coroutine."""
        try:
            await self._brick.initialize()
            self._initialized = True
            self.get_logger().info("Brick initialized successfully")
            
            # Wake camera to ensure PTZ commands work
            if self._brick.is_connected():
                self.get_logger().info("Waking up camera...")
                loop = asyncio.get_running_loop()
                await loop.run_in_executor(None, self._brick.wake_up)
                self.get_logger().info("Camera wake-up complete")
            
            # Keep running with periodic wake-up to prevent sleep
            while not self._shutdown_event.is_set():
                await asyncio.sleep(60.0)
                if self._brick.is_connected() and self._enabled:
                    loop = asyncio.get_running_loop()
                    await loop.run_in_executor(None, self._brick.wake_up)
                    
        except Exception as e:
            self.get_logger().error(f"Async main error: {e}")
    
    # === Command Handlers ===
    
    def _on_ptz_command(self, msg: Twist):
        """
        Handle PTZ movement command.
        
        Twist message mapping:
        - angular.z: Pan (positive=left, negative=right)
        - angular.y: Tilt (positive=up, negative=down)
        - linear.z: Zoom (positive=in, negative=out)
        """
        if not self._enabled or not self._initialized:
            self.get_logger().debug(f"PTZ ignored: enabled={self._enabled}, initialized={self._initialized}")
            return
        
        pan_speed = int(abs(msg.angular.z) * 100)
        tilt_speed = int(abs(msg.angular.y) * 100)
        zoom_step = int(msg.linear.z * 10)
        
        # Stop gimbal if all values are zero (e.g. stop command from UI)
        if pan_speed <= 5 and tilt_speed <= 5 and zoom_step == 0:
            self.get_logger().debug("Stopping gimbal")
            threading.Thread(target=self._brick.stop_gimbal, daemon=True).start()
            return
        
        def _execute_ptz():
            if pan_speed > 5:
                if msg.angular.z > 0:
                    self._brick.gimbal_left(pan_speed)
                else:
                    self._brick.gimbal_right(pan_speed)
            
            if tilt_speed > 5:
                if msg.angular.y > 0:
                    self._brick.gimbal_up(tilt_speed)
                else:
                    self._brick.gimbal_down(tilt_speed)
            
            if zoom_step != 0:
                if zoom_step > 0:
                    self._brick.zoom_in(zoom_step)
                else:
                    self._brick.zoom_out(abs(zoom_step))
        
        threading.Thread(target=_execute_ptz, daemon=True).start()
    
    def _on_tracking_command(self, msg: TrackingCommand):
        """Handle AI tracking command."""
        if not self._enabled or not self._initialized:
            return
        
        command = msg.command
        
        if command == 'start':
            mode = self._tracking_mode_from_string(msg.mode)
            self._brick.enable_tracking(mode)
            self.get_logger().info(f"Tracking enabled: {mode.name}")
        elif command == 'stop':
            self._brick.disable_tracking()
            self.get_logger().info("Tracking disabled")
        elif command == 'preset':
            self._brick.recall_preset(msg.preset_id)
            self.get_logger().info(f"Recalled preset {msg.preset_id}")
        elif command == 'zoom':
            self._brick.set_zoom(msg.zoom_level)
            self.get_logger().info(f"Zoom set to {msg.zoom_level}")
    
    def _on_camera_action(self, msg: CameraAction):
        """Handle camera action from skill execution."""
        if not self._enabled or not self._initialized:
            return
        
        action = msg.action_type
        
        if action == 'save_preset':
            # Map confidence to preset_id for this message type
            preset_id = int(msg.confidence)
            self._brick.save_preset(preset_id)
            self.get_logger().info(f"Saved preset {preset_id}")
            
        elif action == 'recall_preset':
            preset_id = int(msg.confidence)
            self._brick.recall_preset(preset_id)
            self.get_logger().info(f"Recalled preset {preset_id}")
            
        elif action == 'sleep':
            self._brick.sleep()
            self.get_logger().info("Camera sleeping")
            
        elif action == 'wake':
            self._brick.wake_up()
            self.get_logger().info("Camera waking up")
    
    def _on_control_command(self, msg: String):
        """Handle control commands."""
        command = msg.data.lower().strip()
        self.get_logger().info(f"Received control command: {command}")
        
        if command == 'start':
            self._enabled = True
        elif command == 'stop':
            self._enabled = False
        elif command == 'status':
            self._publish_status()
        elif command == 'reconnect':
            if self._loop:
                asyncio.run_coroutine_threadsafe(
                    self._brick.initialize(), self._loop
                )
    
    # === Callback Handlers ===
    
    def _on_status_change(self, status: ObsbotStatus):
        """Handle brick status change."""
        self._current_status = status
        
        # Publish connection status
        connected_msg = Bool()
        connected_msg.data = status.connected
        self._connected_pub.publish(connected_msg)
        
        if status.error_message:
            self.get_logger().error(f"Camera error: {status.error_message}")
    
    def _on_tracking_update(self, mode: TrackingMode):
        """Handle tracking mode update."""
        mode_msg = String()
        mode_msg.data = mode.name.lower()
        self._tracking_mode_pub.publish(mode_msg)
    
    # === Publishing ===
    
    def _publish_status(self):
        """Publish camera status."""
        if not self._current_status:
            return
        
        status = self._current_status
        status_str = (
            f"connected={status.connected}, "
            f"tracking={status.tracking_mode.name}, "
            f"zoom={status.zoom_level}, "
            f"sleeping={status.is_sleeping}"
        )
        
        msg = String()
        msg.data = status_str
        self._status_pub.publish(msg)
    
    # === Utilities ===
    
    def _tracking_mode_from_string(self, mode_str: str) -> TrackingMode:
        """Convert string to TrackingMode enum."""
        mode_map = {
            'normal': TrackingMode.NORMAL,
            'upper_body': TrackingMode.UPPER_BODY,
            'closeup': TrackingMode.CLOSEUP,
            'headless': TrackingMode.HEADLESS,
            'desk': TrackingMode.DESK,
            'whiteboard': TrackingMode.WHITEBOARD,
            'hand': TrackingMode.HAND,
            'group': TrackingMode.GROUP,
        }
        return mode_map.get(mode_str.lower(), TrackingMode.NORMAL)
    
    def _on_parameters_changed(self, params):
        """Handle parameter changes."""
        results = []
        
        for param in params:
            if param.name == 'enabled':
                self._enabled = param.value
                self.get_logger().info(f"Updated enabled: {param.value}")
                results.append(SetParametersResult(successful=True))
                
            elif param.name == 'tracking_sensitivity':
                self._brick.tracking_sensitivity = param.value
                self.get_logger().info(f"Updated sensitivity: {param.value}")
                results.append(SetParametersResult(successful=True))
                
            elif param.name == 'video_device':
                self._video_device = param.value
                self.get_logger().info(f"Updated video device: {param.value}")
                results.append(SetParametersResult(successful=True))
                
            elif param.name == 'snapshot_default_resolution':
                self._snapshot_default_resolution = param.value
                self.get_logger().info(f"Updated snapshot resolution: {param.value}")
                results.append(SetParametersResult(successful=True))
                
            else:
                results.append(SetParametersResult(
                    successful=False,
                    reason=f"Parameter {param.name} requires restart"
                ))
        
        return results
    
    # === Snapshot Service ===
    
    def _on_camera_image(self, msg: Image):
        """Buffer the latest camera frame for zero-contention snapshots."""
        with self._latest_frame_lock:
            self._latest_frame = msg
            self._frame_count += 1

    def _encode_frame_to_jpeg(self, img: Image, quality: int) -> Optional[bytes]:
        """Convert a sensor_msgs/Image to JPEG bytes using OpenCV."""
        try:
            import cv2
            import numpy as np
        except ImportError:
            self.get_logger().warning("OpenCV not available for frame encoding")
            return None

        try:
            # Convert raw bytes to numpy array
            arr = np.frombuffer(img.data, dtype=np.uint8)

            # Handle different encodings
            if img.encoding in ('rgb8', 'bgr8'):
                expected_size = img.height * img.width * 3
                if len(arr) != expected_size:
                    self.get_logger().warning(
                        f"Frame size mismatch: got {len(arr)}, expected {expected_size}"
                    )
                    return None
                arr = arr.reshape((img.height, img.width, 3))
                if img.encoding == 'rgb8':
                    arr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
            elif img.encoding in ('rgba8', 'bgra8'):
                expected_size = img.height * img.width * 4
                if len(arr) != expected_size:
                    return None
                arr = arr.reshape((img.height, img.width, 4))
                if img.encoding == 'rgba8':
                    arr = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
                else:
                    arr = cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR)
            elif img.encoding == 'mono8':
                expected_size = img.height * img.width
                if len(arr) != expected_size:
                    return None
                arr = arr.reshape((img.height, img.width))
            else:
                self.get_logger().warning(f"Unsupported image encoding: {img.encoding}")
                return None

            # Encode to JPEG
            quality = max(1, min(100, quality))
            encode_params = [cv2.IMWRITE_JPEG_QUALITY, quality]
            success, encoded = cv2.imencode('.jpg', arr, encode_params)
            if success:
                return encoded.tobytes()
            else:
                self.get_logger().warning("cv2.imencode failed")
                return None
        except Exception as e:
            self.get_logger().warning(f"Frame encoding error: {e}")
            return None

    def _capture_via_v4l2(self, video_size: str, output_path: str) -> bytes:
        """Capture a frame directly from V4L2 device (fallback)."""
        image_data = b''
        width, height = video_size.split('x')
        cmd_v4l2 = [
            'v4l2-ctl', '--device', self._video_device,
            '--set-fmt-video', f'width={width},height={height},pixelformat=MJPG',
            '--stream-mmap', '--stream-to', output_path, '--stream-count', '1'
        ]
        result_v4l2 = subprocess.run(
            cmd_v4l2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10
        )
        if result_v4l2.returncode == 0:
            with open(output_path, 'rb') as f:
                image_data = f.read()
        else:
            err_v4l2 = result_v4l2.stderr.decode('utf-8', errors='replace').strip()
            self.get_logger().warning(f"v4l2-ctl failed: {err_v4l2}")
        return image_data

    def _capture_via_ffmpeg(self, video_size: str, output_path: str, qv: int) -> bytes:
        """Capture a frame via ffmpeg (last resort fallback)."""
        cmd = [
            'ffmpeg', '-y',
            '-f', 'v4l2',
            '-input_format', 'mjpeg',
            '-video_size', video_size,
            '-i', self._video_device,
            '-frames:v', '1',
            '-q:v', str(qv),
            output_path,
        ]
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=15
        )
        if result.returncode != 0:
            stderr = result.stderr.decode('utf-8', errors='replace')
            self.get_logger().error(f"ffmpeg failed: {stderr}")
            raise RuntimeError(stderr)
        with open(output_path, 'rb') as f:
            return f.read()

    def _on_capture_snapshot(self, request, response):
        """Handle snapshot capture request.

        Primary path: use the latest buffered frame from /camera/image_raw
        (zero V4L2 contention, instant, reliable).

        Fallback path: direct V4L2 capture via v4l2-ctl / ffmpeg
        (for when usb_cam is not running or higher resolution is needed).
        """
        resolution = request.resolution.strip().lower()
        quality = request.quality

        # Map resolution string to size
        size_map = {
            '': self._snapshot_default_resolution,
            'default': self._snapshot_default_resolution,
            '1080p': '1920x1080',
            '1920x1080': '1920x1080',
            '4k': '3840x2160',
            '2160p': '3840x2160',
            '3840x2160': '3840x2160',
            '720p': '1280x720',
            '1280x720': '1280x720',
            '480p': '640x480',
            '640x480': '640x480',
            'vga': '640x480',
        }
        video_size = size_map.get(resolution, self._snapshot_default_resolution)
        quality = max(1, min(100, quality))

        self.get_logger().info(
            f"Snapshot requested: {video_size} (quality={quality})"
        )

        # ─── Primary: buffered frame from streaming topic ───
        with self._latest_frame_lock:
            buffered_frame = self._latest_frame
            frame_count = self._frame_count

        if buffered_frame is not None:
            # Check if buffered frame resolution matches request
            req_width, req_height = video_size.split('x')
            req_width = int(req_width)
            req_height = int(req_height)

            # Use buffered frame if resolution matches or is "close enough"
            # (within 10% — streaming might be slightly different due to driver rounding)
            buf_width = buffered_frame.width
            buf_height = buffered_frame.height
            width_ok = abs(buf_width - req_width) <= max(req_width * 0.1, 16)
            height_ok = abs(buf_height - req_height) <= max(req_height * 0.1, 16)

            if width_ok and height_ok:
                self.get_logger().info(
                    f"Using buffered frame ({buf_width}x{buf_height}, "
                    f"frame_count={frame_count})"
                )
                image_data = self._encode_frame_to_jpeg(buffered_frame, quality)
                if image_data:
                    header = Header()
                    header.stamp = self.get_clock().now().to_msg()
                    header.frame_id = 'camera'
                    response.image = CompressedImage(
                        header=header,
                        format='jpeg',
                        data=image_data,
                    )
                    response.success = True
                    response.message = (
                        f"Snapshot from stream: {buf_width}x{buf_height}, "
                        f"{len(image_data)} bytes"
                    )
                    self.get_logger().info(response.message)
                    return response
                else:
                    self.get_logger().warning(
                        "Buffered frame encoding failed, falling back to V4L2"
                    )
            else:
                self.get_logger().info(
                    f"Buffered frame resolution mismatch "
                    f"({buf_width}x{buf_height} vs {video_size}), "
                    f"falling back to V4L2"
                )
        else:
            self.get_logger().info(
                "No buffered frame available (usb_cam may not be running), "
                "falling back to V4L2"
            )

        # ─── Fallback: direct V4L2 capture ───
        with tempfile.NamedTemporaryFile(
            suffix='.jpg', prefix='obsbot_snapshot_', delete=False
        ) as tmp:
            output_path = tmp.name

        try:
            image_data = b''

            # Try v4l2-ctl first
            image_data = self._capture_via_v4l2(video_size, output_path)

            # Fallback to ffmpeg
            if not image_data:
                qv = max(1, min(31, 32 - quality // 3))
                image_data = self._capture_via_ffmpeg(video_size, output_path, qv)

            if not image_data:
                response.success = False
                response.message = "Captured image is empty"
                return response

            header = Header()
            header.stamp = self.get_clock().now().to_msg()
            header.frame_id = 'camera'

            response.image = CompressedImage(
                header=header,
                format='jpeg',
                data=image_data,
            )
            response.success = True
            response.message = (
                f"Snapshot captured (V4L2): {video_size}, "
                f"{len(image_data)} bytes"
            )
            self.get_logger().info(response.message)

        except subprocess.TimeoutExpired:
            response.success = False
            response.message = "Snapshot capture timed out (V4L2/ffmpeg >15s)"
            self.get_logger().error(response.message)

        except Exception as e:
            stderr = str(e).lower()
            if 'busy' in stderr or 'resource temporarily unavailable' in stderr:
                response.success = False
                response.message = (
                    f"Device {self._video_device} is busy. "
                    "Another process is using the camera."
                )
            else:
                response.success = False
                response.message = f"Snapshot error: {e}"
            self.get_logger().error(response.message)

        finally:
            try:
                os.unlink(output_path)
            except Exception:
                pass

        return response
    
    # === Lifecycle ===
    
    def destroy_node(self):
        """Clean shutdown."""
        self.get_logger().info("Shutting down ObsbotNode...")
        
        self._status_timer.cancel()
        
        self._shutdown_event.set()
        
        # Shutdown brick
        if self._loop and self._initialized:
            future = asyncio.run_coroutine_threadsafe(
                self._brick.shutdown(),
                self._loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as e:
                self.get_logger().error(f"Error during brick shutdown: {e}")
        
        # Stop thread
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        
        super().destroy_node()
        self.get_logger().info("Shutdown complete")


def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)
    
    node = None
    try:
        node = ObsbotNode()
        rclpy.spin(node)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        if node:
            node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

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
import sys
import threading
from typing import Optional

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from rcl_interfaces.msg import SetParametersResult
from std_msgs.msg import String, Bool
from geometry_msgs.msg import Twist

from aimee_msgs.msg import TrackingCommand, CameraAction, RobotState

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
            
            # Keep running
            while not self._shutdown_event.is_set():
                await asyncio.sleep(0.1)
                
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
            return
        
        pan_speed = int(abs(msg.angular.z) * 100)
        tilt_speed = int(abs(msg.angular.y) * 100)
        zoom_step = int(msg.linear.z * 10)
        
        # Execute commands
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
                
            else:
                results.append(SetParametersResult(
                    successful=False,
                    reason=f"Parameter {param.name} requires restart"
                ))
        
        return results
    
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

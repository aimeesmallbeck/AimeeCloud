#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
UGV02 Platform Controller Node

Controls the Waveshare UGV02 rover via JSON serial protocol.
Subscribes to /cmd_vel, publishes odometry, handles ESP32 communication.

JSON Protocol (115200 baud, 8N1):
- Move:        {"T":1,"L":0.5,"R":0.5}  (L/R wheel speeds -0.5 to 0.5)
- Velocity:    {"T":13,"X":0.25,"Z":0.3} (linear X, angular Z)
- Odometry:    {"T":130} → chassis feedback
- IMU:         {"T":126} → IMU data
- LED:         {"T":3,"R":255,"G":0,"B":0}
- Continuous:  {"T":131,"cmd":1} (enable auto-feedback for ROS)

Usage:
    ros2 run aimee_ugv02_controller ugv02_controller_node
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from geometry_msgs.msg import Twist, TransformStamped, Quaternion
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu, BatteryState
from std_msgs.msg import Float32, String, Bool
import tf2_ros
import serial
import json
import threading
import time
import math
from typing import Optional, Dict, Any


class UGV02ControllerNode(Node):
    """
    ROS2 node for UGV02 rover control via JSON serial protocol.
    
    Publishes:
        - /odom (Odometry): Wheel odometry from ESP32
        - /imu (ImU): IMU data from ESP32
        - /battery (BatteryState): Battery voltage
        - /tf (TF): odom → base_link transform
    
    Subscribes:
        - /cmd_vel (Twist): Velocity commands
    """

    # Command types
    CMD_SPEED_CTRL = 1       # Direct wheel speed control
    CMD_VELOCITY = 13        # Linear/angular velocity
    CMD_ODOMETRY = 130       # Get chassis feedback
    CMD_CONTINUOUS_FEEDBACK = 131  # Enable/disable continuous feedback
    CMD_IMU = 126            # Get IMU data
    CMD_LED = 3              # LED control
    CMD_OLED = 3             # OLED display (lineNum, Text)
    CMD_ECHO = 143           # Echo switch

    def __init__(self):
        super().__init__('ugv02_controller')

        # Declare parameters
        self.declare_parameters(namespace='', parameters=[
            ('serial_port', '/dev/ttyACM0'),
            ('baud_rate', 115200),
            ('timeout', 1.0),
            ('base_frame', 'base_link'),
            ('odom_frame', 'odom'),
            ('wheel_separation', 0.23),    # meters (distance between wheels)
            ('wheel_radius', 0.04),        # meters
            ('max_speed', 0.5),            # m/s
            ('cmd_timeout', 0.5),          # seconds before stopping
            ('heartbeat_interval', 0.1),   # seconds between heartbeat commands
            ('continuous_feedback', True), # Enable ESP32 continuous feedback
            ('publish_tf', True),
            ('linear_scale', 1.0),         # Scale factor for linear velocity
            ('angular_scale', 1.0),        # Scale factor for angular velocity
        ])

        # Get parameters
        self._serial_port = self.get_parameter('serial_port').value
        self._baud_rate = self.get_parameter('baud_rate').value
        self._timeout = self.get_parameter('timeout').value
        self._base_frame = self.get_parameter('base_frame').value
        self._odom_frame = self.get_parameter('odom_frame').value
        self._wheel_sep = self.get_parameter('wheel_separation').value
        self._wheel_radius = self.get_parameter('wheel_radius').value
        self._max_speed = self.get_parameter('max_speed').value
        self._cmd_timeout = self.get_parameter('cmd_timeout').value
        self._heartbeat_interval = self.get_parameter('heartbeat_interval').value
        self._continuous_feedback = self.get_parameter('continuous_feedback').value
        self._publish_tf = self.get_parameter('publish_tf').value
        self._linear_scale = self.get_parameter('linear_scale').value
        self._angular_scale = self.get_parameter('angular_scale').value

        # Setup QoS
        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        odom_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        # Publishers
        self._odom_pub = self.create_publisher(Odometry, '/odom', odom_qos)
        self._imu_pub = self.create_publisher(Imu, '/imu', odom_qos)
        self._battery_pub = self.create_publisher(BatteryState, '/battery', reliable_qos)
        self._status_pub = self.create_publisher(String, '/ugv02/status', reliable_qos)

        # TF broadcaster
        if self._publish_tf:
            self._tf_broadcaster = tf2_ros.TransformBroadcaster(self)

        # Subscribers
        self._cmd_vel_sub = self.create_subscription(
            Twist, '/cmd_vel', self._on_cmd_vel, 10
        )

        # Serial connection
        self._serial: Optional[serial.Serial] = None
        self._serial_lock = threading.Lock()

        # State
        self._connected = False
        self._last_cmd_time = time.time()
        self._last_linear = 0.0
        self._last_angular = 0.0
        self._cmd_vel_active = False

        # Odometry state
        self._x = 0.0
        self._y = 0.0
        self._theta = 0.0
        self._vx = 0.0
        self._vth = 0.0
        self._last_odom_time = time.time()

        # Serial read thread
        self._read_thread: Optional[threading.Thread] = None
        self._running = False

        # Timers
        self._heartbeat_timer = None
        self._watchdog_timer = None

        # Connect to serial
        self._connect_serial()

        if self._connected:
            # Enable continuous feedback if requested
            if self._continuous_feedback:
                self._enable_continuous_feedback(True)
            
            # Start timers
            self._heartbeat_timer = self.create_timer(
                self._heartbeat_interval, self._heartbeat_callback
            )
            self._watchdog_timer = self.create_timer(
                0.1, self._watchdog_callback
            )

        self.get_logger().info(
            f"UGV02 Controller initialized:\n"
            f"  Serial: {self._serial_port} @ {self._baud_rate} baud\n"
            f"  Base frame: {self._base_frame}\n"
            f"  Odom frame: {self._odom_frame}\n"
            f"  Max speed: {self._max_speed} m/s\n"
            f"  Connected: {self._connected}"
        )

    def _connect_serial(self) -> bool:
        """Connect to the ESP32 via serial."""
        try:
            self._serial = serial.Serial(
                port=self._serial_port,
                baudrate=self._baud_rate,
                timeout=self._timeout,
                dsrdtr=None
            )
            self._serial.setRTS(False)
            self._serial.setDTR(False)
            
            # Clear buffers
            self._serial.reset_input_buffer()
            self._serial.reset_output_buffer()
            
            self._connected = True
            
            # Start read thread
            self._running = True
            self._read_thread = threading.Thread(target=self._serial_read_loop)
            self._read_thread.daemon = True
            self._read_thread.start()
            
            self.get_logger().info(f"Connected to {self._serial_port}")
            return True
            
        except serial.SerialException as e:
            self.get_logger().error(f"Failed to connect to {self._serial_port}: {e}")
            self._connected = False
            return False

    def _serial_read_loop(self):
        """Background thread to read serial data."""
        while self._running and self._serial and self._serial.is_open:
            try:
                with self._serial_lock:
                    if self._serial.in_waiting > 0:
                        line = self._serial.readline().decode('utf-8').strip()
                        if line:
                            self._process_serial_data(line)
            except Exception as e:
                self.get_logger().debug(f"Serial read error: {e}")
            time.sleep(0.001)  # Small delay to prevent CPU spinning

    def _process_serial_data(self, data: str):
        """Process incoming JSON data from ESP32."""
        try:
            msg = json.loads(data)
            cmd_type = msg.get('T')
            
            if cmd_type == 130:  # Base feedback
                self._process_odometry(msg)
            elif cmd_type == 126:  # IMU data
                self._process_imu(msg)
            elif cmd_type == 2:  # Legacy odometry
                self._process_legacy_odometry(msg)
            else:
                # Log other messages for debugging
                self.get_logger().debug(f"Received: {data}")
                
        except json.JSONDecodeError:
            self.get_logger().debug(f"Non-JSON data: {data}")
        except Exception as e:
            self.get_logger().debug(f"Error processing data: {e}")

    def _process_odometry(self, msg: Dict[str, Any]):
        """Process odometry feedback from ESP32."""
        # Parse feedback - exact format depends on ESP32 firmware
        # Typical format: {"T":130, "L":left_speed, "R":right_speed, 
        #                  "X":x_pos, "Y":y_pos, "Z":heading}
        
        try:
            left_speed = msg.get('L', 0)  # Left wheel speed
            right_speed = msg.get('R', 0)  # Right wheel speed
            
            # Calculate robot velocities
            # v = (v_r + v_l) / 2
            # omega = (v_r - v_l) / wheel_separation
            v_left = left_speed * self._wheel_radius
            v_right = right_speed * self._wheel_radius
            
            self._vx = (v_right + v_left) / 2.0
            self._vth = (v_right - v_left) / self._wheel_sep
            
            # Update position using dead reckoning
            current_time = time.time()
            dt = current_time - self._last_odom_time
            self._last_odom_time = current_time
            
            if dt > 0:
                delta_x = self._vx * math.cos(self._theta) * dt
                delta_y = self._vx * math.sin(self._theta) * dt
                delta_th = self._vth * dt
                
                self._x += delta_x
                self._y += delta_y
                self._theta += delta_th
                
                # Normalize theta
                self._theta = math.atan2(math.sin(self._theta), math.cos(self._theta))
            
            # Publish odometry
            self._publish_odometry()
            
        except Exception as e:
            self.get_logger().debug(f"Odometry processing error: {e}")

    def _process_legacy_odometry(self, msg: Dict[str, Any]):
        """Process legacy odometry format (T=2)."""
        # Format: {"T":2,"L":100,"R":100,"X":10,"Y":5,"Z":90}
        try:
            # This appears to be encoder counts or PWM values
            # Convert to velocities if needed
            pass
        except Exception as e:
            self.get_logger().debug(f"Legacy odometry error: {e}")

    def _process_imu(self, msg: Dict[str, Any]):
        """Process IMU data from ESP32."""
        try:
            imu_msg = Imu()
            imu_msg.header.stamp = self.get_clock().now().to_msg()
            imu_msg.header.frame_id = 'imu_link'
            
            # Parse IMU data - exact fields depend on firmware
            # Typical: heading, pitch, roll, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z
            if 'heading' in msg:
                # Convert heading to quaternion (simplified - assuming 2D)
                heading_rad = math.radians(msg['heading'])
                imu_msg.orientation = self._euler_to_quaternion(0, 0, heading_rad)
            
            if 'accel_x' in msg:
                imu_msg.linear_acceleration.x = msg['accel_x']
                imu_msg.linear_acceleration.y = msg.get('accel_y', 0)
                imu_msg.linear_acceleration.z = msg.get('accel_z', 0)
            
            if 'gyro_x' in msg:
                imu_msg.angular_velocity.x = msg['gyro_x']
                imu_msg.angular_velocity.y = msg.get('gyro_y', 0)
                imu_msg.angular_velocity.z = msg.get('gyro_z', 0)
            
            self._imu_pub.publish(imu_msg)
            
        except Exception as e:
            self.get_logger().debug(f"IMU processing error: {e}")

    def _publish_odometry(self):
        """Publish odometry message and TF."""
        now = self.get_clock().now()
        
        # Odometry message
        odom = Odometry()
        odom.header.stamp = now.to_msg()
        odom.header.frame_id = self._odom_frame
        odom.child_frame_id = self._base_frame
        
        # Position
        odom.pose.pose.position.x = self._x
        odom.pose.pose.position.y = self._y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation = self._euler_to_quaternion(0, 0, self._theta)
        
        # Velocity
        odom.twist.twist.linear.x = self._vx
        odom.twist.twist.angular.z = self._vth
        
        # Covariances (set high since we don't have covariance estimates)
        odom.pose.covariance[0] = 0.1
        odom.pose.covariance[7] = 0.1
        odom.pose.covariance[35] = 0.2
        odom.twist.covariance[0] = 0.1
        odom.twist.covariance[35] = 0.1
        
        self._odom_pub.publish(odom)
        
        # Publish TF
        if self._publish_tf:
            t = TransformStamped()
            t.header.stamp = now.to_msg()
            t.header.frame_id = self._odom_frame
            t.child_frame_id = self._base_frame
            t.transform.translation.x = self._x
            t.transform.translation.y = self._y
            t.transform.translation.z = 0.0
            t.transform.rotation = odom.pose.pose.orientation
            self._tf_broadcaster.sendTransform(t)

    def _on_cmd_vel(self, msg: Twist):
        """Handle incoming velocity commands."""
        self._last_cmd_time = time.time()
        self._cmd_vel_active = True
        
        # Extract velocities
        linear_x = msg.linear.x * self._linear_scale
        angular_z = msg.angular.z * self._angular_scale
        
        # Clamp to max speed
        linear_x = max(-self._max_speed, min(self._max_speed, linear_x))
        angular_z = max(-self._max_speed, min(self._max_speed, angular_z))
        
        self._last_linear = linear_x
        self._last_angular = angular_z
        
        # Send to robot
        self._send_velocity_command(linear_x, angular_z)

    def _send_velocity_command(self, linear_x: float, angular_z: float):
        """Send velocity command to ESP32."""
        if not self._connected or not self._serial:
            return
        
        # Convert Twist to wheel speeds
        # v_left = v - (omega * wheel_sep / 2)
        # v_right = v + (omega * wheel_sep / 2)
        v_left = linear_x - (angular_z * self._wheel_sep / 2.0)
        v_right = linear_x + (angular_z * self._wheel_sep / 2.0)
        
        # Normalize to -0.5 to 0.5 range
        max_wheel_speed = max(abs(v_left), abs(v_right), self._max_speed)
        if max_wheel_speed > self._max_speed:
            scale = self._max_speed / max_wheel_speed
            v_left *= scale
            v_right *= scale
        
        # Convert to ESP32 format (-0.5 to 0.5)
        left_cmd = v_left / (self._max_speed * 2)  # Scale to -0.5 to 0.5
        right_cmd = v_right / (self._max_speed * 2)
        
        # Send command
        cmd = {"T": self.CMD_SPEED_CTRL, "L": left_cmd, "R": right_cmd}
        self._send_json(cmd)

    def _send_velocity_command_alt(self, linear_x: float, angular_z: float):
        """Alternative: Use T=13 velocity command."""
        if not self._connected or not self._serial:
            return
        
        cmd = {"T": self.CMD_VELOCITY, "X": linear_x, "Z": angular_z}
        self._send_json(cmd)

    def _send_json(self, cmd: Dict[str, Any]):
        """Send JSON command to ESP32."""
        try:
            with self._serial_lock:
                json_str = json.dumps(cmd) + '\n'
                self._serial.write(json_str.encode('utf-8'))
                self._serial.flush()
        except serial.SerialException as e:
            self.get_logger().error(f"Serial write error: {e}")
            self._connected = False

    def _enable_continuous_feedback(self, enable: bool):
        """Enable or disable continuous feedback from ESP32."""
        cmd = {"T": self.CMD_CONTINUOUS_FEEDBACK, "cmd": 1 if enable else 0}
        self._send_json(cmd)
        self.get_logger().info(f"Continuous feedback {'enabled' if enable else 'disabled'}")

    def _heartbeat_callback(self):
        """Send periodic heartbeat to keep robot moving."""
        if not self._connected:
            return
        
        # If we have an active command, resend it to prevent auto-stop
        if self._cmd_vel_active:
            self._send_velocity_command(self._last_linear, self._last_angular)

    def _watchdog_callback(self):
        """Watchdog to stop robot if no commands received."""
        if not self._connected:
            return
        
        time_since_last_cmd = time.time() - self._last_cmd_time
        
        if time_since_last_cmd > self._cmd_timeout and self._cmd_vel_active:
            self.get_logger().warn("Command timeout - stopping robot")
            self._send_velocity_command(0.0, 0.0)
            self._cmd_vel_active = False
            self._last_linear = 0.0
            self._last_angular = 0.0

    def set_led(self, r: int, g: int, b: int):
        """Set LED color."""
        cmd = {"T": self.CMD_LED, "R": r, "G": g, "B": b}
        self._send_json(cmd)

    def set_oled(self, line: int, text: str):
        """Set OLED display text."""
        cmd = {"T": self.CMD_OLED, "lineNum": line, "Text": text[:16]}  # Limit to 16 chars
        self._send_json(cmd)

    def _euler_to_quaternion(self, roll: float, pitch: float, yaw: float) -> Quaternion:
        """Convert Euler angles to quaternion."""
        cy = math.cos(yaw * 0.5)
        sy = math.sin(yaw * 0.5)
        cp = math.cos(pitch * 0.5)
        sp = math.sin(pitch * 0.5)
        cr = math.cos(roll * 0.5)
        sr = math.sin(roll * 0.5)
        
        q = Quaternion()
        q.w = cr * cp * cy + sr * sp * sy
        q.x = sr * cp * cy - cr * sp * sy
        q.y = cr * sp * cy + sr * cp * sy
        q.z = cr * cp * sy - sr * sp * cy
        
        return q

    def destroy_node(self):
        """Clean shutdown."""
        self.get_logger().info("Shutting down UGV02 controller...")
        
        self._running = False
        
        # Stop robot
        if self._connected:
            self._send_velocity_command(0.0, 0.0)
            time.sleep(0.1)
        
        # Close serial
        if self._serial and self._serial.is_open:
            self._serial.close()
        
        if self._read_thread and self._read_thread.is_alive():
            self._read_thread.join(timeout=1.0)
        
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = UGV02ControllerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Interrupted by user")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

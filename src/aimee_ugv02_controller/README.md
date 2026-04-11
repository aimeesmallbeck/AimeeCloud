# Aimee UGV02 Controller

ROS2 controller for Waveshare UGV02 rover using JSON serial protocol.

## Overview

This package provides ROS2 integration for the UGV02 6x4 off-road rover platform. It communicates with the ESP32 slave controller via JSON commands over serial UART.

## Hardware Interface

- **Connection**: Serial UART (GPIO pins or USB)
- **Baud Rate**: 115200
- **Protocol**: JSON commands
- **Default Port**: `/dev/ttyACM0`

## JSON Protocol

### Command Types

| T Value | Command | Description |
|---------|---------|-------------|
| 1 | CMD_SPEED_CTRL | Wheel speed control `{"T":1,"L":0.5,"R":0.5}` |
| 13 | CMD_VELOCITY | Linear/angular velocity `{"T":13,"X":0.25,"Z":0.3}` |
| 130 | CMD_ODOMETRY | Get chassis feedback |
| 131 | CMD_CONTINUOUS_FEEDBACK | Enable continuous feedback |
| 126 | CMD_IMU | Get IMU data |
| 3 | CMD_LED | LED control `{"T":3,"R":255,"G":0,"B":0}` |

### Parameters

- L/R: Left/Right wheel speeds (-0.5 to +0.5)
- X: Linear velocity (m/s)
- Z: Angular velocity (rad/s)

## Nodes

### ugv02_controller_node

Main controller node that interfaces with the ESP32.

**Subscribers:**
- `/cmd_vel` (geometry_msgs/Twist): Velocity commands

**Publishers:**
- `/odom` (nav_msgs/Odometry): Wheel odometry
- `/imu` (sensor_msgs/Imu): IMU data
- `/battery` (sensor_msgs/BatteryState): Battery voltage
- `/tf` (tf2_msgs/TFMessage): odom → base_link transform

**Parameters:**
- `serial_port`: Serial device path (default: `/dev/ttyACM0`)
- `baud_rate`: Serial baud rate (default: `115200`)
- `wheel_separation`: Distance between wheels in meters (default: `0.23`)
- `wheel_radius`: Wheel radius in meters (default: `0.04`)
- `max_speed`: Maximum speed in m/s (default: `0.5`)
- `cmd_timeout`: Stop robot after timeout seconds (default: `0.5`)
- `publish_tf`: Publish TF transforms (default: `true`)

### ugv02_teleop_node

Keyboard teleoperation node.

**Controls:**
- `w/s`: Forward/Backward
- `a/d`: Rotate Left/Right
- `space`: Stop
- `+/-`: Increase/Decrease speed
- `e`: Emergency stop toggle
- `q/ESC`: Quit

## Usage

### Basic Launch

```bash
# Launch controller
ros2 launch aimee_ugv02_controller ugv02_bringup.launch.py

# With custom serial port
ros2 launch aimee_ugv02_controller ugv02_bringup.launch.py serial_port:=/dev/ttyUSB0

# With teleop
ros2 launch aimee_ugv02_controller ugv02_bringup.launch.py enable_teleop:=true
```

### Individual Nodes

```bash
# Controller node
ros2 run aimee_ugv02_controller ugv02_controller_node --ros-args -p serial_port:=/dev/ttyACM0

# Teleop node
ros2 run aimee_ugv02_controller ugv02_teleop_node
```

### Command Velocity

```bash
# Move forward
ros2 topic pub /cmd_vel geometry_msgs/Twist '{linear: {x: 0.3}}' --once

# Rotate in place
ros2 topic pub /cmd_vel geometry_msgs/Twist '{angular: {z: 0.5}}' --once

# Stop
ros2 topic pub /cmd_vel geometry_msgs/Twist '{}' --once
```

## Nav2 Integration

This package includes Nav2 configuration files for autonomous navigation.

### Required Hardware for Nav2

- Lidar (e.g., LD06, LD19, or RPLidar)
- Optional: Camera for visual odometry

### Launch Nav2

```bash
# Launch UGV02 controller
ros2 launch aimee_ugv02_controller ugv02_bringup.launch.py

# Launch lidar driver (example for LD06)
ros2 launch ldlidar_stl_ros2 ld06.launch.py

# Launch Nav2
ros2 launch nav2_bringup navigation_launch.py params_file:=/path/to/nav2_params.yaml

# Or with SLAM
ros2 launch nav2_bringup navigation_launch.py slam:=true
```

## Robot Dimensions

- **Wheel Separation**: 0.23m
- **Wheel Radius**: 0.04m
- **Robot Radius**: 0.22m
- **Max Speed**: 0.41 m/s (hardware limit)
- **Weight**: ~2kg

## References

- [Waveshare UGV02 Wiki](https://www.waveshare.com/wiki/UGV02)
- [Waveshare UGV Base ROS](https://github.com/waveshareteam/ugv_base_ros)
- [StuartGJohnson Nav2 Integration](https://github.com/StuartGJohnson/ugv_ws)

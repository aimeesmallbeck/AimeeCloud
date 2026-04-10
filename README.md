# Aimee Robot ROS2 Workspace

ROS2 Humble workspace for the Aimee social assistance robot.

## Quick Start

```bash
# Source the environment
source ~/aimee-robot-ws/setup_env.sh

# Build the workspace
colcon build --symlink-install

# Launch the robot
ros2 launch aimee_bringup robot.launch.py robot:=ron
```

## Directory Structure

```
aimee-robot-ws/
├── src/
│   ├── aimee_msgs/           # Custom ROS2 messages and actions
│   ├── aimee_bringup/        # Launch files and configuration
│   ├── aimee_brick_template/ # Template for creating new bricks
│   │   └── brick_template/
│   └── aimee_*/              # Other packages (created in subsequent phases)
├── config/
│   ├── robot_config.yaml     # Hardware configuration
│   └── skills_config.yaml    # Intent routing and skills
├── scripts/
│   ├── create_brick.py       # Brick generator tool
│   └── fix_routing.sh        # Network routing fix
├── systemd/
│   ├── aimee-robot.service   # Main robot service
│   └── aimee-routing.service # Network routing service
├── fastdds_shm.xml           # Fast DDS Shared Memory configuration
├── setup_env.sh              # Environment setup script
└── README.md                 # This file
```

## Critical Optimizations

This workspace includes three critical optimizations for the UNO Q's 4GB RAM:

### 1. Fast DDS Shared Memory

Prevents message duplication between local nodes:

```bash
# Already configured in setup_env.sh
export FASTRTPS_DEFAULT_PROFILES_FILE=~/aimee-robot-ws/fastdds_shm.xml
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
```

### 2. LLM Action Server

Non-blocking LLM with streaming and cancellation support.

### 3. Network Routing Fix

Prevents OBSBOT USB RNDIS from hijacking default gateway.

## Creating New Bricks

Use the brick generator script:

```bash
python3 scripts/create_brick.py \
    --name my_brick \
    --class MyBrick \
    --description "My awesome brick" \
    --category hardware
```

Categories: `hardware`, `audio`, `vision`, `sensors`, `network`, `general`

## Installation

### 1. Install System Services

```bash
# Network routing fix
sudo cp systemd/aimee-routing.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable aimee-routing

# Main robot service
sudo cp systemd/aimee-robot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable aimee-robot
```

### 2. Add to .bashrc

```bash
echo 'source ~/aimee-robot-ws/setup_env.sh' >> ~/.bashrc
```

## Configuration

Edit `config/robot_config.yaml` for hardware settings:

```yaml
ron:
  hardware:
    base:
      serial_port: "/dev/ttyACM0"
    arm:
      serial_port: "/dev/ttyUSB0"
    cameras:
      main:
        ip: "192.168.5.1"
```

## Development

### Building

```bash
cd ~/aimee-robot-ws
source setup_env.sh
colcon build --symlink-install
```

### Testing

```bash
# Test voice
ros2 topic pub /voice/speak std_msgs/String "data: 'Hello!'"

# Test motion
ros2 topic pub /cmd_vel geometry_msgs/Twist "{linear: {x: 0.5}}"

# View topics
ros2 topic list
ros2 topic echo /voice/transcription
```

## Troubleshooting

### Memory Issues

If running out of RAM:
- Check SHM configuration is loaded: `echo $FASTRTPS_DEFAULT_PROFILES_FILE`
- Monitor memory: `free -h`
- Reduce node count in launch file

### Network Issues

If cloud connectivity fails:
```bash
# Check routing
ip route show

# Fix routing manually
sudo ~/aimee-robot-ws/scripts/fix_routing.sh

# Test connectivity
ping 8.8.8.8
ping 192.168.5.1
```

### OBSBOT Camera Not Found

```bash
# Check USB network interface
ip addr show | grep 192.168.5

# List USB devices
lsusb | grep OBSBOT
```

## License

MPL-2.0

## See Also

- Full Project Plan: `~/Aimee_Project_Plan.md`
- Quick Reference: `~/Aimee_Project_Plan_Summary.md`

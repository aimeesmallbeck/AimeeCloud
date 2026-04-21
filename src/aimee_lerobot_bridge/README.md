# Aimee LeRobot Bridge

Integration between Hugging Face LeRobot and ROS2 for the Aimee robot platform.

## Overview

This package provides the bridge layer between LeRobot's learning framework and ROS2's robot control system. It enables:

- **Data Collection**: Record demonstrations in ROS2 bag format
- **Policy Inference**: Run trained LeRobot policies in real-time
- **Teleoperation**: Manual control for data collection and testing
- **Dataset Conversion**: Convert ROS2 bags to LeRobot format

## Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                    LEARNING WORKFLOW                            │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Data Collection → ROS2 Bag → LeRobot Dataset → Training        │
│       ↑                                                   ↓     │
│       └──────────────── Policy Inference ←────────────────┘     │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## Nodes

### dataset_recorder

Records robot demonstrations to ROS2 bags.

**Topics Subscribed:**
- `/camera/image_raw` - Camera observations
- `/joint_states` - Joint positions
- `/arm/command` - Arm actions
- `/cmd_vel` - Base velocity commands

**Services:**
- `/start_recording` - Start a new episode
- `/stop_recording` - Stop current episode
- `/new_episode` - Start episode with task description

**Usage:**
```bash
ros2 run aimee_lerobot_bridge dataset_recorder

# Start recording
ros2 service call /start_recording std_srvs/srv/Trigger

# Stop recording
ros2 service call /stop_recording std_srvs/srv/Trigger
```

### policy_controller

Loads and executes trained LeRobot policies.

**Topics Subscribed:**
- `/camera/image_raw` - Visual observations
- `/joint_states` - Current joint positions

**Topics Published:**
- `/arm/command` - Joint trajectory commands

**Services:**
- `/load_policy` - Load policy from Hugging Face
- `/start_inference` - Start autonomous control
- `/stop_inference` - Stop and return to manual

**Usage:**
```bash
ros2 run aimee_lerobot_bridge policy_controller \
    --ros-args \
    -p policy_repo_id:=aimee/pick_place_policy \
    -p device:=cpu

# Start autonomous control
ros2 service call /start_inference std_srvs/srv/Trigger
```

### teleop_keyboard

Keyboard teleoperation for data collection.

**Controls:**
- `1-6` - Select joint (1-5 = arm, 6 = gripper)
- `+/-` - Increase/decrease joint angle
- `r` - Reset to home position
- `s` - Save current pose
- `p` - Play saved pose
- `space` - Emergency stop
- `q/ESC` - Quit

**Usage:**
```bash
ros2 run aimee_lerobot_bridge teleop_keyboard
```

### bag_to_dataset

Converts ROS2 bags to LeRobot dataset format.

**Usage:**
```bash
ros2 run aimee_lerobot_bridge bag_to_dataset \
    --ros-args \
    -p bag_path:=./dataset_session_1 \
    -p output_repo:=aimee/pick_place_v1
```

## Launch Files

### Data Collection

```bash
ros2 launch aimee_lerobot_bridge data_collection.launch.py \
    output_dir:=~/aimee_datasets \
    dataset_name:=pick_place_demo
```

### Teleoperation

```bash
ros2 launch aimee_lerobot_bridge teleop.launch.py \
    teleop_type:=keyboard
```

### Policy Inference

```bash
ros2 launch aimee_lerobot_bridge policy_inference.launch.py \
    policy_repo_id:=aimee/pick_place_policy \
    policy_type:=act \
    device:=cpu
```

## Workflow

### 1. Data Collection

```bash
# Terminal 1: Start data collection
ros2 launch aimee_lerobot_bridge data_collection.launch.py

# Terminal 2: Record episodes
ros2 service call /new_episode lerobot_interfaces/srv/NewEpisode \
    'task: "pick up the red ball"'

# Perform the task using teleop...

ros2 service call /end_episode lerobot_interfaces/srv/EndEpisode
```

### 2. Convert to LeRobot Format

```bash
ros2 run aimee_lerobot_bridge bag_to_dataset \
    --ros-args \
    -p bag_path:=~/aimee_datasets/pick_place_demo \
    -p output_repo:=aimee/pick_place_v1

# Upload to Hugging Face
hf upload --repo-type dataset aimee/pick_place_v1 \
    ~/aimee_datasets/aimee/pick_place_v1
```

### 3. Train Policy

On a machine with GPU:

```bash
lerobot-train \
    --dataset.repo_id=aimee/pick_place_v1 \
    --policy.type=act \
    --policy.dim_model=512 \
    --policy.n_action_steps=8 \
    --batch_size=8 \
    --num_epochs=2000 \
    --job_name=aimee_pick_place_act

# Upload trained policy
hf upload --repo-type model aimee/pick_place_policy \
    ./outputs/aimee_pick_place_act/checkpoints
```

### 4. Deploy Policy

```bash
ros2 launch aimee_lerobot_bridge policy_inference.launch.py \
    policy_repo_id:=aimee/pick_place_policy

# Start autonomous control
ros2 service call /start_inference std_srvs/srv/Trigger
```

## RoArm-M3 Hardware Integration

The `roarm_m3_http_driver.py` node connects directly to the RoArm-M3-Pro via HTTP WiFi API.

### Verified Joint Limits (Empirical Testing)

These limits were determined by physically testing the arm at `192.168.1.57`:

| Joint | ROS Name | Min | Max | Home | Notes |
|-------|----------|-----|-----|------|-------|
| Base | `joint1` | -180° | +180° | 0° | Full rotation |
| Shoulder | `joint2` | -90° | +90° | 0° | SDK claims ±109°, HW is ±90° |
| Elbow | `joint3` | 0° | **170°** | **90°** | 180° hits the base |
| Wrist | `joint4` | -90° | +90° | 0° | SDK claims ±109°, HW is ±90° |
| Roll | `joint5` | -180° | +180° | 0° | Full rotation |
| Gripper | `gripper` | 0° | 180° | 0° | Effective range ~64°–178° |

### Coordinate Frame (Firmware-Native)

The driver uses **firmware-native coordinates** (not the Waveshare SDK's π-transformed frame):

- **Elbow**: `0° = straight up`, `90° = horizontal forward`, `170° = max down`
- **Gripper**: `0° = fully open`, `180° = fully closed`
  - Firmware clamps commands below ~64° to ~64° (physical open limit)
  - Commands above ~178° clamp to ~178° (physical closed limit)

### HTTP API Commands

| Type | Code | Description |
|------|------|-------------|
| `T:100` | Home | Return to home position |
| `T:102` | Joint control | All joints in radians: `base, shoulder, elbow, wrist, roll, hand` |
| `T:105` | Feedback | Returns joint positions, torques, and Cartesian pose |
| `T:106` | Gripper control | Dedicated gripper command with `cmd` field |

### Running the Driver

```bash
# Inside the ROS2 container
docker exec -it aimee-robot bash
source /ros_entrypoint.sh && source /workspace/install/setup.bash

# Start the driver
ros2 run aimee_lerobot_bridge roarm_m3_http_driver \
    --ros-args -p arm_ip:=192.168.1.57 -p poll_rate:=5.0

# Test movement via topic
ros2 topic pub /arm/joint_trajectory trajectory_msgs/JointTrajectory "{
  joint_names: ['joint1','joint2','joint3','joint4','joint5','gripper'],
  points: [{positions: [0.0,0.0,1.57,0.0,0.0,3.14], time_from_start: {sec:1}}]
}" --once
```

## Configuration

See `config/roarm_m3_config.yaml` for robot-specific settings:
- Joint limits and initial positions
- Camera configuration
- Policy hyperparameters

## Dependencies

```bash
# LeRobot
pip install lerobot[huggingface]

# ROS2 packages
sudo apt install ros-humble-ros2-control ros-humble-ros2-controllers
sudo apt install ros-humble-cv-bridge

# Additional Python packages
pip install opencv-python numpy pyyaml toml
```

## References

- [LeRobot Documentation](https://github.com/huggingface/lerobot)
- [LeRobot + ROS2 (sacovo)](https://github.com/sacovo/lerobot_ros)
- [SO101 ROS2](https://github.com/AgRoboticsResearch/Lerobot_ros2)
- [RoArm-M3 Documentation](https://github.com/jhacksman/RoArm-M3)

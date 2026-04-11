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

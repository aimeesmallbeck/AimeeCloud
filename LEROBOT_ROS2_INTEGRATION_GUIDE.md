# LeRobot + ROS2 Integration Guide for Aimee Robot

## Overview

This guide outlines best practices for integrating Hugging Face LeRobot with ROS2 for the Aimee robot platform, specifically for the RoArm-M3 robotic arm and UGV02 rover.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LEARNING PIPEWORK (LeRobot)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │ Data Collection  │  │ Policy Training  │  │ Policy Inference │          │
│  │ (Teleoperation)  │→│ (ACT, Diffusion) │→│ (Real-time Ctrl) │          │
│  └────────┬─────────┘  └──────────────────┘  └────────┬─────────┘          │
│           │                                           │                     │
│           └───────────────────────────────────────────┘                     │
│                           │                                                 │
│           ╔═══════════════╧═══════════════╗                                 │
│           ║     ROS2 BRIDGE LAYER         ║                                 │
│           ║  (aimee_lerobot_bridge)       ║                                 │
│           ╚═══════════════╤═══════════════╝                                 │
│                           │                                                 │
│  ┌────────────────────────┼─────────────────────────────────────────┐      │
│  │                   ROS2 SYSTEM                                      │      │
│  │  ┌─────────────┐  ┌───┴──────┐  ┌─────────────┐  ┌─────────────┐ │      │
│  │  │ /joint_cmd  │  │ /obs_im  │  │ /joint_state│  │ /cmd_vel    │ │      │
│  │  │ (Actions)   │  │ (Camera) │  │ (States)    │  │ (Base)      │ │      │
│  │  └──────┬──────┘  └────┬─────┘  └──────┬──────┘  └──────┬──────┘ │      │
│  │         │              │               │                │        │      │
│  │  ┌──────┴──────────────┴───────────────┴────────────────┘        │      │
│  │  │              HARDWARE DRIVERS                                 │      │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │      │
│  │  │  │RoArm-M3 Ctrl│  │UGV02 Ctrl   │  │Camera/OBSBOT│           │      │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘           │      │
│  │  └──────────────────────────────────────────────────────────────┘      │
│  └───────────────────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────────────────────┘
```

## Best Practices for LeRobot + ROS2 Integration

### 1. Data Collection Architecture

**Recommended: ROS2 Bag → LeRobot Dataset**

Based on best practices from `ros2bag_lerobot` and `so101_ros2`:

```python
# Record demonstrations using ROS2 bags
ros2 bag record \
    /joint_states \
    /arm/command \
    /camera/color/image_raw \
    /camera/depth/image_raw \
    /tf \
    -o dataset_session_1

# Convert to LeRobot format
ros2 run aimee_lerobot_bridge bag_to_dataset \
    --ros-args \
    -p bag_path:=./dataset_session_1 \
    -p output_repo:=aimee/pick_place_v1
```

**Why this approach:**
- ROS2 bags are robust, timestamp-synchronized
- Easy to replay and verify
- Supports multiple cameras and sensors
- Can be post-processed (filter, augment)

### 2. Policy Training Workflow

```bash
# 1. Upload dataset to Hugging Face
hf upload --repo-type dataset aimee/pick_place_v1 ./data/aimee/pick_place_v1

# 2. Train policy (on GPU workstation)
lerobot-train \
    --dataset.repo_id=aimee/pick_place_v1 \
    --policy.type=act \
    --policy.dim_model=512 \
    --policy.num_actions=16 \
    --batch_size=8 \
    --num_epochs=2000 \
    --job_name=aimee_pick_place_act

# 3. Upload trained policy
hf upload --repo-type model aimee/pick_place_policy ./outputs/aimee_pick_place_act/checkpoints
```

### 3. ROS2 Bridge Design

Based on `lerobot_ros` by sacovo and `lerobot-ros` by ycheng517:

```python
# aimee_lerobot_bridge/policy_controller.py

class PolicyController(Node):
    """
    Loads LeRobot policies and executes them in ROS2.
    
    Subscribes to observation topics (cameras, joint states)
    Publishes action topics (joint commands, gripper)
    """
    
    def __init__(self):
        # Load policy from Hugging Face
        self.policy = ACTPolicy.from_pretrained("aimee/pick_place_policy")
        
        # ROS2 subscribers
        self.create_subscription(Image, '/camera/image_raw', self.on_image)
        self.create_subscription(JointState, '/joint_states', self.on_joint_state)
        
        # ROS2 publishers
        self.action_pub = self.create_publisher(JointTrajectory, '/arm/command')
        
    def on_image(self, msg):
        # Preprocess image for policy
        obs = self.preprocess_observation(msg)
        
        # Run inference
        with torch.no_grad():
            actions = self.policy.select_action(obs)
        
        # Publish actions
        self.publish_actions(actions)
```

### 4. Teleoperation Modes

**Mode A: Manual (Keyboard/Joystick)**
```python
# For data collection
ros2 run aimee_lerobot_bridge keyboard_teleop
```

**Mode B: Leader-Follower (if leader arm available)**
```python
# SO-101 style leader-follower
ros2 run aimee_lerobot_bridge leader_follower_node \
    --ros-args \
    -p leader_port:=/dev/ttyUSB0 \
    -p follower_port:=/dev/ttyACM0
```

**Mode C: Autonomous (Policy)**
```python
# Run trained policy
ros2 run aimee_lerobot_bridge policy_controller \
    --ros-args \
    -p policy_repo:=aimee/pick_place_policy \
    -p device:=cpu
```

## Recommended ROS2 Packages for Aimee

### Package 1: `aimee_roarm_controller`
Direct hardware control (existing, needs enhancement)

### Package 2: `aimee_lerobot_bridge` (NEW)
LeRobot integration layer

```
aimee_lerobot_bridge/
├── aimee_lerobot_bridge/
│   ├── __init__.py
│   ├── dataset_recorder.py      # Record to LeRobot format
│   ├── policy_controller.py     # Run trained policies
│   ├── teleop_keyboard.py       # Keyboard control for data collection
│   ├── teleop_gamepad.py        # Gamepad control
│   ├── bag_converter.py         # ROS2 bag → LeRobot dataset
│   └── config/
│       └── roarm_m3_config.yaml # Joint limits, camera params
├── launch/
│   ├── teleop.launch.py
│   ├── policy_inference.launch.py
│   └── data_collection.launch.py
└── package.xml
```

### Package 3: `aimee_lerobot_description` (NEW)
URDF/XACRO for RoArm-M3

```
aimee_lerobot_description/
├── urdf/
│   ├── roarm_m3.urdf.xacro
│   └── aimee_robot.urdf.xacro  # Full robot (UGV02 + RoArm-M3)
├── meshes/
│   └── roarm_m3/
└── config/
    └── roarm_m3_calibration.yaml
```

## Key Implementation Details

### 1. ROS2 Control Architecture

```yaml
# roarm_m3_controllers.yaml
controller_manager:
  ros__parameters:
    update_rate: 50  # Hz

    joint_trajectory_controller:
      type: joint_trajectory_controller/JointTrajectoryController

    joint_state_broadcaster:
      type: joint_state_broadcaster/JointStateBroadcaster

joint_trajectory_controller:
  ros__parameters:
    joints:
      - joint1
      - joint2
      - joint3
      - joint4
      - joint5
      - gripper
    command_interfaces:
      - position
    state_interfaces:
      - position
      - velocity
```

### 2. LeRobot Configuration

```toml
# lerobot_config.toml
[robot]
type = "roarm_m3"

[robot.cameras]
camera_0 = { type = "obsbot", topic = "/camera/image_raw" }

[robot.motors]
joint1 = { topic = "/arm/joint1/command", type = "position" }
joint2 = { topic = "/arm/joint2/command", type = "position" }
joint3 = { topic = "/arm/joint3/command", type = "position" }
joint4 = { topic = "/arm/joint4/command", type = "position" }
joint5 = { topic = "/arm/joint5/command", type = "position" }
gripper = { topic = "/arm/gripper/command", type = "position" }

[robot.dataset]
fps = 30
image_keys = ["camera_0"]
state_keys = ["joint1", "joint2", "joint3", "joint4", "joint5", "gripper"]
action_keys = ["joint1", "joint2", "joint3", "joint4", "joint5", "gripper"]
```

### 3. Policy Training Configuration

```python
# ACT policy config for RoArm-M3
policy:
  type: act
  
  # Image encoder
  vision_backbone: resnet18
  pretrained_backbone: true
  
  # Transformer
  dim_model: 512
  n_heads: 8
  dim_feedforward: 2048
  n_encoder_layers: 4
  n_decoder_layers: 7
  
  # Actions
  n_actions: 16  # Chunk size
  action_dim: 6  # 5 joints + gripper
  
  # Training
  lr: 1e-5
  batch_size: 8
  num_epochs: 2000
```

## Integration Workflow

```
Phase 1: Hardware Setup
├── Connect RoArm-M3 via serial/WiFi
├── Verify UGV02 base control
├── Test OBSBOT camera integration
└── Calibrate all sensors

Phase 2: ROS2 Integration
├── Create aimee_lerobot_bridge package
├── Implement dataset_recorder node
├── Test teleoperation (keyboard/gamepad)
└── Verify data flow: camera → joints

Phase 3: Data Collection
├── Record demonstration episodes
├── Store as ROS2 bags
├── Convert to LeRobot format
└── Upload to Hugging Face

Phase 4: Policy Training
├── Train ACT/Diffusion policy on GPU
├── Validate in simulation (Isaac Sim)
├── Fine-tune on real hardware
└── Upload trained policy

Phase 5: Deployment
├── Load policy in ROS2
├── Test autonomous execution
├── Monitor and collect metrics
└── Iterate and improve
```

## Tools and Dependencies

```bash
# Core LeRobot
pip install lerobot[huggingface]

# ROS2 packages
sudo apt install ros-humble-ros2-control ros-humble-ros2-controllers
sudo apt install ros-humble-moveit

# Camera/vision
pip install opencv-python opencv-contrib-python

# Optional: Simulation
pip install isaacsim

# Hugging Face tools
pip install huggingface-hub datasets
```

## References

1. **LeRobot Official**: https://github.com/huggingface/lerobot
2. **LeRobot + ROS2 (sacovo)**: https://github.com/sacovo/lerobot_ros
3. **SO101 ROS2**: https://github.com/AgRoboticsResearch/Lerobot_ros2
4. **ros2bag → LeRobot**: https://github.com/konu-droid/ros2bag_lerobot
5. **RoArm-M3**: https://github.com/jhacksman/RoArm-M3

## Next Steps

1. Create `aimee_lerobot_bridge` package
2. Implement dataset recorder node
3. Create URDF for RoArm-M3
4. Test teleoperation pipeline
5. Record first demonstration dataset

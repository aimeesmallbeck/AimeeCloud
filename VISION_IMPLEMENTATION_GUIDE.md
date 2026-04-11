# Aimee Vision System Implementation Guide
## For "Pick Up the Red Ball" Type Commands

---

## 🎯 Overview

This guide outlines the implementation of a complete vision-to-manipulation pipeline for the Aimee robot. The system is designed to handle natural language requests like:
- "Pick up the red ball"
- "Grab the blue cup"
- "Put the ball in the box"

**Status**: Camera control (OBSBOT) is ✅ operational. This guide covers the vision/manipulation layer.

---

## 📐 Architecture

```
User Request: "Pick up the red ball"
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│  SKILL LAYER (aimee_skill_pick_place)                          │
│  - Parses natural language                                      │
│  - Creates PickPlace action goal                                │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼ Action: /manipulation/pick_place
┌─────────────────────────────────────────────────────────────────┐
│  MANIPULATION LAYER                                            │
│  ┌──────────────────┐  ┌──────────────────┐                    │
│  │ pick_place_node  │──► arm_controller   │──► (Simulated)     │
│  │ (action server)  │  │ (RoArm-M3 driver)│                    │
│  └──────────────────┘  └──────────────────┘                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼ Subscribes to: /vision/detections
┌─────────────────────────────────────────────────────────────────┐
│  PERCEPTION LAYER                                              │
│  ┌──────────────────┐  ┌──────────────────┐                    │
│  │ pose_estimator   │──► grasp_planner    │                    │
│  │ (2D→3D position) │  │ (grasp strategy) │                    │
│  └──────────────────┘  └──────────────────┘                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼ Subscribes to: /camera/image_raw
┌─────────────────────────────────────────────────────────────────┐
│  VISION LAYER                                                  │
│  ┌──────────────────┐  ┌──────────────────┐                    │
│  │ color_detector   │──► object_tracker   │                    │
│  │ (OpenCV/HSV)     │  │ (KF tracking)    │                    │
│  └──────────────────┘  └──────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Packages to Install (ROS2)

Add these to your Dockerfile or install on the system:

```dockerfile
# In your ROS2 container Dockerfile

# Standard ROS2 vision packages
RUN apt-get update && apt-get install -y \
    ros-humble-vision-msgs \
    ros-humble-cv-bridge \
    ros-humble-image-transport \
    ros-humble-tf2-ros \
    ros-humble-tf2-geometry-msgs \
    python3-opencv \
    python3-numpy \
    python3-scipy \
    && rm -rf /var/lib/apt/lists/*

# Optional: For AprilTag detection (useful for calibration)
RUN apt-get update && apt-get install -y \
    ros-humble-apriltag-ros \
    && rm -rf /var/lib/apt/lists/*
```

---

## 📋 ROS2 Topics for Vision/Manipulation

| Topic | Type | Description |
|-------|------|-------------|
| `/camera/image_raw` | `sensor_msgs/Image` | Raw camera feed |
| `/camera/camera_info` | `sensor_msgs/CameraInfo` | Camera calibration |
| `/vision/detections` | `aimee_msgs/ObjectDetection[]` | Detected objects |
| `/vision/tracked_objects` | `aimee_msgs/ObjectDetection[]` | Tracked objects with IDs |
| `/manipulation/grasp_pose` | `aimee_msgs/GraspPose` | Planned grasp |
| `/arm/command` | `aimee_msgs/ArmCommand` | Arm motion commands |
| `/arm/state` | `sensor_msgs/JointState` | Current arm state |
| `/tf` | `tf2_msgs/TFMessage` | Coordinate transforms |

---

## 🔧 Implementation Steps

### Phase 1: Update Message Definitions ✅

Already done - added `ObjectDetection.msg`, `GraspPose.msg`, `ArmCommand.msg`, and `PickPlace.action`.

Rebuild messages:
```bash
cd ~/aimee-robot-ws
colcon build --packages-select aimee_msgs
source install/setup.bash
```

### Phase 2: Create Vision Pipeline Package

```bash
cd ~/aimee-robot-ws/src
# Create package
cd ..
colcon build --packages-select aimee_vision_pipeline
```

### Phase 3: Create Perception Package

```bash
cd ~/aimee-robot-ws/src
# Create package
cd ..
colcon build --packages-select aimee_perception
```

### Phase 4: Create Manipulation Package (Simulated)

```bash
cd ~/aimee-robot-ws/src
# Create package
cd ..
colcon build --packages-select aimee_manipulation
```

---

## 🧠 Color-Based Object Detection Strategy

Since we don't have depth camera or GPU for YOLO, we'll use **color segmentation**:

```python
# color_detector_node.py - Key Algorithm

import cv2
import numpy as np

class ColorDetector:
    def detect_red_ball(self, image):
        # Convert to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Red has two ranges in HSV
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])
        
        # Create mask
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = mask1 + mask2
        
        # Find contours
        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter by size (ball should be within certain area range)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 100 < area < 10000:  # Tune these values
                x, y, w, h = cv2.boundingRect(cnt)
                center_x = x + w/2
                center_y = y + h/2
                return (center_x, center_y, w, h)
        
        return None
```

---

## 📐 3D Position Estimation (Monocular)

Without a depth camera, estimate 3D position using:

```python
# pose_estimator_node.py

def estimate_3d_position(self, bbox_x, bbox_y, bbox_width, bbox_height, object_diameter=0.065):
    """
    Estimate 3D position from 2D bounding box using known object size.
    
    Args:
        bbox_width: Width of bounding box in pixels
        object_diameter: Known physical diameter (e.g., 6.5cm for tennis ball)
    
    Returns:
        (x, y, z) in camera frame (meters)
    """
    # Camera intrinsic parameters (need calibration)
    fx = self.camera_info.k[0]  # Focal length x
    fy = self.camera_info.k[4]  # Focal length y
    cx = self.camera_info.k[2]  # Principal point x
    cy = self.camera_info.k[5]  # Principal point y
    
    # Estimate distance using apparent size
    # distance = (real_size * focal_length) / apparent_size
    z = (object_diameter * fx) / bbox_width
    
    # Calculate x, y in camera frame
    x = (bbox_x - cx) * z / fx
    y = (bbox_y - cy) * z / fy
    
    return (x, y, z)
```

---

## 🤖 Simulated Arm Controller

Until the real arm arrives, create a simulator:

```python
# arm_controller_node.py (Simulated)

class SimulatedArmController(Node):
    """Simulated RoArm-M3 controller for testing."""
    
    def execute_arm_command(self, command: ArmCommand):
        """Execute arm command in simulation."""
        
        self.get_logger().info(f"🤖 SIMULATED ARM: {command.command_type}")
        
        if command.command_type == "grasp":
            self.get_logger().info(
                f"  Moving to pre-grasp: {command.grasp_pose.pre_grasp_pose}"
            )
            time.sleep(1.0)  # Simulate motion
            
            self.get_logger().info(f"  Opening gripper")
            time.sleep(0.5)
            
            self.get_logger().info(f"  Moving to grasp: {command.grasp_pose.grasp_pose}")
            time.sleep(1.0)
            
            self.get_logger().info(f"  Closing gripper")
            time.sleep(0.5)
            
            self.get_logger().info(f"  Lifting: {command.grasp_pose.lift_pose}")
            time.sleep(1.0)
            
        elif command.command_type == "cartesian":
            self.get_logger().info(f"  Moving to: {command.target_pose}")
            time.sleep(1.0)
        
        # Publish success
        result = ArmCommandResult()
        result.success = True
        result.message = "Simulated execution complete"
        return result
```

---

## 🎯 Pick and Place Skill Flow

```
1. User: "Pick up the red ball"
            │
            ▼
2. Intent Router classifies → "pick_place" intent
            │
            ▼
3. Skill Manager creates PickPlace action goal:
   - object_class: "ball"
   - object_color: "red"
            │
            ▼
4. PickPlace Action Server executes:
   ├─ Phase 1: SEARCH
   │  └─ Wait for /vision/detections with matching object
   │
   ├─ Phase 2: APPROACH
   │  └─ Call grasp_planner → GraspPose
   │  └─ Send arm_command (pre_grasp)
   │
   ├─ Phase 3: GRASP
   │  └─ Send arm_command (grasp)
   │  └─ Send arm_command (gripper close)
   │
   └─ Phase 4: LIFT
      └─ Send arm_command (lift)
      └─ ✓ Success!
```

---

## 📁 File Structure

```
~/aimee-robot-ws/src/
├── aimee_msgs/                    # ✅ Already exists
│   └── msg/
│       ├── ObjectDetection.msg    # ✅ Created
│       ├── GraspPose.msg          # ✅ Created
│       └── ArmCommand.msg         # ✅ Created
│   └── action/
│       └── PickPlace.action       # ✅ Created
│
├── aimee_vision_pipeline/         # ⬜ NEW: Color detection
│   └── aimee_vision_pipeline/
│       ├── color_detector_node.py
│       └── object_tracker_node.py
│
├── aimee_perception/              # ⬜ NEW: 3D estimation
│   └── aimee_perception/
│       ├── pose_estimator_node.py
│       └── grasp_planner_node.py
│
├── aimee_manipulation/            # ⬜ NEW: Arm control
│   └── aimee_manipulation/
│       ├── arm_controller_node.py (simulated)
│       └── pick_place_skill.py
│
└── aimee_skills/                  # ⬜ NEW: Skill implementations
    └── aimee_skills/
        └── skill_pick_place.py    # High-level skill
```

---

## 🔧 Testing the Pipeline

### 1. Test Color Detection
```bash
# Terminal 1: Start camera
docker exec -it aimee-robot ros2 run aimee_vision_obsbot obsbot_node

# Terminal 2: Start color detector
docker exec -it aimee-robot ros2 run aimee_vision_pipeline color_detector_node

# Terminal 3: View detections
docker exec -it aimee-robot ros2 topic echo /vision/detections
```

### 2. Test Pick Action (Simulation)
```bash
# Send test pick request
docker exec -it aimee-robot ros2 action send_goal /manipulation/pick_place aimee_msgs/action/PickPlace "{
  object_class: 'ball',
  object_color: 'red',
  enable_place: false,
  natural_language_request: 'pick up the red ball'
}"
```

### 3. Test via Voice
```
You: "Aimee, pick up the red ball"
Aimee: "I'll find and pick up the red ball"
      [visual search...]
Aimee: "Found the red ball, picking it up now"
      [simulated arm motion...]
Aimee: "Got it! The red ball is now in my gripper"
```

---

## 🎨 Extending to Other Objects

Add more color definitions:

```python
# In color_detector_node.py

COLOR_RANGES = {
    "red": [
        (np.array([0, 100, 100]), np.array([10, 255, 255])),
        (np.array([160, 100, 100]), np.array([180, 255, 255]))
    ],
    "blue": [
        (np.array([100, 100, 100]), np.array([130, 255, 255]))
    ],
    "green": [
        (np.array([40, 100, 100]), np.array([80, 255, 255]))
    ],
    "yellow": [
        (np.array([20, 100, 100]), np.array([35, 255, 255]))
    ],
}

OBJECT_SIZES = {
    "ball": {"diameter": 0.065},      # Tennis ball
    "cup": {"height": 0.10, "diameter": 0.08},
    "block": {"width": 0.05, "height": 0.05, "depth": 0.05},
}
```

---

## 🚀 Next Steps

1. **Build the messages**: Run `colcon build --packages-select aimee_msgs`
2. **Create skeleton packages**: Use the implementation files in this guide
3. **Calibrate camera**: Get camera_info for accurate 3D estimation
4. **Test color detection**: Hold up a red ball and verify detection
5. **Test full pipeline**: Voice → Detection → Grasp → Simulated pickup

---

## 📚 References

- [ROS2 Vision Messages](https://github.com/ros-perception/vision_msgs)
- [OpenCV Color Spaces](https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html)
- [Camera Calibration](http://wiki.ros.org/camera_calibration)
- [RoArm-M3 Protocol](https://www.waveshare.com/wiki/RoArm-M3)

---

**Document Version**: 1.0  
**Created**: April 11, 2026  
**Status**: Ready for implementation

# Aimee Vision System Implementation Summary

## 🎯 What Was Implemented

Complete vision-to-manipulation pipeline enabling commands like:
- **"Pick up the red ball"**
- **"Grab the blue cup"** 
- **"Lift the yellow block"**

---

## 📁 New Message Types (aimee_msgs)

| Message | Purpose |
|---------|---------|
| `ObjectDetection.msg` | 2D/3D object position, class, color, confidence |
| `GraspPose.msg` | Pre-grasp, grasp, and lift poses for manipulation |
| `ArmCommand.msg` | Joint/cartesian/gripper commands for arm control |
| `PickPlace.action` | Full pick-place action with feedback |

---

## 📦 New ROS2 Packages

### 1. **aimee_vision_pipeline** - Color Detection
```
nodes:
  - color_detector_node.py   # Detect red/blue/green/yellow objects
  - object_tracker_node.py   # Track objects across frames

topics:
  /vision/detections         # Raw color detections
  /vision/tracked_objects    # Objects with stable IDs
  /vision/debug_image        # Visualization
```

### 2. **aimee_perception** - 3D Estimation
```
nodes:
  - pose_estimator_node.py   # 2D → 3D position estimation
  - grasp_planner_node.py    # Calculate grasp strategies

topics:
  /vision/detections_3d      # Objects with 3D positions
  /manipulation/grasp_pose   # Planned grasp poses
  /tf                        # Object transforms
```

### 3. **aimee_manipulation** - Arm Control (Simulated)
```
nodes:
  - arm_controller_node.py   # Simulated RoArm-M3 driver
  - pick_place_server.py     # PickPlace action server

actions:
  /manipulation/pick_place   # Execute pick/place operations
  
topics:
  /arm/command               # Arm motion commands
  /arm/joint_states          # Current arm state
```

---

## 🔧 Build Instructions

### Step 1: Build in Docker Container

```bash
# Start the ROS2 container
docker start aimee-robot
docker exec -it aimee-robot bash

# Inside container:
cd /home/arduino/aimee-robot-wx
source /opt/ros/humble/setup.bash

# Build all new packages
colcon build --packages-select aimee_msgs aimee_vision_pipeline aimee_perception aimee_manipulation --symlink-install

# Source the workspace
source install/setup.bash
```

### Step 2: Test Color Detection

```bash
# Terminal 1: Start camera node
docker exec -it aimee-robot bash
ros2 run aimee_vision_obsbot obsbot_node

# Terminal 2: Start color detector
docker exec -it aimee-robot bash
ros2 run aimee_vision_pipeline color_detector_node --ros-args -p enabled_colors:="['red', 'blue', 'green', 'yellow']"

# Terminal 3: View detections
docker exec -it aimee-robot bash
ros2 topic echo /vision/detections
```

### Step 3: Test Full Pipeline

```bash
# Start all perception nodes
docker exec -it aimee-robot bash
ros2 run aimee_perception pose_estimator_node
ros2 run aimee_perception grasp_planner_node

# Start arm controller (simulated)
ros2 run aimee_manipulation arm_controller_node

# Start pick_place server
ros2 run aimee_manipulation pick_place_server
```

### Step 4: Test Pick Action

```bash
# Send test pick request
docker exec -it aimee-robot bash
ros2 action send_goal /manipulation/pick_place aimee_msgs/action/PickPlace "{
  object_class: 'ball',
  object_color: 'red',
  enable_place: false,
  natural_language_request: 'pick up the red ball'
}"
```

---

## 🧠 How It Works

### Pipeline Flow:

```
1. COLOR DETECTION (aimee_vision_pipeline)
   
   OBSBOT Camera → Color Detector → ObjectDetection
   
   - Converts image to HSV
   - Applies color masks (red, blue, green, yellow)
   - Finds contours → bounding boxes
   - Classifies shape (ball, cup, block)

2. OBJECT TRACKING (aimee_vision_pipeline)
   
   ObjectDetection → Tracker → TrackedObject
   
   - Assigns stable IDs to objects
   - Smooths position over frames
   - Filters false positives

3. 3D POSE ESTIMATION (aimee_perception)
   
   TrackedObject + CameraInfo → 3D Position
   
   - Uses known object size + apparent size
   - Z = (real_diameter × focal_length) / apparent_width
   - Publishes in camera frame + robot frame

4. GRASP PLANNING (aimee_perception)
   
   3D Position → GraspPose
   
   - Top-down grasp for balls/blocks
   - Side grasp for cups
   - Calculates pre-grasp, grasp, and lift poses

5. PICK & PLACE EXECUTION (aimee_manipulation)
   
   GraspPose → ArmCommand Sequence
   
   Phase 1: SEARCH → Wait for object detection
   Phase 2: APPROACH → Move to pre-grasp
   Phase 3: GRASP → Open gripper → Move to grasp → Close
   Phase 4: LIFT → Move to lift position
   Phase 5: PLACE → (optional) Place at target
```

---

## 🎨 Supported Objects & Colors

### Colors:
- **Red** (HSV: 0-10° + 160-180°)
- **Blue** (HSV: 100-130°)
- **Green** (HSV: 40-80°)
- **Yellow** (HSV: 20-35°)
- **Orange** (HSV: 10-20°)
- **Purple** (HSV: 130-160°)

### Objects:
| Object | Grasp Type | Size (default) |
|--------|------------|----------------|
| ball | top_down | 6.5cm diameter |
| cup | side | 8cm diameter, 10cm height |
| block | top_down | 5cm cube |

---

## 🔌 ROS2 Topic Reference

| Topic | Type | Description |
|-------|------|-------------|
| `/camera/image_raw` | sensor_msgs/Image | Camera feed from OBSBOT |
| `/vision/detections` | aimee_msgs/ObjectDetection | Raw color detections |
| `/vision/tracked_objects` | aimee_msgs/ObjectDetection | Tracked objects |
| `/vision/detections_3d` | aimee_msgs/ObjectDetection | With 3D positions |
| `/manipulation/grasp_pose` | aimee_msgs/GraspPose | Planned grasps |
| `/arm/command` | aimee_msgs/ArmCommand | Arm motion commands |
| `/arm/joint_states` | sensor_msgs/JointState | Current joint positions |
| `/tf` | tf2_msgs/TFMessage | Object transforms |

---

## 📊 Example Output

### Color Detection:
```
object_id: "red_ball_001"
object_class: "ball"
color: "red"
confidence: 0.85
bbox_x: 0.45          # Center X (normalized 0-1)
bbox_y: 0.55          # Center Y (normalized 0-1)
bbox_width: 0.15      # Width (normalized)
bbox_height: 0.15     # Height (normalized)
```

### 3D Position:
```
position_camera:
  x: 0.52             # 52cm forward from camera
  y: -0.08            # 8cm to the right
  z: -0.05            # 5cm below camera center
```

### Grasp Plan:
```
object_id: "red_ball_001"
grasp_type: "top_down"
grasp_quality: 0.82
pre_grasp_pose:       # 15cm above ball
  position: {x: 0.52, y: -0.08, z: 0.10}
grasp_pose:           # At ball position
  position: {x: 0.52, y: -0.08, z: 0.02}
lift_pose:            # 10cm above
  position: {x: 0.52, y: -0.08, z: 0.12}
```

---

## 🚀 Next Steps

1. **Build & Test in Container**
   ```bash
   docker exec -it aimee-robot bash
   cd /home/arduino/aimee-robot-ws
   colcon build --packages-select aimee_msgs aimee_vision_pipeline aimee_perception aimee_manipulation
   ```

2. **Calibrate Camera** (for accurate 3D estimation)
   - Print checkerboard pattern
   - Run camera calibration
   - Update camera_info topic

3. **Test with Real Objects**
   - Hold up a red ball
   - Verify detection in RViz or echo topics
   - Check 3D position accuracy

4. **Integrate with Voice**
   - Add "pick up" intent to intent router
   - Connect pick_place action to skill manager
   - Test: "Aimee, pick up the red ball"

5. **When Arm Arrives**
   - Replace simulated arm_controller_node with real serial driver
   - Tune grasp parameters for actual gripper
   - Test with real pick/place operations

---

## 📚 ROS2 Packages Used (Leveraged)

| Package | Purpose | Why Used |
|---------|---------|----------|
| `vision_msgs` | Standard detection interfaces | Interoperability |
| `cv_bridge` | OpenCV ↔ ROS2 Image conversion | Essential for OpenCV |
| `image_transport` | Efficient image publishing | Performance |
| `tf2_ros` | Coordinate transforms | Camera → Robot frame |
| `geometry_msgs` | Points, Poses, Vectors | Standard ROS2 types |
| `sensor_msgs` | Images, CameraInfo, JointState | Standard ROS2 types |

---

## 💡 Design Decisions

1. **Color-based detection** instead of YOLO
   - Lighter on 4GB RAM
   - Faster inference
   - Reliable for known colored objects

2. **Monocular depth estimation** instead of depth camera
   - Uses known object sizes
   - No additional hardware needed
   - Sufficient for manipulation

3. **Simple grasp planner** instead of MoveIt
   - Much lighter resource usage
   - Predefined grasp types per object
   - Easy to tune for specific objects

4. **Simulated arm controller**
   - Test full pipeline before arm arrives
   - Visualize what commands would be sent
   - Easy to swap for real driver

---

## 📁 Files Created

```
~/aimee-robot-ws/
├── src/aimee_msgs/
│   ├── msg/ObjectDetection.msg    # NEW
│   ├── msg/GraspPose.msg          # NEW
│   ├── msg/ArmCommand.msg         # NEW
│   └── action/PickPlace.action    # NEW
│
├── src/aimee_vision_pipeline/     # NEW PACKAGE
│   ├── aimee_vision_pipeline/
│   │   ├── color_detector_node.py
│   │   └── object_tracker_node.py
│   ├── package.xml
│   └── setup.py
│
├── src/aimee_perception/          # NEW PACKAGE
│   ├── aimee_perception/
│   │   ├── pose_estimator_node.py
│   │   └── grasp_planner_node.py
│   ├── package.xml
│   └── setup.py
│
├── src/aimee_manipulation/        # NEW PACKAGE
│   ├── aimee_manipulation/
│   │   ├── arm_controller_node.py (simulated)
│   │   └── pick_place_server.py
│   ├── package.xml
│   └── setup.py
│
├── VISION_IMPLEMENTATION_GUIDE.md # Detailed guide
└── VISION_SYSTEM_SUMMARY.md       # This file
```

---

**Status**: ✅ Implementation Complete  
**Next**: Build & Test in Docker Container

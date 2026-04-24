# AimeeNav — Integrated SLAM + Navigation Node

Self-contained navigation stack for the AIMEE Robot that replaces `slam_toolbox`, Nav2, and their supporting nodes with a single monolithic ROS2 node.

## Overview

AimeeNav directly interfaces with the LD19 lidar and Wave Rover base, performing:
- **360° lidar processing** (direct serial, no `ldlidar_stl_ros2`)
- **Real-time 2D SLAM** with scan-to-map matching and loop closure
- **Global occupancy grid mapping** (64 m × 64 m)
- **A* global path planning** on the SLAM map
- **Reactive obstacle avoidance** (Virtual Force Field + sector analysis)
- **Recovery behaviors** (spin, backup, clear costmap, wait)
- **Direct motor control** (no `aimee_ugv02_controller` dependency)

All navigation and SLAM computations happen in a single process without ROS2 topic passing for the hot path.

## Architecture

```
┌─────────────────────────────────────────┐
│           AimeeNav Node (Python)        │
│  ┌─────────┐      ┌───────────────┐    │
│  │ LD19    │      │ Wave Rover    │    │
│  │ Driver  │      │ Driver        │    │
│  └────┬────┘      └───────┬───────┘    │
│       │                   │             │
│  ┌────▼───────────────────▼────┐        │
│  │   aimee_nav_core (C++)      │        │
│  │  ┌─────────────────────┐    │        │
│  │  │  RobotCentricGridMap│    │        │
│  │  │  GridMap (global)   │    │        │
│  │  │  ScanMatcher        │    │        │
│  │  │  EKF2D              │    │        │
│  │  │  GlobalPlanner (A*) │    │        │
│  │  │  DWALocalPlanner    │    │        │
│  │  │  PoseGraph          │    │        │
│  │  └─────────────────────┘    │        │
│  └────────────┬────────────────┘        │
│               │                         │
│  ┌────────────▼────────────────┐        │
│  │  State Machine + Recovery   │        │
│  └────────────┬────────────────┘        │
│               │                         │
│  ┌────────────▼────────────────┐        │
│  │    ROS2 Pub/Sub / Actions   │        │
│  └─────────────────────────────┘        │
└─────────────────────────────────────────┘
```

## Why AimeeNav?

The standard distributed navigation stack (`ldlidar_stl_ros2` → `slam_toolbox` → `nav2` → `aimee_ugv02_controller`) suffers from DDS queue overflows on the Arduino UNO Q's 4GB RAM. AimeeNav replaces the entire stack with one node, reducing RAM from ~400–500 MB to ~130–150 MB and eliminating inter-node latency.

## Performance

| Metric | Old (Python) | New (C++ Core) |
|---|---|---|
| Grid update (360 rays, 5m @ 0.05m) | ~150 ms | ~0.9 ms |
| Speedup | 1× | **178×** |
| Scan matching | N/A | < 5 ms |
| Global planning (A*) | N/A | < 15 ms |
| RAM footprint | ~100 MB | ~130–150 MB |

## Topics

### Published

| Topic | Type | Purpose |
|-------|------|---------|
| `/scan` | `sensor_msgs/LaserScan` | Lidar data |
| `/map` | `nav_msgs/OccupancyGrid` | **Global SLAM map** |
| `/local_map` | `nav_msgs/OccupancyGrid` | Local grid for debugging |
| `/odom` | `nav_msgs/Odometry` | EKF-fused odometry with covariance |
| `/path` | `nav_msgs/Path` | Current planned path |
| `/cmd_vel` | `geometry_msgs/Twist` | Commanded velocity |
| `/tf` | `tf2_msgs/TFMessage` | `map→odom` (SLAM correction), `odom→base_link` |

### Subscribed

| Topic | Type | Purpose |
|-------|------|---------|
| `/goal_pose` | `geometry_msgs/PoseStamped` | Simple goal injection |
| `/initialpose` | `geometry_msgs/PoseWithCovarianceStamped` | Set initial pose |

### Action Servers

| Action | Type |
|--------|------|
| `navigate_to_pose` | `nav2_msgs/action/NavigateToPose` |

### Services

| Service | Type |
|---------|------|
| `/save_map` | `std_srvs/srv/Empty` |
| `/clear_costmap` | `std_srvs/srv/Empty` |
| `/reinitialize_global_localization` | `std_srvs/srv/Empty` |

## Usage

### Standalone
```bash
ros2 launch aimee_nav aimee_nav.launch.py
```

### Send a goal (topic)
```bash
ros2 topic pub /goal_pose geometry_msgs/PoseStamped "{
  header: {frame_id: 'map'},
  pose: {position: {x: 2.0, y: 1.0}, orientation: {w: 1.0}}
}"
```

### Send a goal (action)
```bash
ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose "{
  pose: {header: {frame_id: 'map'}, pose: {position: {x: 2.0, y: 1.0}, orientation: {w: 1.0}}}
}"
```

## Parameters

See `config/aimee_nav_params.yaml` for all tunable parameters.

Key parameters:
- `navigation_mode`: `"reactive"` (avoid only) or `"planned"` (goal-directed with A*)
- `safety_distance_m`: Stop/turn when obstacle is this close
- `grid_size_m`: Local map size in meters
- `max_speed`: Maximum linear speed in m/s

## License

MPL-2.0

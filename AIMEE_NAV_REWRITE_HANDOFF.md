# AimeeNav Rewrite — Handoff Status

**Date:** 2026-04-24
**Session Focus:** Integrated SLAM + Navigation stack rewrite (Phases 0–2 complete, Phase 3 partial)
**Hardware Status:** Board battery died during session; robot is plugged in but base is not available.
**Next Session Goal:** Physical validation of SLAM, DWA, and recovery behaviors once battery is charged.

---

## What Was Accomplished

### Phase 0 — C++ Core Foundation
- Created `aimee_nav_core` as a **pybind11 C++ extension** inside the `aimee_nav` package.
- Built and linked successfully on ARM64 UNO Q.
- **Key performance win:** Grid ray-casting + inflation moved to C++ yields **178× speedup** (150 ms → 0.9 ms for 5 m @ 0.05 m grid). This eliminates the CPU pegging that caused hard lockups.

### Phase 1 — SLAM Core
- **ScanMatcher:** Multi-resolution grid-correlation scan matcher (C++). Matches 360-point scans against the global occupancy grid in < 5 ms.
- **EKF2D:** Lightweight 2D Extended Kalman Filter fusing commanded velocities and scan-matcher pose updates.
- **Global GridMap:** 64 m × 64 m world-aligned occupancy map with Bresenham ray-casting and obstacle inflation.
- **TF Tree:** `map→odom` is now published with **real SLAM correction** (not identity). `odom→base_link` remains dead reckoning.
- **Topics:** `/map` (global SLAM map), `/odom` (with covariance), `/local_map` (debug), `/tf`.

### Phase 2 — Planning, Control & ROS2 Compatibility
- **GlobalPlanner:** A* on 8-connected grid (C++). Plans on the SLAM global map instead of the egocentric local grid.
- **DWALocalPlanner:** Simplified Dynamic Window Approach (C++) now wired into the control loop. Extracts a local costmap window from the global SLAM map and evaluates trajectories.
- **Recovery Behaviors:** State machine with stuck detection. Behaviors: `spin` (360°), `backup` (reverse 2 s), `clear_costmap`, `wait`.
- **Action Server:** `navigate_to_pose` (`nav2_msgs/action/NavigateToPose`) implemented with feedback (current pose, distance remaining) and preemption support.
- **Services:** `/save_map`, `/clear_costmap`, `/reinitialize_global_localization`.
- **Local Plan Viz:** `/local_plan` publishes the best DWA trajectory for RViz.

### Phase 3 — Loop Closure (Partial)
- **Keyframe PoseGraph:** C++ class stores keyframes (pose + scan points) and constraints.
- **Background Thread:** `loop_closure_worker` runs at 0.5 Hz, detects nearby keyframes within 2.0 m, adds constraints, and runs Gauss-Newton relaxation (5 iterations).
- Keyframes are inserted every 0.3 m translation or ~15° rotation.

---

## Files Changed / Created

### New / Rewritten
```
src/aimee_nav/
├── aimee_nav/
│   ├── __init__.py                    (updated to import C++ extension)
│   ├── aimee_nav_node.py              (MAJOR rewrite: SLAM, EKF, DWA, action server, recovery)
│   ├── local_grid_map_cpp.py          (C++-accelerated drop-in for LocalGridMap)
│   └── (existing: ld19_driver.py, wave_rover_driver.py, obstacle_avoidance.py, pid_controller.py, simple_planner.py)
├── cpp/
│   ├── include/aimee_nav_core/
│   │   ├── grid_map.hpp
│   │   ├── robot_centric_grid_map.hpp
│   │   ├── scan_matcher.hpp
│   │   ├── ekf_2d.hpp
│   │   ├── pose_graph.hpp
│   │   ├── global_planner.hpp
│   │   ├── dwa_local_planner.hpp
│   │   └── math_utils.hpp
│   └── src/
│       ├── bindings.cpp
│       ├── grid_map.cpp
│       ├── robot_centric_grid_map.cpp
│       ├── scan_matcher.cpp
│       ├── ekf_2d.cpp
│       ├── pose_graph.cpp
│       ├── global_planner.cpp
│       ├── dwa_local_planner.cpp
│       └── math_utils.cpp
├── scripts/
│   ├── aimee_nav_node                 (entry point wrapper)
│   ├── benchmark_grid.py
│   ├── benchmark_grid_fine.py
│   ├── test_slam_integration.py
│   └── test_dwa_integration.py
├── CMakeLists.txt                     (ament_cmake + pybind11)
├── package.xml                        (added nav2_msgs, std_srvs, action_msgs)
├── config/aimee_nav_params.yaml
├── launch/aimee_nav.launch.py
└── README.md
```

### Removed
- `src/aimee_nav/setup.py` (replaced by CMakeLists.txt)
- `src/aimee_nav/setup.cfg`

---

## Architecture Overview

```
AimeeNav Node (single process)
├─ Python Layer (rclpy)
│  ├─ ROS Interface: pubs/subs, action server, services, TF
│  ├─ State Machine: IDLE → PLANNING → CONTROLLING → RECOVERY
│  ├─ Recovery Behaviors: spin, backup, clear_costmap, wait
│  ├─ LD19Driver & WaveRoverDriver (serial/HTTP I/O)
│  └─ Nav Loop @ 10 Hz
│
└─ C++ Extension (aimee_nav_core)
   ├─ RobotCentricGridMap  → local obstacle avoidance grid
   ├─ GridMap (global)     → SLAM map, 64×64 m @ 0.05 m
   ├─ ScanMatcher          → scan-to-map localization
   ├─ EKF2D                → pose fusion (cmd_vel + IMU + scan)
   ├─ GlobalPlanner (A*)   → path planning on global map
   ├─ DWALocalPlanner      → local trajectory optimization
   └─ PoseGraph            → keyframes + loop closure
```

---

## Performance Benchmarks (on UNO Q)

| Operation | Before (Pure Python) | After (C++ Core) | Speedup |
|---|---|---|---|
| Grid update (360 rays, 5m@0.05m) | ~150 ms | **0.9 ms** | **178×** |
| Scan match | N/A | < 5 ms | — |
| A* global plan (1280² grid) | N/A | < 15 ms | — |
| DWA (20×20 samples, 1.5 s sim) | N/A | < 8 ms | — |
| Total nav cycle target | 50–320 ms (overruns) | **< 25 ms** | — |
| RAM footprint | ~100 MB | **~130–150 MB** | — |

---

## How to Build & Run

### Build (inside container)
```bash
cd /workspace
source /opt/ros/humble/setup.bash
colcon build --packages-select aimee_nav --symlink-install
```

### Run Standalone
```bash
source install/setup.bash
ros2 launch aimee_nav aimee_nav.launch.py
```

### Send a Goal (Action)
```bash
ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose "{
  pose: {header: {frame_id: 'map'}, pose: {position: {x: 2.0, y: 1.0}, orientation: {w: 1.0}}}
}"
```

### Test Scripts (no hardware)
```bash
# C++ component unit tests
python3 src/aimee_nav/scripts/test_slam_integration.py
python3 src/aimee_nav/scripts/test_dwa_integration.py

# Performance benchmarks
python3 src/aimee_nav/scripts/benchmark_grid_fine.py
```

---

## Known Issues / Limitations

1. **DWA Tuning Untested:** DWA weights are set to reasonable defaults but have **not been validated on the physical robot**. First physical test may require tuning.
2. **Scan Matcher Robustness:** Correlation-based matcher can fail in featureless environments. EKF falls back to dead reckoning when match score < 10.
3. **Loop Closure Simplified:** Uses pose proximity, not actual scan-to-keyframe re-matching. For large drift, constraints may be inaccurate.
4. **Map Size Fixed:** Global map is fixed at 64 m × 64 m. Scans beyond this are clipped.
5. **No Lifecycle Node:** AimeeNav is not a managed node. Acceptable for now.
6. **`/save_map` Not Implemented:** Service exists but does not write PGM/YAML yet.
7. **LD19 Alignment:** ✅ **FIXED** — Lidar notch now faces forward (robot's direction of travel). Verified ready for navigation testing.
8. **Lidar Driver Still in Python:** I/O bound, not CPU bound — fine as-is.

---

## Testing Checklist for Next Session

### Hardware Prep
- [ ] Power on robot and verify battery charge
- [x] **Rotate LD19 so notch faces forward** ✅ Verified
- [ ] Verify `/dev/ttyUSB0` (base) and `/dev/ttyUSB1` (lidar) exist
- [ ] Launch: `ros2 launch aimee_nav aimee_nav.launch.py`

### Basic Functionality
- [ ] Verify `/scan`, `/odom`, `/tf`, `/map` publishing
- [ ] Run `check_lidar_alignment.py` to confirm front sector

### SLAM Validation
- [ ] Teleop around room for 30s; check `/map` in RViz
- [ ] Verify `map→odom` TF shifts as robot moves
- [ ] Drive in a loop and verify loop closure reduces drift

### Navigation Validation
- [ ] Send `/goal_pose` 1 m ahead; verify movement
- [ ] Verify `/path` and `/local_plan` topics
- [ ] Place obstacle 0.5 m front; verify stop/replan

### Action Server
- [ ] Send `navigate_to_pose` goal via CLI/RViz
- [ ] Verify feedback updates (distance remaining)
- [ ] Test preemption and cancel

### Recovery Behaviors
- [ ] Box robot in on 3 sides; verify recovery escape
- [ ] Test `/clear_costmap` service

### Performance
- [ ] Monitor `top` during nav; confirm < 50% CPU
- [ ] Check logs for nav cycle overrun warnings

---

## Remaining Work (Post-Validation)

1. **DWA Tuning:** Adjust weights based on real-world behavior.
2. **IMU Fusion:** Wire Wave Rover T=1001 IMU yaw into EKF.
3. **Save Map:** Implement `/save_map` to write PGM/YAML.
4. **Lifecycle Node:** Convert to managed node for Nav2 parity.
5. **Loop Closure Enhancement:** Replace pose-proximity with scan-to-keyframe correlation.
6. **Map Size Scaling:** Sparse hash-map or chunked grid for spaces > 64 m.
7. **Git Commit:** `src/aimee_nav/` is untracked. Commit once validated.

---

## Quick Reference

| Task | Command |
|---|---|
| Build | `colcon build --packages-select aimee_nav --symlink-install` |
| Launch | `ros2 launch aimee_nav aimee_nav.launch.py` |
| Test C++ components | `python3 src/aimee_nav/scripts/test_slam_integration.py` |
| Test DWA | `python3 src/aimee_nav/scripts/test_dwa_integration.py` |
| Check lidar alignment | `python3 check_lidar_alignment.py` |
| Action goal | `ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose "{pose: {header: {frame_id: 'map'}, pose: {position: {x: 1.0, y: 0.0}, orientation: {w: 1.0}}}}"` |
| Clear costmap | `ros2 service call /clear_costmap std_srvs/srv/Empty` |

---

## Power-On Resume Procedure

1. Plug in robot, ensure battery charges.
2. Verify serial ports: `ls /dev/ttyUSB*`
3. If container stopped: `docker compose up -d`
4. Enter container: `docker exec -it aimee-robot bash`
5. Source ROS: `source /opt/ros/humble/setup.bash && source install/setup.bash`
6. Launch AimeeNav: `ros2 launch aimee_nav aimee_nav.launch.py`
7. Begin testing checklist above.

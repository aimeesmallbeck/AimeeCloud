# Aimee Robot - Session Checkpoint

**Date:** 2026-04-28
**Session Focus:** C++ Vision Pipeline Migration & Monitor Integration
**Status:** 🟢 Vision pipeline successfully migrated to C++ and integrated with monitor dashboard.

---

## 🎉 MISSION ACCOMPLISHED!

### What Was Done Today

1. **Vision Pipeline Migrated to C++**
   - Completely rewrote `color_detector_node` and `object_tracker_node` from Python to C++ using `rclcpp` and OpenCV.
   - Configured nodes as ROS 2 components (`rclcpp_components`) to allow zero-copy pointer sharing (Intra-Process Communication).
   - Changed package type from `ament_python` to `ament_cmake`.
   - Eliminated Python GIL and serialization overhead for pixel processing.

2. **Decoupled Control from Streaming (`obsbot_node.py`)**
   - Removed blocking Python-based JPEG encoding and heavy `ffmpeg` / `v4l2-ctl` subprocess fallbacks from the `/camera/capture_snapshot` service.
   - The service now relies strictly on the fast, zero-contention buffered frame provided by the native hardware stream.

3. **Optimized Data Recording (`dataset_recorder.py`)**
   - Refactored recording logic to eliminate Python-level subscription to high-bandwidth topics like `/camera/image_raw`.
   - The node now spawns the native C++ `ros2 bag record` tool as a subprocess, preventing the Python `rclpy` executor from deserializing massive image byte arrays.

4. **Monitor Dashboard Live Camera Integration**
   - Embedded the Live Camera View directly onto the main page of the AIMEE ROS2 Monitor Dashboard.
   - Updated the USB Camera node to use the camera's natively supported `YUYV 4:2:2` format at `640x480` to resolve segmentation faults caused by unsupported MJPEG formats.
   - CPU usage dropped to ~60% with full 30 FPS available to the C++ tracking nodes.

### Files Modified

```
/home/arduino/aimee-robot-ws/
├── src/aimee_vision_pipeline/                           [MIGRATED TO C++]
│   ├── include/aimee_vision_pipeline/color_detector.hpp [NEW]
│   ├── include/aimee_vision_pipeline/object_tracker.hpp [NEW]
│   ├── src/color_detector.cpp                           [NEW]
│   ├── src/color_detector_main.cpp                      [NEW]
│   ├── src/object_tracker.cpp                           [NEW]
│   ├── src/object_tracker_main.cpp                      [NEW]
│   ├── CMakeLists.txt                                   [NEW]
│   └── package.xml                                      [UPDATED]
├── src/aimee_vision_obsbot/
│   └── aimee_vision_obsbot/obsbot_node.py               [UPDATED - Snapshot optimizations]
├── src/aimee_lerobot_bridge/
│   └── aimee_lerobot_bridge/dataset_recorder.py         [UPDATED - Native rosbag recording]
├── src/aimee_ros2_monitor/
│   ├── aimee_ros2_monitor/monitor_node.py               [UPDATED - USB cam resolution/format fix]
│   └── templates/index.html                             [UPDATED - Embedded live camera feed]
└── CHECKPOINT.md                                        [THIS FILE - updated]
```

---

# Aimee Robot - Session Checkpoint

**Date:** 2026-04-26 (Late Session — Exploration & Mapping Test)
**Session Focus:** AimeeNav exploration test, map viewer integration, scan matcher diagnosis on UGV02 (Ron)
**Previous Session:** AimeeNav audit fixes verified; stack healthy and stationary.
**Status:** 🔴 Exploration works but scan matcher fails during motion — map does not update beyond initial scan. Robot odometry tracks correctly.

---

## 🧪 Exploration Test Results

### Code Changes Made
| Change | File | Status |
|--------|------|--------|
| Frontier scoring: prefers open areas + farther frontiers | `aimee_nav_node.py` | ✅ |
| Auto-save on shutdown | `aimee_nav_node.py` | ✅ |
| Rosbridge in robot.launch.py | `robot.launch.py` | ✅ |
| `world_to_grid` unpack bug fix (returns `(ok, gx, gy)`) | `aimee_nav_node.py` | ✅ |

### Test Execution
- **3-minute exploration run** completed
- Robot moved autonomously, found frontiers, avoided obstacles
- **Map saved:** `/root/aimee_maps/map_20260426_141933.json` (341 KB)
- **Map viewer:** Connected via `ws://localhost:9090`, served at `http://localhost:8080/map_viewer.html`

### Critical Finding
**Scan matcher fails during motion:**
- Scores consistently **9–15** vs threshold **30.0**
- Map never updates beyond initial stationary scan
- Robot odometry works (pose tracks on viewer), but SLAM map is frozen
- This is the same issue noted in previous session: "scan matcher can't track rotation"
- Without scan matching, SLAM cannot build maps during exploration

### System Issues During Session
- Full `robot.launch.py` launched entire stack (voice manager, monitor, intent router, arm nodes, etc.) — caused CPU overload
- Non-essential nodes killed manually; only nav + base + rosbridge kept
- 88 zombie PIDs remain in container from previous unclean restarts
- Robot moved unexpectedly when exploration was enabled; zero-vel stop required multiple attempts

### Next Steps
1. **Fix scan matcher** — likely needs larger search radius/angle, lower threshold, or rotation-aware matching
2. **Test with manual goal** instead of exploration to isolate scan matcher behavior
3. **Launch minimal stack only** — do not use full `robot.launch.py` for nav testing
4. **Commit uncommitted changes** — frontier scoring, auto-save, rosbridge launch

---

# Aimee Robot - Session Checkpoint

**Date:** 2026-04-26 (Continued)
**Session Focus:** AimeeNav audit fixes, build verification, and safe launch on UGV02 (Ron)
**Previous Session:** Lost unexpectedly at ~18:12 UTC during troubleshooting. Recovered and verified stack health.
**Status:** 🟢 AimeeNav launches cleanly, robot stationary, all audit fixes verified in code. Ready for exploration test (requires user confirmation to move robot).

---

## ✅ What Was Accomplished (Audit Fixes Verified)

All **5 critical issues** from `AIMEENAV_AUDIT_RON_2026-04-25.md` were implemented and verified:

| # | Audit Issue | Status | Details |
|---|-------------|--------|---------|
| 1 | **Duplicate `/odom` publishers** | ✅ Fixed | `_publish_odom()` returns early when `base_interface == 'ros'`. Controller owns `/odom`. |
| 2 | **Hardcoded reactive/recovery speeds** | ✅ Fixed | Reactive panic/caution turns, recovery backup, and exploration bias now use `self._max_speed` and `self._max_angular`. |
| 3 | **Global map fixed at 10 m** | ✅ Fixed | `global_map_size_m` raised to **50.0** |
| 4 | **EKF covariance propagation bug** | ✅ Fixed | `ekf_2d.cpp` now implements `F*P*F^T + Q*dt` |
| 5 | **`_std` naming ambiguity** | ✅ Fixed | Renamed to `scan_match_pos_variance` / `scan_match_yaw_variance` |

**Additional changes:**
- `base_interface: "ros"` fully implemented — AimeeNav subscribes to `/odom`, publishes `/cmd_vel` (RELIABLE QoS)
- Scan matcher parameters exposed in YAML (`search_radius_m`, `search_angle_rad`, `score_threshold`)
- `robot.launch.py` forwards base params to `aimee_nav_node`
- `ron.yaml` updated with calibrated UGV02 params (`ticks_per_meter: 106.0`, `base_interface: "ros"`)
- IMU yaw fusion removed from nav node (`imu_yaw_variance` deleted)
- `enable_exploration` changed from `true` to `false` in default YAML for safe launch

---

## 🚀 Launch Verification Results

**Launch command used:**
```bash
ros2 launch aimee_bringup robot.launch.py use_voice:=false use_vision:=false use_llm:=false use_arm:=false
```

**Verified healthy:**
- ✅ `/aimee_nav` node started with "Base interface: ROS topics"
- ✅ `/base_controller` connected to `/dev/ttyACM0`, encoder odometry ON
- ✅ `/scan` publishing (LD19 lidar active)
- ✅ `/odom` publishing from base controller (`frame_id: odom`, `child_frame_id: base_link`)
- ✅ `/cmd_vel` publishing zeros — **robot is stationary**
- ✅ `/map` publishing (global occupancy grid building)
- ✅ Scan matching working (scores 37–84, well above threshold 30.0)
- ✅ Cycle timing excellent: ~2–11 ms total (target 333 ms @ 3 Hz)
- ✅ One transient nav cycle overrun at startup (531 ms) — initialization hiccup, not recurring
- ✅ `map -> odom` TF publishing (every 50 s due to `publish_decimation: 150`)
- ✅ `odom -> base_link` TF publishing from base controller at ~20 Hz
- ⚠️ `base_link -> base_laser` TF also on 50 s decimation — may affect RViz visualization

**Warnings observed (non-critical):**
- `tts_node`: Lemonfox API key missing, pygame/ALSA failure (expected — TTS not in use)
- `monitor_node`: Failed subscription for `/intent/classified` (DDS allocator issue, non-blocking)
- `base_controller`: One command timeout during startup overrun (watchdog behaved correctly)

---

## 🎯 Next Steps (Require User Confirmation to Move Robot)

1. **Exploration test** — Set `enable_exploration=true` and observe autonomous wandering
2. **Reactive obstacle avoidance** — Place object in front and verify avoidance
3. **Goal-directed navigation** — Publish a `PoseStamped` goal and verify robot turns/moves toward it
4. **Map save** — Run `save_map` service after a brief exploration
5. **Commit changes** — 18 files modified, all uncommitted

---

## 📋 Pre-Test Checklist (from Audit)

| # | Issue | Severity | Fix Location |
|---|-------|----------|-------------|
| 1 | Duplicate `/odom` publishers | HIGH | `aimee_nav_node.py` — skip `/odom` pub when `base_interface: "ros"` |
| 2 | Hardcoded 0.5 rad/s / -0.15 m/s speeds | HIGH | `aimee_nav_node.py` — replace constants with param refs |
| 3 | Global map fixed at 10 m | HIGH | `aimee_nav_params.yaml` — raise `global_map_size_m` |
| 4 | EKF covariance propagation bug | HIGH | `ekf_2d.cpp` — `P = F*P*F^T + Q` |
| 5 | `_std` naming ambiguity | HIGH | Rename to `_variance` or square values |
| 6 | Local grid too coarse (21×21) | MEDIUM | Increase `grid_size_m` / reduce `grid_resolution_m` |
| 7 | Hardcoded scan-match thresholds | MEDIUM | Expose in YAML |
| 8 | Process noise Q not scaled by dt | MEDIUM | Multiply by `dt` in `predict()` |
| 9 | Missing param forwarding from launch | MEDIUM | `robot.launch.py` → `aimee_nav_node` |
| 10 | `ugv02_bringup.launch.py` hardcodes | MEDIUM | Accept `control_mode` / `wheel_separation` args |

---

## 🔧 Current Hardware Configuration (Ron)

| Component | Connection | Parameters |
|-----------|-----------|------------|
| UGV02 base | `/dev/ttyACM0` serial | `ticks_per_meter: 200.0`, `wheel_separation: 0.172` |
| LD19 lidar | `/dev/ttyUSB0` | `lidar_downsample: 6` (60 points) |
| Control mode | `velocity` (T=13) | `max_speed: 0.5`, `max_angular: 1.0` (controller); `0.3` / `0.3` (AimeeNav) |
| Odometry | Encoder-based | Real `odl`/`odr` from T=1001; dead-reckoning fallback disabled |
| EKF | C++ extension | Lower Q/P after encoder tuning (see 2026-04-25 late session) |

---

## 🚀 Launch Command

```bash
# Full stack with AimeeNav integrated nav (no Nav2/SLAM Toolbox)
docker exec -it aimee-robot bash -c \
  "source /ros_entrypoint.sh && source /workspace/install/setup.bash && \
   ros2 launch aimee_bringup robot.launch.py use_voice:=false use_vision:=false use_llm:=false"

# In another terminal — enable exploration
ros2 param set /aimee_nav enable_exploration true
ros2 param set /aimee_nav max_speed 0.2
ros2 param set /aimee_nav max_angular 0.3
```

---

## 📝 Notes

- **Battery:** Monitor voltage via T=1001 `v` field (centivolts). Charge if < 11.5V.
- **IMU yaw:** Untested on UGV02. If scan matcher force-fits during rotation, may need to skip scan matching when turning.
- **Map save dir:** `~/aimee_maps` (inside container = `/root/aimee_maps`)
- **Safety:** Keep hand on e-stop / power switch. First exploration run in small, clear area.

---

## 🗂️ Files of Interest

```
src/aimee_nav/
├── aimee_nav/aimee_nav_node.py           [Navigation loop, exploration, recovery]
├── aimee_nav/wave_rover_driver.py        [Serial encoder/IMU parsing]
├── cpp/src/ekf_2d.cpp                    [Covariance propagation fix needed]
├── cpp/src/scan_matcher.cpp              [Threshold exposure]
├── config/aimee_nav_params.yaml          [All tunables]
└── launch/aimee_nav.launch.py            [Standalone launch]

src/aimee_ugv02_controller/
└── aimee_ugv02_controller/ugv02_controller_node.py   [Encoder odometry, /odom pub]

AIMEENAV_AUDIT_RON_2026-04-25.md         [Full audit with line references]
```

---

# Aimee Robot - Session Checkpoint

**Date:** 2026-04-25 (Late Session)
**Session Focus:** Map persistence, waypoints, localization mode, precise movement control, lidar downsampling
**Git Commit:** `4bef2b9`

---

## 🎉 MISSION ACCOMPLISHED!

### What Was Done Today

1. **Added Map Save / Load**
   - `save_map` service serializes global occupancy grid + pose graph + EKF state to timestamped JSON
   - `load_map` service loads the most recent saved map and auto-enables localization mode
   - File format: JSON with base64-encoded grid data
   - C++ changes: exposed `PoseGraph.constraints()` and `GridMap.set_data()` in pybind11 bindings
   - Helper scripts: `save_map.py`, `load_map.py`

2. **Added Named Waypoints**
   - Load waypoints from YAML file via `waypoints_file` parameter
   - `/go_to_waypoint_name` topic accepts `std_msgs/String` to navigate by name
   - Example: `ros2 topic pub /go_to_waypoint_name std_msgs/msg/String '{data: "kitchen"}'`
   - Example YAML in `config/waypoints_example.yaml`
   - Helper script: `go_to_waypoint.py`

3. **Added Velocity Smoothing**
   - `WaveRoverDriver` now supports `accel_limit_linear` and `accel_limit_angular`
   - Ramp-rate limits velocity changes to prevent jerky starts/stops
   - Parameters in `aimee_nav_params.yaml`

4. **Added Localization Mode**
   - `localization_mode` parameter + `/set_localization_mode` service
   - When enabled: scan matching corrects EKF pose but does NOT modify the global map
   - Loop closure thread is paused in localization mode
   - Map load auto-enables localization mode

5. **Fixed Wheel Speed Formula**
   - Previous formula `diff = angular_z / max_speed * angular_scale` was physically incorrect
   - Caused extreme wheel differential amplification (any turn = max spin)
   - **Fix:** Replaced with proper differential-drive kinematics:
     ```
     v_left  = linear_x - angular_z * wheel_sep / 2
     v_right = linear_x + angular_z * wheel_sep / 2
     ```
   - Added motor dead-zone compensation: boosts small commands to MIN_POWER=0.18

6. **Added IMU Yaw Fusion (Later Found Unreliable)**
   - Added `_ekf.update_imu_yaw()` calls in nav cycle using relative IMU yaw
   - Tracks IMU yaw offset on EKF reset
   - **CRITICAL FINDING:** IMU yaw is wildly inaccurate during motion
     - User observed ~90° physical spin; IMU reported only 15°
     - This caused the EKF to think the robot hadn't turned, leading to repeated turn commands
   - **Decision:** IMU fusion should be REMOVED or disabled in next session

7. **Downsampled Lidar for CPU Efficiency**
   - `lidar_downsample: 6` parameter uses every 6th point (60 points instead of 360)
   - Scan matching frequency increased from 2 Hz → 5 Hz
   - Scan match time dropped from ~45ms → ~20ms per cycle
   - Total nav cycle well under 200ms target even at 5Hz

8. **Tuned Heading PID**
   - `heading_kp`: 2.0 → 0.6 (less aggressive)
   - `heading_kd`: 0.5 → 1.0 (more damping)
   - Added explicit state machine states: `EXPLORING`, `GOING_TO_GOAL`

9. **Created Motion Test Scripts**
   - `test_motion.py`: ROS-based goal-directed turn tests
   - `test_a.py`: Direct HTTP motor command tests with IMU yaw measurement

### Critical Hardware Findings from Testing

| Finding | Impact | Status |
|---------|--------|--------|
| **IMU yaw is broken** | Reports 15° for 90° physical spin | Must remove from EKF |
| **Scan matcher can't track rotation** | Force-fits rotated scans back to origin pose | Needs higher score threshold or rotation-aware matching |
| **Robot has two turn speeds** | Fast phase overshoots; slow phase is smooth and good | Cap max_angular lower |
| **Motor dead zone ~0.18** | Commands below this produce no motion | Compensated in driver |
| **Battery dropping** | Started at 12.39V, now ~12.05V | Needs charging soon |

### Current Parameters (`aimee_nav_params.yaml`)

```yaml
nav_rate_hz: 5.0
lidar_downsample: 6           # 60 points
scan_match_interval: 0.2      # 5 Hz
angular_scale: 0.25           # Calibrated for hard floor + dead zone
heading_kp: 0.6
heading_kd: 1.0
max_speed: 0.3
accel_limit_linear: 0.5
accel_limit_angular: 1.0
imu_yaw_variance: 0.05
localization_mode: false
enable_exploration: false     # Set true for mapping runs
map_save_dir: "~/aimee_maps"
```

### Files Modified

```
src/aimee_nav/
├── aimee_nav/aimee_nav_node.py           [IMU fusion, downsampling, localization, state machine]
├── aimee_nav/wave_rover_driver.py        [Kinematic fix, dead-zone comp, velocity smoothing]
├── cpp/include/aimee_nav_core/grid_map.hpp      [set_data() method]
├── cpp/include/aimee_nav_core/pose_graph.hpp    [constraints() getter]
├── cpp/src/bindings.cpp                  [Expose new methods]
├── config/aimee_nav_params.yaml          [All new params]
├── config/waypoints_example.yaml         [New]
├── scripts/test_motion.py                [New]
├── scripts/go_to_waypoint.py             [New]
├── scripts/save_map.py                   [New]
├── scripts/load_map.py                   [New]
└── CMakeLists.txt                        [Install new scripts]
```

### Known Issues / Next Steps (Priority Order)

1. **REMOVE IMU yaw fusion** — It makes heading tracking worse, not better. The EKF works better with dead reckoning + scan matching alone.
2. **Cap max_angular at ~0.4 rad/s** — User observed the "slow" turn speed is good; the "fast" speed overshoots. Current max_angular=1.5 is too high.
3. **Fix scan matcher for rotation** — When robot turns 90°, scan matcher force-fits back to original pose. Options:
   - Increase score threshold (currently 10.0, maybe raise to 30.0+)
   - Skip scan matching when angular velocity is high
   - Use scan-to-scan matching instead of scan-to-map for rotation detection
4. **Charge battery** — Down to ~12.0V; torque will suffer on carpet.
5. **Test goal-directed navigation** — After fixes 1-3, test a 90° turn goal and verify the robot turns once, stops, and faces the goal.
6. **Save a good map** — Once movement is precise, do an exploration run and save the map.

---

# Aimee Robot - Session Checkpoint

**Date:** 2026-04-24
**Session Focus:** Hardware validation of AimeeNav integrated navigation; fixes for autonomous wandering, motor power, and turning

---

## 🎉 MISSION ACCOMPLISHED!

### What Was Done Today

1. **Lidar Alignment Verified**
   - Confirmed LD19 notch faces forward (robot's direction of travel)
   - Front sector (0°) reads ~0.6m, consistent with physical obstacle placement
   - Updated `AIMEE_NAV_REWRITE_HANDOFF.md` and `CHECKPOINT.md` to reflect fixed alignment

2. **Fixed EKF Covariance Binding Bug**
   - `covariance()` pybind11 binding returned a 3×3 numpy array, but Python code indexed it as flat
   - `float(P[0])` on a 3×3 array threw "only length-1 arrays can be converted to Python scalars"
   - **Fix:** Changed binding shape from `{3, 3}` to `{9}` in `bindings.cpp`
   - Rebuilt C++ extension successfully on ARM64 UNO Q

3. **Fixed Autonomous Wandering (Critical Safety Bug)**
   - `enable_reactive: true` caused the robot to drive forward autonomously whenever front was clear — even with no goal set
   - In a confined space, this created a panic/reverse loop (moving toward walls, then emergency reversing)
   - **Fix:** Changed `elif self._enable_reactive:` to `elif self._enable_reactive and has_goal:` in `aimee_nav_node.py`
   - Robot now stays stationary when idle

4. **Fixed YAML Duplicate Keys**
   - `aimee_nav_params.yaml` had TWO `nav_rate_hz` and TWO `publish_decimation` entries
   - The "Timing" section at the bottom (`nav_rate_hz: 4.0`, `publish_decimation: 10`) overrode the intended values
   - **Fix:** Removed the duplicate "Timing" section; kept `nav_rate_hz: 5.0` and `publish_decimation: 50`

5. **Fixed Motor Power (50% → 100%)**
   - `WaveRoverDriver.send_velocity()` scaled wheel commands to `[-0.5, 0.5]` — only 50% of available motor torque
   - Robot struggled with hard-floor-to-rug transitions
   - **Fix:** Changed clamp from `0.5` to `1.0` (Waveshare T=1 protocol supports `[-1.0, 1.0]`)

6. **Fixed Turning (Added `angular_scale: 4.0`)**
   - `angular_scale` was not defined in `aimee_nav_params.yaml`, defaulting to `1.0`
   - N20 motors have a deadband; small angular commands produced no actual wheel differential
   - Robot only went forward/back, never turned
   - **Fix:** Added `angular_scale: 4.0` to `aimee_nav_params.yaml` (matches `minnie.yaml` base controller setting)

7. **Hardware Validation Results**
   - Goal: 0.5m forward — robot moved, turned, and progressed to `x=0.467m, y=-0.231m`
   - Turning is now visible and effective
   - Full motor power successfully traverses rug transitions
   - Y-drift is expected (no wheel encoders; dead-reckoning only)

### Current Parameters (`aimee_nav_params.yaml`)

```yaml
nav_rate_hz: 5.0                 # 200ms period
publish_decimation: 50           # Viz topics every ~10s
angular_scale: 4.0               # N20 deadband compensation
max_speed: 0.5
safety_distance_m: 0.50
```

### Files Modified

```
/home/arduino/aimee-robot-ws/
├── src/aimee_nav/
│   ├── aimee_nav/aimee_nav_node.py              [UPDATED - reactive mode requires has_goal]
│   ├── aimee_nav/wave_rover_driver.py           [UPDATED - full motor power [-1.0, 1.0]]
│   ├── cpp/src/bindings.cpp                     [UPDATED - covariance flat array shape {9}]
│   └── config/aimee_nav_params.yaml             [UPDATED - angular_scale, removed dupes]
├── AIMEE_NAV_REWRITE_HANDOFF.md                 [UPDATED - lidar aligned]
└── CHECKPOINT.md                                [THIS FILE - updated]
```

### Known Issues / Next Steps

1. **CPU saturation:** AimeeNav uses ~90% of one core (5Hz loop, ~200ms cycles). Functional but no headroom.
2. **Odometry drift:** No wheel encoders on Wave Rover; pure dead-reckoning drifts significantly in y-axis.
3. **Map publishing heavy:** `_publish_map()` serializes 1.6M cells in Python every 50 cycles; future optimization needed.
4. **IMU fusion pending:** Wave Rover T=1001 IMU yaw available but not yet fused into EKF.
5. **DWA tuning untested:** First successful movement achieved; weights may need adjustment for different environments.
6. **Action server:** `navigate_to_pose` implemented but not yet tested with preemption/cancel.

---

# Aimee Robot - Session Checkpoint

**Date:** 2026-04-23 (Late Session)
**Session Focus:** Create AimeeNav integrated navigation node; diagnose & fix CPU pegging on obstacle avoidance test

---

## 🎉 MISSION ACCOMPLISHED!

### What Was Done Today

1. **Created `aimee_nav` Package — Integrated Navigation Node (AimeeNav)**
   - New package `src/aimee_nav/` with self-contained navigation node
   - Directly interfaces with LD19 lidar (`ld19_driver.py`) and Wave Rover (`wave_rover_driver.py`)
   - Performs local mapping (`local_grid_map.py`), path planning (`simple_planner.py`), and obstacle avoidance (`obstacle_avoidance.py`) all in-process
   - Publishes `/scan`, `/map`, `/odom`, `/tf`, `/path`, `/cmd_vel` for visualization and interoperability
   - Designed to replace the distributed stack (`ldlidar` → `slam_toolbox` → `nav2` → `base_controller`) to reduce RAM and DDS overhead on the UNO Q

2. **Diagnosed CPU Pegging During Obstacle Avoidance Test**
   - **Symptom:** UNO Q became completely unresponsive during `obstacle_test.py`; required hard restart. Two core dumps present (`core.3753` 18:21, `core.15211` 19:09).
   - **Root cause:** AimeeNav's `_navigation_loop` defaulted to 20 Hz (50 ms period). Each `_nav_cycle()` ran expensive pure-Python Bresenham ray-casting in `update_from_scan()` for ~360 lidar points, plus obstacle inflation. On the UNO Q this took >50 ms, causing the loop to spin continuously with no sleep, pegging CPU at 100%.
   - **Contributing factors:**
     - `/map` published at 10 Hz (`publish_decimation: 2`) — serializing a 10,000-cell `OccupancyGrid` in Python is heavy
     - `obstacle_test.py` bypassed `minnie.yaml` optimized params and used hardcoded defaults
     - Grid update ran even in pure reactive mode where it is unused (`enable_planning=False`)

3. **Applied Performance Fixes**
   - Lowered default `nav_rate_hz` from `20.0` → `10.0` (100 ms period, more headroom)
   - Raised default `publish_decimation` from `2` → `10` (viz topics at ~1 Hz instead of 10 Hz)
   - **Skipped grid map update when `enable_planning=False`** — the biggest single optimization; reactive obstacle avoidance only needs sector/VFF analysis, not the occupancy grid
   - Added cycle-overrun warning log in `_navigation_loop` for future diagnosis
   - Hardened `obstacle_test.py` with `_nav_rate = 5.0` and `_publish_decimation = 100` to minimize load during testing
   - Updated `aimee_nav_params.yaml` to reflect new defaults

### Files Modified / Created

```
/home/arduino/aimee-robot-ws/
├── src/aimee_nav/                                       [NEW - integrated navigation package]
│   ├── aimee_nav/aimee_nav_node.py                      [UPDATED - performance fixes]
│   ├── aimee_nav/ld19_driver.py                         [NEW]
│   ├── aimee_nav/wave_rover_driver.py                   [NEW]
│   ├── aimee_nav/local_grid_map.py                      [NEW]
│   ├── aimee_nav/obstacle_avoidance.py                  [NEW]
│   ├── aimee_nav/simple_planner.py                      [NEW]
│   ├── aimee_nav/pid_controller.py                      [NEW]
│   ├── config/aimee_nav_params.yaml                     [UPDATED - conservative defaults]
│   ├── launch/aimee_nav.launch.py                       [NEW]
│   ├── package.xml                                      [NEW]
│   ├── setup.py                                         [NEW]
│   └── README.md                                        [NEW]
├── src/aimee_bringup/launch/robot.launch.py             [UPDATED - integrated nav mode support]
├── src/aimee_bringup/config/robots/minnie.yaml          [UPDATED - navigation_mode: integrated]
├── obstacle_test.py                                     [UPDATED - safe defaults for UNO Q]
├── odom_calibration.py                                  [NEW]
├── goal_movement_test.py                                [NEW]
└── CHECKPOINT.md                                        [THIS FILE - updated]
```

### Notes

- **Do not run `obstacle_test.py` while `robot.launch.py` is already active** — this creates duplicate publishers and potential serial port conflicts. Kill existing stacks first (`docker compose restart aimee-robot` or `ros2 node list` to verify).
- AimeeNav is currently **uncommitted** — `src/aimee_nav/` and test scripts are untracked. Commit once obstacle avoidance is verified.
- The distributed Nav2 stack is still available; set `navigation_mode: distributed` in `minnie.yaml` to revert.

### Obstacle Avoidance Test Results (2026-04-23)

**Run 1 (before angular_scale fix):** Robot detected obstacle (~0.41 m) but did **not turn** — distances remained static for 15 s. Root cause: `WaveRoverDriver` clamped `angular_z` to `max_speed` (0.15 rad/s) instead of a proper angular limit, and did not apply `angular_scale` (4.0) needed for N20 deadband.

**Run 2 (after angular_scale fix):** Robot **turned and reacted** to the obstacle. Front distance varied between 0.26–0.57 m. However, the reactive logic oscillated: when front briefly cleared (>0.50 m), the robot drove straight forward and immediately re-entered the obstacle. Nav cycle overrun persisted at ~320 ms (HTTP latency blocking the nav loop).

**Fixes applied between runs:**
- **Background HTTP sender thread** (`WaveRoverDriver`): Nav loop no longer blocked by ESP32 response time. Overrun warnings eliminated.
- **Persistent turn direction**: Robot now picks left or right and sticks with it until front clears, preventing flip-flopping.
- **Lower drive threshold**: `drive_dist = safety * 1.2` (was 1.5) — robot drives forward sooner after turning away.

**Run 3 (open space):** Robot moved forward steadily for 15 s. Front stayed at ~1.5–1.7 m (clear), while `fr` dropped to ~0.52 m (wall on one side). **User observed robot hit a wall directly in front.**

**Critical discovery — Lidar orientation:** The LD19 lidar notch was pointing **to the right** (90° offset), meaning the "front" sector was actually looking at the robot's left side. This explains why the robot drove forward into walls while the front sensor reading stayed clear. ~~**Action: physically rotate the lidar so the notch faces forward (robot's direction of travel).**~~ ✅ **COMPLETED** — Lidar notch now faces forward. Verified aligned with robot's direction of travel.

**Next steps:**
1. ~~Power down and rotate LD19 so notch points forward (0° aligned with robot front).~~ ✅ Done
2. Re-test obstacle avoidance with correctly aligned lidar.
3. Once verified, commit `aimee_nav` package to git.

---

# Aimee Robot - Session Checkpoint

**Date:** 2026-04-23
**Session Focus:** Fix ESP32 HTTP timeout via rate limiting (RoArm pattern); execute SLAM square test

---

## 🎉 MISSION ACCOMPLISHED!

### What Was Done Today

1. **Diagnosed ESP32 HTTP Command Timeouts**
   - The vexown/wave_rover_driver ESP32 firmware only accepts movement commands via HTTP GET (`/js?json=...`)
   - Serial `/dev/ttyUSB0` is used exclusively for T=1001 continuous feedback (odometry/IMU/battery)
   - The base controller's 10 Hz heartbeat (`heartbeat_interval: 0.1`) overwhelmed the ESP32 web server
   - Result: `<urlopen error timed out>` on nearly every HTTP request

2. **Applied RoArm-M3 HTTP Driver Rate-Limiting Pattern**
   - Studied `aimee_lerobot_bridge/roarm_m3_http_driver.py` which solved the exact same problem
   - Key techniques adapted:
     - `threading.Lock()` around all HTTP sends
     - `Connection: close` header (ESP32 crashes on keep-alive)
     - `min_http_interval = 0.2` (max 5 Hz) — drop requests that arrive too fast
     - Heartbeat self-suppression: skip heartbeat if a command was recently sent via HTTP
   - Changed default `heartbeat_interval` from `0.1` → `0.5` (2 Hz)
   - Increased HTTP timeout from `0.5` → `1.0` seconds

3. **Fixed Launch File Bug: `http_ip` Not Forwarded**
   - `robot.launch.py` was NOT passing `http_ip` from `base_params` to the controller node
   - This meant HTTP mode silently failed when launched via `robot.launch.py`
   - Added both `http_ip` and `heartbeat_interval` forwarding

4. **Built and Tested**
   - `colcon build --packages-select aimee_ugv02_controller aimee_bringup --symlink-install` succeeded
   - Killed stale base controller from previous session (PID 8146 was still running)
   - Launched minimal stack: `robot.launch.py` with all software toggles off (voice/vision/LLM/monitor/skills/intent/cloud/tts)
   - Launched SLAM: `slam.launch.py`
   - Verified nodes: `/base_controller`, `/ldlidar`, `/slam_toolbox` all healthy

5. **Square Test Executed**
   - Ran `square_test.py` (open-loop: forward 1s @ 0.3 m/s, turn ~90° right @ 1.0 rad/s × 4 sides)
   - **Robot moved and turned successfully** — no HTTP timeouts
   - SLAM processed scans without errors (no "queue is full" warnings)
   - Turn accuracy was approximate; square was not geometrically perfect, but a good baseline
   - Watchdog fired briefly between sides due to 0.5s pause in test script (non-critical)

### Files Modified

```
/home/arduino/aimee-robot-ws/
├── src/aimee_ugv02_controller/aimee_ugv02_controller/ugv02_controller_node.py
│   [UPDATED - HTTP rate limiting, Connection: close, 2 Hz heartbeat default]
├── src/aimee_bringup/launch/robot.launch.py
│   [UPDATED - forward http_ip and heartbeat_interval from base_params]
├── src/aimee_bringup/config/robots/minnie.yaml
│   [UPDATED - added heartbeat_interval: 0.5]
└── CHECKPOINT.md
    [THIS FILE - updated]
```

### Running Services (at end of session)

| Service | Container | Status |
|---------|-----------|--------|
| **ROS2 Base Controller** | `aimee-robot` | 🟢 Running (PID 9941) |
| **LD19 Lidar** | `aimee-robot` | 🟢 Running (PID 9945) |
| **SLAM Toolbox** | `aimee-robot` | 🟢 Running (PID 10061) |

### Current Parameters (minnie.yaml)

```yaml
base: "wave_rover"
base_params:
  serial_port: "/dev/ttyUSB0"
  baud_rate: 115200
  wheel_separation: 0.172
  wheel_radius: 0.04
  max_speed: 0.5
  control_mode: "wheel_speed"
  http_ip: "192.168.1.56"
  angular_scale: 4.0            # overcome N20 motor deadband
  heartbeat_interval: 0.5       # max 2 Hz heartbeat
```

### Known Issues / Next Steps

1. **Odometry drift:** T=1001 feedback reports L=0, R=0 (no encoders). Controller integrates commanded velocities for `/odom`. Heading from onboard IMU (`y` field) is available but not yet fused into odometry.
2. **Turn accuracy:** Open-loop square test turns were approximate. For precise navigation, need either:
   - IMU yaw feedback fused into odometry (available from T=1001 `y` field)
   - Nav2 DWB controller with proper `yaw_goal_tolerance`
3. **QoS mismatch:** `/odom` publisher uses `BEST_EFFORT`; some Nav2 nodes may request `RELIABLE`. Non-blocking but should be cleaned up.
4. **Watchdog sensitivity:** `cmd_timeout: 0.5s` triggers during pauses between test sides. For Nav2 continuous operation this is fine, but for discrete motion scripts consider increasing `cmd_timeout`.
5. **Nav2 autonomous test pending:** Once base control is reliable, launch `navigation.launch.py slam:=true` with `use_voice:=false use_llm:=false ...` and let Nav2 drive the square autonomously.

### Hardware State

- **Battery:** Almost depleted (user report at end of session)
- **Serial ports:** `/dev/ttyUSB0` (base), `/dev/ttyUSB1` (lidar)
- **Network:** Base on `192.168.1.56` via HTTP; host `Minnie` on local network

---

# Aimee Robot - Session Checkpoint

**Date:** 2026-04-23
**Session Focus:** Replace Fast DDS with Fast DDS; free disk space; stabilize Nav2/ROS2 middleware

---

## 🎉 MISSION ACCOMPLISHED!

### What Was Done Today

1. **Freed Disk Space on Root Partition**
   - Identified root partition (`/`) was 100% full (9.8G)
   - Removed two unused Arduino brick Docker images:
     - `ghcr.io/arduino/app-bricks/python-apps-base:0.8.0` (768MB)
     - `ghcr.io/arduino/app-bricks/ei-models-runner:0.8.0` (1.33GB)
   - Freed ~2.1GB on root partition; dropped from 100% to 80% usage

2. **Installed Fast DDS in Running Container**
   - Installed `ros-humble-rmw-fastrtps-cpp` (v1.3.4) plus dependencies inside the running `aimee-robot` container via `apt-get install --allow-unauthenticated`
   - Committed the updated container to a new image: `aimee-robot:cyclone-installed`

3. **Switched RMW from Fast DDS to Fast DDS**
   - Updated `docker-compose.yml`: changed image to `aimee-robot:cyclone-installed`, set `RMW_IMPLEMENTATION=rmw_fastrtps_cpp`, removed `FASTRTPS_DEFAULT_PROFILES_FILE` and `FASTRTPS_PROFILE` env vars
   - Updated `.env`: cleared `FASTRTPS_PROFILE=`, added Fast DDS comment
   - Updated `.env.example`: same changes for consistency
   - Updated `setup_env.sh`: replaced Fast DDS SHM exports with `RMW_IMPLEMENTATION=rmw_fastrtps_cpp`
   - Updated `Dockerfile`: added `ros-humble-rmw-fastrtps-cpp` to ROS2 package install list for future builds

4. **Updated Project Documentation**
   - Updated `Aimee_Project_Plan.md`:
     - Changed key design decision from "Fast DDS + SHM" to "Fast DDS"
     - Updated architecture diagram label to "ROS2 Topic Bus (Fast DDS)"
     - Rewrote "Memory Optimization (4GB Limit)" section to explain why Fast DDS was chosen and included feature comparison table

5. **Recreated Container & Verified**
   - Ran `docker compose up -d` to recreate the container from `aimee-robot:cyclone-installed`
   - Container starts healthy with `RMW_IMPLEMENTATION=rmw_fastrtps_cpp`
   - Confirmed `rmw_fastrtps_cpp` v1.3.4 is installed and available
   - Removed old `aimee-robot:latest` tag to prevent accidental use
   - Root partition now at ~81% with 1.9GB free

### Files Modified

```
/home/arduino/aimee-robot-ws/
├── docker-compose.yml          [UPDATED - image, RMW env vars]
├── .env                        [UPDATED - cleared FASTRTPS_PROFILE]
├── .env.example                [UPDATED - cleared FASTRTPS_PROFILE]
├── setup_env.sh                [UPDATED - Fast DDS exports]
├── Dockerfile                  [UPDATED - added ros-humble-rmw-fastrtps-cpp]
├── Aimee_Project_Plan.md       [UPDATED - Fast DDS rationale & comparison]
└── CHECKPOINT.md               [THIS FILE - updated]
```

### Notes

- The old Fast DDS XML profiles (`fastdds_shm.xml`, `fastdds_disable_shm.xml`, `fastdds_shm_simple.xml`) are still present in the repo for reference but are no longer used.
- If you ever need to revert to Fast DDS temporarily, set `RMW_IMPLEMENTATION=rmw_fastrtps_cpp` and `FASTRTPS_DEFAULT_PROFILES_FILE` before launching.
- Disk space is still tight on root (81%). Consider moving `/var/lib/docker` to the user partition (`/home/arduino`) for future headroom if more Docker builds are planned.

---

# Aimee Robot - Session Checkpoint

**Date:** 2026-04-22  
**Session Focus:** SLAM/Nav2 integration for Minnie; multi-base platform architecture; robot description URDF

---

## 🎉 MISSION ACCOMPLISHED!

### What Was Done Today

1. **SLAM & Nav2 Stack Integration**
   - Created `aimee_description` package with `minnie.urdf` (`base_footprint`, `base_link`, `base_laser`, `camera`)
   - Created `slam.launch.py` — standalone `slam_toolbox` (online sync) with LD19-tuned params
   - Created `nav2.launch.py` — Nav2 Humble bringup wrapper with Minnie-specific params
   - Created `navigation.launch.py` — combined robot bringup + SLAM + Nav2
   - Nav2 params: `robot_radius: 0.15`, `max_vel_x: 0.5`, `use_sim_time: false`, Humble API compatible
   - SLAM params: `max_laser_range: 12.0`, `min_laser_range: 0.05`, `minimum_travel_distance: 0.2`
   - Added `slam_toolbox` params to `nav2_params.yaml` so Nav2's `slam_launch.py` picks them up via `HasNodeParams`

2. **Robot State Publisher & TF Tree**
   - `robot.launch.py` now auto-discovers `aimee_description/urdf/{robot_name}.urdf`
   - Launches `robot_state_publisher` when URDF exists
   - Skips static lidar TF publisher when URDF already defines `base_link → base_laser`
   - Added `use_lidar` CLI launch arg for symmetry with `use_base`

3. **Multi-Base Platform Architecture**
   - Verified `ugv02_controller_node` is fully parameterized via `base_params` YAML
   - Fixed `minnie.yaml`: changed `base: "ugv02"` → `base: "wave_rover"` for clarity
   - Updated `robot.launch.py` with explicit comments explaining that `ugv02` and `wave_rover` share the same Waveshare JSON protocol node
   - Added warning log for unknown base types
   - Updated `default.yaml` template with base type docs and `lidar` section

4. **Launch Fixes**
   - Fixed `navigation.launch.py`: moved `LogInfo` after `DeclareLaunchArgument`s (was causing `map` not found)
   - Fixed `robot.launch.py`: added missing `use_base_arg` to LaunchDescription
   - Fixed `nav2.launch.py`: changed `slam`/`use_composition`/`autostart` defaults from lowercase `true`/`false` to Python literals `True`/`False` (Nav2 `PythonExpression` requirement)

### Running Services

| Service | Container | Status | URL |
|---------|-----------|--------|-----|
| **ROS2 Core + Nav2 + SLAM** | `aimee-robot` | 🟢 Running | — |
| **Monitor** | `aimee-robot` | 🟢 Operational | http://minnie.local:8081 |

### Files Modified

```
/home/arduino/aimee-robot-ws/
├── src/aimee_description/                               [NEW - URDF package]
│   ├── urdf/minnie.urdf
│   ├── package.xml
│   └── CMakeLists.txt
├── src/aimee_bringup/
│   ├── config/nav2_params.yaml                          [NEW - Nav2 Humble params for Minnie]
│   ├── config/slam_params.yaml                          [NEW - SLAM Toolbox params for LD19]
│   ├── launch/slam.launch.py                            [NEW]
│   ├── launch/nav2.launch.py                            [NEW]
│   ├── launch/navigation.launch.py                      [NEW]
│   ├── launch/robot.launch.py                           [UPDATED - URDF support, use_lidar, base platform docs]
│   ├── config/robots/minnie.yaml                        [UPDATED - base: wave_rover]
│   ├── config/robots/default.yaml                       [UPDATED - base docs + lidar section]
│   ├── CMakeLists.txt                                   [UPDATED - install config/]
│   └── package.xml                                      [UPDATED - nav2, slam, robot_state_publisher deps]
├── Aimee_Project_Plan.md                                [UPDATED - Phase 4b SLAM/Nav2]
└── CHECKPOINT.md                                        [THIS FILE - updated]
```

### Notes

- Nav2 / SLAM are completely decoupled from the base controller. Any platform that publishes `/odom`, subscribes `/cmd_vel`, and broadcasts `odom → base_link` will work without code changes.
- `color_detector_node` crashes due to NumPy 2.2.6 / `cv_bridge` incompatibility. Fix: `pip install "numpy<2"` in container.
- Lidar and base currently fight for `/dev/ttyUSB0`. Need udev rules or manual port assignment in `minnie.yaml`.
- `ros2 node list` is very slow on this board; `ps aux` is faster for health checks.

---

# Aimee Robot - Session Checkpoint

**Date:** 2026-04-13 (Updated 2026-04-16)  
**Session Focus:** Migrate routing to AimeeAgent; simplify Intent Router; add command execution in ACC

---

## 🎉 MISSION ACCOMPLISHED!

### What Was Done Today

1. **Separated Video Pipeline from OBSBOT SDK Node**
   - Stripped `obsbot_brick.py` to SDK-only (no OpenCV/UVC capture code)
   - Stripped `obsbot_node.py` of all video publishing (`/camera/image_raw`, cv_bridge, video timer)
   - `obsbot_node` is now a pure PTZ/tracking/status node

2. **Added Dedicated USB Camera Node**
   - `core.launch.py` now launches `usb_cam_node_exe` from `ros-humble-usb-cam`
   - Configured for `/dev/video2`, 1280×720, `mjpeg2rgb`, `mmap` I/O
   - Publishes to `/camera/image_raw` and `/camera/camera_info`
   - **Note:** `ros-humble-v4l2-camera` v0.6.2 was installed first but does not support MJPG format (crashes with `cv_bridge::Exception: Unrecognized image encoding []`)

3. **Performance Results**
   - `obsbot_node` CPU usage: **~88% → ~5%**
   - Video stream stable at **~23 fps** at 1280×720
   - Python GIL + MJPEG decode overhead completely eliminated from video pipeline

4. **Fixed Monitor Node for New Configuration**
   - Added `usb_camera` to monitor's node definitions
   - Removed obsolete `publish_video:=true` arg from `obsbot_camera` definition
   - Replaced `ros2 node list` subprocess with `get_node_names_and_namespaces()`
   - Replaced `ros2 topic list -t` subprocess with `get_topic_names_and_types()`
   - Replaced `ros2 topic hz` subprocess with frame timestamp-based Hz calculation
   - Changed monitor to subscribe to `/camera/image_raw/compressed` instead of raw `sensor_msgs/Image`
   - Added `image_transport/republish` node to `core.launch.py` to generate compressed topic
   - Camera stream now yields JPEG bytes directly with zero OpenCV conversion
   - Monitor CPU: **~70% → ~40%** (subprocess starvation eliminated)

5. **Verification**
   - `/api/nodes` returns live node list without shell-outs
   - `/api/topics` returns topic metadata from native ROS2 API
   - `/api/camera/status` reports `connected: true`
   - `/camera/stream` serves valid MJPEG with `ff d8 ff e0` JPEG headers

---

## 🔊 TTS Migration to Standard ROS2 Node (2026-04-15)

### What Was Done

1. **Migrated TTS to Pure Standard ROS2 Node**
   - `tts_node.py` was already a standard ROS2 node; removed all remaining brick artifacts
   - Deleted `aimee_tts/aimee_tts/brick/tts.py` (old brick implementation)
   - Removed Piper and pyttsx3 support per migration plan

2. **Engine Consolidation: Kokoro Primary + gTTS Fallback**
   - Updated `tts_engines.py` to support only **Kokoro** (primary, offline) and **gTTS** (cloud fallback)
   - Removed `PiperEngine`, `Pyttsx3Engine`, and all related parameters/fallback logic
   - `TTSEngineManager` now initializes only Kokoro (pykokoro preferred, official package fallback) and gTTS

3. **Configuration & Launch Updates**
   - Updated `core.launch.py` to default `default_engine:=kokoro` and `fallback_engine:=gtts`
   - Updated `config/brick_config.yaml` to remove deprecated engines and reflect new defaults
   - Cleaned up `setup.py` and `package.xml` descriptions
   - Rewrote `README.md` to document the standard ROS2 node usage with Kokoro/gTTS

4. **Files Modified**
   ```
   /home/arduino/aimee-robot-ws/src/
   ├── aimee_tts/
   │   ├── aimee_tts/tts_node.py            [UPDATED - removed piper/pyttsx3 params]
   │   ├── aimee_tts/tts_engines.py         [UPDATED - kokoro + gtts only]
   │   ├── aimee_tts/brick/tts.py           [DELETED - deprecated brick]
   │   ├── config/brick_config.yaml         [UPDATED - removed deprecated engines]
   │   ├── setup.py                         [UPDATED - description]
   │   ├── package.xml                      [UPDATED - description]
   │   └── README.md                        [REWRITTEN - standard node docs]
   └── aimee_bringup/launch/core.launch.py  [UPDATED - kokoro primary, gtts fallback]
   ```

---

## 🎯 Intent Router Rewrite & AimeeCloud Integration (2026-04-16)

### What Was Done

1. **External Intent Configuration**
   - Created `/workspace/config/aimee_intent_config.json` containing all keyword/phrase matching rules
   - Intent Router now loads intent definitions from this file at runtime
   - Config is reloaded on every classification so edits apply immediately without node restart

2. **Intent Router Rewrite (`aimee_intent_router`)**
   - Converted to standard ROS2 node loading config from external JSON
   - Classification uses word-boundary checks, phrase substrings, and `question_words` fallback for `chat`
   - Emits AimeeCloud-compatible intent types directly: `chat`, `weather`, `news`, `story`, `game`, `help`, `status`, `robot_*`, `arm_*`, `gripper_*`, `unclassified`
   - Added `"exact": true` phrase matching for movement and arm/gripper commands so only exact full utterances trigger local skills

3. **Explicit Local Command Requirements**
   - Robot movement commands must now be the exact phrases:
     - `move forward`, `move backward`, `move left`, `move right`, `move stop`
   - Arm/gripper commands must now be the exact phrases:
     - `wave arm`, `raise arm`, `lower arm`, `open gripper`, `close gripper`
   - Single words like `right`, `stop`, `wave`, `open` no longer trigger local skills and are routed to AimeeCloud

4. **Noise Word Updates**
   - Added `hello` and `hey` to `noise_words` in the intent config
   - These single-word utterances are now silently ignored instead of being routed to `chat` or AimeeCloud

5. **AimeeCloud Client Simplification (`aimee_cloud_bridge`)**
   - Renamed all `cloud_proxy` / `cloud_bridge` references to `AimeeCloud` in code and docs
   - `cloud_bridge_node.py` now forwards intents to AimeeCloud solely based on `skill_name == "AimeeCloud"`
   - Removed the old intent-type-to-skill mapping layer
   - Session lifecycle (load, save, resume, expiry, clear) handled by ACC

6. **Launch File Updates**
   - `core.launch.py` updated to pass `intent_config_path` to the Intent Router
   - Whisper API credentials (Lemonfox.ai `api_base_url` and `api_key`) passed to Voice Manager

### Files Modified
```
/home/arduino/aimee-robot-ws/
├── config/aimee_intent_config.json                    [NEW - external intent config]
├── src/aimee_intent_router/
│   └── aimee_intent_router/intent_router_node.py      [REWRITTEN - external config, hot-reload, exact matching]
├── src/aimee_cloud_bridge/
│   └── aimee_cloud_bridge/cloud_bridge_node.py        [UPDATED - AimeeCloud branding, simplified forwarding]
├── src/aimee_bringup/launch/core.launch.py            [UPDATED - intent_config_path + Whisper API params]
├── Aimee_Project_Plan.md                              [UPDATED - AimeeCloud branding, intent routing docs]
└── CHECKPOINT.md                                      [THIS FILE - updated]
```

### Verification Results

| Input | Classification | Routing |
|-------|----------------|---------|
| `move right` | `robot_right` | local movement ✅ |
| `move left` | `robot_left` | local movement ✅ |
| `move forward` | `robot_forward` | local movement ✅ |
| `move backward` | `robot_backward` | local movement ✅ |
| `move stop` | `robot_stop` | local movement ✅ |
| `wave arm` | `arm_wave` | local arm_control ✅ |
| `raise arm` | `arm_raise` | local arm_control ✅ |
| `lower arm` | `arm_lower` | local arm_control ✅ |
| `open gripper` | `gripper_open` | local arm_control ✅ |
| `close gripper` | `gripper_close` | local arm_control ✅ |
| `right` | `unclassified` | AimeeCloud ✅ |
| `stop` | `unclassified` | AimeeCloud ✅ |
| `wave` | `unclassified` | AimeeCloud ✅ |
| `open` | `unclassified` | AimeeCloud ✅ |
| `hello` | ignored | noise ✅ |
| `hey` | ignored | noise ✅ |
| `what time is it right now` | `chat` | AimeeCloud ✅ |

---

## 🎤 Voice Manager Migration to Standard ROS2 Node (2026-04-16)

### What Was Done

1. **Migrated `voice_manager` from Brick Pattern to Standard ROS2 Node**
   - Merged `brick/voice_manager.py` directly into `voice_manager_node.py`
   - Removed the background asyncio thread and brick callbacks
   - The Vosk listen loop now runs as a simple `threading.Thread` inside the node
   - TTS echo suppression now uses native ROS2 subscriptions (`/tts/is_speaking`, `/tts/speak`) directly
   - Removed `brick` package from `setup.py`; `brick/voice_manager.py` is now unused

2. **Added Auto-Recovery for Audio Capture Stalls**
   - Replaced blocking `stdout.read(4000)` with `select.select` + `os.read` in the listen loop
   - Detects arecord stalls (no data for 5+ seconds) and exits the loop, triggering auto-restart after 2 seconds
   - Detects arecord process death and restarts automatically
   - Detects zero-byte silence floods and restarts

3. **Fixed OBSBOT Microphone Dependency on `usb_cam`**
   - Discovered that the OBSBOT Tiny 2 Lite microphone only produces audio when its video stream is active
   - Added `_ensure_usb_camera_running()` to start `usb_cam_node_exe` before the listen loop
   - Includes a 3-second delay to let the V4L2 interface activate the mic
   - Verified: `hw_ptr` and `appl_ptr` advance correctly after `usb_cam` starts

4. **PONG Log Spam Reduction**
   - Changed AimeeCloud Client (`cloud_bridge_node.py`) to log MQTT `pong` messages at `debug` level instead of `info`

### Files Modified
```
/home/arduino/aimee-robot-ws/
├── src/aimee_voice_manager/
│   ├── aimee_voice_manager/voice_manager_node.py      [REWRITTEN - merged brick, standard ROS2 node]
│   └── setup.py                                         [UPDATED - removed brick package]
├── src/aimee_cloud_bridge/
│   └── aimee_cloud_bridge/cloud_bridge_node.py          [UPDATED - pong at debug level]
└── CHECKPOINT.md                                        [THIS FILE - updated]
```

---

## ☁️ Monitor Cloud Session Clear Button (2026-04-16)

### What Was Done

1. **Added "Clear AimeeCloud Session" Button to Monitor Dashboard**
   - New "☁️ Cloud Session" panel in the left sidebar
   - Button publishes `Bool(data=True)` to `/cloud/clear_session`

2. **Cloud Bridge Handles Session Clear**
   - New subscriber `/cloud/clear_session` in `cloud_bridge_node.py`
   - Calls `_clear_session()` then immediately `_publish_connect()` to request a new session from AimeeCloud
   - Fixed initial bug where clearing only deleted the local session file without sending a new `connect`, causing subsequent requests to fail

3. **End-to-End Verification**
   - Clicked "Clear Session" → local session cleared → new `connect` sent → AimeeCloud replied with `session_init`
   - Voice query "What time is it in Seattle right now?" flowed through correctly after session reset

### Files Modified
```
/home/arduino/aimee-robot-ws/
├── src/aimee_cloud_bridge/
│   └── aimee_cloud_bridge/cloud_bridge_node.py          [UPDATED - clear_session subscriber + reconnect]
├── src/aimee_ros2_monitor/
│   ├── aimee_ros2_monitor/monitor_node.py               [UPDATED - /cloud/clear_session publisher + API endpoint]
│   └── aimee_ros2_monitor/templates/index.html          [UPDATED - Cloud Session panel + JS handler]
└── CHECKPOINT.md                                        [THIS FILE - updated]
```

---

## 🤖 AimeeAgent Migration & ACC Command Execution (2026-04-16)

### What Was Done

1. **Retrieved AimeeCloud Protocol v1.1**
   - Subscribed to MQTT topic `aimeecloud/service/protocol`
   - Saved updated spec to `docs/AimeeCloud_Protocol_v1.1.md`
   - Key addition: `AimeeAgent` message type and `commands` array in responses

2. **Simplified Intent Router (`aimee_intent_router`)**
   - Removed all LLM action client code (`_llm_client`, `_call_llm`, `_generate_llm_response_async`)
   - Router now has exactly two paths:
     - **Local skills** (`movement`, `arm_control`, `camera`) → execute locally with fallback TTS
     - **Everything else** → publish `IntentMsg(skill_name="AimeeCloud")` for ACC to forward
   - Removed `chat_routing`, `enable_conversation_mode`, and conversation context parameters
   - This eliminates the problematic local intent-to-response generation path

3. **Updated AimeeCloud Client (`aimee_cloud_bridge`)**
   - Added `send_agent_request()` to publish `type: "AimeeAgent"` instead of `type: "intent"`
   - All non-local voice requests now bypass AimeeCloud's keyword router and go straight to the LLM agent
   - Added `aimee_agent` response handler in `_handle_out_message()`
   - Added `_execute_command()` dispatcher that handles:
     - `motor` → publishes `Twist` to `/cmd_vel` with optional duration
     - `arm` / `gripper` → publishes `ArmCommand` to `/arm/command`
     - `snapshot` → stops `usb_camera`, calls `CaptureSnapshot` service, uploads result back to AimeeCloud, restarts camera
     - `game_move` → publishes `CloudIntent` to `/game/command`
   - Fixed missing `import subprocess` bug
   - Added `/game/command` publisher for local game handler integration

4. **Rebuild & Verification**
   - Rebuilt both packages with `colcon build --packages-select aimee_cloud_bridge aimee_intent_router`
   - Cleanly restarted the ROS2 core stack
   - All 7 nodes up and running with no duplicates

### New Voice Request Flow

1. **Voice Manager** → `/voice/transcription`
2. **Intent Router** classifies:
   - `move forward`, `wave arm`, etc. → local execution + TTS
   - Everything else → `IntentMsg(skill_name="AimeeCloud")`
3. **ACC** receives intent and sends `AimeeAgent` MQTT message to AimeeCloud
4. **AimeeCloud** responds with `sub_type: "aimee_agent"` + optional `commands` array
5. **ACC** speaks the `tts` response and executes commands locally in order

### Files Modified

```
/home/arduino/aimee-robot-ws/
├── docs/AimeeCloud_Protocol_v1.1.md                    [NEW - retrieved from MQTT]
├── src/aimee_intent_router/
│   └── aimee_intent_router/intent_router_node.py      [UPDATED - stripped LLM, simplified routing]
├── src/aimee_cloud_bridge/
│   └── aimee_cloud_bridge/cloud_bridge_node.py        [UPDATED - AimeeAgent requests + command execution]
├── Aimee_Project_Plan.md                              [UPDATED - AimeeAgent docs]
└── CHECKPOINT.md                                      [THIS FILE - updated]
```

### Notes

- Offline fallback LLM will be implemented later as a separate layer (e.g., in the bridge or a dedicated offline-agent node), not inside the intent router.
- The `AimeeAgent` command reference from the protocol:
  - Motor: `{ "type": "motor", "action": "forward", "duration_ms": 1000 }`
  - Arm: `{ "type": "arm", "action": "raise" }`
  - Gripper: `{ "type": "gripper", "action": "open" }`
  - Snapshot: `{ "type": "snapshot", "camera": "front", "purpose": "analysis" }`
  - Game move: `{ "type": "game_move", "game": "tic-tac-toe", "position": 4 }`

---

## 🔊 Lemonfox TTS Primary, Voice Metadata & Interstitial Removal (2026-04-16)

### What Was Done

1. **Retrieved AimeeCloud Protocol v1.2**
   - Subscribed to MQTT topic `aimeecloud/service/protocol`
   - Saved updated spec to `docs/AimeeCloud_Protocol_v1.1.md`
   - Key addition: `voice` object in all outbound responses and optional `voice_segments` for multi-character dialogue

2. **Added Lemonfox.ai TTS Engine**
   - Implemented `LemonfoxEngine` in `tts_engines.py` using OpenAI-compatible TTS API (`/v1/audio/speech`)
   - Added API key and base URL parameters to `TTSEngineManager` and `TTSNode`
   - Updated `core.launch.py` to pass the Lemonfox API key and set `default_engine:=lemonfox`, `fallback_engine:=gtts`
   - Updated `brick_config.yaml` to reflect new defaults

3. **TTS Node Voice Support**
   - `tts_node.py` now recognizes `lemonfox` in the `engine|voice:text` prefix parser
   - Default voice changed from `af_heart` (Kokoro) to `sarah` (Lemonfox)
   - All three engines available: `lemonfox`, `kokoro`, `gtts`

4. **AimeeCloud Client Voice Integration**
   - ACC parses `voice` metadata from every AimeeCloud response
   - Publishes TTS with engine|voice prefix (e.g., `lemonfox|sarah:Hello!`)
   - Supports `voice_segments`: publishes sequential `/tts/speak` messages with per-segment voice mapping
   - `robot_command`, `chat_response`, `game_update`, `error`, and `aimee_agent` sub-types all pass voice info to TTS

5. **Removed Interstitial Responses**
   - Stripped `_enable_interstitials`, `_interstitial_phrases`, and suppression logic from ACC
   - Interstitials unnecessary while AimeeCloud is online (responses are fast)
   - Will re-introduce later as part of offline fallback architecture

### Files Modified

```
/home/arduino/aimee-robot-ws/
├── docs/AimeeCloud_Protocol_v1.1.md                    [UPDATED - protocol v1.2 retrieved]
├── src/aimee_tts/
│   ├── aimee_tts/tts_engines.py                       [UPDATED - LemonfoxEngine added]
│   ├── aimee_tts/tts_node.py                          [UPDATED - lemonfox support, voice params]
│   └── config/brick_config.yaml                       [UPDATED - lemonfox defaults]
├── src/aimee_cloud_bridge/
│   └── aimee_cloud_bridge/cloud_bridge_node.py        [UPDATED - voice support, removed interstitials]
├── src/aimee_bringup/launch/core.launch.py            [UPDATED - lemonfox TTS params]
├── Aimee_Project_Plan.md                              [UPDATED - TTS and voice docs]
└── CHECKPOINT.md                                      [THIS FILE - updated]
```

---

## 📊 Running Services

| Service | Container | Status | URL |
|---------|-----------|--------|-----|
| **ROS2 Core** | `aimee-robot` | 🟢 Running | — |
| **Monitor** | `aimee-robot` | 🟢 Operational | http://192.168.1.100:8081 |

---

## 🔮 Next Steps (Future Sessions)

1. **Dashboard Enhancements**
   - Add action goal widgets (test PickPlace from dashboard)
   - Add voice pipeline visualization

2. **Hardware Testing**
   - Connect UGV02 via serial and verify `/cmd_vel` response
   - Test OBSBOT PTZ commands through ROS2 topics

3. **Remaining Optimizations**
   - Further reduce monitor camera-stream CPU (e.g., lower-resolution direct V4L2 read or reduce republish frequency)

4. **Dynamic AimeeCloud Capabilities**
   - After hardware arrives, scan active ROS2 nodes to determine capabilities dynamically
   - e.g., `/ugv02_controller` present → add `"motors"`; `/arm_controller` present → add `"arm"`; camera nodes present → keep `"snapshot"`
   - This avoids hardcoding capabilities in `cloud_bridge_node.py`

5. **Brick-to-Standard-ROS2 Migration (Remaining Nodes)**
   - Cloud Bridge (already migrated to AimeeCloud ACC) ✅
   - Voice Manager (Priority 1)

---

## 📝 Notes

- `usb_cam` package works well for MJPEG streams on the UNO Q; `v4l2_camera` does not.
- The `image_transport/republish` C++ node consumes significant CPU (~85%) because it re-encodes 1280×720 rgb8 back to JPEG. This is acceptable for now since it offloads work from the Python monitor.
- Fast DDS SHM config is still disabled (`FASTRTPS_DEFAULT_PROFILES_FILE` set to disable SHM) to avoid `open_and_lock_file` errors.
- TTS brick `__pycache__` directory could not be fully removed due to root-owned `.pyc` files inside the container; source brick files are deleted.
- Intent Router config hot-reload means future keyword/phrase tuning can be done by editing `/workspace/config/aimee_intent_config.json` with no node restart required.

---

## 🔊 TTS Storytelling Voice Options — Research Notes (2026-04-15)

**Context:** Kokoro TTS exhibits ~20 s latency on the UNO Q. The `PyKokoroEngine` (ONNX-based) recreates its entire pipeline when switching voices, making mid-story character voice changes impractical. The `KokoroOfficialEngine` (torch-based) does *not* recreate the pipeline on voice changes, but the initial model load is slow on this hardware. Default engine was switched back to `gtts` while we evaluate storytelling alternatives.

### Decision Log
- **Immediate action:** Revert default TTS engine to `gtts` to restore responsive speech.
- **Future work:** Evaluate one of the four approaches below for multi-voice storytelling.

### Option 1: Pre-recorded Character Clips + gTTS Narrator (Recommended)
- **How it works:** Use gTTS for the narrator and any dynamic / unpredictable text. Pre-record character dialogue as `.wav`/`.mp3` files, store them on the robot, and play them directly via `pygame.mixer` or a dedicated media player node.
- **Message format idea:** `play:/path/to/owl.wav` or `char_owl:Hello` routed to playback instead of synthesis.
- **Pros:** Theatrical quality, zero latency, works offline, true distinct voices.
- **Cons:** Requires recording / generating lines ahead of time.

### Option 2: gTTS with Regional Accents (Easy Code Change)
- **How it works:** Leverage gTTS `tld` parameter (`com`, `co.uk`, `com.au`, `co.in`, `ca`, `ie`) combined with `slow=True/False` to create 6–10 recognizably different "characters."
- **Message format idea:** `gtts|co.uk:Hello, I'm the British fox`
- **Pros:** No new dependencies, works today with a small parser patch.
- **Cons:** Still sounds like Google Translate, just with different accents.

### Option 3: OpenAI TTS Engine (Best Cloud Multi-Voice Quality)
- **How it works:** Add an `OpenAITTSEngine` to `tts_engines.py` that calls the OpenAI TTS API. Supports 6 distinct voices: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`.
- **Pros:** Excellent storytelling quality, fast, natural sounding, true multi-voice.
- **Cons:** Requires internet connection and an API key; not free at scale.

### Option 4: Fix Kokoro for True Offline Multi-Voice
- **Sub-option A — Official `kokoro` package:** Use `kokoro` (torch-based) instead of `pykokoro`. It keeps one `KPipeline` instance and passes `voice=` directly, so voice switching is instant after the slow initial load.
- **Sub-option B — Cached `PyKokoroEngine` instances:** Modify `TTSEngineManager` to maintain one ONNX pipeline per voice in a dictionary (`voice -> pipeline`). Switching voices just selects a different cached pipeline instead of rebuilding it.
- **Pros:** High quality, fully offline.
- **Cons:** Sub-option A uses more RAM (torch). Sub-option B uses more RAM (multiple ONNX sessions) and needs code changes.

### Configuration Changes Made Today
- `aimee_bringup/launch/core.launch.py`: `default_engine` changed from `kokoro` back to `gtts`.
- `aimee_tts/config/brick_config.yaml`: `DEFAULT_ENGINE` default and `development` profile changed from `kokoro` back to `gtts`.

**Status:** 🤖 **VIDEO PIPELINE SEPARATED, MONITOR OPERATIONAL, TTS MIGRATED TO STANDARD ROS2 NODE WITH LEMONFOX PRIMARY, INTENT ROUTER REWRITTEN WITH EXTERNAL CONFIG, AIMEEAGENT PROTOCOL IMPLEMENTED WITH VOICE SUPPORT!**


---

# Aimee Robot - Session Checkpoint

**Date:** 2026-04-26 (Evening session)
**Session Focus:** Scan matcher tuning, stationary drift fix, LocalGridMapCpp.clear() fix, forward-motion test attempt
**Status:** 🔴 **HALTED — Battery dead (0.59V). Session ended unexpectedly.**
**Container:** `aimee-robot` (Docker), Python 3.10.12
**Git:** Main branch at `c4b8927`
**Hardware:** Arduino UNO Q + UGV02 base (Ron) + LD19 lidar
**Battery:** 18650 pack (likely 3S). Failed at 0.59V during forward-motion test.

---

## ✅ What Was Accomplished

### 1. Scan Matcher Tuning (commit `419bb60`)
The scan matcher was rejecting too many matches (threshold 30.0 with scores in 15–25 range), causing pure-encoder odometry drift.

| Parameter | Old | New | Rationale |
|-----------|-----|-----|-----------|
| `score_threshold` | 30.0 | **15.0** | Accept more matches; observed scores 42–91 after fix |
| `search_radius_m` | 0.2 | **0.4** | Larger search for encoder drift |
| `search_angle_rad` | 0.1 | **0.25** | Allow bigger heading correction |
| `interval` | 1.0 | **0.3** | Match more frequently |
| `lidar_downsample` | 6 | **4** | More points = better correlation |

**Result:** Scan matching resumed working. Scores observed: 42–91 (well above 15.0 threshold).

### 2. Stationary Deadband — Drift Spiral Fix (commit `5272431`)
**Problem:** Even with robot physically still, encoder odometry reported tiny velocities. Scan matcher found slightly better scores at small rotations (inflated cell partial credit). EKF applied these → pose drifted → map smeared.

**Fix:** Skip scan matching when `abs(vx) < 0.01 and abs(vth) < 0.01`. Lock pose to last known good value and still update map.

```python
is_stationary = abs(vx) < 0.01 and abs(vth) < 0.01
if is_stationary:
    cx, cy, ctheta = init_x, init_y, init_theta  # Lock pose
    # Update map only (no scan matching)
```

**Result:** Map no longer smears during stationary tests. Saved PNGs and live viewer show consistent room geometry when robot is still.

### 3. LocalGridMapCpp.clear() — Missing Method Fix (commit `c4b8927`)
**Problem:** `AttributeError: 'LocalGridMapCpp' object has no attribute 'clear'` triggered during recovery mode.

**Fix:** Added `clear()` method to `LocalGridMapCpp`:
```python
def clear(self) -> None:
    self._cpp.clear()
    self.grid.fill(0)
    self.origin_x = 0.0
    self.origin_y = 0.0
    self.origin_theta = 0.0
```

### 4. Auto-Save on Shutdown (committed)
`destroy_node()` now calls `_save_map_to_file()` so maps are persisted even on SIGINT.

### 5. Rosbridge in Launch (committed)
`robot.launch.py` now includes `rosbridge_websocket_launch.xml` for web-based map viewer.

### 6. Map Viewer Fix (committed)
Fixed `localhost:9090` hardcode; viewer served on HTTP port 8080. Verified working.

### 7. world_to_grid Unpack Bug Fix (committed)
C++ binding returns `(ok, gx, gy)` tuple; Python code was incorrectly unpacking. Fixed.

---

## 🔋 Battery Failure Incident

**Timeline:**
- **Earlier in session:** Battery ~12.1V (healthy for 3S Li-ion)
- **Forward-motion test:** Robot commanded to drive 1m forward
- **Immediate result:** Robot did not move
- **Base controller log:** Voltage dropped to **0.20V**, then recovered to **0.59V**
- **Root cause:** 18650 pack depleted. The 12.1V reading earlier may have been surface charge or measurement artifact.
- **System behavior:** No automatic motor cutoff. Nav node kept publishing `/cmd_vel`. Base controller logged warnings but continued to accept and forward motor commands.

**Impact:**
- Robot did not move (battery too low to drive motors)
- No hardware damage observed, but cells may have been discharged below safe threshold
- Session had to halt for charging

---

## ⚠️ Active Issues Requiring Attention

### 1. Battery Monitoring is Passive (CRITICAL)
- Base controller publishes `/battery_status` ("LOW"/"OK") and logs warnings
- **Nav node does NOT subscribe to battery status**
- **No automatic motor cutoff at critical voltage**
- **Recommendation:** Add battery subscriber to nav node. Stop motors and enter low-power standby when voltage < 9.0V (for 3S). Protect cells from deep discharge.

### 2. Forward-Motion Test Incomplete
- Robot never actually drove under its own power in this session
- Need to retry after battery is charged
- Before retry: verify battery voltage > 11.0V under load

### 3. Map Viewer Coordinate Frames
- Live viewer renders `/odom` pose alongside `/map` (SLAM pose)
- When stationary deadband is active, these frames should converge
- **Not yet verified** with actual robot motion
- Saved PNGs: forward on robot = right on image

### 4. Zombie Processes
- 88+ defunct PIDs from unclean kills earlier in the day
- **Recommendation:** Restart container when resuming to clean up

---

## 🎯 Next Steps (After Charging)

1. **Charge battery** to >11.5V (3S Li-ion full = 12.6V)
2. **Restart container** to clear zombie processes
3. **Verify voltage under load** — run base controller, check `/battery_status`
4. **Stationary verification** — launch nav, let robot sit, confirm map is stable
5. **Forward-motion test** — command 1m forward, verify:
   - Robot actually moves
   - Encoder odometry reports reasonable distance
   - Scan matcher scores remain healthy
   - Map updates correctly (walls appear where expected)
6. **Implement battery safety** — add `/battery_status` subscriber to nav node, motor cutoff at critical voltage

---

## 📋 Performance Summary (Post-Optimizations)

| Metric | Value |
|--------|-------|
| Nav cycle time | ~2–11 ms (target 333 ms @ 3 Hz) |
| DWA samples | 7 vel × 14 ang = 98 (was 20×28 = 560) |
| Frontier detection | `scipy.ndimage.label` (vectorized, replaces BFS) |
| Scan match interval | 0.3 s (was 1.0 s) |
| Lidar downsample | 4 (was 6) |
| Executor | SingleThreadedExecutor (was MultiThreaded) |
| Publish decimation | 150 (map TF every ~50 s) |

---

## 🔧 Code State at Session End

**Modified files (all committed to main):**
- `src/aimee_nav/aimee_nav/aimee_nav_node.py` — Stationary deadband, scan matcher params, auto-save
- `src/aimee_nav/aimee_nav/local_grid_map_cpp.py` — Added `clear()`
- `src/aimee_nav/cpp/src/scan_matcher.cpp` — Unchanged in this session (params in YAML)
- `src/aimee_nav/config/nav_params.yaml` — Scan matcher params exposed
- `src/aimee_bringup/launch/robot.launch.py` — Rosbridge included
- `src/aimee_ugv02_controller/aimee_ugv02_controller/ugv02_controller_node.py` — Battery pub (unchanged in this session)

**Git log (last 5 commits):**
```
c4b8927 Add LocalGridMapCpp.clear() and auto-save on shutdown
5272431 Add stationary deadband to prevent drift spiral
419bb60 Tune scan matcher: threshold 15, radius 0.4, angle 0.25, interval 0.3
[... earlier commits ...]
```

**Status:** 🔴 **SESSION HALTED DUE TO DEAD BATTERY. CHARGE BEFORE RESUMING.**


---

# Aimee Robot - Session Checkpoint

**Date:** 2026-04-27
**Session Focus:** Mapping test — stationary + 1m forward goal
**Status:** 🟡 **TEST RAN BUT ROBOT BEHAVED INCORRECTLY**

---

## What Actually Happened (Honest Record)

### Setup Mistake
I (the agent) created an ad-hoc parameter file (`/tmp/base_params.yaml`) instead of using the project's actual configuration system. I relied on compacted context memory rather than reading the actual `robot.launch.py` and `ron.yaml` files. This is a process failure.

### Test Execution
- **Nodes launched:** Only `base_controller` + `aimee_nav` (minimal stack)
- **Battery:** 12.14V (healthy)
- **Stationary phase:** Robot sat at origin, map built correctly. Pose locked at (0.00, 0.00). Stationary deadband working.
- **Goal published:** `(1.0, 0.0)` in map frame via `/goal_pose`

### Robot Behavior (USER OBSERVED — NOT WHAT I REPORTED)
- Robot moved forward **partially**
- Then **spun approximately 90 degrees to the right**
- Ended facing perpendicular to the intended direction
- **Did NOT reach the goal correctly**

### What I Logged (Nav node logs)
- Pose reached `(0.97, 0.14)` according to SLAM
- But user says robot physically spun 90° right — this is a **critical discrepancy**
- Possible causes:
  1. Wrong `track_width_multiplier` or `wheel_separation` causing bad odometry
  2. Navigation controller commanding rotation instead of straight-line
  3. Base controller parameters incorrect (I used ad-hoc values, not project config)
  4. EKF/scan matcher corrupting heading

---

## Root Cause Investigation Needed

### Configuration Issue
The proper way to launch the base controller is via `robot.launch.py` which reads `src/aimee_bringup/config/robots/ron.yaml`. I bypassed this and hand-wrote parameters. Need to verify:
- `track_width_multiplier: 2.0` — is this still correct?
- `wheel_separation: 0.172` — is this still correct?
- `ticks_per_meter: 106.0` — is this still correct?

### Navigation Issue
With goal at `(1.0, 0.0)` and robot at `(0, 0)` facing forward, the nav node should drive straight. Why did it command a 90° spin?
- Check `_nav_cycle()` goal-directed behavior
- Check if DWA/reactive layer is overriding the straight path
- Check if scan matcher heading is drifting

---

## Action Items
1. [ ] Use proper `robot.launch.py` or at minimum read actual `ron.yaml` for params
2. [ ] Re-run test with correct configuration
3. [ ] Add debug logging to nav node showing commanded velocities during goal pursuit
4. [ ] Verify physical robot behavior matches logged pose

**Status:** ⚠️ **REQUIRES INVESTIGATION BEFORE NEXT TEST**

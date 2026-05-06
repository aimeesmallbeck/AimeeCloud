# GEMINI.md

## Project Summary: Aimee Robot
Aimee is a modular social assistance robot platform built on **ROS 2 Humble**.

## Mandatory Engineering Safety Protocols
### 1. Mandatory Backup Before Edit
**STRICT RULE:** Before making ANY structural, logic, or formatting changes to a source file, the agent MUST create a backup in the `/home/arduino/aimee-robot-ws/backups/` directory.
- Format: `<filename>.<date>_<time>_<reason>.bak`

### 2. Standard ROS 2 Transition
**MANDATE:** All "Arduino Bricks" must be rebuilt as standard ROS 2 nodes during validation.

---

## Current Best Calibration (2026-04-27)
- **Base:** UGV02 (Encoders active, IMU Disabled)
- **Ticks Per Meter:** 106.0
- **Wheel Separation:** 0.26m (Effective width to prevent over-correction)
- **Max Speed:** 0.4 m/s (Ramped)
- **Accel Limits:** Linear: 0.5 m/s², Angular: 1.0 rad/s²
- **Min Power Floor:** 0.18
- **Lidar Offset:** 0.0 deg
- **Safety Stop:** 0.4m (Lidar-based, hard override)

## Current Best Setup (2026-05-06)
- **Vision Pipeline:** Hybrid C++/Python pipeline. `color_detector_node` and `object_tracker_node` (C++). `pose_estimator_node` (Python) now utilizes registered hardware depth map from Astra Pro to extract precise 3D object coordinates.
- **Camera Device:** Orbbec Astra Pro (RGB+Depth). RGB stream via UVC (`/dev/video0`) using `usb_cam` with `YUYV` at `640x480` at 30fps. Depth stream via OpenNI (`orbbec_camera`) at 30fps. IR and PointCloud generation disabled for CPU efficiency.
- **CPU Footprint:** ~80-85% peak usage with full vision-to-manipulation pipeline running alongside live dashboard monitoring.
- **Arm Manipulation:** The ROS 2 Python node (`arm_kinematics_bridge_rpc`) communicates via MessagePack RPC over a Unix socket (`/var/run/arduino-router.sock`) to the UNO Q's `arduino-router` background service. Hard Cartesian safety limits are enforced within the bridge (Z-floor at 0.08m, min radial reach 0.10m, max radial reach 0.35m) to prevent workspace violations. The router forwards commands to the STM32 co-processor acting as a Real-Time Trajectory Engine. The STM32 calculates a smooth quintic trajectory and natively streams micro-waypoints at 50Hz over Hardware Serial (921600 baud) to the ESP32.

## Latest Test Observations
- **Pick and Place Flow:** Successfully triggered autonomous pick sequence on colored block. Hardware bridge safety interlocks proven necessary and functional.
- **1m Goal Test:** Robot reached distance but overshot by several centimeters.
- **Motion Quality:** Ramping provided smoother starts/stops, but perceived speed was lower.
- **Battery:** 11.75V (Pre-charge status).

---

## Technical Operational Details
- **Container:** `aimee-robot` (Docker)
- **DDS:** Fast DDS / Fast DDS
- **Hardware Ports:** Lidar: `/dev/ttyUSB0`, Base: `/dev/ttyACM0`, Camera: `/dev/video0` (RGB) / OpenNI (Depth)

## Agent Editing Protocol (Anti-Corruption)
1. **Staging Pattern:** Write all complex code to `/root/staging_file.py` first. Use `cp` or `docker cp` to deploy. Never use multiline strings inside `run_shell_command`.
2. **Pre-Flight Linting:** After every edit, the agent MUST run `python3 -m py_compile` on the file.
3. **Atomic Backups:** Use the `/backups` folder exclusively for session recovery to avoid version drift.
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

## Current Best Calibration (2026-05-07)
- **Base:** UGV02 (Encoders active, IMU Disabled)
- **Ticks Per Meter:** 106.0
- **Wheel Separation:** 0.26m
- **Arm Limits (Raw):** Home: `[2056, 2060, 2636, 2484, 2043, 2062]`. Floor (X=0.196m): `[2059, 2703, 2435, 2038]`.
- **Coordinate Origin:** Shoulder joint is (0,0,0). Desk surface is at `Z ≈ -0.088m`.
- **Safety Stop:** 0.4m (Lidar-based, hard override)

## Current Best Setup (2026-05-07)
- **Vision Pipeline:** Hybrid C++/Python pipeline. `pose_estimator_node` extracts 3D coordinates from registered depth map.
- **Arm Manipulation (Hardware HAL):**
    - **STM32 Trajectory Engine:** Hosts native 2D Trigonometric IK solver. Directly accepts Cartesian coordinates (`X, Y, Z, Pitch`).
    - **ESP32 Chaser:** Performs dynamic mechanical offset calibration for shoulder parallel linkage on boot.
    - **Python Bridge Node:** Pure RPC proxy. All kinematic math removed from high-level scripting for hardware abstraction.
- **Safety Interlocks:** Hard Cartesian limits enforced in STM32 firmware (Z-floor -0.088m, min reach 0.10m). 2000ms startup delay and 5000ms default movement duration active for safe validation.

## Latest Test Observations
- **Critical Incident (2026-05-08):** Severe hardware desynchronization led to violent, continuous erratic arm movements causing slight physical damage.
- **Incident Root Causes:**
    1. **Vision Auto-Trigger:** A rogue callback in `arm_kinematics_bridge_rpc.py` autonomously executed grasp commands the moment the camera detected an object, bypassing the Action Server.
    2. **Missing TF Calibration:** The `camera_to_arm_tf` transform was uncalibrated (`0,0,0`). The robot assumed the camera was inside its base. Vision targets thus triggered catastrophic IK calculations, forcing the arm to over-extend to absolute physical limits.
    3. **Serial Buffer Corruption / Ghost Commands:** When the ESP32 boots without 12V motor power, its calibration routine (`st.ReadPos()`) fails and returns `-1`. This causes a massive integer underflow in the driven shoulder math (offset = 4097, result = large negative). Furthermore, attempting to "fix" the STM32 by adding 50Hz continuous `stream_cartesian` and auto-syncing caused severe race conditions. The STM32 stored a corrupt coordinate in RAM and endlessly blasted it over the serial line.
- **MANDATORY RECOVERY PROTOCOL (NEXT SESSION):**
    1. **HARD SHUTDOWN:** Ensure 12V power AND logic power (USB) are fully disconnected to clear STM32 and ESP32 RAM.
    2. **SAFE FIRMWARE FLASH:** Before applying 12V power, manually flash BOTH the STM32 and ESP32 with bare-bones, rigorously clamped firmware. The ESP32 **MUST** have strict input validation to ignore malformed serial commands and prevent math underflow on startup offsets.
    3. **NO STREAMING:** Disable the continuous 50Hz streaming from the STM32 until serial checksums and strict bounds-checking are implemented on the ESP32.
    - **CAMERA CALIBRATION:** Run `/home/arduino/auto_calibrate_camera.py` purely in software (or physically moving the arm by hand) to fix the TF math before enabling the PickPlace server.

    ---

    ## Session Progress (2026-05-09)
    ### 1. Camera-to-Arm Calibration Success
    - **Status:** Complete.
    - **Results:** Computed new `camera_link` to `arm_base_link` physical offsets.
    - **Applied TF:** `X=-0.3088, Y=0.2370, Z=0.0869`.
    - **Note:** Updated `vision_pipeline.launch.py` with these values.

    ### 2. Manipulation Bug Fixes
    - **Grasp Loop Resolved:** Identified that `arm_kinematics_bridge_rpc.py` had a rogue autonomous subscription bypassing the Action Server. Recompiled `aimee_manipulation` package to apply the fix.
    - **Z-Height Alignment:** Fixed math error in `grasp_planner_node.py` where `gripper_length` (0.08m) was incorrectly added to the target Z, causing the arm to hover 8cm above the table.
    - **Return Home:** Updated `pick_place_server.py` to command the arm back to the `home` position after a vision-based pick-up completion.
    - **Hardware Integration:** Swapped simulated `arm_controller_node` with the real `arm_kinematics_bridge_rpc` in the main launch file.

    ### 3. Vision Stability
    - **USB Cam Fix:** Corrected `pixel_format` to `yuyv` and device path to `/dev/video4`.
    - **Pose Estimator Robustness:** Patched `pose_estimator_node.py` to handle empty `CameraInfo` (prevent divide-by-zero/NaN coordinates).

    ## Current Issues & Next Steps
    - **X/Y Accuracy:** The arm is currently "moving past" the object. This indicates the TF rotation or the X/Y translation offset needs manual fine-tuning.
    - **NEXT SESSION:**
        1. Place a block at a known coordinate (e.g., center of camera view).
        2. Compare vision coordinates (`/vision/detections_3d`) vs actual arm reach.
        3. Surgically adjust the translation arguments in `vision_pipeline.launch.py` until X/Y alignment is pixel-perfect.

    ---

    ## Technical Operational Details
- **Container:** `aimee-robot` (Docker)
- **DDS:** Fast DDS / Fast DDS
- **Hardware Ports:** Lidar: `/dev/ttyUSB0`, Base: `/dev/ttyACM0`, Camera: `/dev/video0` (RGB) / OpenNI (Depth)

## Agent Editing Protocol (Anti-Corruption)
1. **Staging Pattern:** Write all complex code to `/root/staging_file.py` first. Use `cp` or `docker cp` to deploy. Never use multiline strings inside `run_shell_command`.
2. **Pre-Flight Linting:** After every edit, the agent MUST run `python3 -m py_compile` on the file.
3. **Atomic Backups:** Use the `/backups` folder exclusively for session recovery to avoid version drift.
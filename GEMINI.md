# GEMINI.md

## Project Summary: Aimee Robot
Aimee is a modular social assistance robot platform built on **ROS 2 Humble**.

---

## Agent Environment Reference (STOP — READ THIS FIRST)
**This section documents critical environment facts. Do NOT rediscover these.**

### ROS2 / Container Layout
- **Docker container:** `aimee-robot` (image `aimee-ros-dashboard:usb-cam`) runs dashboard/web UI nodes.
- **Host processes:** Main robot stack (`vision_pipeline.launch.py`, `usb_cam`, TF publishers, `color_detector_node`, `aimee_ros2_monitor`) run directly on the host in a mount namespace where `/opt/ros/humble` exists. They are NOT inside the Docker container.
- **To run ROS2 commands:** Use `docker exec aimee-robot bash -c "source /opt/ros/humble/setup.bash && ..."` if the container has the needed packages. Otherwise, the host ROS2 env is in a separate mount namespace; use `nsenter` or work through existing nodes.

### Hardware Interfaces
| Device | Path | Baud/Details | Notes |
|--------|------|-------------|-------|
| **STM32** (trajectory engine) | `/dev/ttyHS1` via `arduino-router` | 115200 | Unix socket: `/var/run/arduino-router.sock` (msgpack RPC) |
| **ESP32** (chaser) | `/dev/ttyUSB0` (CP2102N) | 921600 | Direct serial. Boot: DTR=True→False, RTS=True→False |
| **Camera** (Orbbec Astra Pro) | `/dev/video0` | 640×480 RGB | Held **exclusively** by host `usb_cam` node. Must kill it to use OpenCV directly. |
| **Lidar** | `/dev/ttyUSB0` historically | — | Verify before use; conflicts with ESP32 if same port |

### Critical Access Info
- **Sudo password:** `<REDACTED>`
- **STM32 network upload:** IP `192.168.1.100`, FQBN `arduino:zephyr:unoq`, password `<REDACTED>`
  - Command: `arduino-cli upload -b arduino:zephyr:unoq -p 192.168.1.100 --upload-field password="<REDACTED>" .`
- **Calibration file:** `/home/arduino/aimee-robot-ws/calibration.yaml`
- **Calibration measurements:** `/home/arduino/aimee-robot-ws/calibration_measurements_2026-05-11.md`

### STM32 ↔ ESP32 Serial Contention (CRITICAL)
- The **STM32 TX and host PC TX both drive ESP32 UART0 RX** (shared bus).
- When STM32 is streaming waypoints at 50Hz, **direct host ESP32 serial reads fail** (`/dev/ttyUSB0` commands get corrupted/drowned).
- **Solution implemented:** Added `read_arm_positions()` RPC to STM32 firmware. Host queries positions **through the router socket**, not direct ESP32 serial.
- **If you MUST use direct ESP32 serial:** Disconnect STM32 TX/RX from ESP32 first.

### Coordinate System & Kinematics
- **z = 0 is at the SHOULDER joint**, NOT the ground.
- **Desk surface:** `z = -0.075m` (7.5cm below shoulder).
- **Grasp height:** `z = -0.065m` (desk + 0.01m offset).
- **Safe transit:** `z = 0.05m`.
- **Top-down grasp pitch:** `pitch = π/2 ≈ 1.571 rad`. **Side approach:** `pitch = 0.0`.
- **FK convention (verified):** `test_fk.py` Waveshare replica.
  - J1 (base/yaw): zero at 2047
  - J2 (shoulder): zero at 2047
  - J3 (elbow): zero at **1024**
  - J4 (wrist): zero at 2047
- **ESP32 READ format:** `POS:<base, shoulder_driving, shoulder_driven, elbow, wrist, roll, gripper>`
  - For FK, use indices: `[0]=base, [1]=shoulder, [3]=elbow, [4]=wrist`

### Camera Frame Capture Procedure
To capture a frame with OpenCV when `usb_cam` is running:
```bash
# 1. Find and kill usb_cam (requires sudo)
sudo -S kill $(pgrep -f usb_cam_node_exe)   # password: <REDACTED>

# 2. Capture with OpenCV
python3 -c "import cv2; cap=cv2.VideoCapture(0); ret,frame=cap.read(); cv2.imwrite('frame.png', frame); cap.release()"

# 3. Restart usb_cam inside container or relaunch vision pipeline
```

---

## Mandatory Engineering Safety Protocols
### 1. Mandatory Backup Before Edit
**STRICT RULE:** Before making ANY structural, logic, or formatting changes to a source file, the agent MUST create a backup in the `/home/arduino/aimee-robot-ws/backups/` directory.
- Format: `<filename>.<date>_<time>_<reason>.bak`

### 2. Standard ROS 2 Transition
**MANDATE:** All "Arduino Bricks" must be rebuilt as standard ROS 2 nodes during validation.

---

## Current Best Calibration (2026-05-12)
- **Base:** UGV02 (Encoders active, IMU Disabled)
- **Ticks Per Meter:** 106.0
- **Wheel Separation:** 0.26m
- **Arm Limits (Raw):** Home: `[2056, 2060, 2636, 2484, 2043, 2062]`. Floor (X=0.196m): `[2059, 2703, 2435, 2038]`.
- **Coordinate Origin:** Shoulder joint is (0,0,0). Desk surface is at `Z ≈ -0.088m`.
- **Safety Stop:** 0.4m (Lidar-based, hard override)
- **Arm Speed (Duration ms):**
  - **Ideal Testing:** Transit: 6000ms, Z-moves: 4000ms, Gripper: 3000ms
  - **Standard Safe:** Transit: 2666ms, Z-moves: 1733ms, Gripper: 1333ms
  - **Max Safe:** Transit: 2000ms, Z-moves: 1500ms, Gripper: 1000ms
- **Grasp Height:** Z-offset is now 0.02m (was 0.01m) to avoid collisions with the desk.

## Current Best Setup (2026-05-12)
- **Vision Pipeline:** Hybrid C++/Python pipeline. `pose_estimator_node` extracts 3D coordinates from registered depth map.
- **Camera Height:** 60cm above desk (sweet spot — see findings below).
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

    ## Quick Start: Voice & Dashboard
    To launch the full AIMEE stack (Voice, LLM, Intent, Skills, and Monitor Dashboard) on the verified production domain:
    ```bash
    # 1. (On Host) Ensure the container is running
    docker start aimee-robot

    # 2. (In Container) Launch the core stack
    docker exec -it aimee-robot bash -c "
        export ROS_DOMAIN_ID=42
        source /opt/ros/humble/setup.bash
        source /workspace/install/setup.bash
        ros2 launch aimee_bringup core.launch.py
    "
    ```
    - **Dashboard URL:** `http://<robot_ip>:8081` (Verification: `curl -I localhost:8081`)
    - **Voice Manager:** Uses Vosk STT on Domain 42 by default.

    ---

    ## Technical Operational Details- **Container:** `aimee-robot` (Docker)
- **DDS:** Fast DDS / Fast DDS
- **Hardware Ports:** Lidar: `/dev/ttyUSB0`, Base: `/dev/ttyACM0`, Camera: `/dev/video0` (RGB) / OpenNI (Depth)

## Agent Editing Protocol (Anti-Corruption)
1. **Staging Pattern:** Write all complex code to `/root/staging_file.py` first. Use `cp` or `docker cp` to deploy. Never use multiline strings inside `run_shell_command`.
2. **Pre-Flight Linting:** After every edit, the agent MUST run `python3 -m py_compile` on the file.
3. **Atomic Backups:** Use the `/backups` folder exclusively for session recovery to avoid version drift.


---

## Session Progress (2026-05-09 Late Session — Camera Repositioning & Direct Pick Tests)

### 1. Camera Height Optimization
- **Tested 80cm:** Depth worked (78 raw = 0.78m), but 1.5cm dice were at the limit of detection.
- **Tested 50cm:** Astra Pro depth sensor had blind spot at center (0 raw). Too close — minimum range violated.
- **Settled on 60cm (Sweet Spot):**
  - Center depth: 59 raw = 0.59m ✅
  - Clean depth across entire desk — no blind spots.
  - Pixel size: ~1.1mm/pixel.
  - 6cm character = ~56 pixels wide (easily detectable).
  - 1.5cm die = ~14 pixels wide (detectable by color, marginal in depth).
  - **Dice numbers:** Dots are 2-3 pixels across — visible but not reliably readable at 640×480.

### 2. TF Updates for 60cm Height
- **Static TF Z updated:** `0.0869m → 0.7020m → 0.5000m`
  - Camera is 60cm above desk, arm base is ~10cm above desk (on UGV02).
  - Z = 0.50m reflects this geometry.
- **`max_depth` increased:** `0.80m → 1.20m` to allow desk edges and background.
- **`camera_pitch_deg` corrected:** `30.0° → 90.0°` (camera is directly overhead, perpendicular to desk).

### 3. Depth & Object Detectability Summary (at 60cm)
| Object | Height | Raw Depth | Detectable in Depth? | Detectable by Color? |
|--------|--------|-----------|---------------------|---------------------|
| Desk surface | — | 59-60 | ✅ Yes — 44.9% of image | N/A |
| 6cm pink character | 6cm | ~53-54 | ✅ Yes (6-unit contrast) | ✅ Yes (detected as "red") |
| 1.5cm die | 1.5cm | ~57-58 | ❌ No (blended into desk by 5×5 median) | ⚠️ Marginal (~14px wide) |

### 4. Direct Pick Tests (Vision Bypassed)
- **Goal:** Pick up at specific (X,Y,Z) coordinate without waiting for vision detection.
- **Command used:** `ros2 run aimee_manipulation direct_pick` (new script created).
- **Test 1 — Pink character at vision coords (-0.245, 0.293, -0.08):**
  - Arm moved approximately correct **distance** from base.
  - **Angle was 90° to the side** — indicates camera yaw rotation is not accounted for in pose_estimator.
- **Root cause:** `_transform_to_robot_frame()` only applies pitch rotation, not yaw. Camera is likely rotated ~90° around its optical axis relative to robot base.

### 5. Software Fixes Applied
- **`pose_estimator_node.py`:** Added `camera_yaw_deg` parameter. Transform now applies **yaw → pitch → reorientation**.
- **`vision_pipeline.launch.py`:** Added `camera_yaw_deg: 0.0` parameter (tune in next session).
- **`pick_place_server.py`:** Fixed grasp plan matching — now accepts grasp for same `object_class` when exact `object_id` changes rapidly (object tracker generates new IDs every frame).
- **`grasp_planner_node.py`:** `surface_offset` set to `0.01m` for 1cm-above-desk grasps.
- **`direct_pick.py`:** New reusable script for AimeeCloud-driven picks. Commands arm directly via `/arm/command` without vision pipeline.
- **`setup.py`:** Added `direct_pick` console script entry point.

### 6. Remaining Calibration Issues for Next Session
- **Camera yaw is UNKNOWN:** The `camera_yaw_deg` parameter exists but needs tuning. Try values like `90.0`, `-90.0`, or `180.0` until commanded angle matches physical direction.
- **TF X/Y may still need adjustment:** The translation values `X=-0.3088, Y=0.2370` were from the previous close-mounted camera position. With camera now directly overhead on a separate stand, these likely need recalibration.
- **Recommended calibration procedure:**
  1. Place pink character at center of camera view.
  2. Command arm to pick at a guessed coordinate.
  3. Observe where arm actually goes.
  4. Adjust `camera_yaw_deg` first ( Fixes angle).
  5. Adjust TF X/Y translation second (fixes position).

### 7. Safety Notes
- **12V power was turned OFF by user at end of session.**
- **Before next physical test:** Ensure arm is at home position after power-on. The `arm_kinematics_bridge_rpc` sends safe home on startup.
- **Emergency stop:** Always keep hand near power switch for first picks after coordinate changes.

## Files Modified This Session
```
/home/arduino/aimee-robot-ws/
├── src/aimee_bringup/launch/vision_pipeline.launch.py       [TF Z, pitch, yaw, max_depth]
├── src/aimee_perception/aimee_perception/pose_estimator_node.py  [Added camera_yaw_deg]
├── src/aimee_manipulation/aimee_manipulation/pick_place_server.py [ID matching fix]
├── src/aimee_manipulation/aimee_manipulation/direct_pick.py      [NEW — direct coordinate picking]
├── src/aimee_manipulation/setup.py                          [Added direct_pick entry point]
└── GEMINI.md                                                [This file — updated]
```


---

## Session Progress (2026-05-11 — Pick Verification & Calibration Diagnosis)

### 1. STM32 Firmware Updated
- Added `read_arm_positions()` RPC to STM32 trajectory engine.
  - Sends `READ\n` to ESP32 over serial, parses `POS:<J1,J2,J3,J4,J5,J6,J7>` response.
  - Returns comma-separated string over router socket.
- Added `receive_grasp(x,y,z,pitch,gripper_width,ms)` convenience RPC.
- **Status:** Firmware flashed successfully.

### 2. IK Math Verified Correct
- Replicated exact STM32 `ik_map()` in Python.
- **IK→FK round-trip error <1mm** for target (0.163, 0.199, -0.065, pitch=π/2).
  - Commanded joints: `[1470, 2670, 2169, 2326]`
  - FK returns: `(0.1630, 0.1993, -0.0648, 1.5693)`
- **Conclusion:** The analytic IK formulas are mathematically correct. The 3-4cm physical error is NOT in the math.

### 3. Servo Tracking is Accurate
- Grasp actual servos vs commanded:
  - J1: 1475 vs 1470 (+5 counts)
  - J2: 2670 vs 2670 (0)
  - J4 (elbow): 2168 vs 2169 (-1)
  - J5 (wrist): 2327 vs 2326 (+1)
- **Conclusion:** Servos reach commanded positions within a few counts. Not a tracking/backlash issue.

### 4. Critical Discovery — Grasp Position ≈ Marker 1 Position
**Correct FK** (using proper READ indices: `base[0], shoulder[1], elbow[3], wrist[4]`):

| | X | Y | Z | Pitch |
|---|---|---|---|---|
| **Marker 1** (calibration joints `[1479,2723,1400,2133,2313,2045,1111]`) | 0.1683 | 0.2000 | -0.0837 | 1.575 |
| **Grasp** (actual servos `[1475,2670,1456,2168,2327,2044,861]`) | 0.1647 | 0.1982 | -0.0647 | 1.569 |
| **Delta** | **3.6mm** | **1.8mm** | **19mm** | — |

- The grasp X/Y is **virtually identical** to Marker 1 (only ~4mm difference).
- The Z difference is expected: grasp was at pick height `z=-0.065` vs Marker 1 recorded at desk level `z≈-0.084`.
- **The arm WAS reaching the calibrated Marker 1 position.**

### 5. Tape Markings Have NOT Moved
- User confirmed blue tape markers have not shifted since calibration.
- Since tape hasn't moved and FK says arm is at the tape position, the 3-4cm physical miss the user observed means:
  1. **The camera moved/rotated** after the 5-point calibration was performed, OR
  2. **The calibration affine model has systematic error** — the 5 ground-truth points may not have been accurately placed, or the fitting has drifted, OR
  3. **The calibration ground-truth was recorded when the arm was not actually centered on the marker** (human eyeballing error during manual jogging).

### 6. `read_arm_positions()` Now Broken
- Earlier in session: `read_arm_positions()` returned valid servo values.
- **Current status:** Returns `ERR,ERR,ERR,ERR,ERR,ERR,ERR`.
  - ESP32 `st.ReadPos()` is returning `-1` for all 7 servo IDs.
  - **Writes still work** — arm moves normally when commanded.
  - Reads fail consistently. Likely ESP32 SCServo bus read timing issue or ESP32 needs power cycle/reflash.
- **Impact:** Cannot verify actual vs commanded servo positions until fixed.

### 7. FK Indexing Bug in Test Scripts
**CRITICAL BUG found in multiple test scripts:**
- ESP32 `READ` returns **7 values**: `[base, shoulder_driving, shoulder_driven, elbow, wrist, roll, gripper]`
- `fk_full()` and `fk()` in test scripts take `joints[:4]` or `raw_joints[:6]`, mapping:
  - `j1 = [0]` ✓ (base)
  - `j2 = [1]` ✓ (shoulder)
  - `j3 = [2]` ✗ (shoulder_driven — NOT elbow!)
  - `j4 = [3]` ✗ (elbow — NOT wrist!)
- **Correct indices for FK:** `j1=joints[0], j2=joints[1], j3=joints[3], j4=joints[4]`
- **Affected files:**
  - `/home/arduino/test_pick_loc1_verified.py` — `fk_full(joints)` uses `joints[:4]`
  - `/home/arduino/test_pick_verify_standalone.py` — `fk(raw[:6])` unpacks 6 values
  - Any script that passes READ output directly to FK without re-mapping indices.
- **Fix required:** Slice/re-map READ output before calling FK: `fk([read[0], read[1], read[3], read[4]])`

### 8. Joint Comparison (Grasp vs Marker 1)
Despite reaching the same X/Y, the servo values differ significantly (different posture):

| Joint | Grasp | Marker 1 | Diff | Degrees |
|-------|-------|----------|------|---------|
| J1 base | 1475 | 1479 | -4 | -0.35° |
| J2 shoulder | 2670 | 2723 | -53 | -4.66° |
| J4 elbow | 2168 | 2133 | +35 | +3.08° |
| J5 wrist | 2327 | 2313 | +14 | +1.23° |

The shoulder/elbow differences compensate geometrically to reach the same endpoint.

### 9. Next Steps (2026-05-12)
1. **Fix `read_arm_positions` / ESP32 READ** — try power cycling, or reflash ESP32 chaser firmware.
2. **Fix FK indexing bug** in all test scripts before using them again.
3. **Re-calibrate the affine model** — the 3-4cm error is in the camera-to-arm transform, not the arm kinematics.
   - Option A: Re-run `auto_calibrate_camera.py` or manual 5-point calibration.
   - Option B: Command arm to each of the 4 tape markers using their recorded ground-truth joints, verify visually, and re-fit the affine.
4. **Verify camera has not shifted** — compare `marker1_frame.jpg` to live camera view.

### Files Modified This Session
```
/home/arduino/aimee-robot-ws/
├── src/aimee_firmware/stm32_trajectory_engine/stm32_trajectory_engine.ino  [+read_arm_positions, +receive_grasp]
├── test_pick_loc1_verified.py          [Created/used — has FK indexing bug]
├── test_pick_verify_standalone.py      [Created/used — has FK indexing bug]
├── test_fk.py                          [Created — IK→FK verification]
├── grasp_frame.png                     [Captured at grasp location]
└── GEMINI.md                           [This file — updated]
```

---

## Session Progress (2026-05-12 — Interactive Calibration & Gripper Tuning)

### 1. ESP32 Serial Communication Restored
- Identified that `read_arm_positions()` was returning `ERR` because the ESP32 had crashed or lost sync.
- Created and executed a DTR/RTS serial reset script (`reset_esp32.py`) to soft-reboot the ESP32 chaser board.
- STM32 RPC `read_arm_positions` commands now successfully return valid 7-joint arrays.

### 2. Kinematics (FK) Bug Fix
- Identified a critical indexing bug in all Python test scripts (`test_pick_verify_standalone.py`, `test_pick_loc1_verified.py`, etc.).
- The scripts were incorrectly unpacking the ESP32's 7-value `POS:<base, shoulder_driving, shoulder_driven, elbow, wrist, roll, gripper>` response. They used indices `[:4]` mapping `shoulder_driven` to `elbow`, which skewed FK calculations by 3-4cm.
- Corrected the scripts to use exact indices: `[0], [1], [3], [4]`.
- Mapped FK `pitch` calculation precisely to the STM32's `ik_map` inverse: `pitch = w_rad + alpha + beta - π/2`.

### 3. Interactive Affine Camera Calibration
- Analyzed previous calibration data and found the 'Pink Character' ground-truth point was severely skewed (over 20cm off), polluting the least-squares affine fit.
- De-energized the arm (`FREEZE` command) to allow manual manipulation.
- Ran a new interactive script (`calibrate_step.py`) to visually record the pink character and mathematically record the exact arm joints at 4 corners of the desk.
- Recalculated the `calibration.yaml` affine matrix using the correct `fk_full` kinematics.
- **Result:** The new map perfectly compensated for a 4.3cm Y-axis physical shift in the arm's base. Residual mathematical error is now ~1.5mm.

### 4. Successful Pick & Gripper Tuning
- The arm accurately navigated to the newly calibrated coordinates (`X=0.2727, Y=-0.0856`).
- However, the `0.02m` gripper width was too wide to securely grasp the character.
- **Fix:** Changed the commanded grasp width from `0.02` to `0.005` in `test_pink_pick.py`.
- **Result:** The arm successfully picked up the pink character with a top-down grasp (`pitch=1.571`).

### Files Modified This Session
```
/home/arduino/aimee-robot-ws/
├── calibration.yaml                    [Updated affine matrix]
├── src/aimee_firmware/stm32_trajectory_engine/stm32_trajectory_engine.ino [Freeze support]
├── test_pick_verify_standalone.py      [Fixed FK indexing, top-down pitch]
├── test_pick_loc1_verified.py          [Fixed FK indexing]
├── test_pick_verify_direct.py          [Fixed FK indexing]
├── test_pick_verify.py                 [Fixed FK indexing]
├── test_pink_pick.py                   [New — RPC + Top-Down + 0.005 Gripper]
├── reset_esp32.py                      [New — DTR/RTS reset]
├── calibrate_step.py                   [New — Interactive 4-point calibration]
├── fit_new_affine.py                   [New — Affine least squares solver]
└── GEMINI.md                           [This file — updated]
```

---

## Session Progress (2026-06-02 — Voice Streaming & Storage Optimization)

### 1. Voice Streaming (Cloud) Implementation
- **Research:** Investigated the `aimee_voice_streaming` pipeline, which uses native PCM16 audio streaming via WebSockets to `aimeecloud.com` (Gemini Live/OpenAI Realtime backend).
- **Build:** Identified that the `aimee_voice_streaming` package was not built. Executed `colcon build` and fixed a ROS2 path mismatch by manually linking the executable to the `libexec` directory.
- **Verification:** Manually verified node startup and successful handshake with the AimeeCloud bridge. The node now correctly initializes `webrtcvad` and waits for a session ID.

### 2. Web Monitor Dashboard Updates
- **Node Integration:** Added **Voice Streaming (Cloud)** to the Node Launcher registry in `monitor_node.py`.
- **UI Refinement:** Updated `index.html` to start with all left-column sections (Active Nodes, Live Camera, Node Launcher, etc.) in a **collapsed state** for a cleaner initial view.
- **Bug Fix:** Fixed a structural issue in the dashboard where the **Live Camera** section failed to collapse.
- **Patching:** Manually updated the installed files in the ROS2 workspace to apply these changes without requiring a full rebuild during storage migration.

### 3. Storage Optimization & Docker Relocation
- **Disk Space Reclaimed:** Freed up approximately **6 GB** on the user partition (`/home/arduino`) and **4.2 GB** on the system root (`/`).
- **Cleanup Actions:**
    - Removed **5.3 GB** of ESP32 board packages from `~/.arduino15/packages/esp32`.
    - Cleared **~1 GB** of VS Code server caches, extensions, and logs.
    - Deleted old Docker logs and the `whisper-test` project.
- **Docker Data Relocation:** Successfully moved the Docker data root from the system partition (`/var/lib/docker`) to the user partition (`/home/arduino/docker-data`).
- **Configuration:** Updated `/etc/docker/daemon.json` with the new `data-root` and verified that the `aimee-robot` container starts and operates correctly from the new location.

### Files Modified This Session
```
/home/arduino/
├── .arduino15/packages/esp32           [Deleted — reclaimed 5.3GB]
├── .vscode-server/...                  [Cleaned — reclaimed ~1GB]
├── aimee-robot-ws/
│   ├── install/aimee_ros2_monitor/     [Patched — UI/Streaming updates]
│   └── install/aimee_voice_streaming/   [Built & Path-fixed]
├── docker-data/                        [New — Docker data root]
└── /etc/docker/daemon.json             [Updated — data-root redirection]
```


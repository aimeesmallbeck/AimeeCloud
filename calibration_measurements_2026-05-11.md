# Camera-to-Arm Calibration Measurements — 2026-05-11

## Hardware Setup
- **Camera**: Orbbec Astra Pro RGB+Depth; 640×480 color via `/dev/video0`
- **Camera position**: 60cm above desk, 10cm right, 30cm in front of arm base
- **Arm**: RoArm-M3 Pro via ESP32 chaser firmware on `/dev/ttyUSB0` (CP2102N, 921600 baud)
- **STM32 bridge**: `/var/run/arduino-router.sock` (msgpack RPC)
- **Desk Z**: -0.075m
- **Pick Z**: -0.065m (desk + 0.01m grasp_offset)
- **Gripper**: Close=0.02, Open=0.08

---

## Marked Positions (Blue Tape Markers)

### Marker 1 (Bottom-Left of desk, near user)
- **Image coordinates**: ~(45, 391) — see `marker1_frame.jpg`
- **Joint positions**: `POS:<1479,2723,1400,2133,2313,2045,1111>`

### Marker 2 (Top-Left of desk)
- **Image coordinates**: ~(158, 207) — see `marker2_frame.jpg`
- **Joint positions**: `POS:<1874,2919,1201,1445,2784,2045,1111>`

### Marker 3 (Top-Right of desk)
- **Image coordinates**: ~(361, 218) — see `marker3_frame.jpg`
- **Joint positions**: `POS:<2230,2922,1194,1445,2785,2046,1111>`

### Marker 4 (Bottom-Right of desk)
- **Image coordinates**: ~(428, 341) — see `marker4_frame.jpg`
- **Joint positions**: `POS:<2467,2743,1381,2021,2419,2042,1112>`

---

## Character Position (Pink)
- **Image coordinates**: ~(32, 396) bottom of contour — see `character_frame.jpg`
- **Joint positions**: `POS:<2049,2704,1412,2196,2313,2039,1111>`

---

## Historical Ground-Truth Anchors

### Anchor 1 — Successful Pick
- **Image**: centroid (229, 280) → bottom estimated (222, 293)
- **Arm commanded**: X=0.277, Y=0.014
- **Note**: Character fell out due to slight forward overshoot; X=0.270 may be better

### Anchor 2 — Orange Cap Landing Spot (previous miss)
- **Image**: (101, 351)
- **Arm commanded**: X=0.200, Y=0.129

### Anchor 3 — Yellow/Green Marker Landing Spot (last miss)
- **Image**: (24, 434)
- **Arm commanded**: X=0.126, Y=0.204

---

## Calibration Evolution

### Original (centroid-based, 2 anchors)
```
arm_x = 0.0011846 * (240 - v) + 0.32438
arm_y = -0.00092 * (u - 320) - 0.06972
```

### Bottom-based v1 (2 anchors + estimated bottom shift)
```
arm_x = 0.001305 * (240 - v) + 0.3462
arm_y = -0.000950 * (u - 320) - 0.0791
```

### Full-affine v2 (3 anchors, bottom-based)
```
arm_x = 0.000373*u - 0.000549*v + 0.354971
arm_y = -0.000932*u + 0.000039*v + 0.209236
```

### Current YAML (full-affine)
- scale_x: 0.000549
- offset_x: 0.3426
- skew_xy: 0.000373
- scale_y: -0.000932
- offset_y: -0.0796
- skew_yx: -0.000039

---

## Frame Files
- `/workspace/marker1_frame.jpg`
- `/workspace/marker2_frame.jpg`
- `/workspace/marker3_frame.jpg`
- `/workspace/marker4_frame.jpg`
- `/workspace/character_frame.jpg`

---

## ESP32 Chaser Serial Protocol
- **Port**: `/dev/ttyUSB0`
- **Baud**: 921600
- **Boot sequence** (normal mode): `DTR=True,RTS=True` → `DTR=False,RTS=False`
- **Commands**:
  - `PING` → `PONG`
  - `FREEZE` → `FROZEN` (disables torque, servos go limp)
  - `READ` → `POS:<J1,J2,J3,J4,J5,J6,J7>`
- **Waypoint format**: `<J1,J2,J3,J4,J5,J6>` (no spaces, newline terminated)

## STM32 Trajectory Engine RPC Methods
- `receive_waypoints(j1,j2,j3,j4,j5,j6,duration_ms)` — quintic trajectory
- `receive_cartesian(x,y,z,pitch,gripper_width,duration_ms)` — IK then quintic
- `stream_waypoints(j1,j2,j3,j4,j5,j6)` — bypass smoothing
- `stream_cartesian(x,y,z,pitch,gripper_width)` — bypass smoothing
- `freeze_arm()` — sends `FREEZE` to ESP32
- `ping_arm()` → 1/0 — sends `PING`, waits for `PONG`

## RoArm-M3 Link Parameters (from STM32 firmware)
- L1 = 0.12606 (base to shoulder)
- L2 = 0.23871 (upper arm)
- t2rad = 0.1259 (shoulder offset)
- L3 = 0.14449 (forearm)
- t3rad = 0.0
- LE = 0.17221 (wrist extension)
- tErad = 0.0795 (gripper angle offset)

## Joint Angle Mapping
- yaw   = (2047 - J1) * π / 2048
- alpha = (J2 - 2047) * π / 2048
- beta  = (J3 - 1024) * π / 2048
- w_rad = (J4 - 2047) * π / 2048
- pitch = w_rad + alpha + beta - π/2

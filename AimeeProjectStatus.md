# Aimee Project Status (Ground Truth)
**Last Updated:** 2026-06-17 (Session: Hardware Synchronization & Voice Streaming)

## 🎯 Current Mission
The **voice streaming and hardware synchronization** phase is successfully completed. The robot is now uniquely identified as **'Aimee'** and connected to the AimeeCloud native audio pipeline. The hardware stack has been optimized for high-quality audio capture and stereo playback. Parallel goals continue for **eye-in-hand arm camera calibration** with recent fine-tuning to the home position for improved clearance.

---

## 🦾 Hardware Interfaces (Verified)
| Component | Device Path | Details | Status |
|-----------|-------------|---------|--------|
| **Arduino UNO Q** | Host | RK3588S SoC (Identity: **Aimee**) | **Primary Controller** |
| **Arm Camera** | `/dev/video0` | Arducam 1080P-HDR (USB 2.0) | **ACTIVE** |
| **Astra Camera** | `/dev/video2` | Orbbec Astra Pro (USB 2.0) | **ACTIVE** |
| **Audio I/O** | `default` | Cyber Acoustics CA-2890GX (Spk) / USB PnP (Mic) | **ACTIVE** (Spk @ hw:0,0, Mic @ hw:3,0) |
| **STM32** | `/dev/ttyHS1` | Trajectory Engine via `arduino-router` | **ACTIVE** |
| **ESP32** | `/dev/ttyUSB0` | Joint Driver / Encoder Feedback | **ACTIVE** |

---

## 🔊 Audio & Voice Pipeline (v1.6)
- **High-Quality Audio:** Switched to a dedicated USB PnP microphone (`hw:3,0`) providing ~92% signal amplitude.
- **Stereo Playback:** Cyber Acoustics CA-2890GX speaker configured for 2-channel stereo via `.asoundrc`.
- **Cloud Identity:** `device_id` updated to **'Aimee'** to prevent session collisions with other robots.
- **Native Streaming:** `voice_streaming` node active using Gemini Live via AimeeCloud WebSocket.
- **VAD Stability:** webrtcvad calibrated with clear speech detection and automatic conversation timeouts.

---

## 🦾 Manipulation & Kinematics
- **Elevated Home Pose:** Arm `HOME` position raised by **+3.0 cm** (Z-axis) to improve workspace clearance and camera field-of-view.
- **IK-Derived Calibration:** New raw joint values `[2056, 2047, 2502, 2606, 2043, 2062]` calculated and applied to `arm_actions.py` and `arm_kinematics_bridge_rpc.py`.
- **Perspective Calibration:** Base calibration `/home/arduino/dice_fixed_look_calibration_merged.json` remains stable (~3.8 mm residual).
- **Pick-Y Bias Correction:** Empirical offset of `0.010 m` active.
- **Place-Y Bias Correction:** `0.055 m` added to compensate for consistent right-side landing.

---

## ⚠️ Known Constraints & Active Issues
1. **CPU Overhead:** `ros2_monitor` consumes ~50% CPU during high-activity sessions. Further optimization to log polling and metric gathering is needed.
2. **USB 2.0 Latency:** High FPS arm camera streaming can occasionally impact voice streaming audio stability; recommended to keep arm camera at 15fps or lower during voice sessions.
3. **Session Sync:** The `voice_streaming` node depends on the `cloud_bridge` for session IDs; nodes should be started in sequence or with a slight delay.

---

## ✅ Next Steps
1. **Monitor Optimization:** Refactor `monitor_node.py` to use lower frequency polling for system metrics and optimized log buffer management.
2. **Vision Fine-Tuning:** Implement a final short-range visual servo check at `safe_z` before grasping to drive residual error to < 5 mm.
3. **Identity Persistence:** Ensure any future firmware or environment flashes maintain the **'Aimee'** hostname and device ID.

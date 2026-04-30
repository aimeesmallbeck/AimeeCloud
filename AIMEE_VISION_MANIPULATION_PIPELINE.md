# AimeeCloud Architecture: Vision to Fluid Manipulation

This document outlines the end-to-end pipeline for utilizing the OBSBOT camera and Arduino UNO Q to achieve fluid, semantically-aware pick-and-place capabilities using a local-first compute strategy.

## Phase 1: Semantic Vision Bridge (Local + Cloud)
**The Trigger:** A user issues a voice or text command (e.g., "Aimee, pick up the screwdriver").

*   **Image Capture (Local):** AimeeCloud calls a ROS 2 Service (`srv/CaptureFrame`) on the local UNO Q C++ vision node. The node grabs a single frame directly from the zero-copy memory pointer, compresses it to JPEG, and sends it to the cloud.
*   **Semantic Grounding (Cloud):** AimeeCloud’s multimodal model processes the image and prompt. It returns a 2D bounding box `[x_min, y_min, x_max, y_max]` of the target, along with the object's known real-world physical dimensions.

## Phase 2: 3D Localization & Transform (Local)
*   **ROI Masking:** The local C++ vision node applies the cloud-provided 2D bounding box as a Region of Interest (ROI) mask on the live 30fps camera feed.
*   **Monocular Depth:** The node calculates the Z-depth by comparing the apparent pixel width of the object inside the ROI against the cloud-provided real-world dimensions. Target is now localized at `[X, Y, Z]` relative to the camera.
*   **TF2 Transform:** A ROS 2 `static_transform_publisher` broadcasts the physical relationship between the OBSBOT lens (`camera_link`) and the arm base (`arm_base_link`). The target's coordinates are instantly translated into the arm's workspace.

## Phase 3: Inverse Kinematics (Local First)
*   **Local C++ IK Solver:** A dedicated, lightweight C++ node on the UNO Q subscribes to the 3D target coordinates. It uses analytical Inverse Kinematics (trigonometry) to calculate the specific joint angles required to reach the target.
*   *(Contingency Plan: If the IK math throttles the UNO Q's ARM64 processor or pushes against the 4GB RAM limit, this specific step will be offloaded back to AimeeCloud for PyBullet/Pinocchio processing).*

## Phase 4: Smooth Trajectory Generation (Local - STM32 Co-Processor)
*   **Waypoint Definition:** The system defines the major discrete waypoints: Home -> Approach -> Grasp -> Retract -> Drop.
*   **RPC Forwarding:** The ROS 2 `arm_kinematics_bridge_rpc` Python node transmits these 5 major waypoints along with their execution durations via MessagePack RPC to the `arduino-router.sock` Unix socket. The router forwards these seamlessly to the STM32 microcontroller.
*   **Quintic Spline Interpolation (STM32):** The STM32 acts as a dedicated Real-Time Trajectory Engine. It computes a minimum-jerk trajectory (quintic spline) between waypoints, mathematically guaranteeing that the acceleration and deceleration profiles are completely smooth and that velocity never hits zero mid-movement.
*   **Micro-Waypoints:** The STM32 samples this curve at a strict 50Hz internal loop, generating a dense stream of intermediate joint angles. This completely isolates the time-critical motor control from any Linux or ROS 2 scheduling jitter.

## Phase 5: High-Speed Serial Bridge (STM32 to ESP32)
*   **Direct Hardware Serial:** The STM32 bypasses the ARM64 completely for this step, opening its own Hardware Serial connection directly to the ESP32 at a baud rate of 921600.
*   **Lean Payload:** The 50Hz micro-waypoints are streamed as highly compact comma-separated strings (e.g., `<J1, J2, J3, J4, J5, J6>\n`) to avoid JSON parsing overhead on the microcontroller.

## Phase 6: Custom ESP32 Firmware (Waveshare Override)
The factory Waveshare firmware is replaced to eliminate its internal "stop-and-go" discrete waypoint logic.

**Flashing Instructions:**
1. Install the flashing utility on the UNO Q: `pip install esptool`
2. Connect the Waveshare board via USB.
3. Flash the custom binary:
   ```bash
   esptool.py --port /dev/ttyUSB0 --baud 921600 write_flash 0x10000 custom_arm_firmware.bin
   ```

**Firmware Logic (The "Chaser" Loop):**
*   Set `Serial.begin(921600);`.
*   Map mapped ESP32 GPIO pins to standard `ESP32Servo` objects.
    *   **Note on Hardware Pinouts:** The Waveshare ESP32 board communicates with its servos via UART. Based on the factory `RoArm-M3_config.h`, the pinouts are:
        *   `RoArmM3_Servo_RXD`: GPIO 18
        *   `RoArmM3_Servo_TXD`: GPIO 19
*   Implement a non-blocking `loop()` that constantly checks `Serial.available()`.
*   Instantly parse incoming micro-waypoints and write the new values directly to the servos. The constant, high-frequency updating forces the servos to smoothly "chase" the moving target along the spline curve, eliminating all mechanical jerking.
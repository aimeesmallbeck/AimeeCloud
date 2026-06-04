# Aimee Project Plan - Quick Reference (v2.2)

## Overview
- **Platform:** Arduino UNO Q (Raspberry Pi)
- **Architecture:** ROS2 Humble + Arduino Brick Framework
- **Cloud:** AimeeCloud (Digital Ocean)

## Robots
| Robot | Base | Arm | Main Camera | Secondary |
|-------|------|-----|-------------|-----------|
| **Ron** | UGV02 | RoArm-M3 | OBSBOT Tiny 2 | OV7670 |
| **Wren** | Wave Rover | - | OBSBOT Tiny 2 | - |

## Key Technologies
- **Wake Word:** Edge Impulse (custom model)
- **STT:** Vosk (offline)
- **TTS:** Piper/gTTS
- **LLM:** Qwen2.5-0.5B (local) via **Action Server**
- **DDS:** Fast DDS with **Shared Memory (SHM)** transport
- **Camera:** OBSBOT SDK via OSC protocol
- **Memory:** SQLite + ChromaDB

## Architecture Layers
1. **Brick Layer** - Modular hardware components
2. **ROS2 Bridge** - Message bus and node management
3. **Skill Layer** - Local and cloud skills

## Core Bricks
- `brick_wake_word_ei` - Edge Impulse keyword spotting
- `brick_local_asr` - Vosk speech-to-text
- `brick_local_tts` - Piper/gTTS text-to-speech
- `brick_local_llm` - Local LLM inference
- `brick_ugv02_ctrl` - UGV02 base control
- `brick_roarm_ctrl` - RoArm-M3 arm control
- `brick_cloud_bridge` - AimeeCloud communication
- `brick_vision_obsbot` - OBSBOT camera control
- `brick_memory_sqlite` - Local persistence

## Critical Optimizations (Gemini Feedback)

### 1. Memory: Fast DDS + Shared Memory
UNO Q has 4GB RAM. Configure Fast DDS with SHM transport to prevent message duplication.
```bash
export FASTRTPS_DEFAULT_PROFILES_FILE=~/aimee-robot-ws/fastdds_shm.xml
```

### 2. LLM: Action Server (Not Service)
Services block; Actions support:
- Long-running tasks (2-5 sec generation)
- Streaming feedback (token-by-token)
- Preemption (cancel on "Stop!")

### 3. Network: USB RNDIS Routing
OBSBOT at 192.168.5.1 can hijack default gateway. Fix routing:
```bash
# Prioritize Wi-Fi for internet
sudo ip route add default via 192.168.1.1 dev wlan0 metric 100
# OBSBOT only for local subnet
sudo ip route add 192.168.5.0/24 dev usb0 metric 800
```

## Implementation Timeline
- **Week 1-2:** Core Infrastructure (ROS2 workspace, bricks)
- **Week 3:** Voice Bricks (wake word, ASR, TTS)
- **Week 4-5:** Hardware Control (UGV02, RoArm-M3)
- **Week 6-7:** Intelligence (LLM, memory, intent routing)
- **Week 8:** Cloud Integration (AimeeCloud bridge)
- **Week 9:** Vision (OBSBOT, face recognition)
- **Week 10:** Skills Framework
- **Week 11-12:** Integration & Polish

## Quick Commands
```bash
# Build
cd ~/aimee-robot-ws && colcon build --symlink-install

# Launch
source install/setup.bash
ros2 launch aimee_bringup robot.launch.py robot:=ron

# Test
ros2 topic pub /voice/speak std_msgs/String "data: 'Hello!'"
ros2 topic pub /cmd_vel geometry_msgs/Twist "{linear: {x: 0.5}}"
```

## Full Plan
See `Aimee_Project_Plan.md` for complete details.

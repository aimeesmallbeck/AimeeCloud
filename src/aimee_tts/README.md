# Text-to-Speech Node (aimee_tts)

Standard ROS2 node for Text-to-Speech with Kokoro (offline, primary) and gTTS (cloud fallback) for the AIMEE Robot.

## Overview

This is a **standard ROS2 node** (no Arduino brick abstraction). It provides TTS conversion with two engines:
- **Kokoro**: Primary, offline, high quality, multiple voices
- **gTTS**: Cloud fallback when available

### Production Plan

| Phase | Default Engine | Fallback | Use Case |
|-------|---------------|----------|----------|
| Development | kokoro | gtts | Development, testing |
| Pre-Production | auto | gtts | Auto-switch based on connectivity |
| Production | kokoro | gtts | Offline-primary operation |

## Features

- **Kokoro Primary**: Fast, high-quality, offline neural TTS
- **gTTS Fallback**: Cloud backup when needed
- **Auto Fallback**: Automatically switch based on connectivity
- **Preemption**: Interrupt current speech
- **Queue Management**: Sequential playback
- **Volume & Voice Control**: Runtime adjustable

## Installation

```bash
cd ~/aimee-robot-ws
source setup_env.sh
colcon build --packages-select aimee_tts
source install/setup.bash
```

## Usage

### Basic Usage (Kokoro default)

```bash
# Start TTS node
ros2 run aimee_tts tts_node

# Speak text
ros2 topic pub /tts/speak std_msgs/String "data: 'Hello, I am AIMEE'"
```

### With Explicit gTTS Fallback

```bash
ros2 run aimee_tts tts_node \
  --ros-args \
  -p default_engine:=kokoro \
  -p fallback_engine:=gtts
```

### Auto Mode (Hybrid)

```bash
# Automatically selects gtts (online) or kokoro (offline)
ros2 run aimee_tts tts_node \
  --ros-args \
  -p default_engine:=auto \
  -p auto_fallback:=true
```

## ROS2 Interface

### Subscribers

| Topic | Type | Description |
|-------|------|-------------|
| `/tts/speak` | `std_msgs/String` | Text to speak (format: `[engine|voice:]text`) |
| `/tts/control` | `std_msgs/String` | Control: `stop`, `preempt`, `status` |
| `/tts/volume` | `std_msgs/Float32` | Volume (0.0-1.0) |
| `/tts/voice` | `std_msgs/String` | Dynamic voice selection (Kokoro) |

### Publishers

| Topic | Type | Description |
|-------|------|-------------|
| `/tts/status` | `std_msgs/String` | Status info |
| `/tts/is_speaking` | `std_msgs/Bool` | True when speaking |

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `default_engine` | string | "kokoro" | Default: kokoro, gtts, auto |
| `fallback_engine` | string | "gtts" | Fallback on failure |
| `auto_fallback` | bool | true | Auto-switch when offline |
| `default_voice` | string | "af_heart" | Default Kokoro voice |
| `kokoro_lang` | string | "en-us" | Kokoro language code |
| `kokoro_speed` | float | 1.0 | Kokoro speed multiplier |
| `gtts_lang` | string | "en" | gTTS language |
| `volume` | float | 1.0 | Default volume |
| `speed` | float | 1.0 | Default speed |

## Examples

### Specify Engine or Voice in Message

```bash
# Force gTTS
ros2 topic pub /tts/speak std_msgs/String "data: 'gtts:Hello from Google'"

# Use specific Kokoro voice
ros2 topic pub /tts/speak std_msgs/String "data: 'kokoro|am_michael:Hello from Kokoro'"
```

### Control Speech

```bash
# Stop/preempt current speech
ros2 topic pub /tts/control std_msgs/String "data: 'stop'"

# Change volume
ros2 topic pub /tts/volume std_msgs/Float32 "data: 0.5"

# Change voice
ros2 topic pub /tts/voice std_msgs/String "data: 'af_bella'"
```

### Monitor Status

```bash
# Check if speaking
ros2 topic echo /tts/is_speaking

# View status
ros2 topic echo /tts/status
```

## Engine Comparison

| Engine | Quality | Speed | Offline | RAM | Best For |
|--------|---------|-------|---------|-----|----------|
| Kokoro | Very High | Fast | Yes | ~100MB | Primary / Production |
| gTTS | High | 1-3s latency | No | Low | Cloud fallback |

## Troubleshooting

### No Audio Output

```bash
# Check audio device
aplay -l

# Test with aplay
aplay /usr/share/sounds/alsa/Front_Center.wav

# Check pygame
python3 -c "import pygame; pygame.mixer.init(); print('OK')"
```

### gTTS Fails (Offline)

Enable auto-fallback to Kokoro:
```bash
ros2 param set /tts auto_fallback true
```

### Kokoro Import Error

Ensure `pykokoro` or `kokoro` is installed:
```bash
pip install pykokoro
# or
pip install kokoro
```

## License

MPL-2.0

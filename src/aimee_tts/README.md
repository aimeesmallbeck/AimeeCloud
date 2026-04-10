# Text-to-Speech Brick (TTS)

ROS2 brick for Text-to-Speech with gTTS (cloud) and Piper (local) support for the AIMEE Robot.

## Overview

This brick provides TTS conversion with multiple engines:
- **gTTS**: High quality, requires internet (development default)
- **Piper**: Local neural TTS, fast, offline (production target)
- **pyttsx3**: Fallback, always available

### Production Plan

| Phase | Default Engine | Fallback | Use Case |
|-------|---------------|----------|----------|
| Development | gTTS | pyttsx3 | Development, testing |
| Pre-Production | auto | pyttsx3 | Testing local TTS |
| Production | Piper | pyttsx3 | Offline operation |

## Features

- **Multiple Engines**: gTTS, Piper, pyttsx3
- **Auto Fallback**: Automatically switch to local TTS when offline
- **Preemption**: Interrupt current speech
- **Queue Management**: Sequential playback with priority
- **Volume Control**: Runtime adjustable

## Installation

```bash
cd ~/aimee-robot-ws
source setup_env.sh
colcon build --packages-select aimee_tts
source install/setup.bash
```

### Install Piper Models (Optional, for local TTS)

```bash
# Download script
mkdir -p ~/.local/share/piper-tts
cd ~/.local/share/piper-tts

# Download en_US-lessac-medium (recommended)
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
```

## Usage

### Basic Usage (gTTS)

```bash
# Start TTS node
ros2 run aimee_tts tts_node

# Speak text
ros2 topic pub /tts/speak std_msgs/String "data: 'Hello, I am AIMEE'"
```

### With Piper (Local TTS)

```bash
# Start with Piper model
ros2 run aimee_tts tts_node \
  --ros-args \
  -p default_engine:=piper \
  -p piper_model:=~/.local/share/piper-tts/en_US-lessac-medium.onnx

# Speak
ros2 topic pub /tts/speak std_msgs/String "data: 'Hello from local TTS'"
```

### Auto Mode (Hybrid)

```bash
# Automatically selects gtts (online) or piper (offline)
ros2 run aimee_tts tts_node \
  --ros-args \
  -p default_engine:=auto \
  -p auto_fallback:=true \
  -p piper_model:=~/.local/share/piper-tts/en_US-lessac-medium.onnx
```

## ROS2 Interface

### Subscribers

| Topic | Type | Description |
|-------|------|-------------|
| `/tts/speak` | `std_msgs/String` | Text to speak (format: `[engine:]text`) |
| `/tts/control` | `std_msgs/String` | Control: `stop`, `preempt`, `status` |
| `/tts/volume` | `std_msgs/Float32` | Volume (0.0-1.0) |

### Publishers

| Topic | Type | Description |
|-------|------|-------------|
| `/tts/status` | `std_msgs/String` | Status info |
| `/tts/is_speaking` | `std_msgs/Bool` | True when speaking |

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `default_engine` | string | "gtts" | Default: gtts, piper, pyttsx3, auto |
| `fallback_engine` | string | "pyttsx3" | Fallback on failure |
| `auto_fallback` | bool | true | Auto-switch when offline |
| `piper_model` | string | "" | Path to Piper ONNX model |
| `gtts_lang` | string | "en" | gTTS language |
| `volume` | float | 1.0 | Default volume |
| `speed` | float | 1.0 | Default speed |

## Examples

### Specify Engine in Message

```bash
# Force Piper
ros2 topic pub /tts/speak std_msgs/String "data: 'piper:Hello from Piper'"

# Force gTTS
ros2 topic pub /tts/speak std_msgs/String "data: 'gtts:Hello from Google'"

# Force pyttsx3
ros2 topic pub /tts/speak std_msgs/String "data: 'pyttsx3:Hello from pyttsx3'"
```

### Control Speech

```bash
# Stop/preempt current speech
ros2 topic pub /tts/control std_msgs/String "data: 'stop'"

# Change volume
ros2 topic pub /tts/volume std_msgs/Float32 "data: 0.5"
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
| gTTS | High | 1-3s latency | No | Low | Development |
| Piper | High | 0.1-0.3s latency | Yes | ~100MB | Production |
| pyttsx3 | Low | Instant | Yes | ~20MB | Emergency fallback |

## Migration to Production

### Step 1: Test Piper

```bash
# Download model
mkdir -p ~/.local/share/piper-tts
cd ~/.local/share/piper-tts
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json

# Test
ros2 run aimee_tts tts_node \
  -p default_engine:=piper \
  -p piper_model:=~/.local/share/piper-tts/en_US-lessac-medium.onnx
```

### Step 2: Hybrid Mode

```bash
# Use gTTS when online, Piper when offline
ros2 run aimee_tts tts_node \
  -p default_engine:=auto \
  -p auto_fallback:=true \
  -p piper_model:=~/.local/share/piper-tts/en_US-lessac-medium.onnx
```

### Step 3: Production (Local Only)

```bash
# Disable gTTS, use Piper only
ros2 run aimee_tts tts_node \
  -p default_engine:=piper \
  -p fallback_engine:=pyttsx3 \
  -p auto_fallback:=false
```

## Troubleshooting

### Piper Model Not Found

```bash
# Verify model exists
ls -la ~/.local/share/piper-tts/

# Should show:
# en_US-lessac-medium.onnx
# en_US-lessac-medium.onnx.json
```

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

Enable auto-fallback:
```bash
ros2 param set /tts auto_fallback true
```

### Piper Quality Issues

Try different model:
- `en_US-lessac-medium` - Balanced (recommended)
- `en_US-ryan-medium` - Alternative voice
- `en_US-libritts-high` - Higher quality, slower

## License

MPL-2.0

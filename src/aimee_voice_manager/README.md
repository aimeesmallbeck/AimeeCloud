# Voice Manager Brick (STT)

ROS2 brick for speech-to-text using Vosk or Whisper for the AIMEE Robot.

## Overview

This brick captures audio after wake word detection and performs speech-to-text:
- **Triggered by**: `/wake_word/detected` topic
- **Outputs**: `/voice/transcription` topic
- **Engines**: Vosk (fast, offline) or Whisper (accurate)

## Features

- **Vosk Integration**: Fast, offline STT optimized for 4GB RAM
- **Whisper Support**: More accurate, higher resource usage
- **Wake Word Triggered**: Automatically records after wake word detection
- **Streaming Partials**: Optional partial result publishing
- **Configurable**: Runtime adjustable parameters

## Installation

```bash
cd ~/aimee-robot-ws
source setup_env.sh
colcon build --packages-select aimee_msgs aimee_voice_manager
source install/setup.bash
```

## Dependencies

### Vosk (Default)
```bash
pip3 install vosk
```

Models are stored in `/home/arduino/vosk-models/`:
- `vosk-model-small-en-us-0.15` (default, ~40MB)
- `vosk-model-en-us-0.22-lgraph` (larger, more accurate)

### Whisper (Optional)
```bash
pip3 install openai-whisper
```

## Usage

### Basic Usage

```bash
# Start with Vosk (default)
ros2 run aimee_voice_manager voice_manager_node

# Start with Whisper
ros2 run aimee_voice_manager voice_manager_node --ros-args -p engine:=whisper
```

### With Parameters

```bash
ros2 run aimee_voice_manager voice_manager_node \
  --ros-args \
  -p engine:=vosk \
  -p model_path:=/path/to/custom/model \
  -p record_duration:=5.0 \
  -p publish_partials:=true \
  -p debug:=true
```

## ROS2 Interface

### Subscribed Topics

| Topic | Type | Description |
|-------|------|-------------|
| `/wake_word/detected` | `aimee_msgs/WakeWordDetection` | Triggers recording |
| `/voice/control` | `std_msgs/String` | Control commands: `start`, `stop`, `status` |

### Published Topics

| Topic | Type | Description |
|-------|------|-------------|
| `/voice/transcription` | `aimee_msgs/Transcription` | Final transcription results |
| `/voice/partial` | `aimee_msgs/Transcription` | Partial results (streaming) |
| `/voice/status` | `std_msgs/String` | Status updates |

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `engine` | string | "vosk" | STT engine: "vosk" or "whisper" |
| `model_path` | string | "" | Custom model path (empty for default) |
| `record_duration` | double | 5.0 | Max recording duration (seconds) |
| `sample_rate` | int | 16000 | Audio sample rate (Hz) |
| `audio_device` | string | "default" | ALSA audio device |
| `command_timeout` | double | 10.0 | Max time to wait for command |
| `min_command_length` | double | 0.5 | Minimum command duration |
| `enabled` | bool | true | Enable/disable voice manager |
| `publish_partials` | bool | true | Publish partial results |
| `debug` | bool | false | Enable debug logging |

## Pipeline Flow

```
[Microphone] → [WakeWordEIBrick] → /wake_word/detected
                                          ↓
                              [VoiceManagerNode]
                                          ↓
                              /voice/transcription
                                          ↓
                               [Intent Router]
```

## Example Usage

### Test with Mock Wake Word

```bash
# Terminal 1: Start voice manager
ros2 run aimee_voice_manager voice_manager_node

# Terminal 2: Monitor transcriptions
ros2 topic echo /voice/transcription

# Terminal 3: Simulate wake word detection
ros2 topic pub /wake_word/detected aimee_msgs/WakeWordDetection "
  wake_word: 'aimee'
  confidence: 0.95
  source: 'test'
  active: true
  session_id: 'test123'
"
```

### Control Recording

```bash
# Disable voice manager
ros2 topic pub /voice/control std_msgs/String "data: 'stop'"

# Re-enable
ros2 topic pub /voice/control std_msgs/String "data: 'start'"

# Check status
ros2 topic pub /voice/control std_msgs/String "data: 'status'"
```

### Adjust Parameters

```bash
# Change recording duration
ros2 param set /voice_manager record_duration 3.0

# Disable partial results
ros2 param set /voice_manager publish_partials false
```

## Architecture

### VoiceManagerBrick
- Core STT functionality in `brick/voice_manager.py`
- Supports both Vosk and Whisper engines
- Async recording and transcription
- Callback-based result delivery

### VoiceManagerNode
- ROS2 wrapper in `voice_manager_node.py`
- Topic subscription/publishing
- Parameter server
- Lifecycle management

## Troubleshooting

### Model Not Found

```bash
# Check Vosk models
ls -la ~/vosk-models/

# Download model if missing
mkdir -p ~/vosk-models/
cd ~/vosk-models/
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
```

### No Audio Input

```bash
# Check ALSA devices
arecord -l
arecord -L

# Test recording
arecord -D default -f S16_LE -r 16000 -c 1 test.wav

# List available devices
cat /proc/asound/cards
```

### High CPU Usage (Whisper)

Whisper is resource-intensive. For 4GB RAM systems:
- Use `tiny` or `base` model: `-p model_path:=tiny`
- Prefer Vosk for always-on operation
- Use Whisper only for accuracy-critical scenarios

### Low Recognition Accuracy

For Vosk:
- Use larger model (if RAM permits)
- Ensure 16kHz sample rate
- Check audio levels (not too quiet/loud)

For Whisper:
- Use larger model size
- Ensure clear audio input
- Check language setting

## License

MPL-2.0

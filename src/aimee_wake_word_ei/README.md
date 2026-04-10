# Wake Word Detection Brick (Edge Impulse)

ROS2 brick for wake word detection using Edge Impulse keyword spotting model for the AIMEE Robot.

## Overview

This brick continuously listens for the "Hey Aimee" wake word using an Edge Impulse machine learning model and publishes detection events to ROS2 topics.

## Features

- **Edge Impulse Integration**: Uses the trained `.eim` model from Edge Impulse
- **Configurable Threshold**: Adjustable confidence threshold for detections
- **Cooldown Protection**: Prevents rapid-fire detections with configurable cooldown
- **ROS2 Native**: Publishes standard ROS2 messages for easy integration
- **Runtime Control**: Start/stop listening via ROS2 topics

## Model Information

- **Model**: Edge Impulse keyword spotting model
- **Labels**: `aimee`, `noise`, `unknown`
- **Sample Rate**: 16kHz
- **Path**: `/home/arduino/.arduino-bricks/models/custom-ei/ei-model-953002-1/model.eim`

## Installation

```bash
cd ~/aimee-robot-ws
source setup_env.sh
colcon build --packages-select aimee_msgs aimee_wake_word_ei
source install/setup.bash
```

## Usage

### Run the Node

```bash
ros2 run aimee_wake_word_ei wake_word_ei_node
```

### With Parameters

```bash
ros2 run aimee_wake_word_ei wake_word_ei_node \
  --ros-args \
  -p confidence_threshold:=0.75 \
  -p cooldown_seconds:=3.0 \
  -p debug:=true
```

## ROS2 Interface

### Published Topics

| Topic | Type | Description |
|-------|------|-------------|
| `/wake_word/detected` | `aimee_msgs/WakeWordDetection` | Published when wake word is detected |
| `/wake_word/classification` | `std_msgs/String` | Raw classification results (JSON) |

### Subscribed Topics

| Topic | Type | Description |
|-------|------|-------------|
| `/wake_word/control` | `std_msgs/String` | Control commands: `start`, `stop`, `status` |

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `confidence_threshold` | double | 0.70 | Minimum confidence for detection |
| `cooldown_seconds` | double | 2.0 | Minimum time between detections |
| `enabled` | bool | true | Enable/disable detection |
| `debug` | bool | false | Enable debug logging |

## Example Usage

### Monitor Detections

```bash
# Terminal 1: Start the node
ros2 run aimee_wake_word_ei wake_word_ei_node

# Terminal 2: Monitor detections
ros2 topic echo /wake_word/detected
```

### Control Listening

```bash
# Stop listening
ros2 topic pub /wake_word/control std_msgs/String "data: 'stop'"

# Start listening
ros2 topic pub /wake_word/control std_msgs/String "data: 'start'"

# Get status
ros2 topic pub /wake_word/control std_msgs/String "data: 'status'"
```

### Adjust Parameters at Runtime

```bash
# Increase confidence threshold
ros2 param set /wake_word_ei confidence_threshold 0.85

# Disable detection
ros2 param set /wake_word_ei enabled false
```

## Integration with Voice Pipeline

This brick is designed to work with the AIMEE voice pipeline:

1. **Wake Word Detection** (this brick) → Publishes `/wake_word/detected`
2. **Voice Manager** (STT brick) → Subscribes to trigger recording
3. **Intent Router** → Processes transcribed commands

```
[Microphone] → [WakeWordEIBrick] → /wake_word/detected
                                          ↓
[VoiceManager] ← triggers → [Speech-to-Text] → /voice/transcription
                                                   ↓
                                         [Intent Router]
```

## Architecture

The brick consists of two main components:

1. **WakeWordEIBrick** (`brick/wake_word_ei.py`): Core functionality
   - Manages Edge Impulse model process
   - Parses classification output
   - Handles detection logic and cooldowns

2. **WakeWordEINode** (`wake_word_ei_node.py`): ROS2 wrapper
   - Publishes ROS2 messages
   - Handles parameter server
   - Manages node lifecycle

## Troubleshooting

### Model Not Found

```
WakeWordEIBrickError: Model file not found
```

Verify the model exists:
```bash
ls -la /home/arduino/.arduino-bricks/models/custom-ei/ei-model-953002-1/model.eim
```

### No Audio Input

Check ALSA devices:
```bash
arecord -l
arecord -L
```

Test recording:
```bash
arecord -D default -f S16_LE -r 16000 -c 1 test.wav
```

### High False Positives

Increase confidence threshold:
```bash
ros2 param set /wake_word_ei confidence_threshold 0.85
```

Or increase cooldown:
```bash
ros2 param set /wake_word_ei cooldown_seconds 5.0
```

## License

MPL-2.0

# Test Dashboard

Web-based testing dashboard for the AIMEE Robot with simulation mode support.

## Overview

This package provides a web dashboard for testing all AIMEE robot components:
- **Runs on Arduino UNO Q**: Local hosting, no external server needed
- **Simulation Mode**: Test without hardware connected
- **Real Mode**: Test with actual hardware
- **Toggle Switch**: Switch between modes per component

## Features

### Component Testing
- ✅ Wake Word Detection (Edge Impulse)
- ✅ Speech-to-Text (Vosk)
- ✅ Text-to-Speech (gTTS/Piper)
- ✅ LLM Server
- ✅ Intent Router
- ✅ Skill Manager
- ✅ Microphone
- ✅ Speaker
- 📷 Camera (OBSBOT) - when connected

### Dashboard Features
- Real-time ROS2 topic monitoring
- Component enable/disable toggles
- Simulation vs Real mode per component
- Full pipeline testing
- System health monitoring
- Mobile-friendly web interface

## Installation

```bash
cd ~/aimee-robot-ws
source setup_env.sh
colcon build --packages-select aimee_test_dashboard
source install/setup.bash
```

## Usage

### Start Dashboard

```bash
ros2 run aimee_test_dashboard dashboard_node
```

### Access Dashboard

Open browser and navigate to:
```
http://localhost:5000
```

Or from another device on the same network:
```
http://<UNO_Q_IP>:5000
```

## Dashboard Interface

### Component Cards

Each component has a card with:
- **Enable Toggle**: Turn component on/off
- **Simulation Toggle**: Switch between sim/real mode
- **Test Button**: Run test for that component
- **Result Box**: Display test results

### Simulation Mode

When enabled, the dashboard simulates:
- **Wake Word**: Simulated "aimee" detection
- **STT**: Returns predefined text
- **TTS**: Shows what would be spoken
- **LLM**: Returns canned responses
- **Intent**: Predefined intent classification
- **Skills**: No actual hardware movement
- **Camera**: Test pattern

### Real Mode

When disabled (real mode):
- **Wake Word**: Listens to actual microphone
- **STT**: Records and transcribes real speech
- **TTS**: Speaks through actual speaker
- **LLM**: Calls local llama.cpp server
- **Intent**: Real LLM classification
- **Skills**: **ACTUAL HARDWARE MOVES** ⚠️
- **Camera**: Real video feed

## Safety First

⚠️ **Default Configuration for Safety:**
- Skills default to **SIMULATION MODE**
- Movement, arm, camera skills won't move hardware
- Toggle to REAL mode only when ready

## Full Pipeline Test

Test the complete voice interaction:

1. Click "Run Full Pipeline Test"
2. Dashboard simulates the entire flow:
   - Wake word detection
   - Speech-to-text
   - Intent classification
   - Skill execution
   - TTS response

## Development Mode

Run with debug output:
```bash
ros2 run aimee_test_dashboard dashboard_node --ros-args -p debug:=true
```

Change port:
```bash
ros2 run aimee_test_dashboard dashboard_node --ros-args -p port:=8080
```

## Hardware Setup

### Currently Available
- ✅ Microphone: USB or built-in
- ✅ Speaker: USB or 3.5mm audio
- ✅ Non-OBSBOT camera: USB webcam

### Coming Soon
- 📷 OBSBOT Tiny 2: When connected today

### Testing Without Hardware
All components work in simulation mode without physical hardware connected.

## API Endpoints

The dashboard exposes REST API:

```bash
# Get status
curl http://localhost:5000/api/status

# Test component
curl -X POST http://localhost:5000/api/test/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello"}'

# Toggle simulation
curl -X POST http://localhost:5000/api/component/skills/simulation \
  -H "Content-Type: application/json" \
  -d '{"simulation": true}'
```

## Architecture

```
┌─────────────────────────────────────┐
│  Browser (Phone/Tablet/PC)          │
│  http://localhost:5000              │
└─────────────┬───────────────────────┘
              │ HTTP
┌─────────────▼───────────────────────┐
│  Flask Web Server                   │
│  - Serves dashboard UI              │
│  - REST API endpoints               │
│  - Runs on UNO Q                    │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│  Dashboard Node (ROS2)              │
│  - Publishes test commands          │
│  - Subscribes to all topics         │
│  - Updates dashboard state          │
└─────────────────────────────────────┘
```

## Troubleshooting

### Dashboard not loading
```bash
# Check if port is in use
lsof -i :5000

# Use different port
ros2 run aimee_test_dashboard dashboard_node --ros-args -p port:=8080
```

### Cannot access from other devices
```bash
# Make sure to bind to 0.0.0.0
ros2 run aimee_test_dashboard dashboard_node --ros-args -p host:=0.0.0.0

# Check firewall
sudo ufw allow 5000
```

### ROS2 topics not showing
Make sure all AIMEE nodes are running:
```bash
ros2 node list
```

## License

MPL-2.0

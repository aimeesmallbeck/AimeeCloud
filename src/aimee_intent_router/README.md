# Intent Router Brick

ROS2 brick for Intent Classification and Routing for the AIMEE Robot.

## Overview

This brick processes transcribed user commands:
1. **Receives**: `/voice/transcription` from Voice Manager
2. **Classifies**: Intent using LLM (or fallback keyword matching)
3. **Routes**: To appropriate skill handler
4. **Responds**: Sends response to TTS

## Features

- **LLM-based Classification**: Uses LLM for accurate intent recognition
- **Fallback Classification**: Keyword-based fallback when LLM unavailable
- **Multi-turn Conversations**: Maintains context across exchanges
- **Skill Registry**: Pluggable skill handlers
- **Confidence Scoring**: Threshold-based classification confidence

## Architecture

```
┌─────────────────┐     Transcription     ┌──────────────────┐
│  Voice Manager  │ ─────────────────────→│  Intent Router   │
│  (STT)          │                       │  (this brick)    │
└─────────────────┘                       └────────┬─────────┘
                                                   │
                    ┌──────────────────────────────┤
                    │                              │
                    ↓                              ↓
           ┌────────────────┐            ┌─────────────────┐
           │  LLM Server    │            │  Skill Handlers │
           │  (optional)    │            │  - movement     │
           └────────────────┘            │  - arm_control  │
                                         │  - camera       │
                                         └────────┬────────┘
                                                  │
                                                  ↓
                                         ┌─────────────────┐
                                         │  TTS            │
                                         │  (response)     │
                                         └─────────────────┘
```

## Installation

```bash
cd ~/aimee-robot-ws
source setup_env.sh
colcon build --packages-select aimee_msgs aimee_intent_router
source install/setup.bash
```

## Usage

### Start Intent Router

```bash
ros2 run aimee_intent_router intent_router_node
```

### With Parameters

```bash
ros2 run aimee_intent_router intent_router_node \
  --ros-args \
  -p confidence_threshold:=0.7 \
  -p enable_conversation_mode:=true \
  -p debug:=true
```

## ROS2 Interface

### Subscribers

| Topic | Type | Description |
|-------|------|-------------|
| `/voice/transcription` | `aimee_msgs/Transcription` | Transcribed user commands |

### Publishers

| Topic | Type | Description |
|-------|------|-------------|
| `/tts/speak` | `std_msgs/String` | Response text for TTS |
| `/intent/classified` | `aimee_msgs/Intent` | Classified intent details |
| `/intent/status` | `std_msgs/String` | Status updates |

### Action Clients

| Action | Type | Description |
|--------|------|-------------|
| `/llm/generate` | `aimee_msgs/LLMGenerate` | LLM for intent classification |

## Intent Types

| Intent | Description | Example |
|--------|-------------|---------|
| GREETING | Hello, hi, etc. | "Hello AIMEE" |
| MOVEMENT | Robot movement | "Move forward", "Turn left" |
| ARM_CONTROL | Arm/gripper control | "Wave", "Open gripper" |
| CAMERA | Camera/vision | "Look at me", "Track face" |
| SYSTEM | System queries | "What's your name?" |
| QUESTION | General questions | "What time is it?" |
| CONVERSATION | Chat | "Tell me a joke" |

## Classification Modes

### LLM-based (Preferred)
Uses LLM to classify intents with high accuracy:
```python
# LLM prompt includes:
# - User text
# - Conversation context
# - Available intents
# Response: JSON with intent, action, parameters
```

### Fallback (Keyword-based)
When LLM unavailable, uses simple keyword matching:
```python
# Keywords:
# "forward", "move" → MOVEMENT
# "arm", "gripper" → ARM_CONTROL
# "hello", "hi" → GREETING
```

## Conversation Context

The router maintains conversation context per session:

```python
# Session identified by session_id
context = {
    'history': [
        {'user': 'move forward', 'assistant': 'Moving forward'},
        {'user': 'now turn left', 'assistant': 'Turning left'},
    ],
    'entities': {'location': 'kitchen'},
    'last_intent': IntentType.MOVEMENT
}
```

Benefits:
- Multi-turn commands: "Move forward... now turn"
- Contextual understanding: "Do it again"
- Entity tracking: "Go to the kitchen" → "What's there?"

## Example Flow

```
User: "Hello AIMEE"
  ↓
Voice Manager → STT → "hello aimee"
  ↓
Intent Router:
  - Classify: GREETING (confidence: 0.95)
  - Response: "Hello! I'm AIMEE. How can I help you?"
  → Publish to /tts/speak
  ↓
TTS: "Hello! I'm AIMEE..."
```

## Configuration

```yaml
# config/brick_config.yaml
confidence_threshold: 0.6      # Minimum confidence
enable_conversation_mode: true  # Multi-turn support
conversation_timeout: 60.0     # Context expiration
max_context_length: 10         # History exchanges
fallback_to_chat: true         # Chat when no skill match
```

## Testing

### Mock Transcription

```bash
# Terminal 1: Start intent router
ros2 run aimee_intent_router intent_router_node

# Terminal 2: Monitor intents
ros2 topic echo /intent/classified

# Terminal 3: Send mock transcription
ros2 topic pub /voice/transcription aimee_msgs/Transcription "
  text: 'move forward'
  is_command: true
  session_id: 'test123'
"
```

### Test with Full Pipeline

```bash
# 1. Start all components
ros2 run aimee_wake_word_ei wake_word_ei_node
ros2 run aimee_voice_manager voice_manager_node
ros2 run aimee_llm_server llm_server_node
ros2 run aimee_intent_router intent_router_node
ros2 run aimee_tts tts_node

# 2. Trigger wake word (simulated)
ros2 topic pub /wake_word/detected aimee_msgs/WakeWordDetection "
  wake_word: 'aimee'
  confidence: 0.95
"

# 3. Speak and watch the pipeline work!
```

## Future Enhancements

1. **Custom Skill Registration**: Dynamic skill loading
2. **Intent Conflicts**: Handle ambiguous intents
3. **Confirmation**: Confirm before executing critical actions
4. **Learning**: Learn from user corrections
5. **Multi-language**: Support for multiple languages

See `docs/FUTURE_ENHANCEMENTS.md` for details.

## License

MPL-2.0

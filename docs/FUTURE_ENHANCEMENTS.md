# Future Enhancements Roadmap

This document outlines planned enhancements for the AIMEE robot voice/intent system.

## 1. Conversational Mode (Contextual Listening)

### Current Behavior
- Wake word required for every command
- Single-shot recording after each wake word

### Proposed Enhancement
After initial wake word detection, enter "conversational mode" where subsequent commands don't require wake word for a timeout period.

### Implementation Plan

#### State Machine
```
[IDLE] --(wake_word)--> [LISTENING] --(command)--> [PROCESSING]
                           ^                           |
                           |                           |
                           +------(within timeout)-----+
                           |
                    (timeout exceeded)
                           |
                           v
                        [IDLE]
```

#### Configuration
```yaml
conversational_mode:
  enabled: true
  timeout_seconds: 30          # Stay in conv mode for 30s
  max_follow_up_commands: 5    # Max commands before requiring wake word
  visual_indicator: true       # LED/visual feedback when in conv mode
  audio_indicator: true        # Audio feedback (subtle beep)
```

#### ROS2 Topics
- `/conversation/state` (pub): Current conversation state
- `/conversation/extend` (sub): Extend timeout manually
- `/conversation/reset` (sub): Force back to IDLE

#### Implementation Changes Needed
1. **WakeWordEIBrick**: Add conversation state management
2. **VoiceManagerNode**: Skip wake word check when in conversational mode
3. **IntentRouter**: Track conversation context, manage state transitions
4. **StateManager**: Expose conversation state to other bricks

### Benefits
- More natural interactions
- Reduced user friction for multi-turn commands
- "Aimee, turn on the light... and set it to 50%"

---

## 2. Multi-Modal Wake Word Detection

### Current Behavior
- Wake word detection only via audio (Edge Impulse keyword spotting)

### Proposed Enhancement
Support wake word triggering from multiple sources:
- **Gesture**: Hand wave, pointing, specific pose
- **Visual**: Face detection (look at robot)
- **Touch**: Physical button press
- **Remote**: MQTT, HTTP API, mobile app
- **Scheduled**: Time-based triggers

### Implementation Plan

#### Unified Wake Word Interface
```python
# New message: WakeWordSource.msg
string source           # audio | gesture | touch | remote | scheduled
string source_detail    # "edge_impulse" | "hand_wave" | "button_1" | "mqtt"
string wake_word        # "aimee" | "visual_attention" | "button_press"
float32 confidence
geometry_msgs/Point location  # 3D location of trigger (for gesture)
```

#### Gesture Wake Word (OBSBOT Camera)
```python
# GestureDetectorBrick
class GestureDetectorBrick:
    """Detects wake gestures from camera feed."""
    
    SUPPORTED_GESTURES = [
        "hand_wave",      # Wave hand at camera
        "point_at",       # Point at robot
        "thumbs_up",      # Thumbs up
        "open_palm",      # Open palm raised
        "double_tap",     # Double hand clap
    ]
```

#### Camera Integration
```yaml
# config/gesture_wake_config.yaml
gesture_wake_word:
  enabled: true
  camera_topic: /camera/color/image_raw
  gestures:
    - name: hand_wave
      confidence: 0.75
      cooldown_seconds: 3.0
    - name: point_at
      confidence: 0.80
      cooldown_seconds: 2.0
  
  # Visual feedback
  led_feedback: true
  audio_feedback: true
```

#### ROS2 Topics
- `/wake_word/gesture` (pub): Gesture-based wake events
- `/wake_word/touch` (pub): Touch-based wake events  
- `/wake_word/remote` (pub): Remote-triggered wake events
- `/wake_word/all` (pub): Aggregated from all sources

### Implementation Changes Needed

1. **New Brick: GestureWakeBrick**
   - Subscribe to camera feed
   - Run gesture detection model (MediaPipe, YOLO-pose, etc.)
   - Publish WakeWordDetection messages

2. **New Brick: TouchWakeBrick**
   - Monitor GPIO/button inputs
   - Publish wake events on press

3. **WakeWordRouter**
   - Aggregate wake word sources
   - Deduplicate simultaneous triggers
   - Apply global cooldown

4. **Update VoiceManagerNode**
   - Subscribe to `/wake_word/all` instead of just `/wake_word/detected`

### Benefits
- Accessibility (users who can't speak)
- Noisy environments (gesture instead of voice)
- Remote operation (trigger from app)
- Multi-modal confirmation (voice + gesture)

---

## 3. Context-Aware Intent Understanding

### Current Behavior
- Each command processed independently
- No memory of previous commands

### Proposed Enhancement
Maintain conversation context for better intent understanding.

### Examples
```
User: "Aimee, turn on the living room light"
Aimee: [turns on light]

User: "Make it brighter"  # Context: living room light
Aimee: [increases brightness]

User: "What about the bedroom?"  # Context: lights
Aimee: [checks bedroom light status]
```

### Implementation
- Add conversation history to LLM prompt
- Entity tracking (locations, devices, values)
- Reference resolution ("it", "that", "there")

---

## 4. Proactive Suggestions

### Current Behavior
- Robot only responds to direct commands

### Proposed Enhancement
Robot can proactively suggest actions based on:
- Time of day ("Good morning, should I start the coffee?")
- User patterns ("You usually turn on the desk lamp around now")
- External triggers (motion detected, door opened)

---

## 5. Multi-User Support

### Current Behavior
- Single user context

### Proposed Enhancement
- Voice recognition (identify who's speaking)
- User profiles with preferences
- Access control (certain users can do certain things)

---

## Implementation Priority

### Phase 1 (Current)
- [x] Basic wake word (audio)
- [x] STT (Vosk/Whisper)
- [x] Intent routing

### Phase 2 (Next)
- [ ] Conversational mode with timeout
- [ ] Touch/button wake word

### Phase 3 (Future)
- [ ] Gesture wake word (camera)
- [ ] Context-aware understanding

### Phase 4 (Advanced)
- [ ] Multi-user support
- [ ] Proactive suggestions
- [ ] Remote wake word (MQTT/API)

---

## Architecture Notes

The current brick architecture supports these enhancements:
- Modular design allows adding new wake word sources
- ROS2 topics enable loose coupling between components
- Parameter server allows runtime configuration
- Async design supports concurrent processing

### Key Design Principles
1. **Extensibility**: New wake sources are just new bricks
2. **Flexibility**: Configuration-driven, not hardcoded
3. **Fallbacks**: Multiple ways to trigger (audio → gesture → touch)
4. **Graceful Degradation**: If camera fails, audio still works

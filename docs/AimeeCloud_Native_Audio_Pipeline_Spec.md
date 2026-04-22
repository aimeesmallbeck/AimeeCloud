# AimeeCloud Native Audio Streaming Pipeline

**Version:** 1.0-draft  
**Date:** 2026-04-22  
**Status:** Design specification — ready for implementation  
**Owners:** Robot Agent (voice/cloud/arm), AimeeCloud Backend Team

---

## 1. Executive Summary

This document specifies a **native audio streaming pipeline** that enables natural, real-time voice conversation between AIMEE robots and AimeeCloud. It replaces the current text-chunk-based voice interaction with a bidirectional audio stream, while preserving all existing AimeeCloud capabilities (games, education, agent commands, state management).

The robot streams raw audio to AimeeCloud via WebSocket. AimeeCloud proxies the stream to an audio-native LLM (Gemini Live or OpenAI Realtime), intercepts function calls, executes them against local game engines / robot command topics, and streams the spoken response back to the robot.

The existing MQTT-based protocol (v1.4) remains the command-and-control channel. The WebSocket is a **companion transport** for conversational audio.

---

## 2. Goals

1. **Natural conversation feel** — sub-500ms end-to-end latency, barge-in support, turn-taking.
2. **Preserve all AimeeCloud features** — games, education, skills, tool calling work unchanged.
3. **Backward compatibility** — existing text-based voice manager continues to work; new pipeline is opt-in per robot config.
4. **Hardware-agnostic** — works on UNO Q (4GB RAM, ARM64) with CPU-friendly codecs and optional GPU acceleration.

## 3. Non-Goals

1. Replace MQTT protocol v1.4 for commands, telemetry, or session auth.
2. Eliminate the text-based TTS node (it stays for non-conversational announcements).
3. Require cloud GPU for robot-side inference (all robot audio is streamed to cloud).

---

## 4. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ROBOT (UNO Q)                                   │
│  ┌──────────────┐     ┌─────────────────────┐     ┌──────────────┐         │
│  │   Microphone │────►│  aimee_voice_stream │────►│  WebSocket   │────────┐│
│  │   (PCM16)    │     │  - VAD              │     │  Client      │        ││
│  └──────────────┘     │  - AEC (optional)   │     └──────────────┘        ││
│                       │  - Encode (Opus)    │                              ││
│  ┌──────────────┐     └─────────────────────┘     ┌──────────────┐         ││
│  │   Speaker    │◄────│  Audio Playback     │◄────│  WebSocket   │◄───────┘│
│  │   (PCM16)    │     │  - Decode (Opus)    │     │  Client      │         │
│  └──────────────┘     │  - Buffer / Mix     │     └──────────────┘         │
│                       └─────────────────────┘                              │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  MQTT Client (aimee_cloud_bridge) — unchanged v1.4 protocol         │   │
│  │  - Session auth, heartbeats, commands, snapshots, telemetry         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ WebSocket  wss://aimeecloud.com/ws/v1
                                      │ (audio up / audio down / events)
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AIMEECLOUD GATEWAY                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  WebSocket Gateway (FastAPI / aiohttp)                              │   │
│  │  - Auth: Bearer token from MQTT session (reuse api_key + device_id) │   │
│  │  - Rate limiting per tier                                           │   │
│  │  - Multiplex: 1 robot WS ◄──► 1 Gemini Live session                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                      │                                       │
│                                      ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Gemini Live / OpenAI Realtime Proxy                                │   │
│  │  - Register tools (functions) per session                           │   │
│  │  - Forward audio up, receive audio down                             │   │
│  │  - Intercept function_call events                                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                      │                                       │
│                                      ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Function Call Router                                               │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌──────────┐  │   │
│  │  │ Game Engine │  │ Edu Module  │  │ Robot Cmd   │  │ Snapshot │  │   │
│  │  │ (stateful)  │  │ (stateful)  │  │ (MQTT pub)  │  │ (MQTT)   │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └──────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Dual-Channel Design

| Transport | Purpose | Latency Requirement | Reliability |
|---|---|---|---|
| **WebSocket** | Bidirectional audio streaming | <100ms one-way | Best-effort, auto-reconnect |
| **MQTT v1.4** | Commands, auth, telemetry, snapshots | <1s | Guaranteed delivery, QoS 1 |

---

## 5. Robot-Side Specification

### 5.1 New Package: `aimee_voice_streaming`

A new ROS2 Python package with a single node: `voice_streaming_node`.

```
src/aimee_voice_streaming/
├── aimee_voice_streaming/
│   ├── __init__.py
│   ├── voice_streaming_node.py      # Main node
│   ├── audio_capture.py             # Mic capture (pyaudio / sounddevice)
│   ├── audio_playback.py            # Speaker output
│   ├── opus_codec.py                # Opus encode/decode (optional)
│   ├── vad_engine.py                # Silero VAD wrapper
│   └── websocket_client.py          # Async WebSocket client
├── config/
│   └── voice_streaming.yaml
├── launch/
│   └── voice_streaming.launch.py
├── package.xml
└── setup.py
```

### 5.2 ROS2 Parameters

```yaml
voice_streaming:
  ros__parameters:
    # Connection
    gateway_url: "wss://aimeecloud.com/ws/v1"
    api_key: ""                       # Fallback to AIMEECLOUD_API_KEY env
    device_id: "arduino-uno-q-001"
    reconnect_interval_sec: 5.0

    # Audio I/O
    sample_rate_in: 16000             # Mic sample rate (Hz)
    sample_rate_out: 24000            # Speaker sample rate (Hz)
    channels_in: 1
    channels_out: 1
    frame_duration_ms: 20             # 20ms frames (320 samples @ 16kHz)
    audio_device_index: -1            # -1 = default

    # Codec
    use_opus: true                    # true = Opus, false = PCM16 base64
    opus_bitrate: 24000               # bits/sec (low quality but low CPU)

    # VAD
    vad_engine: "silero"              # "silero" | "webrtc" | "none"
    vad_threshold: 0.5                # Silero: 0.0–1.0 probability
    vad_start_sensitivity: "medium"   # low / medium / high
    vad_end_sensitivity: "medium"
    vad_silence_duration_ms: 500      # How long silence before "end of speech"
    vad_prefix_padding_ms: 300        # Audio to keep before speech start

    # Echo Cancellation
    use_aec: false                    # Requires webrtc-audio-processing
    aec_suppression_level: 2          # 0=quiet, 1=moderate, 2=aggressive

    # Interruption / Barge-in
    enable_barge_in: true             # If true, mic stays live during playback
    barge_in_vad_threshold: 0.6       # Higher threshold to avoid false triggers

    # Behavior
    auto_start: false                 # If true, starts streaming on node init
    wake_word_required: true          # If true, only stream after wake word
    wake_word_model: "/models/vosk/wake-word"  # Path to wake word model
    conversation_timeout_sec: 60.0    # Auto-stop after silence timeout
```

### 5.3 Audio Pipeline

```
Mic → PCM16 16kHz mono → [VAD] → [Opus Encoder] → WebSocket binary frame
                                                          ▲
WebSocket binary frame → [Opus Decoder] → PCM16 24kHz mono → [Audio Mixer] → Speaker
                                                          │
                                                    [TTS fallback queue]
```

**VAD States:**
- `IDLE` — Not streaming. Listening for wake word (if enabled) or waiting for `/voice/start` command.
- `LISTENING` — VAD detected speech start. Buffering audio with prefix padding. Streaming to cloud.
- `SPEAKING` — Cloud is sending audio down. Robot is playing it. Mic state depends on `enable_barge_in`.
- `PROCESSING` — Speech ended (VAD silence timeout). Waiting for cloud response.

### 5.4 ROS2 Topics

| Topic | Type | Direction | Description |
|---|---|---|---|
| `/voice/streaming/state` | `String` | Pub | Current state: `idle`, `listening`, `speaking`, `processing` |
| `/voice/streaming/start` | `Bool` | Sub | Trigger to start streaming (e.g., button press or wake word) |
| `/voice/streaming/stop` | `Bool` | Sub | Trigger to stop streaming |
| `/voice/streaming/interrupted` | `Bool` | Pub | True when user barge-in detected during playback |
| `/tts/speak` | `String` | Sub | **Existing topic** — queued and mixed during streaming |

### 5.5 WebSocket Message Format (Robot ↔ AimeeCloud)

All messages are JSON except audio payload, which is binary.

**Connection:**
```json
// Robot → Cloud (first message after WS open)
{
  "type": "session_start",
  "api_key": "ac_free_943d96db38ee49aa",
  "device_id": "arduino-uno-q-001",
  "session_id": "sess_abc123",      // From MQTT session
  "capabilities": {
    "audio_in": {"codec": "opus", "sample_rate": 16000},
    "audio_out": {"codec": "opus", "sample_rate": 24000},
    "barge_in": true,
    "languages": ["en-US"]
  },
  "timestamp": "2026-04-22T18:16:47Z"
}

// Cloud → Robot
{
  "type": "session_ready",
  "session_id": "sess_abc123",
  "status": "connected",
  "server_info": {
    "model": "gemini-2.5-flash-native-audio",
    "supported_codecs": ["opus", "pcm16"]
  }
}
```

**Audio Up (Robot → Cloud):**
- Binary Opus frames OR JSON with base64 PCM16.
- If binary: raw Opus packet per 20ms frame.
- If JSON:
```json
{
  "type": "audio_chunk",
  "seq": 42,
  "format": "pcm16",
  "sample_rate": 16000,
  "data": "//uQxAAAA..."
}
```

**Audio Down (Cloud → Robot):**
- Same binary or JSON format.

**Events:**
```json
// Robot → Cloud (VAD state change)
{
  "type": "vad_event",
  "event": "speech_start",   // or "speech_end"
  "timestamp_ms": 1234567
}

// Cloud → Robot (function call being executed)
{
  "type": "function_call_start",
  "call_id": "call_abc",
  "name": "game_move"
}

// Cloud → Robot (function call completed)
{
  "type": "function_call_end",
  "call_id": "call_abc",
  "duration_ms": 150
}

// Cloud → Robot (error)
{
  "type": "error",
  "code": "RATE_LIMIT_EXCEEDED",
  "message": "Audio streaming rate limit reached",
  "recoverable": true
}
```

### 5.6 Dependencies

```dockerfile
# Add to Dockerfile
RUN pip3 install --no-cache-dir --break-system-packages \
    websockets \
    opuslib \
    pyaudio \
    sounddevice \
    numpy \
    webrtcvad

# Silero VAD is pure PyTorch — download model at runtime
# webrtc-audio-processing for AEC (optional, compile from source)
```

---

## 6. AimeeCloud-Side Specification

### 6.1 WebSocket Gateway

FastAPI application with `aiohttp` or native `websockets` handling.

```python
# Simplified pseudocode
@app.websocket("/ws/v1")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    msg = await websocket.receive_json()
    assert msg["type"] == "session_start"
    
    # Validate api_key + device_id against existing session store
    session = await validate_session(msg["api_key"], msg["device_id"], msg["session_id"])
    if not session:
        await websocket.send_json({"type": "error", "code": "INVALID_API_KEY"})
        return
    
    # Check tier limits (concurrent audio streams)
    if not await check_audio_stream_quota(session.tier, msg["device_id"]):
        await websocket.send_json({"type": "error", "code": "TIER_LIMIT_EXCEEDED"})
        return
    
    await websocket.send_json({"type": "session_ready", ...})
    
    # Spawn Gemini Live session proxy
    proxy = GeminiLiveProxy(session, websocket)
    await proxy.run()
```

### 6.2 Gemini Live Proxy

One proxy instance per robot WebSocket connection.

**Session Setup (to Gemini):**
```json
{
  "model": "gemini-2.5-flash-native-audio-preview",
  "generationConfig": {
    "responseModalities": ["AUDIO"],
    "speechConfig": {
      "voiceConfig": {
        "prebuiltVoiceConfig": {"voiceName": "Puck"}
      }
    }
  },
  "systemInstruction": {
    "parts": [{"text": "You are Aimee, a friendly robot assistant. ..."}]
  },
  "tools": [
    {"functionDeclarations": [/* see §6.4 */]}
  ]
}
```

**Audio Flow:**
- Robot Opus → Decode to PCM16 → Re-encode to Gemini format (PCM16 16kHz) → Gemini Live WebSocket
- Gemini PCM16 24kHz → Opus encode → Robot WebSocket

**Function Call Interception:**
```python
async def on_gemini_message(msg):
    if msg["serverContent"]["modelTurn"]["parts"]:
        # Audio or text response — forward to robot
        await forward_to_robot(msg)
    
    if msg["serverContent"]["interrupted"]:
        # User barge-in detected by Gemini
        await robot_ws.send_json({"type": "interrupted"})
    
    if msg["toolCall"]:
        for call in msg["toolCall"]["functionCalls"]:
            result = await execute_function(call)
            await gemini_ws.send_json({
                "toolResponse": {
                    "functionResponses": [{
                        "id": call["id"],
                        "response": result
                    }]
                }
            })
```

### 6.3 OpenAI Realtime Alternative

If using OpenAI Realtime API instead of Gemini Live:
- Protocol: WebRTC (browser) or WebSocket (server)
- Events: `conversation.item.create`, `response.create`, `function_call` delta events
- Tool schema is similar (JSON Schema function definitions)

AimeeCloud should abstract the provider behind a `AudioModelProvider` interface so we can swap Gemini ↔ OpenAI ↔ future providers without changing the gateway code.

### 6.4 Function Call Schema

These map 1:1 to existing `AimeeAgent` command types from Protocol v1.4.

```json
{
  "functionDeclarations": [
    {
      "name": "game_move",
      "description": "Make a move in an active game",
      "parameters": {
        "type": "object",
        "properties": {
          "game": {"type": "string", "enum": ["tic_tac_toe", "chess", "20_questions"]},
          "move": {"type": "object"}
        },
        "required": ["game", "move"]
      }
    },
    {
      "name": "motor_command",
      "description": "Control robot base movement",
      "parameters": {
        "type": "object",
        "properties": {
          "action": {"type": "string", "enum": ["forward", "backward", "left", "right", "stop", "wave"]},
          "duration_ms": {"type": "integer", "default": 0}
        },
        "required": ["action"]
      }
    },
    {
      "name": "arm_command",
      "description": "Control robot arm",
      "parameters": {
        "type": "object",
        "properties": {
          "action": {"type": "string", "enum": ["raise", "lower", "extend", "retract", "home"]}
        },
        "required": ["action"]
      }
    },
    {
      "name": "gripper_command",
      "description": "Control robot gripper",
      "parameters": {
        "type": "object",
        "properties": {
          "action": {"type": "string", "enum": ["open", "close", "half_open"]}
        },
        "required": ["action"]
      }
    },
    {
      "name": "take_snapshot",
      "description": "Capture an image from the robot camera",
      "parameters": {
        "type": "object",
        "properties": {
          "camera": {"type": "string", "default": "front"},
          "purpose": {"type": "string", "default": "analysis"}
        }
      }
    },
    {
      "name": "set_expression",
      "description": "Trigger an emotional expression on the robot",
      "parameters": {
        "type": "object",
        "properties": {
          "name": {"type": "string", "enum": ["happy", "sad", "surprised", "greeting", "celebration"]},
          "duration_ms": {"type": "integer", "default": 2500},
          "priority": {"type": "string", "enum": ["low", "normal", "high"], "default": "normal"}
        },
        "required": ["name"]
      }
    },
    {
      "name": "get_robot_status",
      "description": "Get current robot telemetry",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    }
  ]
}
```

### 6.5 Function Call Router Logic

```python
async def execute_function(call):
    name = call["name"]
    args = call["args"]
    
    if name == "game_move":
        return await game_engine.make_move(
            session_id=session.id,
            game=args["game"],
            move=args["move"]
        )
    
    elif name in ("motor_command", "arm_command", "gripper_command"):
        # Publish to MQTT command topic
        await mqtt.publish(
            f"aimeecloud/device/{session.device_id}/in",
            {
                "type": "AimeeAgent",
                "session_id": session.id,
                "commands": [{"type": name.replace("_command", ""), **args}],
                "timestamp": iso_now()
            }
        )
        return {"status": "dispatched", "command": name}
    
    elif name == "take_snapshot":
        # Request snapshot via MQTT, wait for response
        image_b64 = await snapshot_service.capture(
            device_id=session.device_id,
            camera=args.get("camera", "front")
        )
        return {"status": "captured", "format": "jpeg", "image_base64": image_b64}
    
    elif name == "set_expression":
        # Publish expression command
        await mqtt.publish(
            f"aimeecloud/device/{session.device_id}/in",
            {
                "type": "AimeeAgent",
                "session_id": session.id,
                "commands": [{"type": "expression", **args}],
                "timestamp": iso_now()
            }
        )
        return {"status": "dispatched"}
    
    elif name == "get_robot_status":
        status = await robot_registry.get_status(session.device_id)
        return status
```

---

## 7. Game / Education Integration Example

### 7.1 Tic-Tac-Toe (Full Audio-Native Flow)

1. **User:** "Hey Aimee, let's play tic-tac-toe. I'll go first."
2. **Robot:** Streams audio to cloud.
3. **Gemini:** Reasons → calls `game_move(game="tic_tac_toe", move={"action": "start", "player": "user"})`
4. **AimeeCloud Game Engine:** Creates new game state. Returns board and rules.
5. **Gemini:** Speaks: "Great! You're X, I'm O. The board is empty. Where do you want to go? Top left is 1, top middle is 2..."
6. **User:** "I'll take the center — position 5."
7. **Gemini:** Calls `game_move(game="tic_tac_toe", move={"position": 5})`
8. **Game Engine:** Validates move. Updates state. Returns: `{valid: true, board: ["_","_","_","_","X","_","_","_","_"], winner: null}`
9. **Game Engine:** Computes AI response move (position 1). Returns: `{ai_move: 1, board: ["O","_","_","_","X","_","_","_","_"]}`
10. **Gemini:** Speaks: "Good choice! I'll take the top left corner. Your turn."

All game state lives in AimeeCloud. The model never sees raw state unless we choose to include it in function responses.

### 7.2 Education: Math Lesson

1. **User:** "Aimee, quiz me on multiplication."
2. **Gemini:** Calls `edu_start_module(module="multiplication", difficulty="medium")`
3. **Edu Engine:** Returns first problem: `{problem: "What is 7 × 8?", hint: "Think of 7 × 7 plus one more 7"}`
4. **Gemini:** Speaks: "What is 7 times 8?"
5. **User:** "Um... 54?"
6. **Gemini:** Calls `edu_validate_answer(answer="54")`
7. **Edu Engine:** Returns `{correct: false, explanation: "7 × 8 = 56. Remember, 7 × 7 is 49, plus 7 more is 56."}`
8. **Gemini:** Speaks: "Close! 7 times 8 is actually 56. Think of it as 7 times 7, which is 49, plus one more 7. Want to try another?"

---

## 8. State Machine & Turn-Taking

### 8.1 Robot-Side State Machine

```
                    ┌─────────────┐
        wake word ─►│    IDLE     │◄──── timeout / stop command
        or /start   │             │
                    └──────┬──────┘
                           │ VAD speech_start
                           ▼
                    ┌─────────────┐
              ┌────►│  LISTENING  │◄────┐
              │     │             │     │ (more speech)
              │     └──────┬──────┘     │
              │            │ VAD speech_end
              │            ▼
              │     ┌─────────────┐
              │     │ PROCESSING  │────► (timeout with no response)
              │     │             │
              │     └──────┬──────┘
              │            │ audio response starts
              │            ▼
              │     ┌─────────────┐
              └─────┤  SPEAKING   │
                    │             │
                    └──────┬──────┘
                           │ response finished
                           ▼
                    (back to IDLE or LISTENING
                     depending on conversation_timeout)
```

**Barge-in during SPEAKING:**
- If `enable_barge_in: true`: Mic stays active. VAD on mic triggers `interrupted` event.
- Robot sends `{"type": "interrupt"}` to cloud.
- Cloud forwards interrupt to Gemini (Gemini stops generating, flushes audio buffer).
- Robot stops speaker playback immediately.
- State transitions: SPEAKING → LISTENING.

### 8.2 Cloud-Side Turn-Taking

Gemini Live handles most turn-taking internally via its own VAD. AimeeCloud can optionally override:
- `end_of_speech_sensitivity`: How eagerly Gemini considers the user done speaking.
- `silence_duration_ms`: How much silence before triggering response.

For robots in noisy environments (motors, servos), AimeeCloud may want to set:
```json
{
  "realtimeInputConfig": {
    "automaticActivityDetection": {
      "disabled": false,
      "start_of_speech_sensitivity": "START_SENSITIVITY_HIGH",
      "end_of_speech_sensitivity": "END_SENSITIVITY_LOW",
      "silence_duration_ms": 800
    }
  }
}
```

Higher start sensitivity = less false triggers from robot motor noise. Lower end sensitivity + longer silence = waits for user to finish (avoids cutting off mid-thought).

---

## 8.5 Snapshot Reliability Improvement

The snapshot pipeline was redesigned to eliminate V4L2 device contention:

**Problem:** `usb_cam` node and `v4l2-ctl`/`ffmpeg` both needed exclusive access to `/dev/video2`. The old fix was `pkill -f usb_cam_node_exe`, wait, capture, restart — race-prone and ~50% reliable.

**Solution:** `obsbot_node` now subscribes to `/camera/image_raw` and maintains a ring buffer of the latest frame. When a snapshot is requested:
1. **Primary path:** Encode the buffered frame to JPEG via OpenCV (zero V4L2 contention, ~instant).
2. **Fallback path:** If no buffered frame exists or resolution doesn't match, fall back to `v4l2-ctl`/`ffmpeg`.

**Result:** Snapshots are reliable, fast, and no longer require stopping `usb_cam`.

## 9. Echo Cancellation (AEC)

This is the hardest hardware problem. The robot speaker bleeds into the microphone.

### 9.1 Options (in order of complexity)

| Approach | Latency | Quality | Effort |
|---|---|---|---|
| **Mute mic during playback** | Zero | Poor (no barge-in) | Trivial |
| **Software AEC (Speex/Webrtc)** | ~20ms | Good | Medium |
| **Hardware separation** | Zero | Excellent | Hard |

### 9.2 Software AEC with `webrtc-audio-processing`

```python
import webrtc_audio_processing as ap

aec = ap.AudioProcessing()
aec.set_aec_mode(ap.AecMode.AEC2)  # aggressive
aec.set_stream_format(sample_rate_hz=16000, num_channels=1)

# Per frame:
cleaned_frame = aec.process_stream(mic_frame, speaker_frame)
```

**Caveat:** `webrtc-audio-processing` must be compiled from source on ARM64. It requires the exact speaker frame that was played out (reference signal), which means tight coupling between playback and capture threads.

### 9.3 Recommended Path

**Phase 1:** Implement with "mute mic during playback" + `enable_barge_in: false`. Get the pipeline working end-to-end.

**Phase 2:** Add barge-in with `enable_barge_in: true` but no AEC. Accept that motor noise may cause false triggers. Tune VAD threshold aggressively.

**Phase 3:** Integrate software AEC. This is a dedicated task requiring audio DSP expertise.

---

## 10. Backward Compatibility

The new pipeline is **opt-in** per robot.

### 10.1 Config-Driven Toggle

```yaml
# robots/minnie.yaml
software:
  voice: true
  voice_pipeline: "streaming"   # "streaming" | "legacy" (default)
  tts: true
  llm: true
  cloud: true
```

### 10.2 Launch File Behavior

```python
# core.launch.py
if config.get('software', {}).get('voice_pipeline', 'legacy') == 'streaming':
    # Launch new aimee_voice_streaming node
    # Do NOT launch legacy voice_manager_node
    launch_actions.append(voice_streaming_node)
else:
    # Legacy path
    launch_actions.append(voice_manager_node)
```

### 10.3 MQTT Protocol v1.4

Unchanged. The cloud bridge node continues to operate. If a function call results in a robot command, it is sent via MQTT just like any other `AimeeAgent` message. The robot does not need to know whether the command came from text-based intent or audio-native function calling.

---

## 11. Implementation Phases

### Phase 1: Robot-Side Prototype (1–2 weeks)
- [ ] Create `aimee_voice_streaming` package skeleton
- [ ] Implement `audio_capture.py` (pyaudio, 16kHz, 20ms frames)
- [ ] Implement `audio_playback.py` (pyaudio, 24kHz, ring buffer)
- [ ] Implement `vad_engine.py` (Silero VAD, download model at runtime)
- [ ] Implement `websocket_client.py` (async websockets, auto-reconnect)
- [ ] Implement `voice_streaming_node.py` (state machine, ROS2 integration)
- [ ] Test against a simple WebSocket echo server

### Phase 2: AimeeCloud Gateway Prototype (1–2 weeks)
- [ ] FastAPI WebSocket endpoint `/ws/v1`
- [ ] Session auth (reuse existing API key + session store)
- [ ] Gemini Live API proxy (WebSocket → Google)
- [ ] Audio transcoding (Opus ↔ PCM16)
- [ ] Tool registration with function schema
- [ ] Function call router with game engine + MQTT dispatch

### Phase 3: End-to-End Integration (1 week)
- [ ] Robot connects to AimeeCloud gateway
- [ ] Free-form conversation works
- [ ] Tic-tac-toe game works via function calling
- [ ] Barge-in works (even if muted-mic fallback)
- [ ] Snapshot command works (audio → function call → MQTT → capture → response)

### Phase 4: Polish & AEC (2+ weeks)
- [ ] Opus codec optimization (lower CPU)
- [ ] Echo cancellation integration
- [ ] Noise-robust VAD tuning for robot motor noise
- [ ] Latency profiling and optimization
- [ ] Config-driven toggle in `robot.launch.py`

---

## 12. Open Questions

1. **Opus on ARM64 CPU:** Is real-time Opus encode/decode feasible on UNO Q without GPU? If not, fallback to PCM16 (higher bandwidth, lower CPU).
2. **Gemini Live pricing:** What's the per-minute cost for audio input/output? Does it fit free tier limits?
3. **OpenAI Realtime fallback:** Should AimeeCloud support both Gemini and OpenAI with a provider switch? (Recommended: yes, abstract behind interface.)
4. **Multilingual:** Vosk wake word models are language-specific. How do we handle wake word in non-English sessions?
5. **Wake word detection:** Should wake word run locally (Vosk) or can Gemini Live handle "always listening" without a wake word? (Gemini Live supports proactive audio — it can ignore irrelevant speech. This might eliminate the wake word entirely.)
6. **Snapshot latency:** Taking a snapshot currently takes 3–5 seconds (stop USB cam, capture, restart). How does the audio model handle long pauses? Should AimeeCloud play "hold music" or filler audio?

---

## 13. Appendix: Message Sequence Diagram

```
Robot                              AimeeCloud                         Gemini Live
  │                                   │                                   │
  │ ────── MQTT connect (v1.4) ─────► │                                   │
  │ ◄──────── session_init ────────── │                                   │
  │                                   │                                   │
  │ ────── WS /ws/v1 (api_key) ─────► │                                   │
  │ ◄──────── session_ready ───────── │                                   │
  │                                   │ ──────── Gemini WS connect ─────► │
  │                                   │ ◄────────── session OK ────────── │
  │                                   │                                   │
  │ ────── binary: audio chunk ─────► │ ────── binary: audio chunk ─────► │
  │ ────── binary: audio chunk ─────► │ ────── binary: audio chunk ─────► │
  │ ◄───── binary: audio chunk ────── │ ◄───── binary: audio chunk ────── │
  │ ◄───── binary: audio chunk ────── │ ◄───── binary: audio chunk ────── │
  │                                   │                                   │
  │ ◄───── {type: "function_call_start", name: "game_move"} ───────────── │
  │                                   │ ◄────── function_call(game_move) ─│
  │                                   │                                   │
  │                                   │ ─────── validate_move() ────────► │
  │                                   │ ◄────────── result ────────────── │
  │                                   │                                   │
  │ ◄───── {type: "function_call_end", call_id: "..."} ────────────────── │
  │ ◄───── binary: audio response ─── │ ◄───── binary: audio response ─── │
  │ ◄───── binary: audio response ─── │ ◄───── binary: audio response ─── │
  │                                   │                                   │
  │ ────── {type: "vad_event", event: "speech_start"} ───────────────────►│
  │                                   │ ────── interrupt signal ─────────►│
  │ [stop speaker playback]           │                                   │
  │                                   │                                   │
  │ ────── binary: audio chunk ─────► │ ────── binary: audio chunk ─────► │
  │ ...                               │ ...                               │
```

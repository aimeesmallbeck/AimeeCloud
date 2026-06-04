# AimeeCloud Robot Communication Protocol Specification
## For: Robot Firmware / Device Agent Developers

---

## 1. Overview

This document defines the exact communication protocol between a robot (or any device) and AimeeCloud. The robot must implement an MQTT client that connects to the AimeeCloud broker and follows the message schemas below. The browser test client at https://aimeecloud.com/aimee is a reference implementation of this same protocol.

- **Transport**: MQTT
- **Broker (TCP)**: `aimeecloud.com:1883` (for robots with MQTT libraries)
- **Broker (WSS)**: `wss://aimeecloud.com/aimeecloud-mqtt` (for browser/WebSocket-capable devices)
- **Authentication**: Anonymous (test environment)

---

## 2. Topic Structure

All communication uses the device ID in the topic path. The device ID must be stable and unique per robot (e.g., `arduino-uno-q-001`).

| Topic | Direction | Purpose |
|-------|-----------|---------|
| `aimeecloud/device/{device_id}/connect` | Robot → Cloud | Session initialization and reconnection |
| `aimeecloud/device/{device_id}/in` | Robot → Cloud | Intents, game moves, system messages |
| `aimeecloud/device/{device_id}/out` | Cloud → Robot | All responses, TTS text, game state updates |
| `aimeecloud/device/{device_id}/status` | Cloud → Robot | Session lifecycle events (disconnect, expiry) |

> **Important**: The robot must subscribe to `out` and `status` before publishing `connect`.

---

## 3. Session Lifecycle

### 3.1 Initial Connection

On boot or when the user activates the robot, publish a connect message:

```json
{
  "type": "connect",
  "device_id": "arduino-uno-q-001",
  "user_profile": {
    "name": "Scott",
    "location": "home",
    "language": "en-US"
  },
  "capabilities": {
    "input": ["voice", "text"],
    "output": ["tts", "display", "motors", "led"]
  },
  "request_session_id": null,
  "timestamp": "2026-04-14T09:46:05Z"
}
```

**Field descriptions:**
- `device_id` — Your robot's stable unique ID.
- `user_profile` — Key-value map of user info. Can be empty `{}`.
- `capabilities` — What the robot can do. Used by the cloud to tailor responses.
- `request_session_id` — `null` for new sessions, or a previous `session_id` to resume.

### 3.2 Session Init Ack

The cloud responds on `out` with:

```json
{
  "type": "session_init",
  "session_id": "sess_abc123def4567890",
  "device_id": "arduino-uno-q-001",
  "status": "connected",
  "expires_in": 600,
  "ttl": 600,
  "timestamp": "2026-04-14T09:46:05Z"
}
```

**Robot action:** Store `session_id` in non-volatile or durable memory. All subsequent messages must include it.

### 3.3 Reconnection After WiFi Drop

If the robot loses connection and reconnects within the TTL (10 minutes), send the stored `session_id`:

```json
{
  "type": "connect",
  "device_id": "arduino-uno-q-001",
  "user_profile": { "name": "Scott" },
  "capabilities": { "input": ["voice"], "output": ["tts"] },
  "request_session_id": "sess_abc123def4567890",
  "timestamp": "2026-04-14T09:55:00Z"
}
```

**Result:** The cloud resumes the existing session with all game state and chat history intact.

### 3.4 Disconnect Notification (Optional but Recommended)

When the robot powers down or goes to sleep, publish:

```json
{
  "type": "disconnect",
  "device_id": "arduino-uno-q-001",
  "session_id": "sess_abc123def4567890",
  "timestamp": "2026-04-14T10:00:00Z"
}
```

> **MQTT LWT:** Set a Last Will and Testament on the MQTT connection to publish this message automatically if the robot drops unexpectedly.

### 3.5 Session Expiry

If the cloud publishes this on `status`, the session is gone:

```json
{
  "type": "status",
  "device_id": "arduino-uno-q-001",
  "session_id": "sess_abc123def4567890",
  "status": "expired",
  "timestamp": "2026-04-14T10:10:00Z"
}
```

**Robot action:** Discard the stored `session_id` and start a new session on next connect.

---

## 4. Message Types (Robot → Cloud)

### 4.1 Intent

The robot's intent classifier parses the user's speech (or text input) and publishes the result. If you do not have an on-device classifier, you may send the raw text and omit the `intent` field—the cloud will classify it for you.

**With on-device classification:**

```json
{
  "type": "intent",
  "device_id": "arduino-uno-q-001",
  "session_id": "sess_abc123def4567890",
  "payload": "what's the weather?",
  "intent": {
    "intent": "weather",
    "category": "cloud_skill",
    "confidence": 0.85,
    "text": "what's the weather?",
    "source": "keyword"
  },
  "timestamp": "2026-04-14T09:46:05Z"
}
```

**Without on-device classification:**

```json
{
  "type": "intent",
  "device_id": "arduino-uno-q-001",
  "session_id": "sess_abc123def4567890",
  "payload": "what color is the sky?",
  "timestamp": "2026-04-14T09:46:05Z"
}
```

### 4.2 Game Move

When the user makes a move in an active game, publish a `game_move`. The exact structure of `move` depends on the game.

**Tic-Tac-Toe:**

```json
{
  "type": "game_move",
  "device_id": "arduino-uno-q-001",
  "session_id": "sess_abc123def4567890",
  "game": "tic-tac-toe",
  "move": { "position": 4 },
  "timestamp": "2026-04-14T09:46:05Z"
}
```

`position` is 0–8 (top-left to bottom-right). The cloud also accepts natural language via `move: { "text": "center" }`, but board indices are preferred for robots.

**Yahtzee:**

```json
{
  "type": "game_move",
  "device_id": "arduino-uno-q-001",
  "session_id": "sess_abc123def4567890",
  "game": "yahtzee",
  "move": { "action": "hold", "indices": [0, 2] },
  "timestamp": "2026-04-14T09:46:05Z"
}
```

Actions: `hold`, `reroll`, `score`

For score:

```json
{ "action": "score", "category": "chance" }
```

### 4.3 Ping

Useful for keepalive or latency checks:

```json
{
  "type": "ping",
  "device_id": "arduino-uno-q-001",
  "session_id": "sess_abc123def4567890",
  "timestamp": "2026-04-14T09:46:05Z"
}
```

Cloud response on `out`:

```json
{
  "type": "response",
  "sub_type": "pong",
  "device_id": "arduino-uno-q-001",
  "session_id": "sess_abc123def4567890",
  "timestamp": "2026-04-14T09:46:05Z"
}
```

---

## 5. Response Types (Cloud → Robot)

All cloud-to-robot traffic arrives on the `out` topic with `type: "response"` and a `sub_type` discriminator.

### 5.1 Chat Response (`sub_type: "chat_response"`)

Returned for chat, help, status, and general knowledge questions.

```json
{
  "type": "response",
  "sub_type": "chat_response",
  "session_id": "sess_abc123def4567890",
  "device_id": "arduino-uno-q-001",
  "intent": "chat",
  "text": "The sky is blue because of the way sunlight scatters in the atmosphere.",
  "tts": "The sky is blue because of the way sunlight scatters in the atmosphere.",
  "source": "llm",
  "context": {
    "active_context": null,
    "context_stack": []
  },
  "timestamp": "2026-04-14T09:46:05Z"
}
```

**Robot action:** Speak the `tts` string. Optionally display the `text` string if the robot has a screen.

### 5.2 Game Update (`sub_type: "game_update"`)

Returned when a game starts or when a move is processed.

```json
{
  "type": "response",
  "sub_type": "game_update",
  "session_id": "sess_abc123def4567890",
  "device_id": "arduino-uno-q-001",
  "intent": "game",
  "game": "tic-tac-toe",
  "state": {
    "board": ["O", "", "", "", "X", "", "", "", ""],
    "current_turn": "X",
    "game_status": "playing"
  },
  "text": "I placed O in the top left.\n O |   |  \n-----------\n   | X |  \n-----------\n   |   |  \nYour turn!",
  "tts": "I placed O in the top left. Your turn!",
  "context": {
    "active_context": "Game: tic-tac-toe",
    "context_stack": []
  },
  "timestamp": "2026-04-14T09:46:05Z"
}
```

**Game state fields:**
- `state.board` — Array of 9 strings for tic-tac-toe
- `state.current_turn` — `"X"` or `"O"`
- `state.game_status` — `"playing"`, `"X_won"`, `"O_won"`, or `"draw"`

**Robot action:**
1. Update your local game representation from `state`.
2. If `game_status` is `X_won`, `O_won`, or `draw`, announce the result and end the game.
3. Otherwise, speak `tts` and wait for the user's next move.

### 5.3 Robot Command (`sub_type: "robot_command"`)

Returned for robot movement, arm, and gripper intents.

```json
{
  "type": "response",
  "sub_type": "robot_command",
  "session_id": "sess_abc123def4567890",
  "device_id": "arduino-uno-q-001",
  "intent": "robot_forward",
  "text": "Moving forward",
  "tts": "Okay, moving forward",
  "command": {
    "motor": "forward",
    "duration_ms": 1000
  },
  "timestamp": "2026-04-14T09:46:05Z"
}
```

**Command payloads by intent:**

| Intent | Command Object |
|--------|----------------|
| `robot_forward` | `{ "motor": "forward", "duration_ms": 1000 }` |
| `robot_backward` | `{ "motor": "backward", "duration_ms": 1000 }` |
| `robot_stop` | `{ "motor": "stop", "duration_ms": 0 }` |
| `robot_left` | `{ "motor": "left", "duration_ms": 500 }` |
| `robot_right` | `{ "motor": "right", "duration_ms": 500 }` |
| `robot_wave` | `{ "motor": "wave", "duration_ms": 1000 }` |
| `arm_raise` | `{ "arm": "raise" }` |
| `arm_lower` | `{ "arm": "lower" }` |
| `gripper_open` | `{ "gripper": "open" }` |
| `gripper_close` | `{ "gripper": "close" }` |

### 5.3.1 Complex Skills (New API)
For more advanced, asynchronous operations (like vision-based pick-and-place or complex animations), the cloud can send a `skill` command. The robot will dispatch these to local ROS 2 Action Servers.

**Example: Pick and Place**
```json
{
  "type": "skill",
  "name": "pick_place",
  "parameters": {
    "object_class": "block",
    "color": "red",
    "enable_place": true
  }
}
```

**Example: Play Animation**
```json
{
  "type": "skill",
  "name": "play_animation",
  "parameters": {
    "animation_name": "figure_8"
  }
}
```

**Robot action:** Execute the hardware command, then speak `tts`.

### 5.4 Error Response (`sub_type: "error"`)

Returned when something goes wrong.

```json
{
  "type": "response",
  "sub_type": "error",
  "session_id": "sess_abc123def4567890",
  "device_id": "arduino-uno-q-001",
  "text": "I didn't understand that move.",
  "tts": "I didn't understand that move.",
  "error": "INVALID_GAME_MOVE",
  "timestamp": "2026-04-14T09:46:05Z"
}
```

**Common error codes:**
- `SESSION_NOT_FOUND` — The session ID is invalid or expired. Start a new session.
- `NO_ACTIVE_GAME` — A `game_move` was sent but no game is in progress.
- `INVALID_GAME_MOVE` — The move format was wrong or illegal.
- `GAME_START_ERROR` — Failed to start the requested game.

---

## 6. Context Management & Interruptions

AimeeCloud handles mid-game interruptions automatically.

### Example Flow

1. User says: "play tic tac toe" → Cloud starts game, `active_context = "Game: tic-tac-toe"`
2. User says: "what's the weather?" → Cloud responds with weather and appends a resume hint to the TTS:
   ```json
   {
     "tts": "It's sunny and 72 degrees outside. Back to Tic-Tac-Toe, your move!",
     "context": {
       "active_context": "Game: tic-tac-toe",
       "was_interrupted": true,
       "previous_context": "Game: tic-tac-toe",
       "return_to": "tic-tac-toe"
     }
   }
   ```
3. User makes a game move → The game continues from its previous state.

**Robot action:** You do not need to implement interruption logic. Simply speak the `tts` string and continue handling game moves normally.

---

## 7. On-Device Intent Classification (Optional)

If your robot has an on-device intent classifier, use these intent names so the cloud routes correctly:

| Intent | When to Use |
|--------|-------------|
| `chat` | General conversation, questions starting with who/what/when/where/how/why |
| `weather` | Weather, temperature, forecast requests |
| `news` | News, headlines |
| `story` | Storytelling, bedtime stories |
| `game` | Starting a game |
| `help` | Help requests |
| `status` | "How are you?" |
| `robot_forward` | Move forward |
| `robot_backward` | Move backward |
| `robot_stop` | Stop |
| `robot_left` | Turn left |
| `robot_right` | Turn right |
| `robot_wave` | Wave / dance |
| `arm_raise` | Raise arm |
| `arm_lower` | Lower arm |
| `gripper_open` | Open gripper |
| `gripper_close` | Close gripper |

If you omit the `intent` field, the cloud will classify the payload text for you.

---

## 8. State Diagram

```
[Robot Boot]
    |
    v
[Subscribe to out + status]
    |
    v
[Publish connect] ----> [Cloud returns session_init]
    |
    v
[Idle] <----> [Publish intent / game_move / ping]
    |                |
    |                v
    |         [Cloud returns response on out]
    |                |
    |         [Speak TTS / Execute command / Render game]
    |
[WiFi drop]
    |
    v
[Reconnect within 10 min] ----> [Publish connect with request_session_id]
    |                                  |
    v                                  v
[Session resumes] <------------- [Same session_id, state intact]
    |
[No reconnect within 10 min]
    |
    v
[Session expired] ----> [Start new session]
```

---

## 9. Quick Reference: Minimal Robot Implementation

### Step 1: Connect and Subscribe

```python
# Pseudocode
mqtt.connect("aimeecloud.com", 1883)
mqtt.subscribe(f"aimeecloud/device/{device_id}/out")
mqtt.subscribe(f"aimeecloud/device/{device_id}/status")
```

### Step 2: Request Session

```python
mqtt.publish(
    f"aimeecloud/device/{device_id}/connect",
    json.dumps({
        "type": "connect",
        "device_id": device_id,
        "user_profile": { "name": user_name },
        "capabilities": { "input": ["voice"], "output": ["tts"] },
        "request_session_id": stored_session_id
    })
)
```

### Step 3: Handle Incoming Messages

```python
def on_message(topic, payload):
    data = json.loads(payload)

    if data["type"] == "session_init":
        store_session_id(data["session_id"])

    elif data["type"] == "response":
        if data["sub_type"] == "chat_response":
            speak(data["tts"])
        elif data["sub_type"] == "game_update":
            update_game_state(data["state"])
            speak(data["tts"])
        elif data["sub_type"] == "robot_command":
            execute_command(data["command"])
            speak(data["tts"])
        elif data["sub_type"] == "error":
            speak(data["tts"])

    elif data["type"] == "status" and data["status"] == "expired":
        clear_session_id()
```

### Step 4: Send User Speech

```python
mqtt.publish(
    f"aimeecloud/device/{device_id}/in",
    json.dumps({
        "type": "intent",
        "session_id": get_session_id(),
        "payload": transcribed_user_text
    })
)
```

### Step 5: Send Game Move

```python
mqtt.publish(
    f"aimeecloud/device/{device_id}/in",
    json.dumps({
        "type": "game_move",
        "session_id": get_session_id(),
        "game": "tic-tac-toe",
        "move": { "position": 4 }
    })
)
```

---

## 10. Testing Against the Reference Client

The browser at https://aimeecloud.com/aimee sends and receives identical messages. You can:
- Open the browser, start a session, and capture the MQTT frames.
- Replay those same JSON payloads from your robot.
- Expect identical responses from the cloud.

If a message works in the browser but fails from the robot, the issue is on the robot side (topic formatting, JSON encoding, missing `session_id`, etc.).

---

## 11. Capabilities Object

Tell the cloud what your robot can do so it can format responses appropriately:

```json
{
  "input": ["voice", "text", "button"],
  "output": ["tts", "display", "led", "motors", "arm"]
}
```

- `input` — How the user interacts with the robot.
- `output` — How the robot can present information back.

Currently, the cloud primarily uses this for game engine formatting. Future features may tailor TTS pacing or LED patterns based on this.

---

## 12. Version

- **Protocol Version**: 1.0
- **Last Updated**: 2026-04-14


# AimeeCloud Robot Protocol Specification

**Version:** 1.1  
**Date:** 2026-04-16

---

## 1. Overview

AimeeCloud uses MQTT as the transport layer between robots (clients) and the cloud gateway. All messages are JSON-encoded. The protocol supports session management, keyword-based intent routing, game state handling, and a new LLM-driven agent mode (`AimeeAgent`).

---

## 2. Topic Structure

| Direction | Topic Pattern | Description |
|-----------|---------------|-------------|
| Client → Cloud | `aimeecloud/device/<deviceId>/connect` | Session initiation / resume |
| Client → Cloud | `aimeecloud/device/<deviceId>/in` | General inbound messages (intent, game moves, pings, agent requests) |
| Cloud → Client | `aimeecloud/device/<deviceId>/out` | Responses from the gateway |
| Cloud → Client | `aimeecloud/device/<deviceId>/status` | Status updates |
| Cloud → Client | `aimeecloud/device/<deviceId>/system` | Operational / system messages |

`<deviceId>` is a stable identifier unique to each robot (e.g., `arduino-uno-q-001`).

---

## 3. Session Management

### 3.1 Connect
**Publish to:** `aimeecloud/device/<deviceId>/connect`

```json
{
  "type": "connect",
  "user_profile": { "name": "BrowserTester", "location": "web" },
  "capabilities": { "input": ["text"], "output": ["display", "tts"] },
  "request_session_id": "sess_abc123"
}
```

- If `request_session_id` is provided and valid for the same device, the session is resumed.
- Otherwise, a new session is created.

### 3.2 Session Init Response
**Received on:** `aimeecloud/device/<deviceId>/out`

```json
{
  "type": "session_init",
  "session_id": "sess_abc123",
  "device_id": "arduino-uno-q-001",
  "status": "connected",
  "expires_in": 600,
  "ttl": 600,
  "timestamp": "2026-04-16T07:00:00.000Z"
}
```

### 3.3 Disconnect
**Publish to:** `aimeecloud/device/<deviceId>/in`

```json
{
  "type": "disconnect",
  "device_id": "arduino-uno-q-001",
  "session_id": "sess_abc123"
}
```

Sessions expire after 10 minutes of being disconnected or 20 minutes of idle inactivity.

---

## 4. Inbound Message Types (`…/in`)

### 4.1 Intent (`intent`)
Routes through the built-in keyword classifier.

```json
{
  "type": "intent",
  "session_id": "sess_abc123",
  "payload": "What is the weather?"
}
```

Supported intents include: `weather`, `news`, `story`, `game`, `help`, `status`, robot movement (`robot_forward`, `robot_backward`, `robot_left`, `robot_right`, `robot_stop`, `robot_wave`), arm control (`arm_raise`, `arm_lower`), and gripper control (`gripper_open`, `gripper_close`). Unmatched input falls back to `chat`.

### 4.2 Game Move (`game_move`)
Sends a move to the currently active game.

```json
{
  "type": "game_move",
  "session_id": "sess_abc123",
  "game": "tic-tac-toe",
  "move": { "position": 4 }
}
```

Supported games: `tic-tac-toe`, `yahtzee`, `candyland`.

### 4.3 Ping (`ping`)

```json
{
  "type": "ping",
  "session_id": "sess_abc123"
}
```

Response: `sub_type: "pong"`.

### 4.4 AimeeAgent (`AimeeAgent`) — NEW IN v1.1
Bypasses the keyword router and sends the request directly to the LLM agent. The agent generates both a conversational reply and any robot-specific commands needed to fulfill the action.

```json
{
  "type": "AimeeAgent",
  "session_id": "sess_abc123",
  "payload": "Look at the red block and tell me what you see"
}
```

**Response:**

```json
{
  "type": "response",
  "sub_type": "aimee_agent",
  "session_id": "sess_abc123",
  "device_id": "arduino-uno-q-001",
  "text": "Sure, let me take a look.",
  "tts": "Sure, let me take a look.",
  "commands": [
    { "type": "snapshot", "camera": "front", "purpose": "analysis" }
  ],
  "context": {
    "active_context": null,
    "context_stack": []
  },
  "timestamp": "2026-04-16T07:00:00.000Z"
}
```

#### Command Reference for AimeeAgent
The `commands` array may contain any of the following objects:

| Action | Example Command |
|--------|-----------------|
| Motor | `{ "type": "motor", "action": "forward", "duration_ms": 1000 }` |
| Arm | `{ "type": "arm", "action": "raise" }` |
| Gripper | `{ "type": "gripper", "action": "open" }` |
| Camera snapshot | `{ "type": "snapshot", "camera": "front", "purpose": "analysis" }` |
| Game move | `{ "type": "game_move", "game": "tic-tac-toe", "position": 4 }` |

Robots MUST execute `commands` in the order provided after (or concurrently with) playing the `tts` response.

---

## 5. Response Sub-Types (`…/out`)

| `sub_type` | Description |
|------------|-------------|
| `chat_response` | General text/tts reply (from keyword routing or LLM fallback). |
| `robot_command` | Keyword-routed robot action; `command` field contains the directive. |
| `game_update` | Game state update; includes `game`, `state`, `text`, `tts`. |
| `aimee_agent` | LLM-agent reply with optional `commands` array (v1.1). |
| `pong` | Reply to a `ping`. |
| `error` | Error condition; includes `error` code and human-readable `text`/`tts`. |

---

## 6. System Messages (`…/system`)

Sent by operators or deployment tools via `send-system-message.js`.

```json
{
  "type": "protocol_update",
  "device_id": "arduino-uno-q-001",
  "msg_id": "proto-v1.1-20260416",
  "timestamp": "2026-04-16T07:00:00.000Z",
  "version": "1.1"
}
```

Supported system message types:
- `protocol_update`
- `config_update`
- `diagnostics_request`
- `restart`
- `firmware_available`

---

## 7. Change Log

### v1.1 — 2026-04-16
- Added `AimeeAgent` inbound message type and `aimee_agent` response sub-type.
- Agents can now return structured `commands` alongside conversational replies.
- Existing keyword router, game engines, and session logic remain unchanged.
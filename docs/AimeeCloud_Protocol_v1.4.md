# AimeeCloud Robot Protocol Specification

**Version:** 1.4  
**Date:** 2026-04-22

---

## 1. Overview

AimeeCloud uses MQTT as the transport layer between robots (clients) and the cloud gateway. All messages are JSON-encoded. The protocol supports session management, keyword-based intent routing, game state handling, LLM-driven agent mode (`AimeeAgent`), and voice-directed TTS responses.

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
  "api_key": "YOUR_API_KEY",
  "user_profile": { "name": "BrowserTester", "location": "web" },
  "capabilities": { "input": ["text"], "output": ["display", "tts"] },
  "tts_mode": "client",
  "request_session_id": "sess_abc123"
}
```

- If `request_session_id` is provided and valid for the same device, the session is resumed.
- Otherwise, a new session is created.
- `api_key` is required for tiered access. Free tier key: `YOUR_API_KEY`

### 3.2 Session Init Response
**Received on:** `aimeecloud/device/<deviceId>/out`

**Success:**
```json
{
  "type": "session_init",
  "session_id": "sess_abc123",
  "device_id": "arduino-uno-q-001",
  "status": "connected",
  "tier": "free",
  "expires_in": 600,
  "ttl": 600,
  "commands": [
    { "type": "expression", "name": "greeting", "priority": "high", "duration_ms": 0, "params": {} }
  ],
  "timestamp": "2026-04-16T07:00:00.000Z"
}
```

**Rejection — Invalid API Key:**
```json
{
  "type": "session_init",
  "device_id": "arduino-uno-q-001",
  "status": "rejected",
  "error": "INVALID_API_KEY",
  "error_detail": "The provided API key is not recognized.",
  "timestamp": "2026-04-16T07:00:00.000Z"
}
```

**Rejection — Tier Limit Exceeded:**
```json
{
  "type": "session_init",
  "device_id": "arduino-uno-q-001",
  "status": "rejected",
  "error": "TIER_LIMIT_EXCEEDED",
  "error_detail": "Max concurrent sessions (2) reached for Hobbyist tier.",
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

### 3.4 Tiered Access

| Tier | Description | Limits |
|------|-------------|--------|
| `free` | Hobbyist / testing | 2 concurrent sessions, 10 sessions/day, 5 API calls/min |
| `paid` | Manufacturer / production | Unlimited sessions and API calls |

---

## 4. Inbound Message Types (`.../in`)

### 4.1 Intent (`intent`)
Routes through the built-in keyword classifier.

```json
{
  "type": "intent",
  "session_id": "sess_abc123",
  "payload": "What is the weather?"
}
```

### 4.2 Game Move (`game_move`)
```json
{
  "type": "game_move",
  "session_id": "sess_abc123",
  "game": "tic-tac-toe",
  "move": { "position": 4 }
}
```

### 4.3 Ping (`ping`)
```json
{
  "type": "ping",
  "session_id": "sess_abc123"
}
```

### 4.4 AimeeAgent (`AimeeAgent`)
Bypasses keyword router, sends directly to LLM agent.

```json
{
  "type": "AimeeAgent",
  "session_id": "sess_abc123",
  "payload": "Look at the red block and tell me what you see"
}
```

**Command Reference for AimeeAgent:**

| Action | Example Command |
|--------|-----------------|
| Motor | `{ "type": "motor", "action": "forward", "duration_ms": 1000 }` |
| Arm | `{ "type": "arm", "action": "raise" }` |
| Gripper | `{ "type": "gripper", "action": "open" }` |
| Camera snapshot | `{ "type": "snapshot", "camera": "front", "purpose": "analysis" }` |
| Game move | `{ "type": "game_move", "game": "tic-tac-toe", "position": 4 }` |
| Expression | `{ "type": "expression", "name": "happy", "duration_ms": 2500, "priority": "high", "params": { "variant": "celebration", "intensity": 1.0 } }` |

---

## 5. Response Sub-Types (`.../out`)

| `sub_type` | Description |
|------------|-------------|
| `chat_response` | General text/tts reply |
| `robot_command` | Keyword-routed robot action |
| `game_update` | Game state update |
| `aimee_agent` | LLM-agent reply with `voice`, `commands` |
| `pong` | Reply to ping |
| `error` | Error condition |

### 5.1 Common Error Codes

| Code | When It Occurs |
|------|---------------|
| `SESSION_NOT_FOUND` | Session ID does not exist or expired |
| `INVALID_API_KEY` | API key unknown or disabled |
| `TIER_LIMIT_EXCEEDED` | Concurrent/daily session limit reached |
| `RATE_LIMIT_EXCEEDED` | Per-minute API call limit exceeded |
| `NO_ACTIVE_GAME` | Game move sent with no active game |
| `INVALID_GAME_MOVE` | Illegal move format or position |
| `GAME_START_ERROR` | Game engine failed to initialize |

---

## 6. Voice Metadata

Every outbound response includes a `voice` object:

```json
{
  "voice": {
    "persona": "aimee-default",
    "provider": "lemonfox",
    "id": "sarah",
    "lang": "en"
  }
}
```

### 6.1 `voice_segments` (optional)
For multi-character dialogue:

```json
{
  "voice_segments": [
    { "speaker": "Narrator", "text": "Once upon a time...", "voice": "narrator" },
    { "speaker": "Dragon", "text": "Roar!", "voice": "character-dragon" }
  ]
}
```

### 6.2 `tts_audio` (optional)
When `tts_mode` is `"server"`:

```json
{
  "tts_audio": {
    "format": "mp3",
    "audio_base64": "//uQxAAAA...",
    "provider": "elevenlabs",
    "voice_id": "XB0fDUnXU5powFXDhCwa"
  }
}
```

---

## 7. System Messages (`.../system`)

```json
{
  "type": "protocol_update",
  "device_id": "arduino-uno-q-001",
  "msg_id": "proto-v1.4-20260422",
  "timestamp": "2026-04-22T07:00:00.000Z",
  "version": "1.4"
}
```

---

## 8. Change Log

### v1.4 — 2026-04-22
- API key authentication with tiered access
- Session-init rejection responses (`INVALID_API_KEY`, `TIER_LIMIT_EXCEEDED`)
- `commands` array in `session_init`
- Common Error Codes section
- Tier-based default `tts_mode`

### v1.3 — 2026-04-17
- ElevenLabs server-side TTS support
- `tts_mode` and `tts_audio`

### v1.2 — 2026-04-16
- `voice` metadata
- `voice_segments` for multi-character TTS
- Game engines capability-aware with `commands`

### v1.1 — 2026-04-16
- `AimeeAgent` inbound type and `aimee_agent` response
- Structured `commands` alongside replies

# AimeeCloud Communication Implementation Plan
## For Arduino UNO Q (ROS2 Humble + 4GB RAM)

**Date:** April 14, 2026  
**Status:** Phase 5 - Cloud Integration (Implementation Complete, Testing Pending)  
**Protocol Version:** 1.0 (Saved to `AIMEE_CLOUD_PROTOCOL.md`)

---

## 1. Executive Summary

This plan defines the implementation of the `aimee_cloud_bridge` ROS2 package to connect the AIMEE robot on the Arduino UNO Q to **AimeeCloud** via the MQTT protocol specified in `AIMEE_CLOUD_PROTOCOL.md`.

### Key Design Principles (4GB Constraint)
- **Lightweight MQTT client** (`paho-mqtt` asyncio variant) — no heavy WebSocket frameworks
- **Non-blocking I/O** — all cloud communication runs in the brick's async loop
- **Minimal memory footprint** — no persistent message history in RAM; session ID only
- **Graceful degradation** — if cloud is unreachable, fall back to local LLM/skills
- **Reuse existing ROS2 infrastructure** — cloud responses route through `/tts/speak`, `/skill/execute`, and `/cmd_vel` just like local skills

---

## 2. Target Architecture

### 2.1 Where the Cloud Bridge Fits

```
[Wake Word] → [Voice Manager] → [Intent Router]
                                        │
                    ┌───────────────────┴───────────────────┐
                    │ Intent Classification                 │
                    │ (keyword + LLM fallback)              │
                    └───────────────────┬───────────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    ▼                                       ▼
            [LOCAL SKILL]                           [CLOUD SKILL]
            (movement, arm,                           (weather, news,
             camera, greeting)                        games, stories, chat)
                    │                                       │
                    ▼                                       ▼
        [Skill Manager / topics]              [aimee_cloud_bridge Node]
                                                        │
                                                        │ MQTT
                                                        ▼
                                                [AimeeCloud Broker]
                                                aimeecloud.com:1883
```

### 2.2 ROS2 Package: `aimee_cloud_bridge`

```
aimee_cloud_bridge/
├── aimee_cloud_bridge/
│   ├── __init__.py
│   ├── cloud_bridge_node.py          # ROS2 node (pub/sub, parameters)
│   └── brick/
│       ├── __init__.py
│       └── cloud_bridge.py           # MQTT client + protocol logic
├── package.xml
├── setup.py
├── setup.cfg
└── config/
    └── cloud_bridge.yaml             # Device ID, broker URL, capabilities
```

---

## 3. Protocol-to-ROS2 Mapping

| Protocol Concept | ROS2 Implementation |
|------------------|---------------------|
| `device_id` | ROS2 parameter `device_id` (default: `arduino-uno-q-001`) |
| `session_id` | Stored in brick + published on `/cloud/session_id` |
| `connect` / `disconnect` | Triggered by node lifecycle + MQTT LWT |
| `intent` (robot→cloud) | Published when Intent Router routes to `cloud_proxy` skill |
| `game_move` | Published by `SkillGameModule` via `/cloud/game_move` topic |
| `ping` | Internal keepalive in brick (every 60s) |
| `out` (cloud→robot) | Subscribed by brick; dispatches to TTS / Skills / Topics |
| `status` (cloud→robot) | Handles `expired` → clears session, re-connects |

### 3.1 Topics Used by Cloud Bridge

**Subscribes:**
- `/intent/classified` → detects `skill_name == "cloud_proxy"` or `category == "cloud_skill"`
- `/cloud/game_move` → `CloudGameMove` msg for tic-tac-toe, yahtzee, etc.
- `/cloud/raw_text` → `std_msgs/String` for direct cloud dispatch (testing/debug)

**Publishes:**
- `/tts/speak` (`std_msgs/String`) — for `chat_response`, `game_update`, `error`
- `/skill/execute` (`ExecuteSkill` action) — for `robot_command` responses
- `/cloud/session_id` (`std_msgs/String`) — session state for other nodes
- `/cloud/connected` (`std_msgs/Bool`) — connection health indicator
- `/robot/state` (`RobotState`) — includes `current_context: "Game: tic-tac-toe"`

---

## 4. Implementation Steps

### Step 1: Create ROS2 Package Skeleton

```bash
cd ~/aimee-robot-ws/src
ros2 pkg create --build-type ament_python aimee_cloud_bridge \
    --dependencies rclpy std_msgs aimee_msgs
```

**Add to `core.launch.py`:**
```python
cloud_bridge = Node(
    package='aimee_cloud_bridge',
    executable='cloud_bridge_node',
    name='cloud_bridge',
    parameters=[config_dir / 'cloud_bridge.yaml'],
    output='screen'
)
```

### Step 2: Implement `CloudBridgeBrick` (`brick/cloud_bridge.py`)

**Dependencies:**
```bash
pip3 install paho-mqtt --break-system-packages
```

**Brick Responsibilities:**
1. **MQTT Connection Management**
   - Connect to `aimeecloud.com:1883`
   - Set LWT to publish `disconnect` on unexpected drop
   - Auto-reconnect with exponential backoff (max 30s)
   - Subscribe to `out` and `status` BEFORE publishing `connect`

2. **Session Lifecycle**
   - On connect: publish `connect` with capabilities + `request_session_id`
   - On `session_init`: store `session_id` to `/tmp/aimee_session.json` (survives reboot)
   - On `status: expired`: clear stored session, reconnect fresh
   - On disconnect: publish graceful `disconnect` message

3. **Inbound Message Dispatch (`out` topic)**
   ```python
   async def _handle_cloud_message(self, payload: dict):
       sub_type = payload.get("sub_type")
       
       if sub_type == "chat_response":
           self._publish_tts(payload["tts"])
           
       elif sub_type == "game_update":
           # Update local game state + speak TTS
           self._publish_game_state(payload["state"])
           self._publish_tts(payload["tts"])
           
       elif sub_type == "robot_command":
           # Route to existing skill manager via action/topic
           self._dispatch_robot_command(payload["intent"], payload["command"], payload["tts"])
           
       elif sub_type == "error":
           if payload.get("error") == "SESSION_NOT_FOUND":
               self._clear_session()
               await self._reconnect()
           else:
               self._publish_tts(payload.get("tts", "I didn't understand that."))
   ```

4. **Outbound Message Publishing**
   - `send_intent(text, intent_dict=None)` → publishes to `in`
   - `send_game_move(game, move)` → publishes to `in`
   - `send_ping()` → publishes to `in`

### Step 3: Implement `CloudBridgeNode` (`cloud_bridge_node.py`)

**Parameters:**
```yaml
cloud_bridge:
  ros__parameters:
    device_id: "arduino-uno-q-001"
    broker_host: "aimeecloud.com"
    broker_port: 1883
    user_name: "Scott"
    user_location: "home"
    user_language: "en-US"
    capabilities:
      input: ["voice", "text"]
      output: ["tts", "display", "motors", "led"]
    reconnect_interval_sec: 5.0
    ping_interval_sec: 60.0
    session_file: "/tmp/aimee_session.json"
```

**Node Structure:**
```python
class CloudBridgeNode(Node):
    def __init__(self):
        super().__init__('cloud_bridge')
        # Load parameters
        # Create brick
        # Subscribe to /intent/classified
        # Subscribe to /cloud/game_move
        # Publishers: /tts/speak, /cloud/session_id, /cloud/connected
        # Start async MQTT loop in background thread
```

### Step 4: Modify Intent Router for Cloud Routing

**File:** `aimee_intent_router/brick/intent_router.py`

**Changes:**
1. Add `CLOUD` intent type and `cloud_skill` category mapping
2. Update `DEFAULT_SYSTEM_PROMPT` to include cloud intents:
   - `weather`, `news`, `story`, `game`, `help`, `chat`
3. Update `_fallback_classify()` to mark cloud intents with:
   - `requires_skill = True`
   - `skill_name = "cloud_proxy"`

**Keyword additions in `_fallback_classify()`:**
```python
elif any(word in text_lower for word in ['weather', 'news', 'story', 'game', 'help']):
    return Intent(
        intent_type=IntentType.CLOUD_SKILL,  # NEW
        action=text_lower,
        confidence=0.7,
        raw_text=text,
        requires_skill=True,
        skill_name="cloud_proxy"
    )
```

**File:** `aimee_intent_router/intent_router_node.py`

Add a publisher for cloud-bound intents:
```python
self._cloud_intent_pub = self.create_publisher(
    IntentMsg, '/intent/classified', reliable_qos
)
# Already exists! Just ensure cloud_proxy skills flow through normally.
```

> **No changes needed** to the intent router node itself if the brick sets `skill_name="cloud_proxy"`. The existing `/intent/classified` topic will carry it to the Skill Manager.

### Step 5: Create `CloudProxySkill` in Skill Manager

**File:** `aimee_skill_manager/brick/skill_manager.py`

Add a new skill that acts as a passthrough to the cloud bridge:

```python
class CloudProxySkill(Skill):
    """Routes user input to AimeeCloud via the cloud bridge."""
    
    def __init__(self, cloud_publish_callback):
        super().__init__("cloud_proxy", "Route requests to AimeeCloud")
        self._publish = cloud_publish_callback
    
    async def execute(self, context: SkillContext) -> SkillResult:
        self._publish(context.user_input)
        return SkillResult(
            success=True,
            response_text="",  # TTS will come from cloud response asynchronously
            execution_time=0.0
        )
```

In `SkillManagerNode.__init__()`:
```python
# Register cloud proxy skill
cloud_skill = CloudProxySkill(self._publish_cloud_intent)
self._brick.register_skill(cloud_skill)

def _publish_cloud_intent(self, text: str):
    msg = String()
    msg.data = text
    self._cloud_intent_pub.publish(msg)
```

> **Alternative (simpler):** Skip the Skill Manager for cloud intents and have the Intent Router publish directly to a new topic `/cloud/user_input`. The Cloud Bridge subscribes to this topic directly. This avoids the action-server latency for cloud requests.

**Recommended approach:**
- Intent Router publishes cloud intents to `/cloud/user_input` (as `std_msgs/String` or a custom `CloudIntent` message)
- Cloud Bridge subscribes and immediately forwards via MQTT
- Skill Manager is bypassed for cloud-only skills (weather, news, chat, games)
- Robot commands coming BACK from cloud still go through Skill Manager/TTS as normal

### Step 6: Add `CloudIntent` Message Type to `aimee_msgs`

**File:** `aimee_msgs/msg/CloudIntent.msg`
```
string raw_text
string intent_type    # weather, news, story, game, chat, robot_command...
string session_id
string game_type      # optional: tic-tac-toe, yahtzee
string move_json      # optional: JSON-encoded game move
```

Update `aimee_msgs/CMakeLists.txt` and `package.xml` accordingly, then rebuild.

### Step 7: Game State Handling

The AimeeCloud protocol supports **Tic-Tac-Toe** and **Yahtzee**.

**For Tic-Tac-Toe:**
- The robot does NOT need to render a board on the UNO Q (no display required)
- The cloud sends `game_update` with a text ASCII board + TTS
- The robot simply speaks the TTS string
- When the user makes a move, the intent router or a simple voice→position mapper publishes to `/cloud/game_move`

**Voice→Move Mapping (minimal):**
```python
# In cloud_bridge_node or a tiny game_mapper node
POSITION_MAP = {
    "top left": 0, "top center": 1, "top right": 2,
    "middle left": 3, "center": 4, "middle": 4, "middle right": 5,
    "bottom left": 6, "bottom center": 7, "bottom right": 8,
}
```

### Step 8: Robot Command Dispatch

When the cloud sends `sub_type: "robot_command"`, the Cloud Bridge must execute the hardware command locally.

**Mapping (Protocol → ROS2):**

| Cloud Intent | Command Object | Local Action |
|--------------|----------------|--------------|
| `robot_forward` | `{"motor": "forward", "duration_ms": 1000}` | Publish `/cmd_vel` Twist for 1s, then stop |
| `robot_backward` | `{"motor": "backward", "duration_ms": 1000}` | Publish `/cmd_vel` negative linear |
| `robot_left` | `{"motor": "left", "duration_ms": 500}` | Publish `/cmd_vel` angular z |
| `robot_right` | `{"motor": "right", "duration_ms": 500}` | Publish `/cmd_vel` negative angular z |
| `robot_stop` | `{"motor": "stop", "duration_ms": 0}` | Publish zero `/cmd_vel` |
| `robot_wave` | `{"motor": "wave", "duration_ms": 1000}` | Publish `/arm/command` or LED pattern |
| `arm_raise` | `{"arm": "raise"}` | Publish `/arm/command` |
| `arm_lower` | `{"arm": "lower"}` | Publish `/arm/command` |
| `gripper_open` | `{"gripper": "open"}` | Publish `/arm/command` |
| `gripper_close` | `{"gripper": "close"}` | Publish `/arm/command` |

**Implementation in Cloud Bridge:**
```python
def _dispatch_robot_command(self, intent: str, command: dict, tts_text: str):
    motor = command.get("motor")
    arm = command.get("arm")
    gripper = command.get("gripper")
    duration_ms = command.get("duration_ms", 0)
    
    if motor:
        twist = Twist()
        if motor == "forward":
            twist.linear.x = 0.5
        elif motor == "backward":
            twist.linear.x = -0.5
        elif motor == "left":
            twist.angular.z = 0.5
        elif motor == "right":
            twist.angular.z = -0.5
        elif motor == "stop":
            pass  # zero twist
        
        self._cmd_vel_pub.publish(twist)
        
        # Auto-stop after duration
        if duration_ms > 0 and motor != "stop":
            threading.Timer(duration_ms / 1000.0, self._stop_motors).start()
    
    if arm or gripper:
        arm_msg = ArmCommand()
        arm_msg.action = arm or gripper
        self._arm_cmd_pub.publish(arm_msg)
    
    # Speak TTS
    self._publish_tts(tts_text)
```

---

## 5. Session Persistence Strategy

Because the UNO Q may reboot or lose WiFi, session persistence is critical.

```python
import json
import os

SESSION_FILE = "/tmp/aimee_session.json"

def _load_session(self) -> str | None:
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE) as f:
            return json.load(f).get("session_id")
    return None

def _save_session(self, session_id: str):
    with open(SESSION_FILE, "w") as f:
        json.dump({"session_id": session_id, "timestamp": time.time()}, f)

def _clear_session(self):
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
```

> `/tmp` is cleared on reboot. If you want session survival across reboots, use `/home/arduino/.config/aimee_session.json` instead.

---

## 6. Error Handling & Fallbacks

| Scenario | Behavior |
|----------|----------|
| **MQTT broker unreachable** | Log warning, publish `/cloud/connected = False`. Intent router can fall back to local LLM if configured. |
| **SESSION_NOT_FOUND** | Clear session file, reconnect immediately with `request_session_id: null` |
| **NO_ACTIVE_GAME** | Speak error TTS, return to idle |
| **Cloud response timeout (>10s)** | Speak "I'm having trouble connecting to the cloud. Let me try locally." Then invoke local LLM via `/llm/generate` action. |
| **WiFi drop + reconnect** | MQTT client auto-reconnects. If within 10min TTL, sends previous `session_id`. |

---

## 7. Memory & CPU Optimization (4GB)

| Technique | Why |
|-----------|-----|
| `paho-mqtt` asyncio loop | No extra threads per subscription |
| No message queue in RAM | Use MQTT broker as the queue |
| `/tmp` session file | No SQLite/DB overhead for one key |
| Bypass Skill Manager for cloud intents | Saves one action-server round-trip |
| 60s ping interval | Keeps NAT/firewall alive without spam |

---

## 8. Testing Plan

### 8.1 Unit Tests
```bash
# Test MQTT connection
python3 -m pytest aimee_cloud_bridge/tests/test_cloud_bridge.py

# Test protocol message formatting
python3 -m pytest aimee_cloud_bridge/tests/test_protocol.py
```

### 8.2 Integration Tests
1. **Broker connectivity:**
   ```bash
   mosquitto_sub -h aimeecloud.com -p 1883 -t "aimeecloud/device/arduino-uno-q-001/out"
   ```
2. **End-to-end flow:**
   - Say: "What's the weather?"
   - Verify: `intent_router` → `/cloud/user_input` → MQTT `in` → Cloud response on `out` → `/tts/speak`
3. **Game flow:**
   - Say: "Play tic tac toe"
   - Cloud responds with `game_update`
   - Say: "Center"
   - Verify `game_move` published with `position: 4`
4. **Command flow:**
   - Say: "Move forward"
   - Cloud responds with `robot_command` (if cloud classifies it)
   - OR local intent router handles it directly via `movement` skill

### 8.3 Network Resilience Tests
- Disconnect WiFi mid-session → reconnect within 10 min → verify session resume
- Disconnect WiFi for >10 min → verify new session initiated
- Block MQTT port → verify graceful fallback to local LLM

---

## 9. Files to Create / Modify

### New Files
```
~/aimee-robot-ws/src/
├── aimee_cloud_bridge/
│   ├── aimee_cloud_bridge/
│   │   ├── __init__.py
│   │   ├── cloud_bridge_node.py
│   │   └── brick/
│   │       ├── __init__.py
│   │       └── cloud_bridge.py
│   ├── package.xml
│   ├── setup.py
│   ├── setup.cfg
│   └── config/
│       └── cloud_bridge.yaml
│
└── aimee_msgs/
    └── msg/
        └── CloudIntent.msg          # NEW message type
        └── CloudGameMove.msg        # Optional: dedicated game message
```

### Modified Files
```
~/aimee-robot-ws/src/
├── aimee_intent_router/
│   └── aimee_intent_router/
│       └── brick/
│           └── intent_router.py     # Add CLOUD_SKILL intent type + routing
│
├── aimee_skill_manager/
│   └── aimee_skill_manager/
│       └── brick/
│           └── skill_manager.py     # Add CloudProxySkill (optional)
│
├── aimee_bringup/
│   └── launch/
│       └── core.launch.py           # Add cloud_bridge_node
│
└── aimee_msgs/
    ├── CMakeLists.txt               # Add CloudIntent.msg
    └── package.xml
```

---

## 10. Implementation Order (Recommended)

1. ~~Create `aimee_msgs/CloudIntent.msg` and rebuild workspace~~ ✅
2. ~~Create `aimee_cloud_bridge` package skeleton~~ ✅
3. ~~Implement `CloudBridgeBrick` with MQTT connect/subscribe/publish~~ ✅
4. ~~Implement `CloudBridgeNode` with ROS2 pub/sub~~ ✅
5. ~~Update `intent_router.py` to classify and route cloud intents~~ ✅
6. ~~Add cloud bridge to `core.launch.py`**~~ ✅
7. Test basic connectivity against AimeeCloud broker
8. ~~Implement robot command dispatch ( Twist + ArmCommand )~~ ✅
9. ~~Add game move support~~ ✅
10. ~~Add session persistence and reconnection logic~~ ✅
11. End-to-end test with voice pipeline

---

## 11. Communication with AimeeCloud Agent

Because I (Kimi CLI) operate in **ephemeral sessions** on this UNO Q, I cannot passively listen to MQTT 24/7. However, within any session I can:

- **Publish test messages** to AimeeCloud to verify connectivity
- **Subscribe and dump** `out`/`status` topics for debugging
- **Inspect session files** and logs
- **Modify code** and restart the cloud bridge node

**For streamlined debugging, I recommend:**
1. AimeeCloud agent exposes a simple HTTP health endpoint: `GET https://aimeecloud.com/health`
2. OR the AimeeCloud agent publishes a "heartbeat" on a diagnostics topic that I can read
3. You can paste MQTT frame dumps or cloud-side logs from the AimeeCloud agent into this CLI, and I will diagnose routing/JSON/schema issues immediately.

**Ready to proceed with implementation?** I can start with Step 1 (creating the message type and package skeleton) right now.

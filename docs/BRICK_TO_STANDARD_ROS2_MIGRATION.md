# Brick-to-Standard-ROS2 Migration Plan

## Executive Summary

The current `arduino.app_utils.brick` abstraction has become a source of friction and bugs. This document explains why, what the trade-offs are, and how to migrate the AIMEE robot nodes to standard ROS2 patterns incrementally.

## What Is the Brick Pattern?

The `arduino.app_utils.brick` decorator wraps a Python class and attempts to provide a framework-agnostic "brick" that can be embedded in ROS2 nodes, standalone scripts, or other runtimes. In practice, this means:

- The **business logic** lives in a `Brick` class (e.g., `IntentRouterBrick`)
- A thin **ROS2 node wrapper** instantiates the brick and bridges ROS2 topics/actions to brick methods
- The brick often runs its own **asyncio event loop in a background thread**

## Problems Observed in Production

### 1. Async-to-ROS2 Executor Deadlocks
**Affected node:** Intent Router  
**Symptom:** `LLM call failed: Timeout waiting for LLM result` or `Timeout waiting for LLM goal acceptance`  
**Root cause:** The brick creates `asyncio.new_event_loop()` in a `threading.Thread`. ROS2 action clients **must** be used from the main executor thread. Bridging them with a thread-safe queue and `asyncio.Event` adds latency, introduces race conditions, and periodically deadlocks under load.

### 2. Zombie / Duplicate Node Processes
**Affected node:** AimeeCloud Client (ACC)  
**Symptom:** Multiple nodes with the same name (`/aimee_cloud`, `/aimee_cloud_client`) or defunct processes  
**Root cause:** `ros2 run` launches the wrapper node, but restarts and the brick’s internal threads sometimes leave stale processes. The abstraction hides process lifecycle, making cleanup harder.

### 3. Cross-Thread State Latency
**Affected node:** Voice Manager  
**Symptom:** TTS echo loop — the robot hears its own speech and transcribes it  
**Root cause:** TTS state (`is_speaking`) arrives via a ROS2 callback in the main executor, but the microphone logic runs in the brick’s background thread. Synchronising them requires custom locks and callbacks instead of native ROS2 topic subscriptions in the same thread.

### 4. Bolted-On Health Monitoring
**Affected nodes:** Voice Manager, TTS  
**Symptom:** Custom `_health_callback` and `_on_health` methods had to be invented  
**Root cause:** ROS2 already has `/diagnostics`, `rosout`, and standard node status patterns. The brick abstraction forces you to re-invent them inside the brick and then proxy them out through the wrapper.

### 5. Cognitive Overhead
**Symptom:** New features require changes in two files (`*_node.py` and `brick/*.py`) and reasoning about two event loops  
**Root cause:** The abstraction splits what should be a single ROS2 node into two layers with different concurrency models.

## Trade-Off Analysis

| Factor | Brick Pattern | Standard ROS2 Node |
|--------|---------------|-------------------|
| **Concurrency model** | Asyncio loop in background thread + ROS2 executor | Single ROS2 executor (can use `MultiThreadedExecutor` where needed) |
| **Action client safety** | Requires manual queue + event bridge | Native executor, no bridge needed |
| **Debugging** | Harder — stack traces cross thread boundaries | Straightforward — everything in one executor |
| **Testing** | Requires custom harnesses | Standard `launch_testing`, `pytest-ros2` |
| **Parameter/QoS handling** | Wrapped behind brick API | Direct `declare_parameter`, `QoSProfile` |
| **Code churn to migrate** | None (already written) | Moderate — one node at a time |
| **Future extensibility** | Worsening technical debt | Clear, idiomatic ROS2 patterns |

## Recommended Migration Strategy: Incremental

Do **not** rewrite everything at once. Migrate in priority order, testing each node before moving to the next.

### Priority 1: Intent Router ✅ Migrated
**Status:** Completed (uncommitted changes present in working tree)  
**What changed:** `intent_router_node.py` was converted to a pure standard ROS2 node. The old `brick/intent_router.py` still exists in the source tree but is no longer imported or used.
- Native `declare_parameter` and `ActionClient` usage
- Fast keyword fallback and cloud routing implemented directly in the node
- LLM worker runs via standard ROS2 patterns

### Priority 2: AimeeCloud Client (ACC) ✅ Migrated
**Status:** Completed (uncommitted changes present in working tree)  
**What changed:** `cloud_bridge_node.py` (AimeeCloud Client) was converted to a pure standard ROS2 node. The old `brick/cloud_bridge.py` still exists in the source tree but is no longer imported or used.
- paho-mqtt client lives directly inside the node class
- All ROS2 callbacks, parameters, and dispatch logic are native
- No brick wrapper or background asyncio thread

### Priority 3: Voice Manager
**Why third:** `arecord` already runs in a subprocess; the brick thread adds no value.  
**Scope:** A standard node with a `threading.Thread` for the Vosk listen loop, publishing transcriptions directly from the main node via `create_publisher`.  
**Key change:** TTS echo suppression becomes a simple subscription to `/tts/is_speaking` in the same thread.

### Priority 4: TTS ✅ Migrated
**Status:** Completed on 2026-04-15  
**What changed:** `tts_node.py` was converted from a brick wrapper to a pure standard ROS2 node. The old `brick/tts.py` was removed.
- Parameters now use native `declare_parameter`
- Playback queue runs as a `threading.Thread` inside the node
- Engine manager (`tts_engines.py`) consolidated to Kokoro + gTTS only
- Removed Piper, pyttsx3, and all brick-related parameters
- Configuration and launch files updated to reflect standard node usage

## What "Standard ROS2" Looks Like

### Intent Router (reference structure)

```python
class IntentRouterNode(Node):
    def __init__(self):
        super().__init__('intent_router')
        
        # Parameters
        self.declare_parameter('chat_routing', 'cloud')
        self.declare_parameter('confidence_threshold', 0.6)
        
        # Publishers
        self._intent_pub = self.create_publisher(Intent, '/intent/classified', 10)
        self._tts_pub = self.create_publisher(String, '/tts/speak', 10)
        
        # Subscribers
        self.create_subscription(Transcription, '/voice/transcription', self._on_transcription, 10)
        
        # Action client (lives in main executor)
        self._llm_client = ActionClient(self, LLMGenerate, '/llm/generate')
        
        # LLM worker queue (simple list + lock)
        self._llm_queue = []
        self._llm_lock = threading.Lock()
        self._llm_worker_timer = self.create_timer(0.05, self._llm_worker)
    
    def _on_transcription(self, msg):
        # Fast keyword classification
        intent = self._classify_intent(msg.text)
        
        if self.chat_routing == 'cloud' and not self._is_local_skill(intent):
            # Send as unclassified to AimeeCloud
            self._publish_unclassified(msg.text, intent)
            return
        
        # Otherwise execute locally
        self._execute_intent(intent)
```

### AimeeCloud Client (reference structure)

```python
class AimeeCloudClientNode(Node):
    def __init__(self):
        super().__init__('aimee_cloud_client')
        
        # MQTT client (paho manages its own network thread)
        self._mqtt_client = mqtt.Client(...)
        self._mqtt_client.on_connect = self._on_mqtt_connect
        self._mqtt_client.on_message = self._on_mqtt_message
        self._mqtt_client.loop_start()
        
        # ROS2 publishers
        self._tts_pub = self.create_publisher(String, '/tts/speak', 10)
        
        # ROS2 subscribers
        self.create_subscription(Intent, '/intent/classified', self._on_intent, 10)
```

## Migration Status

| Node | Status | Date | Notes |
|------|--------|------|-------|
| TTS | ✅ Complete | 2026-04-15 | `tts_node.py` is now a standard ROS2 node; `brick/tts.py` removed. |
| Intent Router | ✅ Complete | 2026-04-14* | `intent_router_node.py` is now a standard ROS2 node; `brick/intent_router.py` unused. |
| AimeeCloud Client (ACC) | ✅ Complete | 2026-04-14* | `cloud_bridge_node.py` is now a standard ROS2 node; `brick/cloud_bridge.py` unused. |
| Voice Manager | ⏳ Pending | — | Still uses `VoiceManagerBrick`; `brick/voice_manager.py` is actively imported. |
| LLM Server | ⏳ Pending | — | Still uses `LLMServerBrick`; `brick/llm_server.py` is actively imported. |
| Skill Manager | ⏳ Pending | — | Still uses `SkillManagerBrick`; `brick/skill_manager.py` is actively imported. |
| Wake Word EI | ⏳ Pending | — | Still uses `WakeWordEIBrick`; `brick/wake_word_ei.py` is actively imported. |
| Vision OBSBOT | ⏳ Pending | — | Still uses `ObsbotBrick`; `brick/obsbot_brick.py` is actively imported. |

*Dates reflect code changes present in the working tree that were not committed before the board locked up.

## Decision Checklist

Use this checklist when deciding whether to migrate a node:

- [ ] Does the node use ROS2 action clients? → **Migrate first**
- [ ] Does the node bridge async I/O (MQTT, HTTP, WebSocket) to ROS2? → **Migrate second**
- [ ] Does the node manage hardware subprocesses (arecord, aplay, ffmpeg)? → **Migrate third**
- [ ] Is the node currently stable and rarely touched? → **Migrate last / never**

## Appendix: Files to Deprecate

| Node | Current files | Future files |
|------|--------------|--------------|
| Intent Router | `intent_router_node.py`, `brick/intent_router.py` | `intent_router_node.py` (single file) ✅ |
| AimeeCloud Client (ACC) | `cloud_bridge_node.py`, `brick/cloud_bridge.py` | `cloud_bridge_node.py` (single file) ✅ |
| Voice Manager | `voice_manager_node.py`, `brick/voice_manager.py` | `voice_manager_node.py` (single file) |
| LLM Server | `llm_server_node.py`, `brick/llm_server.py` | `llm_server_node.py` (single file) |
| Skill Manager | `skill_manager_node.py`, `brick/skill_manager.py` | `skill_manager_node.py` (single file) |
| Wake Word EI | `wake_word_ei_node.py`, `brick/wake_word_ei.py` | `wake_word_ei_node.py` (single file) |
| Vision OBSBOT | `obsbot_node.py`, `brick/obsbot_brick.py` | `obsbot_node.py` (single file) |
| TTS | `tts_node.py`, `brick/tts.py` (deleted) | `tts_node.py` (single file) ✅ |

## Conclusion

The brick pattern added indirection without adding value for nodes that are fundamentally ROS2-native. Migrating to standard ROS2 nodes will reduce bugs, simplify debugging, and make the codebase accessible to any ROS2 developer.

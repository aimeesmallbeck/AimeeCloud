# Aimee Robot - Session Checkpoint

**Date:** 2026-04-13 (Updated 2026-04-16)  
**Session Focus:** Migrate routing to AimeeAgent; simplify Intent Router; add command execution in ACC

---

## 🎉 MISSION ACCOMPLISHED!

### What Was Done Today

1. **Separated Video Pipeline from OBSBOT SDK Node**
   - Stripped `obsbot_brick.py` to SDK-only (no OpenCV/UVC capture code)
   - Stripped `obsbot_node.py` of all video publishing (`/camera/image_raw`, cv_bridge, video timer)
   - `obsbot_node` is now a pure PTZ/tracking/status node

2. **Added Dedicated USB Camera Node**
   - `core.launch.py` now launches `usb_cam_node_exe` from `ros-humble-usb-cam`
   - Configured for `/dev/video2`, 1280×720, `mjpeg2rgb`, `mmap` I/O
   - Publishes to `/camera/image_raw` and `/camera/camera_info`
   - **Note:** `ros-humble-v4l2-camera` v0.6.2 was installed first but does not support MJPG format (crashes with `cv_bridge::Exception: Unrecognized image encoding []`)

3. **Performance Results**
   - `obsbot_node` CPU usage: **~88% → ~5%**
   - Video stream stable at **~23 fps** at 1280×720
   - Python GIL + MJPEG decode overhead completely eliminated from video pipeline

4. **Fixed Monitor Node for New Configuration**
   - Added `usb_camera` to monitor's node definitions
   - Removed obsolete `publish_video:=true` arg from `obsbot_camera` definition
   - Replaced `ros2 node list` subprocess with `get_node_names_and_namespaces()`
   - Replaced `ros2 topic list -t` subprocess with `get_topic_names_and_types()`
   - Replaced `ros2 topic hz` subprocess with frame timestamp-based Hz calculation
   - Changed monitor to subscribe to `/camera/image_raw/compressed` instead of raw `sensor_msgs/Image`
   - Added `image_transport/republish` node to `core.launch.py` to generate compressed topic
   - Camera stream now yields JPEG bytes directly with zero OpenCV conversion
   - Monitor CPU: **~70% → ~40%** (subprocess starvation eliminated)

5. **Verification**
   - `/api/nodes` returns live node list without shell-outs
   - `/api/topics` returns topic metadata from native ROS2 API
   - `/api/camera/status` reports `connected: true`
   - `/camera/stream` serves valid MJPEG with `ff d8 ff e0` JPEG headers

---

## 🔊 TTS Migration to Standard ROS2 Node (2026-04-15)

### What Was Done

1. **Migrated TTS to Pure Standard ROS2 Node**
   - `tts_node.py` was already a standard ROS2 node; removed all remaining brick artifacts
   - Deleted `aimee_tts/aimee_tts/brick/tts.py` (old brick implementation)
   - Removed Piper and pyttsx3 support per migration plan

2. **Engine Consolidation: Kokoro Primary + gTTS Fallback**
   - Updated `tts_engines.py` to support only **Kokoro** (primary, offline) and **gTTS** (cloud fallback)
   - Removed `PiperEngine`, `Pyttsx3Engine`, and all related parameters/fallback logic
   - `TTSEngineManager` now initializes only Kokoro (pykokoro preferred, official package fallback) and gTTS

3. **Configuration & Launch Updates**
   - Updated `core.launch.py` to default `default_engine:=kokoro` and `fallback_engine:=gtts`
   - Updated `config/brick_config.yaml` to remove deprecated engines and reflect new defaults
   - Cleaned up `setup.py` and `package.xml` descriptions
   - Rewrote `README.md` to document the standard ROS2 node usage with Kokoro/gTTS

4. **Files Modified**
   ```
   /home/arduino/aimee-robot-ws/src/
   ├── aimee_tts/
   │   ├── aimee_tts/tts_node.py            [UPDATED - removed piper/pyttsx3 params]
   │   ├── aimee_tts/tts_engines.py         [UPDATED - kokoro + gtts only]
   │   ├── aimee_tts/brick/tts.py           [DELETED - deprecated brick]
   │   ├── config/brick_config.yaml         [UPDATED - removed deprecated engines]
   │   ├── setup.py                         [UPDATED - description]
   │   ├── package.xml                      [UPDATED - description]
   │   └── README.md                        [REWRITTEN - standard node docs]
   └── aimee_bringup/launch/core.launch.py  [UPDATED - kokoro primary, gtts fallback]
   ```

---

## 🎯 Intent Router Rewrite & AimeeCloud Integration (2026-04-16)

### What Was Done

1. **External Intent Configuration**
   - Created `/workspace/config/aimee_intent_config.json` containing all keyword/phrase matching rules
   - Intent Router now loads intent definitions from this file at runtime
   - Config is reloaded on every classification so edits apply immediately without node restart

2. **Intent Router Rewrite (`aimee_intent_router`)**
   - Converted to standard ROS2 node loading config from external JSON
   - Classification uses word-boundary checks, phrase substrings, and `question_words` fallback for `chat`
   - Emits AimeeCloud-compatible intent types directly: `chat`, `weather`, `news`, `story`, `game`, `help`, `status`, `robot_*`, `arm_*`, `gripper_*`, `unclassified`
   - Added `"exact": true` phrase matching for movement and arm/gripper commands so only exact full utterances trigger local skills

3. **Explicit Local Command Requirements**
   - Robot movement commands must now be the exact phrases:
     - `move forward`, `move backward`, `move left`, `move right`, `move stop`
   - Arm/gripper commands must now be the exact phrases:
     - `wave arm`, `raise arm`, `lower arm`, `open gripper`, `close gripper`
   - Single words like `right`, `stop`, `wave`, `open` no longer trigger local skills and are routed to AimeeCloud

4. **Noise Word Updates**
   - Added `hello` and `hey` to `noise_words` in the intent config
   - These single-word utterances are now silently ignored instead of being routed to `chat` or AimeeCloud

5. **AimeeCloud Client Simplification (`aimee_cloud_bridge`)**
   - Renamed all `cloud_proxy` / `cloud_bridge` references to `AimeeCloud` in code and docs
   - `cloud_bridge_node.py` now forwards intents to AimeeCloud solely based on `skill_name == "AimeeCloud"`
   - Removed the old intent-type-to-skill mapping layer
   - Session lifecycle (load, save, resume, expiry, clear) handled by ACC

6. **Launch File Updates**
   - `core.launch.py` updated to pass `intent_config_path` to the Intent Router
   - Whisper API credentials (Lemonfox.ai `api_base_url` and `api_key`) passed to Voice Manager

### Files Modified
```
/home/arduino/aimee-robot-ws/
├── config/aimee_intent_config.json                    [NEW - external intent config]
├── src/aimee_intent_router/
│   └── aimee_intent_router/intent_router_node.py      [REWRITTEN - external config, hot-reload, exact matching]
├── src/aimee_cloud_bridge/
│   └── aimee_cloud_bridge/cloud_bridge_node.py        [UPDATED - AimeeCloud branding, simplified forwarding]
├── src/aimee_bringup/launch/core.launch.py            [UPDATED - intent_config_path + Whisper API params]
├── Aimee_Project_Plan.md                              [UPDATED - AimeeCloud branding, intent routing docs]
└── CHECKPOINT.md                                      [THIS FILE - updated]
```

### Verification Results

| Input | Classification | Routing |
|-------|----------------|---------|
| `move right` | `robot_right` | local movement ✅ |
| `move left` | `robot_left` | local movement ✅ |
| `move forward` | `robot_forward` | local movement ✅ |
| `move backward` | `robot_backward` | local movement ✅ |
| `move stop` | `robot_stop` | local movement ✅ |
| `wave arm` | `arm_wave` | local arm_control ✅ |
| `raise arm` | `arm_raise` | local arm_control ✅ |
| `lower arm` | `arm_lower` | local arm_control ✅ |
| `open gripper` | `gripper_open` | local arm_control ✅ |
| `close gripper` | `gripper_close` | local arm_control ✅ |
| `right` | `unclassified` | AimeeCloud ✅ |
| `stop` | `unclassified` | AimeeCloud ✅ |
| `wave` | `unclassified` | AimeeCloud ✅ |
| `open` | `unclassified` | AimeeCloud ✅ |
| `hello` | ignored | noise ✅ |
| `hey` | ignored | noise ✅ |
| `what time is it right now` | `chat` | AimeeCloud ✅ |

---

## 🎤 Voice Manager Migration to Standard ROS2 Node (2026-04-16)

### What Was Done

1. **Migrated `voice_manager` from Brick Pattern to Standard ROS2 Node**
   - Merged `brick/voice_manager.py` directly into `voice_manager_node.py`
   - Removed the background asyncio thread and brick callbacks
   - The Vosk listen loop now runs as a simple `threading.Thread` inside the node
   - TTS echo suppression now uses native ROS2 subscriptions (`/tts/is_speaking`, `/tts/speak`) directly
   - Removed `brick` package from `setup.py`; `brick/voice_manager.py` is now unused

2. **Added Auto-Recovery for Audio Capture Stalls**
   - Replaced blocking `stdout.read(4000)` with `select.select` + `os.read` in the listen loop
   - Detects arecord stalls (no data for 5+ seconds) and exits the loop, triggering auto-restart after 2 seconds
   - Detects arecord process death and restarts automatically
   - Detects zero-byte silence floods and restarts

3. **Fixed OBSBOT Microphone Dependency on `usb_cam`**
   - Discovered that the OBSBOT Tiny 2 Lite microphone only produces audio when its video stream is active
   - Added `_ensure_usb_camera_running()` to start `usb_cam_node_exe` before the listen loop
   - Includes a 3-second delay to let the V4L2 interface activate the mic
   - Verified: `hw_ptr` and `appl_ptr` advance correctly after `usb_cam` starts

4. **PONG Log Spam Reduction**
   - Changed AimeeCloud Client (`cloud_bridge_node.py`) to log MQTT `pong` messages at `debug` level instead of `info`

### Files Modified
```
/home/arduino/aimee-robot-ws/
├── src/aimee_voice_manager/
│   ├── aimee_voice_manager/voice_manager_node.py      [REWRITTEN - merged brick, standard ROS2 node]
│   └── setup.py                                         [UPDATED - removed brick package]
├── src/aimee_cloud_bridge/
│   └── aimee_cloud_bridge/cloud_bridge_node.py          [UPDATED - pong at debug level]
└── CHECKPOINT.md                                        [THIS FILE - updated]
```

---

## ☁️ Monitor Cloud Session Clear Button (2026-04-16)

### What Was Done

1. **Added "Clear AimeeCloud Session" Button to Monitor Dashboard**
   - New "☁️ Cloud Session" panel in the left sidebar
   - Button publishes `Bool(data=True)` to `/cloud/clear_session`

2. **Cloud Bridge Handles Session Clear**
   - New subscriber `/cloud/clear_session` in `cloud_bridge_node.py`
   - Calls `_clear_session()` then immediately `_publish_connect()` to request a new session from AimeeCloud
   - Fixed initial bug where clearing only deleted the local session file without sending a new `connect`, causing subsequent requests to fail

3. **End-to-End Verification**
   - Clicked "Clear Session" → local session cleared → new `connect` sent → AimeeCloud replied with `session_init`
   - Voice query "What time is it in Seattle right now?" flowed through correctly after session reset

### Files Modified
```
/home/arduino/aimee-robot-ws/
├── src/aimee_cloud_bridge/
│   └── aimee_cloud_bridge/cloud_bridge_node.py          [UPDATED - clear_session subscriber + reconnect]
├── src/aimee_ros2_monitor/
│   ├── aimee_ros2_monitor/monitor_node.py               [UPDATED - /cloud/clear_session publisher + API endpoint]
│   └── aimee_ros2_monitor/templates/index.html          [UPDATED - Cloud Session panel + JS handler]
└── CHECKPOINT.md                                        [THIS FILE - updated]
```

---

## 🤖 AimeeAgent Migration & ACC Command Execution (2026-04-16)

### What Was Done

1. **Retrieved AimeeCloud Protocol v1.1**
   - Subscribed to MQTT topic `aimeecloud/service/protocol`
   - Saved updated spec to `docs/AimeeCloud_Protocol_v1.1.md`
   - Key addition: `AimeeAgent` message type and `commands` array in responses

2. **Simplified Intent Router (`aimee_intent_router`)**
   - Removed all LLM action client code (`_llm_client`, `_call_llm`, `_generate_llm_response_async`)
   - Router now has exactly two paths:
     - **Local skills** (`movement`, `arm_control`, `camera`) → execute locally with fallback TTS
     - **Everything else** → publish `IntentMsg(skill_name="AimeeCloud")` for ACC to forward
   - Removed `chat_routing`, `enable_conversation_mode`, and conversation context parameters
   - This eliminates the problematic local intent-to-response generation path

3. **Updated AimeeCloud Client (`aimee_cloud_bridge`)**
   - Added `send_agent_request()` to publish `type: "AimeeAgent"` instead of `type: "intent"`
   - All non-local voice requests now bypass AimeeCloud's keyword router and go straight to the LLM agent
   - Added `aimee_agent` response handler in `_handle_out_message()`
   - Added `_execute_command()` dispatcher that handles:
     - `motor` → publishes `Twist` to `/cmd_vel` with optional duration
     - `arm` / `gripper` → publishes `ArmCommand` to `/arm/command`
     - `snapshot` → stops `usb_camera`, calls `CaptureSnapshot` service, uploads result back to AimeeCloud, restarts camera
     - `game_move` → publishes `CloudIntent` to `/game/command`
   - Fixed missing `import subprocess` bug
   - Added `/game/command` publisher for local game handler integration

4. **Rebuild & Verification**
   - Rebuilt both packages with `colcon build --packages-select aimee_cloud_bridge aimee_intent_router`
   - Cleanly restarted the ROS2 core stack
   - All 7 nodes up and running with no duplicates

### New Voice Request Flow

1. **Voice Manager** → `/voice/transcription`
2. **Intent Router** classifies:
   - `move forward`, `wave arm`, etc. → local execution + TTS
   - Everything else → `IntentMsg(skill_name="AimeeCloud")`
3. **ACC** receives intent and sends `AimeeAgent` MQTT message to AimeeCloud
4. **AimeeCloud** responds with `sub_type: "aimee_agent"` + optional `commands` array
5. **ACC** speaks the `tts` response and executes commands locally in order

### Files Modified

```
/home/arduino/aimee-robot-ws/
├── docs/AimeeCloud_Protocol_v1.1.md                    [NEW - retrieved from MQTT]
├── src/aimee_intent_router/
│   └── aimee_intent_router/intent_router_node.py      [UPDATED - stripped LLM, simplified routing]
├── src/aimee_cloud_bridge/
│   └── aimee_cloud_bridge/cloud_bridge_node.py        [UPDATED - AimeeAgent requests + command execution]
├── Aimee_Project_Plan.md                              [UPDATED - AimeeAgent docs]
└── CHECKPOINT.md                                      [THIS FILE - updated]
```

### Notes

- Offline fallback LLM will be implemented later as a separate layer (e.g., in the bridge or a dedicated offline-agent node), not inside the intent router.
- The `AimeeAgent` command reference from the protocol:
  - Motor: `{ "type": "motor", "action": "forward", "duration_ms": 1000 }`
  - Arm: `{ "type": "arm", "action": "raise" }`
  - Gripper: `{ "type": "gripper", "action": "open" }`
  - Snapshot: `{ "type": "snapshot", "camera": "front", "purpose": "analysis" }`
  - Game move: `{ "type": "game_move", "game": "tic-tac-toe", "position": 4 }`

---

## 🔊 Lemonfox TTS Primary, Voice Metadata & Interstitial Removal (2026-04-16)

### What Was Done

1. **Retrieved AimeeCloud Protocol v1.2**
   - Subscribed to MQTT topic `aimeecloud/service/protocol`
   - Saved updated spec to `docs/AimeeCloud_Protocol_v1.1.md`
   - Key addition: `voice` object in all outbound responses and optional `voice_segments` for multi-character dialogue

2. **Added Lemonfox.ai TTS Engine**
   - Implemented `LemonfoxEngine` in `tts_engines.py` using OpenAI-compatible TTS API (`/v1/audio/speech`)
   - Added API key and base URL parameters to `TTSEngineManager` and `TTSNode`
   - Updated `core.launch.py` to pass the Lemonfox API key and set `default_engine:=lemonfox`, `fallback_engine:=gtts`
   - Updated `brick_config.yaml` to reflect new defaults

3. **TTS Node Voice Support**
   - `tts_node.py` now recognizes `lemonfox` in the `engine|voice:text` prefix parser
   - Default voice changed from `af_heart` (Kokoro) to `sarah` (Lemonfox)
   - All three engines available: `lemonfox`, `kokoro`, `gtts`

4. **AimeeCloud Client Voice Integration**
   - ACC parses `voice` metadata from every AimeeCloud response
   - Publishes TTS with engine|voice prefix (e.g., `lemonfox|sarah:Hello!`)
   - Supports `voice_segments`: publishes sequential `/tts/speak` messages with per-segment voice mapping
   - `robot_command`, `chat_response`, `game_update`, `error`, and `aimee_agent` sub-types all pass voice info to TTS

5. **Removed Interstitial Responses**
   - Stripped `_enable_interstitials`, `_interstitial_phrases`, and suppression logic from ACC
   - Interstitials unnecessary while AimeeCloud is online (responses are fast)
   - Will re-introduce later as part of offline fallback architecture

### Files Modified

```
/home/arduino/aimee-robot-ws/
├── docs/AimeeCloud_Protocol_v1.1.md                    [UPDATED - protocol v1.2 retrieved]
├── src/aimee_tts/
│   ├── aimee_tts/tts_engines.py                       [UPDATED - LemonfoxEngine added]
│   ├── aimee_tts/tts_node.py                          [UPDATED - lemonfox support, voice params]
│   └── config/brick_config.yaml                       [UPDATED - lemonfox defaults]
├── src/aimee_cloud_bridge/
│   └── aimee_cloud_bridge/cloud_bridge_node.py        [UPDATED - voice support, removed interstitials]
├── src/aimee_bringup/launch/core.launch.py            [UPDATED - lemonfox TTS params]
├── Aimee_Project_Plan.md                              [UPDATED - TTS and voice docs]
└── CHECKPOINT.md                                      [THIS FILE - updated]
```

---

## 📊 Running Services

| Service | Container | Status | URL |
|---------|-----------|--------|-----|
| **ROS2 Core** | `aimee-robot` | 🟢 Running | — |
| **Monitor** | `aimee-robot` | 🟢 Operational | http://192.168.1.100:8081 |

---

## 🔮 Next Steps (Future Sessions)

1. **Dashboard Enhancements**
   - Add action goal widgets (test PickPlace from dashboard)
   - Add voice pipeline visualization

2. **Hardware Testing**
   - Connect UGV02 via serial and verify `/cmd_vel` response
   - Test OBSBOT PTZ commands through ROS2 topics

3. **Remaining Optimizations**
   - Further reduce monitor camera-stream CPU (e.g., lower-resolution direct V4L2 read or reduce republish frequency)

4. **Dynamic AimeeCloud Capabilities**
   - After hardware arrives, scan active ROS2 nodes to determine capabilities dynamically
   - e.g., `/ugv02_controller` present → add `"motors"`; `/arm_controller` present → add `"arm"`; camera nodes present → keep `"snapshot"`
   - This avoids hardcoding capabilities in `cloud_bridge_node.py`

5. **Brick-to-Standard-ROS2 Migration (Remaining Nodes)**
   - Cloud Bridge (already migrated to AimeeCloud ACC) ✅
   - Voice Manager (Priority 1)

---

## 📝 Notes

- `usb_cam` package works well for MJPEG streams on the UNO Q; `v4l2_camera` does not.
- The `image_transport/republish` C++ node consumes significant CPU (~85%) because it re-encodes 1280×720 rgb8 back to JPEG. This is acceptable for now since it offloads work from the Python monitor.
- Fast DDS SHM config is still disabled (`FASTRTPS_DEFAULT_PROFILES_FILE` set to disable SHM) to avoid `open_and_lock_file` errors.
- TTS brick `__pycache__` directory could not be fully removed due to root-owned `.pyc` files inside the container; source brick files are deleted.
- Intent Router config hot-reload means future keyword/phrase tuning can be done by editing `/workspace/config/aimee_intent_config.json` with no node restart required.

---

## 🔊 TTS Storytelling Voice Options — Research Notes (2026-04-15)

**Context:** Kokoro TTS exhibits ~20 s latency on the UNO Q. The `PyKokoroEngine` (ONNX-based) recreates its entire pipeline when switching voices, making mid-story character voice changes impractical. The `KokoroOfficialEngine` (torch-based) does *not* recreate the pipeline on voice changes, but the initial model load is slow on this hardware. Default engine was switched back to `gtts` while we evaluate storytelling alternatives.

### Decision Log
- **Immediate action:** Revert default TTS engine to `gtts` to restore responsive speech.
- **Future work:** Evaluate one of the four approaches below for multi-voice storytelling.

### Option 1: Pre-recorded Character Clips + gTTS Narrator (Recommended)
- **How it works:** Use gTTS for the narrator and any dynamic / unpredictable text. Pre-record character dialogue as `.wav`/`.mp3` files, store them on the robot, and play them directly via `pygame.mixer` or a dedicated media player node.
- **Message format idea:** `play:/path/to/owl.wav` or `char_owl:Hello` routed to playback instead of synthesis.
- **Pros:** Theatrical quality, zero latency, works offline, true distinct voices.
- **Cons:** Requires recording / generating lines ahead of time.

### Option 2: gTTS with Regional Accents (Easy Code Change)
- **How it works:** Leverage gTTS `tld` parameter (`com`, `co.uk`, `com.au`, `co.in`, `ca`, `ie`) combined with `slow=True/False` to create 6–10 recognizably different "characters."
- **Message format idea:** `gtts|co.uk:Hello, I'm the British fox`
- **Pros:** No new dependencies, works today with a small parser patch.
- **Cons:** Still sounds like Google Translate, just with different accents.

### Option 3: OpenAI TTS Engine (Best Cloud Multi-Voice Quality)
- **How it works:** Add an `OpenAITTSEngine` to `tts_engines.py` that calls the OpenAI TTS API. Supports 6 distinct voices: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`.
- **Pros:** Excellent storytelling quality, fast, natural sounding, true multi-voice.
- **Cons:** Requires internet connection and an API key; not free at scale.

### Option 4: Fix Kokoro for True Offline Multi-Voice
- **Sub-option A — Official `kokoro` package:** Use `kokoro` (torch-based) instead of `pykokoro`. It keeps one `KPipeline` instance and passes `voice=` directly, so voice switching is instant after the slow initial load.
- **Sub-option B — Cached `PyKokoroEngine` instances:** Modify `TTSEngineManager` to maintain one ONNX pipeline per voice in a dictionary (`voice -> pipeline`). Switching voices just selects a different cached pipeline instead of rebuilding it.
- **Pros:** High quality, fully offline.
- **Cons:** Sub-option A uses more RAM (torch). Sub-option B uses more RAM (multiple ONNX sessions) and needs code changes.

### Configuration Changes Made Today
- `aimee_bringup/launch/core.launch.py`: `default_engine` changed from `kokoro` back to `gtts`.
- `aimee_tts/config/brick_config.yaml`: `DEFAULT_ENGINE` default and `development` profile changed from `kokoro` back to `gtts`.

**Status:** 🤖 **VIDEO PIPELINE SEPARATED, MONITOR OPERATIONAL, TTS MIGRATED TO STANDARD ROS2 NODE WITH LEMONFOX PRIMARY, INTENT ROUTER REWRITTEN WITH EXTERNAL CONFIG, AIMEEAGENT PROTOCOL IMPLEMENTED WITH VOICE SUPPORT!**

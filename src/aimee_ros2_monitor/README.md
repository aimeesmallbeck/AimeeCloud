# AIMEE ROS2 Monitor Dashboard

A lightweight web-based dashboard for monitoring ROS2 without dealing with lower-level internals.

## Features

### 1. Log Viewer (rqt_console style)
- Real-time log streaming from `/rosout`
- Filter by level (Debug, Info, Warn, Error, Fatal)
- Filter by node name
- Search within messages
- Auto-scroll with pause option
- Log statistics counters

### 2. Node Widgets
- Visual cards for each running ROS2 node
- Color-coded by category:
  - 🟠 **Audio** (wake_word, voice, TTS)
  - 🔵 **AI** (intent, LLM)
  - 🟢 **Skills** (skill_manager)
  - 🩷 **Vision** (camera nodes)
  - ⚪ **Tools** (dashboard, monitor)
  - ⚙️ **Other**
- Click any node for detailed info (subscriptions, publishers, services)
- Auto-refresh every 5 seconds

### 3. Topic Monitor
- List of all active ROS2 topics
- Message type display
- Live frequency (Hz) and bandwidth
- Click to echo topic data

## Usage

### Quick Start
```bash
# Start the monitor
./start_monitor.sh

# Or manually:
docker exec -it aimee-robot bash -c "
    source /opt/ros/humble/setup.bash
    source /workspace/install/setup.bash
    ros2 run aimee_ros2_monitor monitor_node
"
```

Then open your browser to: **http://localhost:8080**

### Running with ROS2
```bash
# Terminal 1: Start your ROS2 nodes
ros2 launch aimee_bringup core.launch.py

# Terminal 2: Start the monitor
ros2 run aimee_ros2_monitor monitor_node
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Toggle auto-refresh |
| `Escape` | Close modal |

## Architecture

```
┌─────────────────────────────────────────┐
│  Browser (http://localhost:8080)        │
│  - Single-page dashboard                │
│  - Auto-refreshing widgets              │
└────────────────┬────────────────────────┘
                 │ HTTP
┌────────────────▼────────────────────────┐
│  Flask Server (port 8080)               │
│  - REST API for logs/nodes/topics       │
│  - Serves web UI                        │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│  ROS2 Monitor Node                      │
│  - Subscribes to /rosout (logs)         │
│  - Polls ros2 node/topic list           │
│  - Caches data for web UI               │
└─────────────────────────────────────────┘
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/logs` | Get logs with filters (level, node, search) |
| `POST /api/logs/clear` | Clear log buffer |
| `GET /api/nodes` | List running nodes |
| `GET /api/nodes/<name>` | Get node details |
| `POST /api/nodes/refresh` | Force node list refresh |
| `GET /api/topics` | List active topics |
| `GET /api/topics/<name>/echo` | Echo single message |
| `GET /api/system` | System status |

## Comparison with rqt_console

| Feature | rqt_console | AIMEE Monitor |
|---------|-------------|---------------|
| Log viewing | ✅ | ✅ |
| Node monitoring | ❌ | ✅ (visual widgets) |
| Topic monitoring | ❌ | ✅ (with Hz/bandwidth) |
| Web-based | ❌ | ✅ |
| Resource usage | Heavy (Qt) | Light (Flask) |
| Setup | Complex | Simple |

## Troubleshooting

### "Connection Error" in status
- Make sure ROS2 is running
- Check that the monitor node is started

### No logs appearing
- Verify nodes are publishing to `/rosout`
- Check log level filters

### Topics show no Hz
- Hz monitoring requires messages to be flowing
- Some topics may be idle

## Future Enhancements

- [ ] Plot/joystick widgets for topic data
- [ ] Service call interface
- [ ] Parameter editing
- [ ] Bag recording control
- [ ] Multi-robot support

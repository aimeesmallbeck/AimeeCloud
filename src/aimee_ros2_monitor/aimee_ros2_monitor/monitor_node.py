#!/usr/bin/env python3
"""
AIMEE ROS2 Monitor - Lightweight Dashboard

A simple web-based dashboard for monitoring ROS2:
- rqt_console-like log viewer (captures /rosout)
- Node status widgets (visual cards for each node)
- Topic monitoring with live data flow
- No complex ROS2 internals - just clean monitoring

Usage:
    ros2 run aimee_ros2_monitor monitor_node
    
Then open browser to: http://localhost:8080
"""

import json
import logging
import os
import subprocess
import threading
import time
from collections import deque
from datetime import datetime
from typing import Dict, List, Any

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from rcl_interfaces.msg import Log
from std_msgs.msg import String
from sensor_msgs.msg import Image, CompressedImage

from flask import Flask, render_template, jsonify, request, Response
from flask import send_from_directory
import queue
import numpy as np

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get template directory (works in both build and install)
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)

# ==================== Global State ====================

# Log storage (rqt_console-like)
MAX_LOGS = 1000
_logs_buffer = deque(maxlen=MAX_LOGS)
_log_stats = {
    'debug': 0,
    'info': 0,
    'warn': 0,
    'error': 0,
    'fatal': 0
}

# Node tracking
_nodes_cache = {}
_nodes_last_update = 0

# Topic tracking
_topics_cache = {}
_topics_hz_cache = {}
_frame_times = deque(maxlen=30)  # Camera frame timestamps for Hz calc

# Camera streaming
_camera_frame_buffer = queue.Queue(maxsize=2)
_camera_jpeg_buffer = queue.Queue(maxsize=2)  # Direct JPEG bytes from compressed topic
_camera_connected = False
_last_camera_frame_time = 0.0

# System status
_system_status = {
    'ros2_running': False,
    'daemon_running': False,
    'last_nodes_scan': 0,
    'last_topics_scan': 0,
}

# ==================== Node Control ====================
# Registry of managed nodes and their processes
_managed_nodes: Dict[str, Dict] = {}
_core_process = None

# Node definitions - available nodes that can be started/stopped
NODE_DEFINITIONS = {
    'obsbot_camera': {
        'name': 'OBSBOT Camera',
        'package': 'aimee_vision_obsbot',
        'executable': 'obsbot_node',
        'args': [],
        'category': 'vision',
        'icon': '📷'
    },
    'usb_camera': {
        'name': 'USB Camera',
        'package': 'usb_cam',
        'executable': 'usb_cam_node_exe',
        'args': [],
        'category': 'vision',
        'icon': '🎥'
    },
    'wake_word': {
        'name': 'Wake Word',
        'package': 'aimee_wake_word_ei',
        'executable': 'wake_word_node',
        'args': [],
        'category': 'audio',
        'icon': '🎯'
    },
    'voice_manager': {
        'name': 'Voice Manager',
        'package': 'aimee_voice_manager',
        'executable': 'voice_manager_node',
        'args': [],
        'category': 'audio',
        'icon': '🎤'
    },
    'intent_router': {
        'name': 'Intent Router',
        'package': 'aimee_intent_router',
        'executable': 'intent_router_node',
        'args': [],
        'category': 'ai',
        'icon': '🧠'
    },
    'skill_manager': {
        'name': 'Skill Manager',
        'package': 'aimee_skill_manager',
        'executable': 'skill_manager_node',
        'args': [],
        'category': 'skills',
        'icon': '🦾'
    },
    'tts': {
        'name': 'Text-to-Speech',
        'package': 'aimee_tts',
        'executable': 'tts_node',
        'args': [],
        'category': 'audio',
        'icon': '🔊'
    },
    'llm_server': {
        'name': 'LLM Server',
        'package': 'aimee_llm_server',
        'executable': 'llm_server_node',
        'args': [],
        'category': 'ai',
        'icon': '🧠'
    },
    'lerobot_bridge': {
        'name': 'LeRobot Bridge',
        'package': 'aimee_lerobot_bridge',
        'executable': 'lerobot_bridge_node',
        'args': [],
        'category': 'skills',
        'icon': '🤖'
    },
    'ugv02_controller': {
        'name': 'UGV02 Controller',
        'package': 'aimee_ugv02_controller',
        'executable': 'ugv02_controller_node',
        'args': [],
        'category': 'skills',
        'icon': '🚗'
    },
}

# ==================== Flask Routes ====================

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('index.html')


@app.route('/api/logs')
def get_logs():
    """Get recent logs (rqt_console style)."""
    level_filter = request.args.get('level', 'all')
    node_filter = request.args.get('node', 'all')
    search = request.args.get('search', '').lower()
    limit = int(request.args.get('limit', 100))
    
    filtered_logs = []
    for log in reversed(_logs_buffer):  # Newest first
        # Level filter
        if level_filter != 'all' and log['level'] != level_filter:
            continue
        # Node filter
        if node_filter != 'all' and node_filter not in log['node']:
            continue
        # Search filter
        if search and search not in log['msg'].lower():
            continue
        
        filtered_logs.append(log)
        if len(filtered_logs) >= limit:
            break
    
    return jsonify({
        'logs': filtered_logs,
        'total': len(_logs_buffer),
        'filtered': len(filtered_logs),
        'stats': _log_stats
    })


@app.route('/api/logs/clear', methods=['POST'])
def clear_logs():
    """Clear log buffer."""
    global _logs_buffer, _log_stats
    _logs_buffer.clear()
    _log_stats = {'debug': 0, 'info': 0, 'warn': 0, 'error': 0, 'fatal': 0}
    return jsonify({'success': True})


@app.route('/api/nodes')
def get_nodes():
    """Get running ROS2 nodes with status."""
    global _nodes_cache, _nodes_last_update
    
    # Refresh if older than 5 seconds
    if time.time() - _nodes_last_update > 5:
        _refresh_nodes()
    
    return jsonify({
        'nodes': list(_nodes_cache.values()),
        'count': len(_nodes_cache),
        'last_update': _nodes_last_update
    })


@app.route('/api/nodes/<path:node_name>')
def get_node_details(node_name):
    """Get detailed info about a specific node."""
    # Remove leading slash if present
    node_name = node_name.lstrip('/')
    
    try:
        # Get node info
        cmd = f'source /opt/ros/humble/setup.bash && ROS2_DISABLE_DAEMON=1 ros2 node info /{node_name}'
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=10,
            shell=True, executable='/bin/bash'
        )
        
        # Parse subscriptions and publications
        info = {'subscriptions': [], 'publishers': [], 'services': []}
        current_section = None
        
        for line in result.stdout.split('\n'):
            line = line.strip()
            if line.startswith('Subscribers:'):
                current_section = 'subscriptions'
            elif line.startswith('Publishers:'):
                current_section = 'publishers'
            elif line.startswith('Services:'):
                current_section = 'services'
            elif line.startswith('/') and current_section:
                # Parse topic name and type
                parts = line.split(':')
                if len(parts) >= 2:
                    name = parts[0].strip()
                    type_str = parts[1].strip()
                    info[current_section].append({
                        'name': name,
                        'type': type_str
                    })
        
        return jsonify({'success': True, 'node': node_name, **info})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/topics')
def get_topics():
    """Get ROS2 topics with metadata."""
    return jsonify({
        'topics': list(_topics_cache.values()),
        'count': len(_topics_cache)
    })


@app.route('/api/topics/<path:topic_name>/echo')
def echo_topic(topic_name):
    """Echo a single message from a topic."""
    topic_name = '/' + topic_name.lstrip('/')
    
    try:
        cmd = f'source /opt/ros/humble/setup.bash && timeout 2 ros2 topic echo --once {topic_name} 2>/dev/null || true'
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=3,
            shell=True, executable='/bin/bash'
        )
        
        # Parse the YAML-like output to JSON
        output = result.stdout.strip()
        if not output:
            return jsonify({'success': False, 'error': 'No data received'})
        
        # Simple YAML to dict conversion for basic types
        data = {}
        current_key = None
        for line in output.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                key = key.strip()
                val = val.strip()
                # Try to convert numbers
                try:
                    if '.' in val:
                        val = float(val)
                    else:
                        val = int(val)
                except:
                    pass
                data[key] = val
        
        return jsonify({'success': True, 'topic': topic_name, 'data': data, 'raw': output[:500]})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/system')
def get_system_status():
    """Get overall system status."""
    return jsonify({
        'ros2_running': _system_status['ros2_running'],
        'log_stats': _log_stats,
        'uptime': time.time() - _system_status.get('start_time', time.time()),
        'timestamp': datetime.now().isoformat()
    })


# ==================== Camera Streaming ====================

def generate_camera_stream():
    """Generate MJPEG stream for camera feed from compressed JPEG bytes."""
    last_frame = None
    last_frame_time = 0.0
    
    while True:
        try:
            # Get JPEG bytes directly from buffer
            jpeg_bytes = _camera_jpeg_buffer.get(timeout=2.0)
            last_frame = jpeg_bytes
            last_frame_time = time.time()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg_bytes + b'\r\n')
        except queue.Empty:
            # Reuse last frame if it's recent (< 3s)
            if last_frame is not None and (time.time() - last_frame_time) < 3.0:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + last_frame + b'\r\n')
            elif CV2_AVAILABLE:
                # No frame for a while, yield placeholder
                placeholder = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(placeholder, 'Camera Not Available', (120, 240), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                _, buffer = cv2.imencode('.jpg', placeholder)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        except Exception as e:
            logger.debug(f"Stream error: {e}")
            time.sleep(0.1)


@app.route('/camera/stream')
def camera_stream():
    """Camera video stream endpoint."""
    return Response(
        generate_camera_stream(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/api/camera/status')
def camera_status():
    """Get camera connection status."""
    global _last_camera_frame_time
    frame_recent = (time.time() - _last_camera_frame_time) < 5.0
    return jsonify({
        'connected': _camera_connected,
        'frame_available': frame_recent,
        'cv2_available': CV2_AVAILABLE,
        'last_frame_age': round(time.time() - _last_camera_frame_time, 1)
    })


@app.route('/api/camera/control', methods=['POST'])
def camera_control():
    """Control camera PTZ and tracking."""
    data = request.get_json() or {}
    command = data.get('command')
    
    try:
        if command == 'ptz':
            direction = data.get('direction')
            speed = data.get('speed', 50)
            
            # Map direction to ROS2 Twist command
            twist_cmd = {'linear': {'x': 0, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': 0}}
            if direction == 'up':
                twist_cmd['angular']['y'] = speed / 100.0
            elif direction == 'down':
                twist_cmd['angular']['y'] = -speed / 100.0
            elif direction == 'left':
                twist_cmd['angular']['z'] = speed / 100.0
            elif direction == 'right':
                twist_cmd['angular']['z'] = -speed / 100.0
            elif direction == 'zoom_in':
                twist_cmd['linear']['z'] = speed / 100.0
            elif direction == 'zoom_out':
                twist_cmd['linear']['z'] = -speed / 100.0
            
            # Publish via subprocess
            cmd = f"""source /opt/ros/humble/setup.bash && source /workspace/install/setup.bash && ros2 topic pub --once /camera/cmd_ptz geometry_msgs/msg/Twist '{{linear: {{x: {twist_cmd['linear']['x']}, y: {twist_cmd['linear']['y']}, z: {twist_cmd['linear']['z']}}}, angular: {{x: {twist_cmd['angular']['x']}, y: {twist_cmd['angular']['y']}, z: {twist_cmd['angular']['z']}}}}}'"""
            subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
            
            return jsonify({'success': True, 'command': command, 'direction': direction})
        
        elif command == 'tracking':
            mode = data.get('mode', 'normal')
            cmd = f"""source /opt/ros/humble/setup.bash && source /workspace/install/setup.bash && ros2 topic pub --once /camera/tracking aimee_msgs/msg/TrackingCommand '{{command: "start", mode: "{mode}"}}'"""
            subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
            return jsonify({'success': True, 'command': command, 'mode': mode})
        
        elif command == 'stop_tracking':
            cmd = """source /opt/ros/humble/setup.bash && source /workspace/install/setup.bash && ros2 topic pub --once /camera/tracking aimee_msgs/msg/TrackingCommand '{command: "stop"}'"""
            subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
            return jsonify({'success': True, 'command': command})
        
        else:
            return jsonify({'success': False, 'error': f'Unknown command: {command}'}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/nodes/refresh', methods=['POST'])
def refresh_nodes():
    """Force refresh node list."""
    _refresh_nodes()
    return jsonify({'success': True, 'count': len(_nodes_cache)})


# ==================== Node Control Endpoints ====================

@app.route('/api/nodes/definitions')
def get_node_definitions():
    """Get available node definitions."""
    return jsonify({
        'nodes': NODE_DEFINITIONS,
        'count': len(NODE_DEFINITIONS)
    })


@app.route('/api/nodes/managed')
def get_managed_nodes():
    """Get status of managed nodes."""
    global _managed_nodes
    
    # Clean up finished processes and build serializable response
    nodes_response = {}
    for node_id, info in list(_managed_nodes.items()):
        proc = info.get('process')
        if proc and proc.poll() is not None:
            info['status'] = 'stopped'
            info['exit_code'] = proc.returncode
        
        # Build response without Popen object (not JSON serializable)
        nodes_response[node_id] = {
            'node_id': info.get('node_id'),
            'name': info.get('name'),
            'status': info.get('status'),
            'pid': info.get('pid'),
            'started_at': info.get('started_at'),
            'stopped_at': info.get('stopped_at'),
            'exit_code': info.get('exit_code'),
            'package': info.get('package'),
            'executable': info.get('executable')
        }
    
    core_running = _core_process is not None and _core_process.poll() is None
    
    return jsonify({
        'nodes': nodes_response,
        'core_running': core_running
    })


@app.route('/api/nodes/start', methods=['POST'])
def start_node():
    """Start a managed node."""
    global _managed_nodes
    
    data = request.get_json() or {}
    node_id = data.get('node_id')
    
    if not node_id or node_id not in NODE_DEFINITIONS:
        return jsonify({'success': False, 'error': 'Invalid node_id'}), 400
    
    # Check if already running
    if node_id in _managed_nodes:
        proc = _managed_nodes[node_id].get('process')
        if proc and proc.poll() is None:
            return jsonify({'success': False, 'error': 'Node already running'}), 409
    
    node_def = NODE_DEFINITIONS[node_id]
    
    try:
        # Build command
        cmd_parts = [
            'source /opt/ros/humble/setup.bash',
            'source /workspace/install/setup.bash',
            f'ros2 run {node_def["package"]} {node_def["executable"]}'
        ]
        if node_def.get('args'):
            cmd_parts[-1] += ' ' + ' '.join(node_def['args'])
        
        cmd = ' && '.join(cmd_parts)
        
        # Start process
        proc = subprocess.Popen(
            cmd,
            shell=True,
            executable='/bin/bash',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True  # Allows clean process group termination
        )
        
        _managed_nodes[node_id] = {
            'node_id': node_id,
            'name': node_def['name'],
            'process': proc,
            'pid': proc.pid,
            'status': 'running',
            'started_at': datetime.now().isoformat(),
            'package': node_def['package'],
            'executable': node_def['executable']
        }
        
        logger.info(f"Started node {node_id} (PID: {proc.pid})")
        
        return jsonify({
            'success': True,
            'node_id': node_id,
            'pid': proc.pid,
            'status': 'running'
        })
        
    except Exception as e:
        logger.error(f"Failed to start node {node_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/nodes/stop', methods=['POST'])
def stop_node():
    """Stop a managed node."""
    global _managed_nodes
    
    data = request.get_json() or {}
    node_id = data.get('node_id')
    
    if not node_id or node_id not in _managed_nodes:
        return jsonify({'success': False, 'error': 'Node not found or not managed'}), 404
    
    node_info = _managed_nodes[node_id]
    proc = node_info.get('process')
    
    if not proc:
        return jsonify({'success': False, 'error': 'No process found'}), 500
    
    try:
        # Try graceful termination first
        import signal
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        
        # Wait for process to terminate
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # Force kill if not terminated
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            proc.wait(timeout=2)
        
        node_info['status'] = 'stopped'
        node_info['stopped_at'] = datetime.now().isoformat()
        
        logger.info(f"Stopped node {node_id} (PID was: {proc.pid})")
        
        return jsonify({
            'success': True,
            'node_id': node_id,
            'status': 'stopped'
        })
        
    except Exception as e:
        logger.error(f"Failed to stop node {node_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/core/start', methods=['POST'])
def start_core():
    """Start core ROS2 nodes (bringup)."""
    global _core_process
    
    if _core_process and _core_process.poll() is None:
        return jsonify({'success': False, 'error': 'Core already running'}), 409
    
    try:
        # Start core bringup
        cmd = 'source /opt/ros/humble/setup.bash && source /workspace/install/setup.bash && ros2 launch aimee_bringup core.launch.py'
        
        _core_process = subprocess.Popen(
            cmd,
            shell=True,
            executable='/bin/bash',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True
        )
        
        logger.info(f"Started core (PID: {_core_process.pid})")
        
        return jsonify({
            'success': True,
            'pid': _core_process.pid,
            'status': 'starting'
        })
        
    except Exception as e:
        logger.error(f"Failed to start core: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/core/stop', methods=['POST'])
def stop_core():
    """Stop core ROS2 nodes."""
    global _core_process
    
    if not _core_process:
        return jsonify({'success': False, 'error': 'Core not running'}), 404
    
    try:
        import signal
        os.killpg(os.getpgid(_core_process.pid), signal.SIGTERM)
        
        try:
            _core_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(os.getpgid(_core_process.pid), signal.SIGKILL)
            _core_process.wait(timeout=2)
        
        logger.info("Stopped core")
        
        return jsonify({
            'success': True,
            'status': 'stopped'
        })
        
    except Exception as e:
        logger.error(f"Failed to stop core: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/core/status')
def core_status():
    """Get core status."""
    global _core_process
    
    is_running = _core_process is not None and _core_process.poll() is None
    
    return jsonify({
        'running': is_running,
        'pid': _core_process.pid if is_running else None
    })


# ==================== Helper Functions ====================

def _refresh_nodes(native_api=None):
    """Refresh the nodes cache using native ROS2 API when available."""
    global _nodes_cache, _nodes_last_update
    
    try:
        if native_api is not None:
            nodes = {}
            for name, namespace in native_api:
                full_name = (namespace.rstrip('/') + '/' + name) if namespace != '/' else '/' + name
                if not full_name.startswith('/'):
                    full_name = '/' + full_name
                
                # Determine node type/category
                category = 'other'
                if 'wake_word' in full_name.lower():
                    category = 'audio'
                elif 'voice' in full_name.lower() or 'stt' in full_name.lower():
                    category = 'audio'
                elif 'tts' in full_name.lower():
                    category = 'audio'
                elif 'intent' in full_name.lower():
                    category = 'ai'
                elif 'llm' in full_name.lower():
                    category = 'ai'
                elif 'skill' in full_name.lower():
                    category = 'skills'
                elif 'camera' in full_name.lower() or 'vision' in full_name.lower():
                    category = 'vision'
                elif 'dashboard' in full_name.lower() or 'monitor' in full_name.lower():
                    category = 'tools'
                
                nodes[full_name] = {
                    'name': full_name,
                    'category': category,
                    'status': 'running',
                    'last_seen': time.time()
                }
            
            _nodes_cache = nodes
            _nodes_last_update = time.time()
            _system_status['ros2_running'] = True
        else:
            _system_status['ros2_running'] = False
    except Exception as e:
        logger.warning(f"Failed to refresh nodes: {e}")
        _system_status['ros2_running'] = False


# ==================== ROS2 Node ====================

class MonitorNode(Node):
    """
    ROS2 Node that captures logs and provides monitoring data.
    """
    
    def __init__(self):
        super().__init__('ros2_monitor')
        
        # Subscribe to /rosout for log messages
        self._log_sub = self.create_subscription(
            Log,
            '/rosout',
            self._on_log_message,
            QoSProfile(
                reliability=ReliabilityPolicy.BEST_EFFORT,
                history=HistoryPolicy.KEEP_LAST,
                depth=100
            )
        )
        
        # Subscribe to compressed camera images (much lower CPU than raw)
        self._image_sub = self.create_subscription(
            CompressedImage,
            '/camera/image_raw/compressed',
            self._on_camera_image,
            QoSProfile(
                reliability=ReliabilityPolicy.BEST_EFFORT,
                history=HistoryPolicy.KEEP_LAST,
                depth=1
            )
        )
        self._last_frame_time = 0
        
        # Timers for periodic updates (reduced frequency to avoid CPU starvation)
        self._nodes_timer = self.create_timer(10.0, self._update_nodes)
        self._topics_timer = self.create_timer(30.0, self._update_topic_hz)
        self._camera_timer = self.create_timer(2.0, self._check_camera_status)
        
        self.get_logger().info("ROS2 Monitor Node started")
    
    def _on_camera_image(self, msg: CompressedImage):
        """Handle incoming compressed camera image (JPEG bytes)."""
        global _camera_connected, _last_camera_frame_time
        now = time.time()
        _camera_connected = True
        self._last_frame_time = now
        _last_camera_frame_time = now
        
        # Record timestamp for Hz calculation
        _frame_times.append(now)
        
        # Throttle frame processing to ~10 fps for dashboard (saves CPU)
        if hasattr(self, '_last_queue_time') and (now - self._last_queue_time) < 0.1:
            return
        
        try:
            # Direct JPEG bytes - zero conversion overhead
            jpeg_bytes = bytes(msg.data)
            try:
                _camera_jpeg_buffer.put_nowait(jpeg_bytes)
                self._last_queue_time = now
            except queue.Full:
                try:
                    _camera_jpeg_buffer.get_nowait()
                    _camera_jpeg_buffer.put_nowait(jpeg_bytes)
                    self._last_queue_time = now
                except queue.Empty:
                    pass
        except Exception as e:
            logger.debug(f"Frame buffer error: {e}")
    
    def _check_camera_status(self):
        """Check if camera is still connected."""
        global _camera_connected, _last_camera_frame_time
        if time.time() - self._last_frame_time > 5.0:
            _camera_connected = False
    
    def _on_log_message(self, msg: Log):
        """Handle incoming log message."""
        global _log_stats
        
        # Map level to string
        level_map = {
            Log.DEBUG: 'debug',
            Log.INFO: 'info',
            Log.WARN: 'warn',
            Log.ERROR: 'error',
            Log.FATAL: 'fatal'
        }
        level_str = level_map.get(msg.level, 'unknown')
        
        # Update stats
        if level_str in _log_stats:
            _log_stats[level_str] += 1
        
        # Create log entry
        log_entry = {
            'timestamp': datetime.fromtimestamp(msg.stamp.sec + msg.stamp.nanosec * 1e-9).isoformat(),
            'level': level_str,
            'node': msg.name,
            'msg': msg.msg,
            'file': msg.file,
            'line': msg.line,
            'function': msg.function
        }
        
        _logs_buffer.append(log_entry)
    
    def _update_nodes(self):
        """Periodic node list update using native ROS2 API."""
        try:
            _refresh_nodes(self.get_node_names_and_namespaces())
        except Exception as e:
            logger.warning(f"Node update error: {e}")
    
    def _update_topic_hz(self):
        """Update topic frequency info from frame timestamps (no subprocess)."""
        global _topics_hz_cache
        
        try:
            # Compute camera topic Hz from frame arrival times
            now = time.time()
            recent_frames = [t for t in _frame_times if now - t < 2.0]
            if len(recent_frames) >= 2:
                duration = recent_frames[-1] - recent_frames[0]
                hz = (len(recent_frames) - 1) / duration if duration > 0 else 0
                _topics_hz_cache['/camera/image_raw'] = {
                    'hz': round(hz, 2),
                    'bandwidth': '0 B',
                    'last_update': now
                }
            
            # Refresh topic list while we're here
            self._refresh_topics()
        except Exception as e:
            logger.debug(f"Hz update error: {e}")

    def _refresh_topics(self):
        """Refresh topic list using native ROS2 API (no subprocess)."""
        global _topics_cache
        try:
            topics = []
            for topic_name, topic_types in self.get_topic_names_and_types():
                msg_type = topic_types[0] if topic_types else 'unknown'
                hz_info = _topics_hz_cache.get(topic_name, {})
                topics.append({
                    'name': topic_name,
                    'type': msg_type,
                    'hz': hz_info.get('hz', 0),
                    'bandwidth': hz_info.get('bandwidth', '0 B'),
                    'last_update': hz_info.get('last_update', 0)
                })
            _topics_cache = {t['name']: t for t in topics}
        except Exception as e:
            logger.warning(f"Failed to refresh topics: {e}")


# ==================== Flask Thread ====================

def run_flask(host='0.0.0.0', port=8081):
    """Run Flask server in background thread."""
    # Disable Flask logging
    import logging as flask_logging
    flask_logging.getLogger('werkzeug').setLevel(flask_logging.ERROR)
    
    app.run(host=host, port=port, debug=False, threaded=True)


# ==================== Main ====================

def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)
    
    # Set start time
    _system_status['start_time'] = time.time()
    
    # Start Flask in background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Create ROS2 node
    node = MonitorNode()
    
    print("\n" + "="*60)
    print("🔍 AIMEE ROS2 Monitor Dashboard")
    print("="*60)
    print(f"\n📊 Dashboard URL: http://localhost:8081")
    print("\n💡 Features:")
    print("   • Real-time log viewer (like rqt_console)")
    print("   • Visual node status widgets")
    print("   • Live topic monitoring")
    print("   • Auto-refresh every 5 seconds")
    print("\n" + "="*60 + "\n")
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

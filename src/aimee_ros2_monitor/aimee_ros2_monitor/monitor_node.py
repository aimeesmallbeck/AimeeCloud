#!/usr/bin/env python3
"""
AIMEE ROS2 Monitor - Lightweight Dashboard

A simple web-based dashboard for monitoring ROS2:
- rqt_console-like log viewer (captures /rosout)
- Node status widgets (visual cards for each node)
- Topic monitoring with live data flow

Usage:
    ros2 run aimee_ros2_monitor monitor_node
    
Then open browser to: http://localhost:8081
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
from geometry_msgs.msg import Twist

try:
    from aimee_msgs.msg import TrackingCommand
    AIMEE_MSGS_AVAILABLE = True
except ImportError:
    AIMEE_MSGS_AVAILABLE = False

try:
    from rosidl_runtime_py.utilities import get_message
    from rosidl_runtime_py import message_to_ordereddict
    ROSIDL_PY_AVAILABLE = True
except ImportError:
    ROSIDL_PY_AVAILABLE = False

from flask import Flask, render_template, jsonify, request, Response, make_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get template directory from package share (works in both build and install)
try:
    from ament_index_python.packages import get_package_share_directory
    template_dir = os.path.join(get_package_share_directory('aimee_ros2_monitor'), 'templates')
except Exception:
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)

# Global reference to ROS2 node (for native pub from Flask threads)
_ros_node = None

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
        'ros_name': '/obsbot_camera',
        'package': 'aimee_vision_obsbot',
        'executable': 'obsbot_node',
        'args': [],
        'category': 'vision',
        'icon': '📷'
    },
    'usb_camera': {
        'name': 'USB Camera',
        'ros_name': '/usb_camera',
        'package': 'usb_cam',
        'executable': 'usb_cam_node_exe',
        'args': [],
        'category': 'vision',
        'icon': '🎥'
    },
    'wake_word': {
        'name': 'Wake Word',
        'ros_name': '/wake_word_ei',
        'package': 'aimee_wake_word_ei',
        'executable': 'wake_word_node',
        'args': [],
        'category': 'audio',
        'icon': '🎯'
    },
    'voice_manager': {
        'name': 'Voice Manager',
        'ros_name': '/voice_manager',
        'package': 'aimee_voice_manager',
        'executable': 'voice_manager_node',
        'args': [],
        'category': 'audio',
        'icon': '🎤'
    },
    'intent_router': {
        'name': 'Intent Router',
        'ros_name': '/intent_router',
        'package': 'aimee_intent_router',
        'executable': 'intent_router_node',
        'args': [],
        'category': 'ai',
        'icon': '🧠'
    },
    'skill_manager': {
        'name': 'Skill Manager',
        'ros_name': '/skill_manager',
        'package': 'aimee_skill_manager',
        'executable': 'skill_manager_node',
        'args': [],
        'category': 'skills',
        'icon': '🦾'
    },
    'tts': {
        'name': 'Text-to-Speech',
        'ros_name': '/tts',
        'package': 'aimee_tts',
        'executable': 'tts_node',
        'args': [],
        'category': 'audio',
        'icon': '🔊'
    },
    'llm_server': {
        'name': 'LLM Server',
        'ros_name': '/llm_server',
        'package': 'aimee_llm_server',
        'executable': 'llm_server_node',
        'args': [],
        'category': 'ai',
        'icon': '🧠'
    },
    'lerobot_bridge': {
        'name': 'LeRobot Bridge',
        'ros_name': '/lerobot_bridge',
        'package': 'aimee_lerobot_bridge',
        'executable': 'lerobot_bridge_node',
        'args': [],
        'category': 'skills',
        'icon': '🤖'
    },
    'ugv02_controller': {
        'name': 'UGV02 Controller',
        'ros_name': '/ugv02_controller',
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
    resp = make_response(render_template('index.html'))
    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp


@app.route('/api/logs')
def get_logs():
    """Get recent logs (rqt_console style)."""
    level_filter = request.args.get('level', 'all')
    node_filter = request.args.get('node', 'all')
    search = request.args.get('search', '').lower()
    limit = int(request.args.get('limit', 100))
    
    filtered_logs = []
    for log in reversed(_logs_buffer):  # Newest first
        if level_filter != 'all' and log['level'] != level_filter:
            continue
        if node_filter != 'all' and node_filter not in log['node']:
            continue
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
    
    if time.time() - _nodes_last_update > 5:
        _refresh_nodes()
    
    return jsonify({
        'nodes': list(_nodes_cache.values()),
        'count': len(_nodes_cache),
        'last_update': _nodes_last_update
    })


@app.route('/api/nodes/<path:node_name>')
def get_node_details(node_name):
    """Get detailed info about a specific node using native ROS2 graph API."""
    node_name = '/' + node_name.lstrip('/')
    
    if _ros_node is None:
        return jsonify({'success': False, 'error': 'ROS2 node not available'}), 503
    
    try:
        parts = node_name.split('/')
        base_name = parts[-1]
        namespace = '/'.join(parts[:-1]) or '/'
        
        publishers = _ros_node.get_publisher_names_and_types_by_node(base_name, namespace)
        subscribers = _ros_node.get_subscriber_names_and_types_by_node(base_name, namespace)
        services = _ros_node.get_service_names_and_types_by_node(base_name, namespace)
        
        return jsonify({
            'success': True,
            'node': node_name,
            'publishers': [{'name': name, 'type': types[0] if types else 'unknown'} for name, types in publishers],
            'subscriptions': [{'name': name, 'type': types[0] if types else 'unknown'} for name, types in subscribers],
            'services': [{'name': name, 'type': types[0] if types else 'unknown'} for name, types in services],
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/topics/<path:topic_name>/subscribe', methods=['POST'])
def topic_subscribe(topic_name):
    """Start a native echo subscription for a topic."""
    topic_name = '/' + topic_name.lstrip('/')
    if _ros_node is None:
        return jsonify({'success': False, 'error': 'ROS2 node not available'}), 503
    topic_info = _topics_cache.get(topic_name)
    if not topic_info:
        return jsonify({'success': False, 'error': f'Topic {topic_name} not found'}), 404
    msg_type = topic_info.get('type', 'unknown')
    if msg_type == 'unknown' or not ROSIDL_PY_AVAILABLE:
        return jsonify({'success': False, 'error': 'Unknown message type or rosidl_runtime_py unavailable'}), 400
    if msg_type in MonitorNode._ECHO_SKIP_TYPES:
        return jsonify({'success': False, 'error': f'Topic type {msg_type} is too large for live inspection'}), 400
    ok = _ros_node.ensure_echo_subscription(topic_name, msg_type)
    if ok:
        return jsonify({'success': True, 'topic': topic_name, 'type': msg_type})
    return jsonify({'success': False, 'error': 'Failed to create subscription'}), 500


@app.route('/api/topics/<path:topic_name>/latest')
def topic_latest(topic_name):
    """Get the latest cached message for a topic."""
    topic_name = '/' + topic_name.lstrip('/')
    if _ros_node is None:
        return jsonify({'success': False, 'error': 'ROS2 node not available'}), 503
    latest = _ros_node.get_echo_latest(topic_name)
    if latest is None:
        return jsonify({'success': True, 'topic': topic_name, 'waiting': True, 'data': None})
    return jsonify({'success': True, 'topic': topic_name, 'waiting': False, 'data': latest['data'], 'received_at': latest['timestamp']})


@app.route('/api/topics/<path:topic_name>/unsubscribe', methods=['POST'])
def topic_unsubscribe(topic_name):
    """Stop the echo subscription for a topic."""
    topic_name = '/' + topic_name.lstrip('/')
    if _ros_node is not None:
        _ros_node.destroy_echo_subscription(topic_name)
    return jsonify({'success': True, 'topic': topic_name})


@app.route('/api/topics')
def get_topics():
    """Get ROS2 topics with metadata."""
    return jsonify({
        'topics': list(_topics_cache.values()),
        'count': len(_topics_cache)
    })


@app.route('/api/system')
def get_system_status():
    """Get overall system status."""
    return jsonify({
        'ros2_running': _system_status['ros2_running'],
        'log_stats': _log_stats,
        'uptime': time.time() - _system_status.get('start_time', time.time()),
        'timestamp': datetime.now().isoformat()
    })


# ==================== Camera Control ====================

@app.route('/api/camera/control', methods=['POST'])
def camera_control():
    """Control camera PTZ and tracking."""
    data = request.get_json() or {}
    command = data.get('command')
    
    try:
        if command == 'ptz':
            direction = data.get('direction')
            speed = data.get('speed', 50)
            
            twist = Twist()
            if direction == 'up':
                twist.angular.y = speed / 100.0
            elif direction == 'down':
                twist.angular.y = -speed / 100.0
            elif direction == 'left':
                twist.angular.z = speed / 100.0
            elif direction == 'right':
                twist.angular.z = -speed / 100.0
            elif direction == 'zoom_in':
                twist.linear.z = speed / 100.0
            elif direction == 'zoom_out':
                twist.linear.z = -speed / 100.0
            elif direction == 'stop':
                pass
            
            if _ros_node is not None:
                _ros_node._ptz_pub.publish(twist)
            else:
                return jsonify({'success': False, 'error': 'ROS2 node not ready'}), 503
            
            return jsonify({'success': True, 'command': command, 'direction': direction})
        
        elif command == 'stop':
            if _ros_node is None:
                return jsonify({'success': False, 'error': 'ROS2 node not ready'}), 503
            _ros_node._ptz_pub.publish(Twist())
            return jsonify({'success': True, 'command': command})
        
        elif command == 'tracking':
            if not AIMEE_MSGS_AVAILABLE or _ros_node is None:
                return jsonify({'success': False, 'error': 'Tracking command not available'}), 503
            
            mode = data.get('mode', 'normal')
            cmd_msg = TrackingCommand()
            cmd_msg.command = 'start'
            cmd_msg.mode = mode
            _ros_node._tracking_pub.publish(cmd_msg)
            return jsonify({'success': True, 'command': command, 'mode': mode})
        
        elif command == 'stop_tracking':
            if not AIMEE_MSGS_AVAILABLE or _ros_node is None:
                return jsonify({'success': False, 'error': 'Tracking command not available'}), 503
            
            cmd_msg = TrackingCommand()
            cmd_msg.command = 'stop'
            _ros_node._tracking_pub.publish(cmd_msg)
            return jsonify({'success': True, 'command': command})
        
        else:
            return jsonify({'success': False, 'error': f'Unknown command: {command}'}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/tts/speak', methods=['POST'])
def tts_speak():
    """Publish a TTS message for testing."""
    data = request.get_json() or {}
    text = data.get('text', '')
    if not text:
        return jsonify({'success': False, 'error': 'No text provided'}), 400
    if _ros_node is None:
        return jsonify({'success': False, 'error': 'ROS2 node not ready'}), 503
    try:
        msg = String()
        msg.data = text
        _ros_node._tts_pub.publish(msg)
        return jsonify({'success': True, 'text': text})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


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
    """Get status of managed nodes + actual ROS2 graph state."""
    global _managed_nodes
    
    # Clean up finished processes
    nodes_response = {}
    for node_id, info in list(_managed_nodes.items()):
        proc = info.get('process')
        if proc and proc.poll() is not None:
            info['status'] = 'stopped'
            info['exit_code'] = proc.returncode
        
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
    
    # Determine which nodes are actually running in ROS2 graph
    ros_running = {}
    for node_id, node_def in NODE_DEFINITIONS.items():
        ros_name = node_def.get('ros_name', '')
        if ros_name and ros_name in _nodes_cache:
            ros_running[node_id] = True
    
    core_running = _core_process is not None and _core_process.poll() is None
    
    return jsonify({
        'nodes': nodes_response,
        'core_running': core_running,
        'ros_running': ros_running
    })


@app.route('/api/nodes/start', methods=['POST'])
def start_node():
    """Start a managed node."""
    global _managed_nodes
    
    data = request.get_json() or {}
    node_id = data.get('node_id')
    
    if not node_id or node_id not in NODE_DEFINITIONS:
        return jsonify({'success': False, 'error': 'Invalid node_id'}), 400
    
    # Check if already running in our managed set
    if node_id in _managed_nodes:
        proc = _managed_nodes[node_id].get('process')
        if proc and proc.poll() is None:
            return jsonify({'success': False, 'error': 'Node already running'}), 409
    
    node_def = NODE_DEFINITIONS[node_id]
    
    try:
        cmd_parts = [
            'source /opt/ros/humble/setup.bash',
            'source /workspace/install/setup.bash',
            f'ros2 run {node_def["package"]} {node_def["executable"]}'
        ]
        if node_def.get('args'):
            cmd_parts[-1] += ' ' + ' '.join(node_def['args'])
        
        cmd = ' && '.join(cmd_parts)
        
        proc = subprocess.Popen(
            cmd,
            shell=True,
            executable='/bin/bash',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True
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
    """Stop a node (managed or core-launched)."""
    global _managed_nodes
    
    data = request.get_json() or {}
    node_id = data.get('node_id')
    
    if not node_id or node_id not in NODE_DEFINITIONS:
        return jsonify({'success': False, 'error': 'Invalid node_id'}), 400
    
    node_def = NODE_DEFINITIONS[node_id]
    proc = None
    
    # If we have it in managed nodes, use that process
    if node_id in _managed_nodes:
        proc = _managed_nodes[node_id].get('process')
    
    try:
        import signal
        
        if proc:
            # Managed process - kill by process group
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                proc.wait(timeout=5)
            except (subprocess.TimeoutExpired, ProcessLookupError):
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                    proc.wait(timeout=2)
                except Exception:
                    pass
            
            _managed_nodes[node_id]['status'] = 'stopped'
            _managed_nodes[node_id]['stopped_at'] = datetime.now().isoformat()
        else:
            # Core-launched or orphaned process - find by executable name
            executable = node_def['executable']
            # Try graceful pkill first
            subprocess.run(
                ['pkill', '-f', executable],
                capture_output=True, timeout=5
            )
            time.sleep(1)
            # Check if still running, force kill if so
            check = subprocess.run(
                ['pgrep', '-f', executable],
                capture_output=True, timeout=2
            )
            if check.returncode == 0:
                subprocess.run(
                    ['pkill', '-9', '-f', executable],
                    capture_output=True, timeout=5
                )
        
        logger.info(f"Stopped node {node_id}")
        
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
        
        # Publishers for camera control and TTS testing
        self._ptz_pub = self.create_publisher(Twist, '/camera/cmd_ptz', 10)
        self._tts_pub = self.create_publisher(String, '/tts/speak', 10)
        if AIMEE_MSGS_AVAILABLE:
            self._tracking_pub = self.create_publisher(TrackingCommand, '/camera/tracking', 10)
        
        # Timers for periodic updates
        self._nodes_timer = self.create_timer(10.0, self._update_nodes)
        self._topics_timer = self.create_timer(30.0, self._refresh_topics)
        
        # Immediate initial refresh
        self._initial_refresh_timer = self.create_timer(1.0, self._initial_refresh)
        
        self.get_logger().info("ROS2 Monitor Node started")
    
    def _initial_refresh(self):
        """One-shot initial refresh after node is fully initialized."""
        self._update_nodes()
        self._refresh_topics()
        self.destroy_timer(self._initial_refresh_timer)
    
    def _on_log_message(self, msg: Log):
        """Handle incoming log message."""
        global _log_stats
        
        level_map = {
            10: 'debug',
            20: 'info',
            30: 'warn',
            40: 'error',
            50: 'fatal'
        }
        level_str = level_map.get(msg.level, 'unknown')
        
        if level_str in _log_stats:
            _log_stats[level_str] += 1
        
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
    
    # Message types to skip for auto echo (large/binary data)
    _ECHO_SKIP_TYPES = {
        'sensor_msgs/msg/Image',
        'sensor_msgs/msg/CompressedImage',
        'sensor_msgs/msg/PointCloud2',
        'sensor_msgs/msg/LaserScan',
        'sensor_msgs/msg/PointCloud',
        'nav_msgs/msg/OccupancyGrid',
        'visualization_msgs/msg/MarkerArray',
        'theora_image_transport/msg/Packet',
    }
    
    def _refresh_topics(self):
        """Refresh topic list using native ROS2 API and auto-subscribe to small topics."""
        global _topics_cache
        try:
            topics = []
            for topic_name, topic_types in self.get_topic_names_and_types():
                msg_type = topic_types[0] if topic_types else 'unknown'
                topics.append({
                    'name': topic_name,
                    'type': msg_type,
                    'hz': 0,
                    'bandwidth': '0 B',
                    'last_update': 0
                })
                # Auto-subscribe to lightweight topics for live inspection
                if (ROSIDL_PY_AVAILABLE and
                        msg_type not in self._ECHO_SKIP_TYPES and
                        msg_type != 'unknown'):
                    self.ensure_echo_subscription(topic_name, msg_type)
            _topics_cache = {t['name']: t for t in topics}
        except Exception as e:
            logger.warning(f"Failed to refresh topics: {e}")
    
    # ==================== Topic Echo Subscriptions ====================
    ECHO_TIMEOUT = 60.0
    
    def ensure_echo_subscription(self, topic_name: str, msg_type_str: str) -> bool:
        """Create a persistent subscription to cache the latest message."""
        if not ROSIDL_PY_AVAILABLE:
            return False
        with getattr(self, '_echo_lock', threading.Lock()):
            if not hasattr(self, '_echo_subs'):
                self._echo_subs = {}
                self._echo_cache = {}
                self._echo_last_access = {}
                self._echo_lock = threading.Lock()
            if topic_name in self._echo_subs:
                self._echo_last_access[topic_name] = time.time()
                return True
        try:
            msg_cls = get_message(msg_type_str)
            sub = self.create_subscription(
                msg_cls, topic_name,
                lambda msg, tn=topic_name: self._on_echo_message(tn, msg),
                QoSProfile(
                    reliability=ReliabilityPolicy.BEST_EFFORT,
                    history=HistoryPolicy.KEEP_LAST,
                    depth=1
                )
            )
            with self._echo_lock:
                self._echo_subs[topic_name] = sub
                self._echo_cache[topic_name] = None
                self._echo_last_access[topic_name] = time.time()
            # Start cleanup timer if not running
            if not hasattr(self, '_echo_cleanup_timer') or self._echo_cleanup_timer is None:
                self._echo_cleanup_timer = self.create_timer(10.0, self._cleanup_echo_subs)
            self.get_logger().info(f"Echo subscription created for {topic_name}")
            return True
        except Exception as e:
            logger.warning(f"Failed to create echo sub for {topic_name}: {e}")
            return False
    
    def destroy_echo_subscription(self, topic_name: str):
        """Destroy a persistent echo subscription."""
        with getattr(self, '_echo_lock', threading.Lock()):
            if not hasattr(self, '_echo_subs'):
                return
            sub = self._echo_subs.pop(topic_name, None)
            self._echo_cache.pop(topic_name, None)
            self._echo_last_access.pop(topic_name, None)
        if sub:
            try:
                self.destroy_subscription(sub)
            except Exception as e:
                logger.warning(f"Failed to destroy echo sub for {topic_name}: {e}")
    
    def _cleanup_echo_subs(self):
        """Remove echo subscriptions idle for too long."""
        now = time.time()
        stale = []
        with getattr(self, '_echo_lock', threading.Lock()):
            if not hasattr(self, '_echo_last_access'):
                return
            for topic_name, last_access in list(self._echo_last_access.items()):
                if now - last_access > self.ECHO_TIMEOUT:
                    stale.append(topic_name)
        for topic_name in stale:
            self.destroy_echo_subscription(topic_name)
    
    def _on_echo_message(self, topic_name: str, msg):
        """Cache an incoming echoed message."""
        self.get_logger().debug(f"Echo received on {topic_name}")
        try:
            data = message_to_ordereddict(msg)
        except Exception as e:
            data = {'_raw': str(msg), '_error': str(e)}
        with getattr(self, '_echo_lock', threading.Lock()):
            if not hasattr(self, '_echo_cache'):
                self._echo_cache = {}
                self._echo_last_access = {}
            self._echo_cache[topic_name] = {
                'data': data,
                'timestamp': time.time(),
                'type': type(msg).__module__ + '/' + type(msg).__name__
            }
            self._echo_last_access[topic_name] = time.time()
    
    def get_echo_latest(self, topic_name: str):
        """Return the latest cached message dict or None."""
        with getattr(self, '_echo_lock', threading.Lock()):
            if not hasattr(self, '_echo_cache'):
                return None
            if topic_name in self._echo_last_access:
                self._echo_last_access[topic_name] = time.time()
            cache = self._echo_cache.get(topic_name)
            if cache is None:
                return None
            return dict(cache)

# ==================== Flask Thread ====================

def run_flask(host='0.0.0.0', port=8081):
    """Run Flask server in background thread."""
    import logging as flask_logging
    flask_logging.getLogger('werkzeug').setLevel(flask_logging.ERROR)
    
    app.run(host=host, port=port, debug=False, threaded=True)


# ==================== Main ====================

def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)
    
    _system_status['start_time'] = time.time()
    
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    global _ros_node
    node = MonitorNode()
    _ros_node = node
    
    print("\n" + "="*60)
    print("🔍 AIMEE ROS2 Monitor Dashboard")
    print("="*60)
    print(f"\n📊 Dashboard URL: http://localhost:8081")
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

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

from flask import Flask, render_template, jsonify, request
from flask import send_from_directory

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

# System status
_system_status = {
    'ros2_running': False,
    'daemon_running': False,
    'last_nodes_scan': 0,
    'last_topics_scan': 0,
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
        cmd = f'source /opt/ros/humble/setup.bash && ros2 node info /{node_name}'
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
    global _topics_cache
    
    try:
        # Get topic list with types
        cmd = 'source /opt/ros/humble/setup.bash && ros2 topic list -t'
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=5,
            shell=True, executable='/bin/bash'
        )
        
        topics = []
        for line in result.stdout.strip().split('\n'):
            if not line or '[' not in line:
                continue
            # Parse "topic_name [type]"
            parts = line.split('[')
            name = parts[0].strip()
            msg_type = parts[1].rstrip(']').strip()
            
            # Get cached or new hz info
            hz_info = _topics_hz_cache.get(name, {})
            
            topics.append({
                'name': name,
                'type': msg_type,
                'hz': hz_info.get('hz', 0),
                'bandwidth': hz_info.get('bandwidth', '0 B'),
                'last_update': hz_info.get('last_update', 0)
            })
        
        _topics_cache = {t['name']: t for t in topics}
        return jsonify({'topics': topics, 'count': len(topics)})
    except Exception as e:
        return jsonify({'topics': [], 'error': str(e)})


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


@app.route('/api/nodes/refresh', methods=['POST'])
def refresh_nodes():
    """Force refresh node list."""
    _refresh_nodes()
    return jsonify({'success': True, 'count': len(_nodes_cache)})


# ==================== Helper Functions ====================

def _refresh_nodes():
    """Refresh the nodes cache."""
    global _nodes_cache, _nodes_last_update
    
    try:
        cmd = 'source /opt/ros/humble/setup.bash && ros2 node list'
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=5,
            shell=True, executable='/bin/bash'
        )
        
        if result.returncode == 0:
            nodes = {}
            for line in result.stdout.strip().split('\n'):
                name = line.strip()
                if name:
                    # Determine node type/category
                    category = 'other'
                    if 'wake_word' in name.lower():
                        category = 'audio'
                    elif 'voice' in name.lower() or 'stt' in name.lower():
                        category = 'audio'
                    elif 'tts' in name.lower():
                        category = 'audio'
                    elif 'intent' in name.lower():
                        category = 'ai'
                    elif 'llm' in name.lower():
                        category = 'ai'
                    elif 'skill' in name.lower():
                        category = 'skills'
                    elif 'camera' in name.lower() or 'vision' in name.lower():
                        category = 'vision'
                    elif 'dashboard' in name.lower() or 'monitor' in name.lower():
                        category = 'tools'
                    
                    nodes[name] = {
                        'name': name,
                        'category': category,
                        'status': 'running',
                        'last_seen': time.time()
                    }
            
            _nodes_cache = nodes
            _nodes_last_update = time.time()
            _system_status['ros2_running'] = True
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
        
        # Timers for periodic updates
        self._nodes_timer = self.create_timer(5.0, self._update_nodes)
        self._topics_timer = self.create_timer(10.0, self._update_topic_hz)
        
        self.get_logger().info("ROS2 Monitor Node started")
    
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
        """Periodic node list update."""
        _refresh_nodes()
    
    def _update_topic_hz(self):
        """Update topic frequency info."""
        try:
            # Get hz info for a few key topics
            key_topics = list(_topics_cache.keys())[:10]  # Limit to avoid overload
            
            for topic in key_topics:
                cmd = f'source /opt/ros/humble/setup.bash && timeout 2 ros2 topic hz {topic} 2>&1 | tail -5 || true'
                result = subprocess.run(
                    cmd, capture_output=True, text=True, timeout=3,
                    shell=True, executable='/bin/bash'
                )
                
                # Parse average rate
                for line in result.stdout.split('\n'):
                    if 'average rate' in line:
                        try:
                            hz = float(line.split(':')[1].strip())
                            _topics_hz_cache[topic] = {
                                'hz': round(hz, 2),
                                'last_update': time.time()
                            }
                        except:
                            pass
                    elif 'bandwidth' in line:
                        try:
                            bw = line.split(':')[1].strip()
                            if topic in _topics_hz_cache:
                                _topics_hz_cache[topic]['bandwidth'] = bw
                        except:
                            pass
        except Exception as e:
            pass  # Silent fail for hz monitoring


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

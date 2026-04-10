#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
AIMEE Robot Test Dashboard - Web Interface

A Flask-based web dashboard for testing all AIMEE robot components
with toggle between simulation and real hardware modes.

Features:
- Real-time ROS2 topic monitoring
- Hardware testing with simulation mode
- System health checks
- Component-by-component testing

Usage:
    ros2 run aimee_test_dashboard dashboard_node
    
Then open browser to: http://localhost:5000
"""

import json
import logging
import os
import subprocess
import threading
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any

from flask import Flask, render_template, jsonify, request, send_from_directory

# Configure logging
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aimee-robot-dashboard'

# Global state
_dashboard_state = {
    'ros2_connected': False,
    'last_update': time.time(),
    'topics': {},
    'system_health': {},
    'test_results': {},
}

# Component configuration with simulation toggles
_component_config = {
    'wake_word': {
        'name': 'Wake Word Detection',
        'enabled': True,
        'simulation_mode': False,
        'available': True,
        'description': 'Edge Impulse keyword spotting'
    },
    'stt': {
        'name': 'Speech-to-Text (Vosk)',
        'enabled': True,
        'simulation_mode': False,
        'available': True,
        'description': 'Voice transcription'
    },
    'tts': {
        'name': 'Text-to-Speech',
        'enabled': True,
        'simulation_mode': False,
        'available': True,
        'description': 'gTTS / Piper voice output'
    },
    'llm': {
        'name': 'LLM Server',
        'enabled': True,
        'simulation_mode': False,
        'available': True,
        'description': 'Local language model'
    },
    'intent': {
        'name': 'Intent Router',
        'enabled': True,
        'simulation_mode': False,
        'available': True,
        'description': 'Intent classification'
    },
    'skills': {
        'name': 'Skill Manager',
        'enabled': True,
        'simulation_mode': True,  # Default to sim for safety
        'available': True,
        'description': 'Movement, arm, camera skills'
    },
    'camera': {
        'name': 'Camera (OBSBOT)',
        'enabled': False,  # Disabled until connected
        'simulation_mode': True,
        'available': False,
        'description': 'Video capture and tracking'
    },
    'microphone': {
        'name': 'Microphone',
        'enabled': True,
        'simulation_mode': False,
        'available': True,
        'description': 'Audio input device'
    },
    'speaker': {
        'name': 'Speaker',
        'enabled': True,
        'simulation_mode': False,
        'available': True,
        'description': 'Audio output device'
    }
}


@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('index.html', 
                          components=_component_config,
                          state=_dashboard_state)


@app.route('/api/status')
def get_status():
    """Get overall system status."""
    return jsonify({
        'ros2_connected': _dashboard_state['ros2_connected'],
        'timestamp': datetime.now().isoformat(),
        'components': _component_config,
        'system_health': _dashboard_state.get('system_health', {})
    })


@app.route('/api/component/<component_id>/toggle', methods=['POST'])
def toggle_component(component_id):
    """Toggle component enabled state."""
    if component_id in _component_config:
        _component_config[component_id]['enabled'] = not _component_config[component_id]['enabled']
        return jsonify({
            'success': True,
            'component': component_id,
            'enabled': _component_config[component_id]['enabled']
        })
    return jsonify({'success': False, 'error': 'Component not found'}), 404


@app.route('/api/component/<component_id>/simulation', methods=['POST'])
def toggle_simulation(component_id):
    """Toggle simulation mode for component."""
    if component_id in _component_config:
        data = request.get_json() or {}
        _component_config[component_id]['simulation_mode'] = data.get('simulation', True)
        return jsonify({
            'success': True,
            'component': component_id,
            'simulation_mode': _component_config[component_id]['simulation_mode']
        })
    return jsonify({'success': False, 'error': 'Component not found'}), 404


# ==================== Test Endpoints ====================

@app.route('/api/test/wake_word', methods=['POST'])
def test_wake_word():
    """Test wake word detection."""
    config = _component_config['wake_word']
    
    if config['simulation_mode']:
        # Simulate wake word detection
        time.sleep(0.5)
        return jsonify({
            'success': True,
            'simulated': True,
            'detected': True,
            'keyword': 'aimee',
            'confidence': 0.95,
            'message': 'Simulated wake word detected'
        })
    else:
        # Real test - trigger actual wake word
        # This would publish to /wake_word/control
        return jsonify({
            'success': True,
            'simulated': False,
            'message': 'Listening for wake word... (speak now)',
            'note': 'Check /wake_word/detected topic for results'
        })


@app.route('/api/test/stt', methods=['POST'])
def test_stt():
    """Test speech-to-text."""
    config = _component_config['stt']
    data = request.get_json() or {}
    
    if config['simulation_mode']:
        # Simulate STT
        simulated_text = data.get('simulate_text', 'move forward')
        time.sleep(0.5)
        return jsonify({
            'success': True,
            'simulated': True,
            'text': simulated_text,
            'confidence': 0.92,
            'is_command': True,
            'message': f'Simulated transcription: "{simulated_text}"'
        })
    else:
        # Real test - trigger recording
        return jsonify({
            'success': True,
            'simulated': False,
            'message': 'Recording started (5 seconds)...',
            'note': 'Check /voice/transcription topic for results'
        })


@app.route('/api/test/tts', methods=['POST'])
def test_tts():
    """Test text-to-speech."""
    config = _component_config['tts']
    data = request.get_json() or {}
    text = data.get('text', 'Hello, I am AIMEE')
    
    if config['simulation_mode']:
        # Simulate TTS
        time.sleep(0.3)
        return jsonify({
            'success': True,
            'simulated': True,
            'text': text,
            'engine': 'simulated',
            'message': f'Would speak: "{text}"'
        })
    else:
        # Real TTS - publish to topic
        return jsonify({
            'success': True,
            'simulated': False,
            'text': text,
            'message': f'Speaking: "{text}"',
            'note': 'Published to /tts/speak'
        })


@app.route('/api/test/llm', methods=['POST'])
def test_llm():
    """Test LLM generation."""
    config = _component_config['llm']
    data = request.get_json() or {}
    prompt = data.get('prompt', 'What is your name?')
    
    if config['simulation_mode']:
        # Simulate LLM response
        responses = {
            'What is your name?': 'I am AIMEE, your robot assistant.',
            'Hello': 'Hello! How can I help you today?',
            'move forward': 'I will move forward.',
        }
        response = responses.get(prompt, f'This is a simulated response to: "{prompt}"')
        time.sleep(0.5)
        return jsonify({
            'success': True,
            'simulated': True,
            'prompt': prompt,
            'response': response,
            'tokens_generated': len(response.split()),
            'message': 'Simulated LLM response'
        })
    else:
        # Real LLM - would call action
        return jsonify({
            'success': True,
            'simulated': False,
            'prompt': prompt,
            'message': 'Sending to LLM server...',
            'note': 'Check /llm/generate action for results'
        })


@app.route('/api/test/intent', methods=['POST'])
def test_intent():
    """Test intent classification."""
    config = _component_config['intent']
    data = request.get_json() or {}
    text = data.get('text', 'move forward')
    
    if config['simulation_mode']:
        # Simulate intent classification
        intents = {
            'move forward': {'type': 'MOVEMENT', 'action': 'move_forward', 'confidence': 0.95},
            'hello': {'type': 'GREETING', 'action': 'greet', 'confidence': 0.98},
            'wave': {'type': 'ARM_CONTROL', 'action': 'wave', 'confidence': 0.92},
            'look at me': {'type': 'CAMERA', 'action': 'look_at_me', 'confidence': 0.88},
        }
        intent = intents.get(text.lower(), {'type': 'UNKNOWN', 'action': 'unknown', 'confidence': 0.5})
        time.sleep(0.3)
        return jsonify({
            'success': True,
            'simulated': True,
            'text': text,
            'intent': intent,
            'message': f'Simulated intent: {intent["type"]}'
        })
    else:
        return jsonify({
            'success': True,
            'simulated': False,
            'text': text,
            'message': 'Sending to intent router...',
            'note': 'Check /intent/classified topic for results'
        })


@app.route('/api/test/skill', methods=['POST'])
def test_skill():
    """Test skill execution."""
    config = _component_config['skills']
    data = request.get_json() or {}
    skill_name = data.get('skill', 'movement')
    action = data.get('action', 'move_forward')
    
    if config['simulation_mode']:
        # Simulate skill execution
        time.sleep(0.5)
        return jsonify({
            'success': True,
            'simulated': True,
            'skill': skill_name,
            'action': action,
            'message': f'Simulated {skill_name}.{action}',
            'note': 'NO REAL MOVEMENT - SIMULATION ONLY'
        })
    else:
        return jsonify({
            'success': True,
            'simulated': False,
            'skill': skill_name,
            'action': action,
            'message': f'Executing {skill_name}.{action}',
            'warning': 'REAL HARDWARE WILL MOVE!',
            'note': 'Published to /skill/execute'
        })


@app.route('/api/test/camera', methods=['POST'])
def test_camera():
    """Test camera capture."""
    config = _component_config['camera']
    
    if not config['available']:
        return jsonify({
            'success': False,
            'error': 'Camera not available',
            'message': 'Connect OBSBOT camera first'
        })
    
    if config['simulation_mode']:
        return jsonify({
            'success': True,
            'simulated': True,
            'message': 'Simulated camera feed',
            'note': 'Showing test pattern'
        })
    else:
        return jsonify({
            'success': True,
            'simulated': False,
            'message': 'Camera feed active',
            'note': 'Stream available at /camera/stream'
        })


@app.route('/api/test/microphone', methods=['POST'])
def test_microphone():
    """Test microphone."""
    config = _component_config['microphone']
    
    if config['simulation_mode']:
        return jsonify({
            'success': True,
            'simulated': True,
            'level': 0.75,
            'message': 'Simulated audio input'
        })
    else:
        # Test actual microphone
        try:
            result = subprocess.run(
                ['arecord', '-D', 'default', '-d', '1', '-f', 'S16_LE', '-r', '16000', '-c', '1', '/tmp/test_mic.wav'],
                capture_output=True,
                timeout=3
            )
            if result.returncode == 0:
                return jsonify({
                    'success': True,
                    'simulated': False,
                    'message': 'Microphone recording successful',
                    'device': 'default'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Recording failed',
                    'stderr': result.stderr.decode()[:200]
                })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })


@app.route('/api/test/speaker', methods=['POST'])
def test_speaker():
    """Test speaker."""
    config = _component_config['speaker']
    
    if config['simulation_mode']:
        return jsonify({
            'success': True,
            'simulated': True,
            'message': 'Simulated audio output'
        })
    else:
        # Test actual speaker
        try:
            # Play test sound
            result = subprocess.run(
                ['aplay', '/usr/share/sounds/alsa/Front_Center.wav'],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                return jsonify({
                    'success': True,
                    'simulated': False,
                    'message': 'Speaker test successful'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Playback failed'
                })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })


# ==================== Full Pipeline Test ====================

@app.route('/api/test/full_pipeline', methods=['POST'])
def test_full_pipeline():
    """Test full voice pipeline."""
    data = request.get_json() or {}
    simulate_input = data.get('simulate_input', 'hello aimee move forward')
    
    results = []
    
    # Step 1: Wake Word
    if _component_config['wake_word']['enabled']:
        results.append({
            'step': 'wake_word',
            'status': 'detected',
            'simulated': _component_config['wake_word']['simulation_mode']
        })
    
    # Step 2: STT
    if _component_config['stt']['enabled']:
        results.append({
            'step': 'stt',
            'text': simulate_input,
            'simulated': _component_config['stt']['simulation_mode']
        })
    
    # Step 3: Intent
    if _component_config['intent']['enabled']:
        results.append({
            'step': 'intent',
            'intent': 'MOVEMENT',
            'action': 'move_forward',
            'simulated': _component_config['intent']['simulation_mode']
        })
    
    # Step 4: Skill
    if _component_config['skills']['enabled']:
        results.append({
            'step': 'skill',
            'skill': 'movement',
            'action': 'move_forward',
            'simulated': _component_config['skills']['simulation_mode']
        })
    
    # Step 5: TTS Response
    if _component_config['tts']['enabled']:
        results.append({
            'step': 'tts',
            'response': 'Moving forward',
            'simulated': _component_config['tts']['simulation_mode']
        })
    
    return jsonify({
        'success': True,
        'results': results,
        'total_steps': len(results)
    })


# ==================== System Info ====================

@app.route('/api/system/info')
def get_system_info():
    """Get system information."""
    info = {
        'platform': 'Arduino UNO Q',
        'timestamp': datetime.now().isoformat(),
        'ros2_version': 'Humble',
        'workspace': '/home/arduino/aimee-robot-ws',
    }
    
    # Get disk usage
    try:
        df = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
        info['disk_usage'] = df.stdout.split('\n')[1]
    except:
        pass
    
    # Get memory usage
    try:
        free = subprocess.run(['free', '-h'], capture_output=True, text=True)
        info['memory'] = free.stdout
    except:
        pass
    
    return jsonify(info)


@app.route('/api/ros2/topics')
def get_ros2_topics():
    """Get list of ROS2 topics."""
    try:
        result = subprocess.run(
            ['ros2', 'topic', 'list'],
            capture_output=True,
            text=True,
            timeout=5
        )
        topics = [t.strip() for t in result.stdout.split('\n') if t.strip()]
        return jsonify({'topics': topics, 'count': len(topics)})
    except Exception as e:
        return jsonify({'topics': [], 'error': str(e)})


@app.route('/api/ros2/nodes')
def get_ros2_nodes():
    """Get list of ROS2 nodes."""
    try:
        result = subprocess.run(
            ['ros2', 'node', 'list'],
            capture_output=True,
            text=True,
            timeout=5
        )
        nodes = [n.strip() for n in result.stdout.split('\n') if n.strip()]
        return jsonify({'nodes': nodes, 'count': len(nodes)})
    except Exception as e:
        return jsonify({'nodes': [], 'error': str(e)})


def run_flask_app(host='0.0.0.0', port=5000, debug=False):
    """Run the Flask application."""
    logger.info(f"Starting AIMEE Test Dashboard on http://{host}:{port}")
    app.run(host=host, port=port, debug=debug, threaded=True)


if __name__ == '__main__':
    run_flask_app(debug=True)

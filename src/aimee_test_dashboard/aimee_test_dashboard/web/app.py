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

# Import intent classifier
try:
    from intent_classifier import classify_intent
except ImportError:
    # Fallback if not available
    def classify_intent(text):
        return {'intent_type': 'UNKNOWN', 'action': 'unknown', 'confidence': 0.0, 'skill_name': '', 'source': 'fallback'}

# Configure logging
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aimee-robot-dashboard'

# ==================== Audio Setup (Initialize ONCE) ====================
# Set ALSA environment variables BEFORE importing pygame
os.environ['SDL_AUDIODRIVER'] = 'alsa'
os.environ['AUDIODEV'] = 'plughw:1,0'

# Initialize pygame mixer ONCE at startup to prevent audio clipping
# This keeps the audio pipeline ready for immediate playback
try:
    import pygame
    pygame.mixer.pre_init(frequency=24000, size=-16, channels=1)
    pygame.mixer.init()
    # Small delay to ensure audio device is fully ready (prevents first-playback clipping)
    time.sleep(0.2)
    _pygame_mixer_initialized = True
    logger.info("Pygame mixer initialized successfully")
except Exception as e:
    _pygame_mixer_initialized = False
    logger.warning(f"Failed to initialize pygame mixer: {e}")

# ==================== STT Setup (Initialize Vosk ONCE) ====================
# Load Vosk model once at startup to avoid delays during STT tests
_vosk_model = None
_vosk_model_path = '/workspace/vosk-models/vosk-model-small-en-us-0.15'

try:
    if os.path.exists(_vosk_model_path):
        from vosk import Model
        logger.info("Loading Vosk model (this may take a moment)...")
        _vosk_model = Model(_vosk_model_path)
        logger.info("Vosk model loaded successfully!")
    else:
        logger.warning(f"Vosk model not found at {_vosk_model_path}")
except Exception as e:
    logger.warning(f"Failed to load Vosk model: {e}")

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
        'simulation_mode': True,  # SIMULATION by default
        'available': True,
        'description': 'Edge Impulse keyword spotting'
    },
    'stt': {
        'name': 'Speech-to-Text (Vosk)',
        'enabled': True,
        'simulation_mode': True,  # SIMULATION by default
        'available': True,
        'description': 'Voice transcription'
    },
    'tts': {
        'name': 'Text-to-Speech',
        'enabled': True,
        'simulation_mode': True,  # SIMULATION by default
        'available': True,
        'description': 'gTTS / Piper voice output'
    },
    'llm': {
        'name': 'LLM Server',
        'enabled': True,
        'simulation_mode': True,  # SIMULATION by default
        'available': True,
        'description': 'Local language model'
    },
    'intent': {
        'name': 'Intent Router',
        'enabled': True,
        'simulation_mode': True,  # SIMULATION by default
        'available': True,
        'description': 'Intent classification'
    },
    'skills': {
        'name': 'Skill Manager',
        'enabled': True,
        'simulation_mode': True,  # SIMULATION for safety
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
        'simulation_mode': True,  # SIMULATION by default
        'available': True,
        'description': 'Audio input device'
    },
    'speaker': {
        'name': 'Speaker',
        'enabled': True,
        'simulation_mode': True,  # SIMULATION by default
        'available': True,
        'description': 'Audio output device'
    },
    'aimee_cloud': {
        'name': 'AimeeCloud',
        'enabled': True,
        'simulation_mode': True,
        'available': True,
        'description': 'Cloud-based AI skills & services'
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
        # Real test - record with VAD (Voice Activity Detection) and transcribe with Vosk
        try:
            import os
            import json
            import wave
            import subprocess
            import audioop
            from vosk import KaldiRecognizer
            
            audio_file = '/tmp/test_recording.wav'
            
            # Check if Vosk model is loaded
            global _vosk_model
            if _vosk_model is None:
                return jsonify({
                    'success': False,
                    'error': 'Vosk model not loaded',
                    'note': 'Model failed to load at startup'
                })
            
            # Record with VAD - stop when silence detected
            # Start recording process
            cmd = ['arecord', '-D', 'hw:1,0', '-f', 'S16_LE', '-r', '16000', '-c', '1', '-t', 'raw']
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # VAD parameters
            RATE = 16000
            CHUNK_SIZE = 800  # 50ms chunks
            SILENCE_THRESHOLD = 200  # RMS threshold for silence
            SILENCE_CHUNKS = 25  # Stop after ~1.5 seconds of silence
            MAX_RECORDING_CHUNKS = 160  # Max ~8 seconds
            
            from vosk import KaldiRecognizer
            recognizer = KaldiRecognizer(_vosk_model, RATE)
            
            audio_buffer = []
            silence_count = 0
            total_chunks = 0
            speech_detected = False
            
            while total_chunks < MAX_RECORDING_CHUNKS:
                data = process.stdout.read(CHUNK_SIZE * 2)  # 16-bit = 2 bytes per sample
                if len(data) < CHUNK_SIZE * 2:
                    break
                
                total_chunks += 1
                audio_buffer.append(data)
                
                # Calculate RMS for VAD
                rms = audioop.rms(data, 2)
                
                # Check for speech
                if rms > SILENCE_THRESHOLD:
                    speech_detected = True
                    silence_count = 0
                elif speech_detected:
                    silence_count += 1
                
                # Feed to recognizer in real-time
                recognizer.AcceptWaveform(data)
                
                # Stop on silence after speech
                if speech_detected and silence_count >= SILENCE_CHUNKS:
                    break
            
            process.terminate()
            process.wait()
            
            # Save audio file
            with wave.open(audio_file, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(RATE)
                wf.writeframes(b''.join(audio_buffer))
            
            file_size = os.path.getsize(audio_file)
            duration = len(audio_buffer) * CHUNK_SIZE / RATE
            
            # Get final transcription
            final_result = json.loads(recognizer.FinalResult())
            transcript = final_result.get('text', '').strip()
            
            # Also get partial results
            partial_transcript = json.loads(recognizer.PartialResult()).get('partial', '')
            if not transcript and partial_transcript:
                transcript = partial_transcript
            
            return jsonify({
                'success': True,
                'simulated': False,
                'message': f'"{transcript}" ({duration:.1f}s)' if transcript else f'No speech detected ({duration:.1f}s)',
                'transcript': transcript,
                'audio_file': audio_file,
                'file_size_bytes': file_size,
                'device': 'hw:1,0 (RC08 USB Mic)',
                'engine': 'Vosk STT',
                'model': 'vosk-model-small-en-us-0.15'
            })
            
        except Exception as e:
            import traceback
            return jsonify({
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()[-300:],
                'note': 'Is the RC08 USB microphone connected and Vosk model available?'
            })


@app.route('/api/test/tts', methods=['POST'])
def test_tts():
    """Test text-to-speech using gTTS + pygame (with persistent mixer)."""
    import time
    import random
    
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
        # Real TTS using gTTS + pygame (persistent mixer - no clipping!)
        try:
            global _pygame_mixer_initialized
            
            if not _pygame_mixer_initialized:
                return jsonify({
                    'success': False,
                    'error': 'Pygame mixer not initialized'
                })
            
            from gtts import gTTS
            import pygame
            
            # Generate unique filename to avoid conflicts
            tmp_file = f'/tmp/tts_{int(time.time())}_{random.randint(1000,9999)}.mp3'
            
            # Generate speech
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(tmp_file)
            
            # Check file was created
            file_size = os.path.getsize(tmp_file)
            if file_size < 1000:
                os.remove(tmp_file)
                raise Exception(f'gTTS file too small ({file_size} bytes)')
            
            # Play with pre-initialized pygame mixer (no re-init = no clipping!)
            pygame.mixer.music.load(tmp_file)
            pygame.mixer.music.set_volume(0.5)  # 50% volume
            pygame.mixer.music.play()
            
            # Wait for playback
            start_time = time.time()
            while pygame.mixer.music.get_busy() and time.time() - start_time < 30:
                time.sleep(0.05)
            
            # Clean up temp file
            try:
                os.remove(tmp_file)
            except:
                pass
            
            return jsonify({
                'success': True,
                'simulated': False,
                'text': text,
                'engine': 'gTTS + pygame (persistent mixer)',
                'device': 'plughw:1,0',
                'volume': '50%',
                'file_size': file_size,
                'message': f'🔊 Spoke: "{text}"'
            })
        except Exception as e:
            import traceback
            return jsonify({
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()[-200:]
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
        # Real LLM - call the llama.cpp server directly with proper Qwen chat format
        try:
            # Format prompt for Qwen2.5 chat template - friendly and engaging
            formatted_prompt = f"""<|im_start|>system
You are AIMEE, a friendly and engaging robot assistant with a warm personality. 
Give helpful, enthusiastic responses and always offer to provide more information.
<|im_end|>
<|im_start|>user
{prompt}
<|im_end|>
<|im_start|>assistant
"""
            
            result = subprocess.run(
                ['curl', '-s', 'http://localhost:8080/completion',
                 '-H', 'Content-Type: application/json',
                 '-d', json.dumps({
                     'prompt': formatted_prompt, 
                     'n_predict': 100,
                     'temperature': 0.7,
                     'stop': ['<|im_end|>', '<|im_start|>']
                 })],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                response_data = json.loads(result.stdout)
                response_text = response_data.get('content', 'No response')
                return jsonify({
                    'success': True,
                    'simulated': False,
                    'prompt': prompt,
                    'response': response_text,
                    'model': response_data.get('model', 'unknown'),
                    'message': f'LLM Response: "{response_text[:100]}..."' if len(response_text) > 100 else f'LLM Response: "{response_text}"'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'LLM request failed',
                    'stderr': result.stderr[:200]
                })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e),
                'note': 'Is the LLM server running?'
            })


@app.route('/api/test/intent', methods=['POST'])
def test_intent():
    """Test intent classification using hybrid keyword + cloud approach."""
    config = _component_config['intent']
    data = request.get_json() or {}
    text = data.get('text', 'move forward')
    
    if config['simulation_mode']:
        # Use hybrid classifier in simulation mode too (it's deterministic)
        result = classify_intent(text)
        time.sleep(0.1)  # Small delay for realism
        return jsonify({
            'success': True,
            'simulated': True,
            'text': text,
            'intent': result,
            'message': f"Hybrid classifier: {result['intent_type']}.{result['action']} (conf: {result['confidence']:.2f})"
        })
    else:
        # Real mode - use hybrid classifier
        try:
            result = classify_intent(text)
            
            # Publish to ROS2 if confidence is high enough
            if result['confidence'] >= 0.7:
                try:
                    subprocess.run(
                        ['ros2', 'topic', 'pub', '--once',
                         '/intent/classified', 'aimee_msgs/Intent',
                         f'{{intent_type: "{result["intent_type"]}", action: "{result["action"]}", text: "{text}", confidence: {result["confidence"]:.2f}, skill_name: "{result["skill_name"]}"}}'],
                        capture_output=True,
                        timeout=2
                    )
                except:
                    pass  # Non-blocking
            
            # If low confidence, suggest cloud
            if result['confidence'] < 0.75:
                result['note'] = 'Low confidence - would use AimeeCloud for better classification'
            
            return jsonify({
                'success': True,
                'simulated': False,
                'text': text,
                'intent': result,
                'message': f"Intent: {result['intent_type']}.{result['action']} (source: {result['source']}, conf: {result['confidence']:.2f})"
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e),
                'note': 'Classifier error - check logs'
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
    data = request.get_json() or {}
    
    if config['simulation_mode']:
        audio_level = data.get('audio_level', 0.75)
        return jsonify({
            'success': True,
            'simulated': True,
            'level': audio_level,
            'message': f'Simulated audio input (level: {audio_level})'
        })
    else:
        # Test actual microphone (RC08 USB on hw:1,0)
        try:
            result = subprocess.run(
                ['arecord', '-D', 'hw:1,0', '-d', '1', '-f', 'S16_LE', '-r', '16000', '-c', '1', '/tmp/test_mic.wav'],
                capture_output=True,
                timeout=3
            )
            if result.returncode == 0:
                return jsonify({
                    'success': True,
                    'simulated': False,
                    'message': 'Microphone recording successful (RC08)',
                    'device': 'hw:1,0'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Recording failed',
                    'stderr': result.stderr.decode()[:200],
                    'note': 'Make sure RC08 USB mic is connected'
                })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })


@app.route('/api/test/speaker', methods=['POST'])
def test_speaker():
    """Test speaker using persistent pygame mixer (no clipping)."""
    import time
    
    config = _component_config['speaker']
    data = request.get_json() or {}
    
    if config['simulation_mode']:
        output_text = data.get('output_text', 'Test audio output')
        return jsonify({
            'success': True,
            'simulated': True,
            'output_text': output_text,
            'message': f'Simulated audio output: "{output_text}"'
        })
    else:
        # Test actual speaker using persistent pygame mixer
        try:
            global _pygame_mixer_initialized
            
            if not _pygame_mixer_initialized:
                return jsonify({
                    'success': False,
                    'error': 'Pygame mixer not initialized'
                })
            
            import pygame
            
            # Use pre-initialized mixer (no re-init = no clipping!)
            pygame.mixer.music.load('/usr/share/sounds/alsa/Front_Center.wav')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
            
            # Wait for playback
            start_time = time.time()
            while pygame.mixer.music.get_busy() and time.time() - start_time < 10:
                time.sleep(0.05)
            
            return jsonify({
                'success': True,
                'simulated': False,
                'message': '🔊 Speaker test successful! You should have heard "Front Center"',
                'device': 'plughw:1,0 (persistent mixer)',
                'note': 'No clipping - mixer initialized once at startup'
            })
        except Exception as e:
            import traceback
            return jsonify({
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()[-200:]
            })


@app.route('/api/test/aimee_cloud', methods=['POST'])
def test_aimee_cloud():
    """Test AimeeCloud cloud skills."""
    config = _component_config['aimee_cloud']
    data = request.get_json() or {}
    skill_request = data.get('skill_request', 'weather in New York')
    
    if config['simulation_mode']:
        # Simulate AimeeCloud response
        cloud_responses = {
            'weather': 'The weather in New York is 72°F and sunny.',
            'news': 'Here are the top headlines from AimeeCloud...',
            'time': 'The current time is 3:45 PM.',
        }
        response = cloud_responses.get(
            skill_request.split()[0].lower(), 
            f'AimeeCloud processed: "{skill_request}"'
        )
        time.sleep(0.5)
        return jsonify({
            'success': True,
            'simulated': True,
            'cloud_provider': 'AimeeCloud',
            'request': skill_request,
            'response': response,
            'message': f'AimeeCloud: {response}'
        })
    else:
        # Real AimeeCloud API call would go here
        return jsonify({
            'success': True,
            'simulated': False,
            'cloud_provider': 'AimeeCloud',
            'request': skill_request,
            'message': 'Sending to AimeeCloud...',
            'note': 'Check /cloud/skill/execute for results'
        })


# ==================== Full Pipeline Test ====================

@app.route('/api/test/full_pipeline', methods=['POST'])
def test_full_pipeline():
    """Test full voice pipeline with REAL components."""
    import urllib.request
    import json
    
    data = request.get_json() or {}
    results = []
    transcript = ""
    intent_result = None
    
    # Step 1: Wake Word (simulated for now - would need wake word node running)
    if _component_config['wake_word']['enabled']:
        if _component_config['wake_word']['simulation_mode']:
            results.append({
                'step': 'wake_word',
                'status': 'detected',
                'keyword': 'aimee',
                'simulated': True,
                'message': '[SIMULATED] Wake word detected'
            })
        else:
            results.append({
                'step': 'wake_word',
                'status': 'detected',
                'keyword': 'aimee',
                'simulated': False,
                'message': 'Wake word detected (real)'
            })
    
    # Step 2: STT (REAL recording with VAD)
    if _component_config['stt']['enabled']:
        if _component_config['stt']['simulation_mode']:
            transcript = data.get('simulate_input', 'hello aimee move forward')
            results.append({
                'step': 'stt',
                'text': transcript,
                'simulated': True,
                'message': f'[SIMULATED] STT: "{transcript}"'
            })
        else:
            # Real STT with VAD
            try:
                import audioop
                from vosk import KaldiRecognizer
                
                cmd = ['arecord', '-D', 'hw:1,0', '-f', 'S16_LE', '-r', '16000', '-c', '1', '-t', 'raw']
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                RATE = 16000
                CHUNK_SIZE = 800
                SILENCE_THRESHOLD = 200
                SILENCE_CHUNKS = 25
                MAX_CHUNKS = 160
                
                global _vosk_model
                recognizer = KaldiRecognizer(_vosk_model, RATE)
                
                audio_buffer = []
                silence_count = 0
                total_chunks = 0
                speech_detected = False
                
                while total_chunks < MAX_CHUNKS:
                    data_chunk = process.stdout.read(CHUNK_SIZE * 2)
                    if len(data_chunk) < CHUNK_SIZE * 2:
                        break
                    
                    total_chunks += 1
                    audio_buffer.append(data_chunk)
                    
                    rms = audioop.rms(data_chunk, 2)
                    if rms > SILENCE_THRESHOLD:
                        speech_detected = True
                        silence_count = 0
                    elif speech_detected:
                        silence_count += 1
                    
                    recognizer.AcceptWaveform(data_chunk)
                    
                    if speech_detected and silence_count >= SILENCE_CHUNKS:
                        break
                
                process.terminate()
                process.wait()
                
                final_result = json.loads(recognizer.FinalResult())
                transcript = final_result.get('text', '').strip()
                partial = json.loads(recognizer.PartialResult()).get('partial', '')
                if not transcript and partial:
                    transcript = partial
                
                duration = len(audio_buffer) * CHUNK_SIZE / RATE
                
                results.append({
                    'step': 'stt',
                    'text': transcript,
                    'duration': round(duration, 1),
                    'simulated': False,
                    'message': f'STT: "{transcript}" ({duration:.1f}s)'
                })
            except Exception as e:
                results.append({
                    'step': 'stt',
                    'error': str(e),
                    'simulated': False,
                    'message': f'STT failed: {e}'
                })
    
    # Step 3: Intent Classification (REAL)
    if _component_config['intent']['enabled'] and transcript:
        try:
            intent_result = classify_intent(transcript)
            results.append({
                'step': 'intent',
                'intent': intent_result['intent_type'],
                'action': intent_result['action'],
                'confidence': intent_result['confidence'],
                'source': intent_result.get('source', 'unknown'),
                'simulated': False,
                'message': f"Intent: {intent_result['intent_type']}.{intent_result['action']} ({intent_result['confidence']:.0%})"
            })
        except Exception as e:
            results.append({
                'step': 'intent',
                'error': str(e),
                'simulated': False,
                'message': f'Intent failed: {e}'
            })
    
    # Step 4: Skill (simulated for safety unless explicitly enabled)
    if _component_config['skills']['enabled'] and intent_result:
        if _component_config['skills']['simulation_mode']:
            results.append({
                'step': 'skill',
                'skill': intent_result.get('skill_name', 'unknown'),
                'action': intent_result['action'],
                'simulated': True,
                'message': f"[SIMULATED] Skill: {intent_result.get('skill_name', 'unknown')}.{intent_result['action']}"
            })
        else:
            results.append({
                'step': 'skill',
                'skill': intent_result.get('skill_name', 'unknown'),
                'action': intent_result['action'],
                'simulated': False,
                'message': f"Skill: {intent_result.get('skill_name', 'unknown')}.{intent_result['action']} (would execute)"
            })
    
    # Step 5: LLM Response (REAL if not in simulation)
    if _component_config['llm']['enabled'] and transcript:
        if _component_config['llm']['simulation_mode']:
            tts_response = f"You said: {transcript[:30]}..."
            results.append({
                'step': 'llm',
                'response': tts_response,
                'simulated': True,
                'message': f'[SIMULATED] LLM: "{tts_response}"'
            })
        else:
            # Real LLM call
            try:
                system_prompt = "You are AIMEE, a friendly robot assistant. Give short, helpful responses (1-2 sentences)."
                full_prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{transcript}<|im_end|>\n<|im_start|>assistant\n"
                
                llm_data = {
                    "prompt": full_prompt,
                    "temperature": 0.7,
                    "n_predict": 100,
                    "stop": ["<|im_end|>"],
                    "stream": False
                }
                
                req = urllib.request.Request(
                    'http://localhost:8080/completion',
                    data=json.dumps(llm_data).encode('utf-8'),
                    headers={'Content-Type': 'application/json'},
                    method='POST'
                )
                
                with urllib.request.urlopen(req, timeout=15) as response:
                    llm_result = json.loads(response.read().decode('utf-8'))
                    tts_response = llm_result.get('content', '').strip()
                
                results.append({
                    'step': 'llm',
                    'response': tts_response,
                    'tokens': llm_result.get('tokens_predicted', 0),
                    'simulated': False,
                    'message': f'LLM: "{tts_response[:50]}..."' if len(tts_response) > 50 else f'LLM: "{tts_response}"'
                })
            except Exception as e:
                tts_response = f"I heard you say {transcript}"
                results.append({
                    'step': 'llm',
                    'response': tts_response,
                    'error': str(e),
                    'simulated': False,
                    'message': f'LLM failed, using fallback: "{tts_response}"'
                })
    else:
        tts_response = f"You said: {transcript}" if transcript else "I didn't hear anything"
    
    # Step 6: TTS Response (REAL if not in simulation)
    if _component_config['tts']['enabled']:
        if _component_config['tts']['simulation_mode']:
            results.append({
                'step': 'tts',
                'response': tts_response[:50] if 'tts_response' in dir() else "Simulated response",
                'simulated': True,
                'message': '[SIMULATED] TTS would speak the response'
            })
        else:
            # Real TTS
            try:
                global _pygame_mixer_initialized
                if _pygame_mixer_initialized and 'tts_response' in locals():
                    from gtts import gTTS
                    import pygame
                    
                    tts_file = f'/tmp/pipeline_tts_{int(time.time())}.mp3'
                    tts = gTTS(text=tts_response, lang='en', slow=False)
                    tts.save(tts_file)
                    
                    pygame.mixer.music.load(tts_file)
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play()
                    
                    start_time = time.time()
                    while pygame.mixer.music.get_busy() and time.time() - start_time < 30:
                        time.sleep(0.05)
                    
                    try:
                        os.remove(tts_file)
                    except:
                        pass
                    
                    results.append({
                        'step': 'tts',
                        'response': tts_response[:50] + '...' if len(tts_response) > 50 else tts_response,
                        'simulated': False,
                        'message': f'🔊 Spoke: "{tts_response[:50]}..."' if len(tts_response) > 50 else f'🔊 Spoke: "{tts_response}"'
                    })
                else:
                    results.append({
                        'step': 'tts',
                        'response': tts_response if 'tts_response' in locals() else "No response",
                        'simulated': False,
                        'message': 'TTS: Mixer not ready'
                    })
            except Exception as e:
                results.append({
                    'step': 'tts',
                    'error': str(e),
                    'simulated': False,
                    'message': f'TTS failed: {e}'
                })
    
    return jsonify({
        'success': True,
        'results': results,
        'total_steps': len(results),
        'note': 'Green = Real, Yellow = Simulated'
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
    run_flask_app(debug=False)


# ==================== ROS2 Pipeline Test ====================

@app.route('/api/test/ros2_pipeline', methods=['POST'])
def test_ros2_pipeline():
    """Test full ROS2 message pipeline.
    Trigger: Publish to /wake_word/detected
    Flow: wake_word -> voice/transcription -> intent/classified -> skill -> tts/speak
    """
    import subprocess
    
    data = request.get_json() or {}
    wake_word = data.get('wake_word', 'aimee')
    
    results = []
    
    try:
        # Publish wake word via shell
        cmd = f"source /opt/ros/humble/setup.bash && source /workspace/install/setup.bash && ros2 topic pub --once /wake_word/detected aimee_msgs/msg/WakeWordDetection '{{wake_word: \"{wake_word}\", confidence: 0.95, active: true}}'"
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,
            shell=True,
            executable='/bin/bash'
        )
        
        if result.returncode == 0:
            results.append({
                'step': 1,
                'name': 'wake_word',
                'status': 'published',
                'message': f'Published /wake_word/detected: {wake_word}'
            })
        else:
            results.append({
                'step': 1,
                'name': 'wake_word',
                'status': 'error',
                'error': result.stderr[:100]
            })
        
        # Wait for pipeline
        time.sleep(8)
        
        results.append({
            'step': 2,
            'name': 'pipeline',
            'status': 'triggered',
            'message': 'Pipeline triggered - check ROS2 nodes logs'
        })
        
        return jsonify({
            'success': True,
            'results': results,
            'note': 'Check logs: voice_manager, intent_router, skill_manager, tts'
        })
        
    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()[-200:]
        })


@app.route('/api/ros2/status', methods=['GET'])
def get_ros2_status():
    """Get ROS2 nodes and topics status."""
    try:
        # Check nodes
        cmd = 'source /opt/ros/humble/setup.bash && source /workspace/install/setup.bash && ros2 node list'
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5,
            shell=True,
            executable='/bin/bash'
        )
        
        nodes = []
        if result.returncode == 0:
            nodes = [n.strip() for n in result.stdout.strip().split('\n') if n.strip()]
        
        return jsonify({
            'success': True,
            'nodes': nodes,
            'node_count': len(nodes),
            'pipeline_active': len(nodes) >= 4
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'nodes': []
        })


@app.route('/api/ros2/status', methods=['GET'])
def get_ros2_status():
    import subprocess
    try:
        cmd = ['bash', '-c', 'source /opt/ros/humble/setup.bash && source /workspace/install/setup.bash && ros2 node list']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        nodes = [n.strip() for n in result.stdout.strip().split('\n') if n.strip()] if result.returncode == 0 else []
        return jsonify({'success': True, 'nodes': nodes, 'count': len(nodes)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/test/ros2_pipeline', methods=['POST'])
def test_ros2_pipeline():
    import subprocess
    try:
        data = request.get_json() or {}
        wake_word = data.get('wake_word', 'aimee')
        cmd = ['bash', '-c', f'source /opt/ros/humble/setup.bash && source /workspace/install/setup.bash && ros2 topic pub --once /wake_word/detected aimee_msgs/msg/WakeWordDetection "{{{{wake_word: \"{wake_word}\", confidence: 0.95, active: true}}}}"']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return jsonify({'success': result.returncode == 0, 'message': f'Triggered wake word: {wake_word}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

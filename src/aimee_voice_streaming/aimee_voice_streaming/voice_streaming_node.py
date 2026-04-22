#!/usr/bin/env python3
"""ROS2 Node for native audio streaming voice pipeline.

Streams bidirectional audio to/from AimeeCloud via WebSocket.
Uses webrtcvad for voice activity detection.
Coexists with legacy voice_manager; launched via config toggle.

Phase 1 implementation:
  - PCM16 audio (no Opus)
  - webrtcvad (no Silero)
  - Mute mic during playback (no barge-in yet)
  - Auto-start on node init (no wake word)
"""

import json
import logging
import os
import threading
import time
from datetime import datetime, timezone
from typing import Optional

import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import String, Bool

from .audio_io import AudioCapture, AudioPlayback
from .vad_engine import VADEngine
from .websocket_client import AudioWebSocketClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VoiceStreamingNode(Node):
    """Native audio streaming voice node."""

    # States
    STATE_IDLE = "idle"
    STATE_LISTENING = "listening"
    STATE_PROCESSING = "processing"
    STATE_SPEAKING = "speaking"

    def __init__(self):
        super().__init__('voice_streaming')

        # ─── Parameters ───
        self.declare_parameters(namespace='', parameters=[
            ('gateway_url', 'wss://aimeecloud.com/ws/v1'),
            ('api_key', os.getenv('AIMEECLOUD_API_KEY', 'ac_free_943d96db38ee49aa')),
            ('device_id', 'arduino-uno-q-001'),
            ('reconnect_interval_sec', 5.0),

            # Audio I/O
            ('sample_rate_in', 16000),
            ('sample_rate_out', 24000),
            ('channels_in', 1),
            ('channels_out', 1),
            ('frame_duration_ms', 20),
            ('audio_device_index', -1),

            # VAD
            ('vad_mode', 2),  # 0-3, higher = more aggressive
            ('vad_silence_duration_ms', 500),
            ('vad_padding_duration_ms', 300),

            # Behavior
            ('auto_start', True),
            ('conversation_timeout_sec', 60.0),
            ('enable_barge_in', False),  # Phase 1: disabled
            ('max_utterance_sec', 30.0),  # Drop utterances longer than this
        ])

        self._gateway_url = self.get_parameter('gateway_url').value
        self._api_key = self.get_parameter('api_key').value
        self._device_id = self.get_parameter('device_id').value
        self._reconnect_interval_sec = self.get_parameter('reconnect_interval_sec').value

        self._sample_rate_in = self.get_parameter('sample_rate_in').value
        self._sample_rate_out = self.get_parameter('sample_rate_out').value
        self._channels_in = self.get_parameter('channels_in').value
        self._channels_out = self.get_parameter('channels_out').value
        self._frame_duration_ms = self.get_parameter('frame_duration_ms').value
        self._audio_device_index = self.get_parameter('audio_device_index').value

        self._vad_mode = self.get_parameter('vad_mode').value
        self._vad_silence_ms = self.get_parameter('vad_silence_duration_ms').value
        self._vad_padding_ms = self.get_parameter('vad_padding_duration_ms').value

        self._auto_start = self.get_parameter('auto_start').value
        self._conversation_timeout_sec = self.get_parameter('conversation_timeout_sec').value
        self._enable_barge_in = self.get_parameter('enable_barge_in').value
        self._max_utterance_sec = self.get_parameter('max_utterance_sec').value

        # Session tracking (from MQTT cloud bridge)
        self._session_id = ""

        # State
        self._state = self.STATE_IDLE
        self._state_lock = threading.Lock()
        self._running = False
        self._capture_thread: Optional[threading.Thread] = None
        self._silence_timer: Optional[threading.Timer] = None
        self._utterance_start_time: Optional[float] = None

        # Audio components
        self._capture = AudioCapture(
            sample_rate=self._sample_rate_in,
            channels=self._channels_in,
            block_duration_ms=self._frame_duration_ms,
            device_index=self._audio_device_index,
        )
        self._playback = AudioPlayback(
            sample_rate=self._sample_rate_out,
            channels=self._channels_out,
            block_duration_ms=self._frame_duration_ms,
            device_index=self._audio_device_index,
        )

        # VAD
        self._vad = VADEngine(
            mode=self._vad_mode,
            sample_rate=self._sample_rate_in,
            frame_duration_ms=self._frame_duration_ms,
            padding_duration_ms=self._vad_padding_ms,
            silence_duration_ms=self._vad_silence_ms,
        )

        # WebSocket client (initialized on start)
        self._ws_client: Optional[AudioWebSocketClient] = None

        # ROS2 QoS
        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # Publishers
        self._state_pub = self.create_publisher(String, '/voice/streaming/state', reliable_qos)
        self._interrupted_pub = self.create_publisher(Bool, '/voice/streaming/interrupted', reliable_qos)

        # Subscribers
        self.create_subscription(Bool, '/voice/streaming/start', self._on_start_cmd, 10)
        self.create_subscription(Bool, '/voice/streaming/stop', self._on_stop_cmd, 10)
        self.create_subscription(String, '/cloud/session_id', self._on_session_id, 10)

        # State publish timer
        self._state_timer = self.create_timer(2.0, self._publish_state)

        self.get_logger().info(
            f"VoiceStreamingNode initialized:\n"
            f"  Gateway: {self._gateway_url}\n"
            f"  Device: {self._device_id}\n"
            f"  Audio: {self._sample_rate_in}Hz in / {self._sample_rate_out}Hz out\n"
            f"  VAD: mode={self._vad_mode}, silence={self._vad_silence_ms}ms\n"
            f"  Auto-start: {self._auto_start}"
        )

        if self._auto_start:
            # Delay slightly to allow session_id to arrive from cloud bridge
            self._auto_start_timer = self.create_timer(3.0, self._auto_start_callback)

    # ─────────────────────────────── ROS2 Callbacks ───────────────────────────────

    def _auto_start_callback(self):
        """One-shot timer to auto-start after node init."""
        self._auto_start_timer.cancel()
        if not self._running:
            self.get_logger().info("Auto-starting voice streaming...")
            self.start_streaming()

    def _on_start_cmd(self, msg: Bool):
        if msg.data:
            self.get_logger().info("Received start command")
            self.start_streaming()
        else:
            self.get_logger().info("Received start=false command")

    def _on_stop_cmd(self, msg: Bool):
        if msg.data:
            self.get_logger().info("Received stop command")
            self.stop_streaming()

    def _on_session_id(self, msg: String):
        """Track session ID from cloud bridge."""
        new_session = msg.data
        if new_session != self._session_id:
            self._session_id = new_session
            self.get_logger().info(f"Session ID updated: {new_session or 'cleared'}")
            # If we have an active connection, it will use the new session on reconnect

    def _publish_state(self):
        with self._state_lock:
            state = self._state
        self._state_pub.publish(String(data=state))

    # ─────────────────────────────── Streaming Control ───────────────────────────────

    def start_streaming(self) -> bool:
        if self._running:
            self.get_logger().warning("Already streaming")
            return True

        # Ensure we have a session ID
        if not self._session_id:
            self.get_logger().warning(
                "No session ID available yet. Waiting for cloud bridge... "
                "Will retry when session is established."
            )
            # Set a retry timer
            self._retry_timer = self.create_timer(2.0, self._retry_start)
            return False

        # Start audio I/O
        if not self._capture.start():
            self.get_logger().error("Failed to start audio capture")
            return False
        if not self._playback.start():
            self.get_logger().error("Failed to start audio playback")
            self._capture.stop()
            return False

        # Start WebSocket client
        capabilities = {
            "audio_in": {"codec": "pcm16", "sample_rate": self._sample_rate_in},
            "audio_out": {"codec": "pcm16", "sample_rate": self._sample_rate_out},
            "barge_in": self._enable_barge_in,
            "languages": ["en-US"],
        }
        self._ws_client = AudioWebSocketClient(
            gateway_url=self._gateway_url,
            api_key=self._api_key,
            device_id=self._device_id,
            session_id=self._session_id,
            capabilities=capabilities,
            on_message=self._on_ws_message,
            on_connected=self._on_ws_connected,
            on_disconnected=self._on_ws_disconnected,
            reconnect_interval_sec=self._reconnect_interval_sec,
        )
        self._ws_client.start()

        self._running = True
        self._vad.reset()

        # Start capture thread
        self._capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._capture_thread.start()

        self._set_state(self.STATE_IDLE)
        self.get_logger().info("Voice streaming started")
        return True

    def _retry_start(self):
        """Retry auto-start when session becomes available."""
        if self._session_id and not self._running:
            self._retry_timer.cancel()
            self.start_streaming()
        elif self._running:
            self._retry_timer.cancel()

    def stop_streaming(self):
        if not self._running:
            return

        self._running = False
        self._cancel_silence_timer()

        if self._capture_thread:
            self._capture_thread.join(timeout=2.0)
            self._capture_thread = None

        if self._ws_client:
            self._ws_client.stop()
            self._ws_client = None

        self._capture.stop()
        self._playback.stop()
        self._capture.drain()
        self._playback.drain()

        self._set_state(self.STATE_IDLE)
        self.get_logger().info("Voice streaming stopped")

    # ─────────────────────────────── Capture Loop ───────────────────────────────

    def _capture_loop(self):
        """Background thread: read audio, run VAD, send to WebSocket."""
        self.get_logger().info("Capture loop started")

        while self._running:
            # If speaking and barge-in disabled, skip capture
            if not self._enable_barge_in:
                with self._state_lock:
                    if self._state == self.STATE_SPEAKING:
                        # Drain capture queue to avoid backlog
                        self._capture.drain()
                        time.sleep(0.02)
                        continue

            frame = self._capture.read_frame(timeout=0.05)
            if frame is None:
                continue

            # Flatten to 1D if mono
            if frame.ndim > 1:
                frame = frame[:, 0]

            # Run VAD
            is_speech, speech_finished, prefix_frames = self._vad.process(frame)

            with self._state_lock:
                current_state = self._state

            if current_state == self.STATE_IDLE:
                if is_speech and prefix_frames:
                    # Speech started
                    self._utterance_start_time = time.time()
                    self._set_state(self.STATE_LISTENING)
                    self.get_logger().info("Speech detected — listening")

                    # Send prefix padding + current frame
                    for pf in prefix_frames:
                        self._send_audio_frame(pf)
                    self._send_audio_frame(frame)

            elif current_state == self.STATE_LISTENING:
                if speech_finished:
                    # Speech ended
                    self.get_logger().info("Speech ended — processing")
                    self._set_state(self.STATE_PROCESSING)
                    self._start_silence_timer()
                else:
                    # Still listening
                    self._send_audio_frame(frame)

                    # Max utterance timeout
                    if self._utterance_start_time:
                        elapsed = time.time() - self._utterance_start_time
                        if elapsed > self._max_utterance_sec:
                            self.get_logger().warning(
                                f"Utterance exceeded {self._max_utterance_sec}s, cutting off"
                            )
                            self._vad.reset()
                            self._set_state(self.STATE_PROCESSING)
                            self._start_silence_timer()

            elif current_state == self.STATE_PROCESSING:
                # Don't capture during processing
                pass

            elif current_state == self.STATE_SPEAKING:
                if self._enable_barge_in and is_speech:
                    # Barge-in detected
                    self.get_logger().info("Barge-in detected")
                    self._interrupted_pub.publish(Bool(data=True))
                    self._playback.drain()
                    self._ws_client.send_event("interrupt")
                    self._vad.reset()
                    self._set_state(self.STATE_LISTENING)
                    self._utterance_start_time = time.time()

        self.get_logger().info("Capture loop exited")

    def _send_audio_frame(self, frame: np.ndarray):
        """Send one audio frame to WebSocket."""
        if self._ws_client and self._ws_client.is_connected:
            self._ws_client.send_audio(frame)

    # ─────────────────────────────── WebSocket Handlers ───────────────────────────────

    def _on_ws_connected(self):
        self.get_logger().info("WebSocket connected to gateway")

    def _on_ws_disconnected(self):
        self.get_logger().warning("WebSocket disconnected")
        with self._state_lock:
            if self._state == self.STATE_SPEAKING:
                self._playback.drain()
                self._set_state(self.STATE_IDLE)

    def _on_ws_message(self, msg: dict):
        msg_type = msg.get("type", "unknown")

        if msg_type == "audio_chunk" or msg.get("binary"):
            self._handle_audio_down(msg)
        elif msg_type == "session_ready":
            self.get_logger().info(f"Gateway session ready: {msg.get('session_id')}")
        elif msg_type == "error":
            code = msg.get("code", "UNKNOWN")
            self.get_logger().error(f"Gateway error: {code} - {msg.get('message')}")
            if code == "INVALID_API_KEY":
                self.get_logger().error("Invalid API key — check configuration")
        elif msg_type == "interrupted":
            self.get_logger().info("Received interrupt from gateway")
            self._playback.drain()
            with self._state_lock:
                if self._state == self.STATE_SPEAKING:
                    self._set_state(self.STATE_LISTENING)
        elif msg_type == "function_call_start":
            self.get_logger().info(f"Function call started: {msg.get('name')}")
        elif msg_type == "function_call_end":
            self.get_logger().info(f"Function call ended: {msg.get('call_id')}")

    def _handle_audio_down(self, msg: dict):
        """Handle incoming audio from cloud."""
        with self._state_lock:
            if self._state != self.STATE_SPEAKING:
                self._set_state(self.STATE_SPEAKING)
                self.get_logger().debug("Started speaking")

        # Extract PCM data
        if msg.get("binary"):
            pcm_bytes = msg.get("data", b"")
            audio = np.frombuffer(pcm_bytes, dtype=np.int16)
        else:
            import base64
            data_b64 = msg.get("data", "")
            if not data_b64:
                return
            pcm_bytes = base64.b64decode(data_b64)
            audio = np.frombuffer(pcm_bytes, dtype=np.int16)

        if len(audio) == 0:
            return

        # Resample if needed (simple linear for now)
        if self._sample_rate_out != self._sample_rate_in:
            # For Phase 1, assume cloud sends correct sample rate
            pass

        # Queue for playback in block-sized chunks
        block_size = self._playback.block_size
        for i in range(0, len(audio), block_size):
            chunk = audio[i : i + block_size]
            if len(chunk) < block_size:
                # Pad last chunk
                padded = np.zeros(block_size, dtype=np.int16)
                padded[: len(chunk)] = chunk
                chunk = padded
            self._playback.write_frame(chunk)

    # ─────────────────────────────── State Machine Helpers ───────────────────────────────

    def _set_state(self, new_state: str):
        with self._state_lock:
            old_state = self._state
            if old_state == new_state:
                return
            self._state = new_state
        self.get_logger().info(f"State: {old_state} -> {new_state}")
        self._state_pub.publish(String(data=new_state))

    def _start_silence_timer(self):
        """Start timer to transition from PROCESSING back to IDLE."""
        self._cancel_silence_timer()
        self._silence_timer = threading.Timer(
            self._conversation_timeout_sec,
            self._on_conversation_timeout
        )
        self._silence_timer.daemon = True
        self._silence_timer.start()

    def _cancel_silence_timer(self):
        if self._silence_timer:
            self._silence_timer.cancel()
            self._silence_timer = None

    def _on_conversation_timeout(self):
        """Called when no activity for conversation_timeout_sec."""
        with self._state_lock:
            if self._state in (self.STATE_PROCESSING, self.STATE_IDLE):
                self.get_logger().info("Conversation timeout — returning to idle")
                self._set_state(self.STATE_IDLE)
        self._silence_timer = None

    # ─────────────────────────────── Lifecycle ───────────────────────────────

    def destroy_node(self):
        self.get_logger().info("Shutting down VoiceStreamingNode...")
        self.stop_streaming()
        if hasattr(self, '_state_timer'):
            self._state_timer.cancel()
        if hasattr(self, '_auto_start_timer'):
            self._auto_start_timer.cancel()
        super().destroy_node()
        self.get_logger().info("Shutdown complete")


def main(args=None):
    rclpy.init(args=args)
    node = VoiceStreamingNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

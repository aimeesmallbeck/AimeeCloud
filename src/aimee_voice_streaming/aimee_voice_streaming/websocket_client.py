#!/usr/bin/env python3
"""Async WebSocket client for AimeeCloud audio streaming gateway.

Runs in a background thread with its own asyncio event loop.
"""

import asyncio
import base64
import json
import logging
import threading
import time
from typing import Callable, Optional

import numpy as np

try:
    import websockets
except ImportError:
    websockets = None

logger = logging.getLogger(__name__)


class AudioWebSocketClient:
    """WebSocket client that connects to AimeeCloud audio gateway."""

    def __init__(
        self,
        gateway_url: str,
        api_key: str,
        device_id: str,
        session_id: str,
        capabilities: dict,
        robot_name: str = "Aimee",
        robot_personality: str = "Adorable Brat",
        gemini_voice: str = "Leda",
        provider: str = "gemini",
        robot_config: Optional[dict] = None,
        session_context: Optional[dict] = None,
        on_message: Optional[Callable[[dict], None]] = None,
        on_connected: Optional[Callable[[], None]] = None,
        on_disconnected: Optional[Callable[[], None]] = None,
        reconnect_interval_sec: float = 5.0,
    ):
        self.gateway_url = gateway_url
        self.api_key = api_key
        self.device_id = device_id
        self.session_id = session_id
        self.capabilities = capabilities
        self.robot_name = robot_name
        self.robot_personality = robot_personality
        self.gemini_voice = gemini_voice
        self.provider = provider
        self.robot_config = robot_config
        self.session_context = session_context
        self.on_message = on_message
        self.on_connected = on_connected
        self.on_disconnected = on_disconnected
        self.reconnect_interval_sec = reconnect_interval_sec

        self._ws = None
        self._connected = False
        self._should_run = False
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self._seq = 0

    def start(self):
        """Start the WebSocket client in a background thread."""
        if self._thread is not None and self._thread.is_alive():
            logger.warning("WebSocket client already running")
            return
        self._should_run = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        logger.info("WebSocket client thread started")

    def stop(self):
        """Stop the WebSocket client."""
        self._should_run = False
        if self._loop and self._loop.is_running():
            # Schedule close on the event loop
            asyncio.run_coroutine_threadsafe(self._disconnect(), self._loop)
        if self._thread:
            self._thread.join(timeout=5.0)
            self._thread = None
        logger.info("WebSocket client stopped")

    def _run_loop(self):
        """Thread target: run asyncio event loop."""
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_until_complete(self._connect_loop())
        except Exception as e:
            logger.error(f"WebSocket event loop error: {e}")
        finally:
            self._loop.close()
            self._loop = None

    async def _connect_loop(self):
        """Main connection loop with auto-reconnect."""
        while self._should_run:
            try:
                if websockets is None:
                    logger.error("websockets library not installed")
                    await asyncio.sleep(self.reconnect_interval_sec)
                    continue

                logger.info(f"Connecting to {self.gateway_url} ...")
                async with websockets.connect(
                    self.gateway_url,
                    ping_interval=20,
                    ping_timeout=10,
                ) as ws:
                    self._ws = ws
                    self._connected = True
                    logger.info("WebSocket connected")

                    # Send session start
                    await self._send_json({
                        "type": "session_start",
                        "api_key": self.api_key,
                        "device_id": self.device_id,
                        "session_id": self.session_id or None,
                        "robot_name": self.robot_name,
                        "robot_personality": self.robot_personality,
                        "gemini_voice": self.gemini_voice,
                        "provider": self.provider,
                        "robot_config": self.robot_config,
                        "session_context": self.session_context,
                        "capabilities": self.capabilities,
                        "timestamp": self._iso_timestamp(),
                    })

                    if self.on_connected:
                        try:
                            self.on_connected()
                        except Exception as e:
                            logger.error(f"on_connected callback error: {e}")

                    # Receive loop
                    await self._receive_loop()

            except websockets.exceptions.ConnectionClosed as e:
                logger.warning(f"WebSocket closed: {e}")
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
            finally:
                with self._lock:
                    self._connected = False
                    self._ws = None
                if self.on_disconnected:
                    try:
                        self.on_disconnected()
                    except Exception as e:
                        logger.error(f"on_disconnected callback error: {e}")

            if self._should_run:
                logger.info(f"Reconnecting in {self.reconnect_interval_sec}s ...")
                await asyncio.sleep(self.reconnect_interval_sec)

    async def _receive_loop(self):
        """Receive messages from WebSocket."""
        while self._should_run and self._ws:
            try:
                msg = await self._ws.recv()
                if isinstance(msg, bytes):
                    # Binary audio frame
                    self._handle_binary(msg)
                else:
                    # Text/JSON message
                    self._handle_text(msg)
            except websockets.exceptions.ConnectionClosed:
                break
            except Exception as e:
                logger.error(f"Receive error: {e}")
                break

    def _handle_text(self, msg: str):
        """Handle text/JSON message."""
        try:
            data = json.loads(msg)
        except json.JSONDecodeError:
            logger.warning(f"Received non-JSON text: {msg[:100]}")
            return

        msg_type = data.get("type", "unknown")
        if msg_type == "session_ready":
            logger.info(f"Session ready: {data.get('session_id')}")
        elif msg_type == "error":
            logger.error(f"Gateway error: {data.get('code')} - {data.get('message')}")
        elif msg_type == "function_call_start":
            logger.info(f"Function call started: {data.get('name')}")
        elif msg_type == "function_call_end":
            logger.info(f"Function call ended: {data.get('call_id')}")
        elif msg_type == "interrupted":
            logger.info("Interrupted by user")

        if self.on_message:
            try:
                self.on_message(data)
            except Exception as e:
                logger.error(f"on_message callback error: {e}")

    def _handle_binary(self, data: bytes):
        """Handle binary audio frame."""
        # Forward to on_message as a synthetic audio_chunk message
        if self.on_message:
            try:
                self.on_message({
                    "type": "audio_chunk",
                    "format": "pcm16",
                    "data": data,
                    "binary": True,
                })
            except Exception as e:
                logger.error(f"on_message binary callback error: {e}")

    def send_audio(self, frame: np.ndarray):
        """Send audio frame to WebSocket (thread-safe)."""
        if not self.is_connected or self._ws is None or self._loop is None:
            return False

        self._seq += 1
        # Convert numpy int16 to bytes
        pcm_bytes = frame.astype(np.int16).tobytes()

        try:
            # For Phase 1, send as base64 JSON for simplicity
            # In Phase 2, switch to binary Opus frames
            payload = {
                "type": "audio_chunk",
                "seq": self._seq,
                "format": "pcm16",
                "sample_rate": self.capabilities.get("audio_in", {}).get("sample_rate", 16000),
                "data": base64.b64encode(pcm_bytes).decode("utf-8"),
            }
            asyncio.run_coroutine_threadsafe(
                self._send_json(payload), self._loop
            )
            return True
        except Exception as e:
            logger.debug(f"Send audio error: {e}")
            return False

    def send_event(self, event_type: str, payload: Optional[dict] = None):
        """Send an event message (e.g., vad_event, interrupt)."""
        if not self.is_connected or self._ws is None or self._loop is None:
            return False

        msg = {"type": event_type}
        if payload:
            msg.update(payload)
        try:
            asyncio.run_coroutine_threadsafe(
                self._send_json(msg), self._loop
            )
            return True
        except Exception as e:
            logger.debug(f"Send event error: {e}")
            return False

    async def _send_json(self, data: dict):
        """Async send JSON (must be called from event loop)."""
        if self._ws:
            await self._ws.send(json.dumps(data))

    async def _disconnect(self):
        """Async disconnect (must be called from event loop)."""
        if self._ws:
            await self._ws.close()
            self._ws = None

    @property
    def is_connected(self) -> bool:
        with self._lock:
            return self._connected and self._ws is not None

    @staticmethod
    def _iso_timestamp() -> str:
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

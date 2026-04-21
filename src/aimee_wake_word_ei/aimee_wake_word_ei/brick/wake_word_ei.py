#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
wake_word_ei Brick - Wake word detection using Edge Impulse keyword spotting model

This brick continuously listens for the 'aimee' wake word using an Edge Impulse
keyword spotting model and publishes detection events to ROS2 topics.

The brick runs the Edge Impulse model.eim executable which handles audio capture
and inference, then parses the output to detect when the wake word is spoken.
"""

import asyncio
import json
import logging
import os
import signal
import subprocess
import threading
import time
import uuid
from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass, field

from arduino.app_utils import brick

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class WakeWordConfig:
    """Configuration for wake word detection."""
    model_path: str = "/home/arduino/.arduino-bricks/models/custom-ei/ei-model-953002-1/model.eim"
    target_keyword: str = "aimee"
    confidence_threshold: float = 0.70
    cooldown_seconds: float = 2.0  # Minimum time between detections
    debug: bool = False


@dataclass
class DetectionResult:
    """Result of a wake word detection."""
    detected: bool = False
    keyword: str = ""
    confidence: float = 0.0
    timestamp: float = field(default_factory=time.time)
    session_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])


class WakeWordEIBrickError(Exception):
    """Custom exception for WakeWordEIBrick errors."""
    pass


@brick
class WakeWordEIBrick:
    """
    Wake word detection using Edge Impulse keyword spotting model.
    
    This brick runs the Edge Impulse model.eim executable which handles:
    - Audio capture from microphone
    - Keyword spotting inference
    - Continuous classification output
    
    The brick parses the classification output and triggers callbacks when
    the target keyword ("aimee") is detected with sufficient confidence.
    
    Attributes:
        model_path: Path to the Edge Impulse .eim model file
        target_keyword: The keyword to detect (default: "aimee")
        confidence_threshold: Minimum confidence to trigger detection (0.0-1.0)
        cooldown_seconds: Minimum time between detections
        debug: Enable debug logging
        
    Example:
        >>> brick = WakeWordEIBrick(
        ...     model_path="/path/to/model.eim",
        ...     confidence_threshold=0.70,
        ...     debug=True
        ... )
        >>> await brick.initialize()
        >>> brick.on_wake_word(lambda det: print(f"Detected: {det.keyword}"))
        >>> await brick.start_listening()
        >>> # Run for a while...
        >>> await brick.shutdown()
    """
    
    def __init__(
        self,
        model_path: Optional[str] = None,
        target_keyword: str = "aimee",
        confidence_threshold: float = 0.70,
        cooldown_seconds: float = 2.0,
        audio_device: str = "default",
        debug: bool = False,
        **kwargs
    ):
        """
        Initialize the WakeWordEIBrick.
        
        Args:
            model_path: Path to Edge Impulse .eim model (default uses built-in model)
            target_keyword: Keyword to detect (default: "aimee")
            confidence_threshold: Minimum confidence threshold (0.0-1.0, default 0.70)
            cooldown_seconds: Cooldown between detections (default: 2.0s)
            audio_device: ALSA audio device to use (default: "default")
            debug: Enable debug logging
            **kwargs: Additional arguments
        """
        # Set default model path if not provided
        if model_path is None:
            model_path = "/home/arduino/.arduino-bricks/models/custom-ei/ei-model-953002-1/model.eim"
        
        self.config = WakeWordConfig(
            model_path=model_path,
            target_keyword=target_keyword,
            confidence_threshold=confidence_threshold,
            cooldown_seconds=cooldown_seconds,
            debug=debug
        )
        
        self.audio_device = audio_device
        self._initialized = False
        self._running = False
        self._listening = False
        self._lock = asyncio.Lock()
        
        # Edge Impulse process
        self._ei_process: Optional[subprocess.Popen] = None
        self._ei_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        
        # Callbacks
        self._wake_word_callbacks: list[Callable[[DetectionResult], None]] = []
        self._classification_callbacks: list[Callable[[Dict[str, float]], None]] = []
        
        # State tracking
        self._last_detection_time: float = 0.0
        self._session_id: str = str(uuid.uuid4())[:8]
        self._detection_count: int = 0
        
        # Latest classification results
        self._latest_classifications: Dict[str, float] = {}
        
        if debug:
            logging.basicConfig(level=logging.DEBUG)
            
        logger.info(f"WakeWordEIBrick initialized: target='{target_keyword}', "
                   f"threshold={confidence_threshold}, model={model_path}")
        
    async def initialize(self) -> "WakeWordEIBrick":
        """
        Initialize the brick and verify the model exists.
        
        Returns:
            self for method chaining
            
        Raises:
            WakeWordEIBrickError: If model file doesn't exist or is invalid
        """
        async with self._lock:
            if self._initialized:
                logger.warning("Already initialized, skipping")
                return self
                
            # Verify model file exists
            if not os.path.exists(self.config.model_path):
                raise WakeWordEIBrickError(
                    f"Model file not found: {self.config.model_path}"
                )
            
            # Verify model is executable
            if not os.access(self.config.model_path, os.X_OK):
                logger.warning(f"Model may not be executable: {self.config.model_path}")
            
            # Test model by getting info
            try:
                model_info = await self._get_model_info()
                labels = model_info.get("model_parameters", {}).get("labels", [])
                logger.info(f"Model loaded successfully. Labels: {labels}")
                
                # Verify target keyword is in model labels
                if self.config.target_keyword not in labels:
                    logger.warning(
                        f"Target keyword '{self.config.target_keyword}' not found "
                        f"in model labels: {labels}"
                    )
            except Exception as e:
                logger.warning(f"Could not verify model info: {e}")
            
            self._initialized = True
            logger.info("WakeWordEIBrick initialization complete")
                
        return self
    
    async def _get_model_info(self) -> Dict[str, Any]:
        """Get model information from the EIM executable."""
        try:
            proc = await asyncio.create_subprocess_exec(
                self.config.model_path,
                "--print-info",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=10.0)
            
            # Parse JSON output (skip non-JSON lines)
            output = stdout.decode('utf-8', errors='ignore')
            for line in output.split('\n'):
                line = line.strip()
                if line and line.startswith('{'):
                    return json.loads(line)
            return {}
        except asyncio.TimeoutError:
            raise WakeWordEIBrickError("Timeout getting model info")
        except json.JSONDecodeError as e:
            raise WakeWordEIBrickError(f"Invalid model info JSON: {e}")
    
    def on_wake_word(self, callback: Callable[[DetectionResult], None]):
        """
        Register a callback to be called when wake word is detected.
        
        Args:
            callback: Function that receives DetectionResult
        """
        self._wake_word_callbacks.append(callback)
        logger.debug(f"Registered wake word callback. Total: {len(self._wake_word_callbacks)}")
        
    def on_classification(self, callback: Callable[[Dict[str, float]], None]):
        """
        Register a callback for all classification results (for monitoring).
        
        Args:
            callback: Function that receives classification dict
        """
        self._classification_callbacks.append(callback)
        
    def remove_callback(self, callback: Callable):
        """Remove a previously registered callback."""
        if callback in self._wake_word_callbacks:
            self._wake_word_callbacks.remove(callback)
        if callback in self._classification_callbacks:
            self._classification_callbacks.remove(callback)
    
    async def start_listening(self):
        """
        Start listening for the wake word.
        
        This launches the Edge Impulse model process and begins parsing
        classification results.
        
        Raises:
            WakeWordEIBrickError: If not initialized or already listening
        """
        if not self._initialized:
            raise WakeWordEIBrickError("Brick not initialized. Call initialize() first.")
        
        async with self._lock:
            if self._listening:
                logger.warning("Already listening, skipping")
                return
            
            self._stop_event.clear()
            self._listening = True
            self._running = True
            
            # Start the EI process in a separate thread
            self._ei_thread = threading.Thread(target=self._run_ei_process, daemon=True)
            self._ei_thread.start()
            
            logger.info("Wake word listening started")
    
    def _run_ei_process(self):
        """
        Run the Edge Impulse model process and parse output.
        
        This runs in a separate thread to handle the blocking subprocess I/O.
        """
        try:
            # Start the model with stdin mode (expects audio data)
            # For microphone input, we use socket mode or the built-in microphone support
            logger.info(f"Starting EI model: {self.config.model_path}")
            
            # The EIM model supports running with microphone directly
            # Using socket mode for better control
            import socket
            import struct
            
            # Create a socket for the model to connect to
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            socket_path = "/tmp/ei_wake_word.sock"
            
            # Remove old socket if exists
            try:
                os.unlink(socket_path)
            except FileNotFoundError:
                pass
            
            sock.bind(socket_path)
            sock.listen(1)
            
            # Start the model process with socket argument
            self._ei_process = subprocess.Popen(
                [self.config.model_path, socket_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1  # Line buffered
            )
            
            # Accept connection from model
            conn, addr = sock.accept()
            logger.debug("EI model connected to socket")
            
            # Read and parse output lines
            while not self._stop_event.is_set() and self._ei_process.poll() is None:
                try:
                    line = self._ei_process.stdout.readline()
                    if not line:
                        time.sleep(0.01)
                        continue
                    
                    self._parse_ei_output(line.strip())
                    
                except Exception as e:
                    if self.config.debug:
                        logger.debug(f"Error parsing EI output: {e}")
                    
        except Exception as e:
            logger.error(f"EI process error: {e}")
        finally:
            self._listening = False
            logger.info("EI process thread ended")
    
    def _parse_ei_output(self, line: str):
        """
        Parse a line of output from the Edge Impulse model.
        
        Expected format (JSON):
        {"classification": {"aimee": 0.85, "noise": 0.10, "unknown": 0.05}}
        or similar variations depending on model output format.
        """
        if not line:
            return
        
        try:
            # Try to parse as JSON
            if line.startswith('{'):
                data = json.loads(line)
                
                # Handle classification results
                if 'classification' in data:
                    classifications = data['classification']
                    self._latest_classifications = classifications
                    
                    # Notify classification callbacks
                    for callback in self._classification_callbacks:
                        try:
                            callback(classifications)
                        except Exception as e:
                            logger.error(f"Classification callback error: {e}")
                    
                    # Check for target keyword
                    target = self.config.target_keyword
                    if target in classifications:
                        confidence = float(classifications[target])
                        
                        if confidence >= self.config.confidence_threshold:
                            self._handle_detection(target, confidence)
                            
        except json.JSONDecodeError:
            # Not JSON, might be debug output
            if self.config.debug:
                logger.debug(f"EI output: {line}")
        except Exception as e:
            logger.error(f"Error parsing EI output '{line}': {e}")
    
    def _handle_detection(self, keyword: str, confidence: float):
        """
        Handle a wake word detection.
        
        Applies cooldown and notifies callbacks.
        """
        now = time.time()
        
        # Check cooldown
        if now - self._last_detection_time < self.config.cooldown_seconds:
            return
        
        self._last_detection_time = now
        self._detection_count += 1
        
        result = DetectionResult(
            detected=True,
            keyword=keyword,
            confidence=confidence,
            timestamp=now,
            session_id=self._session_id
        )
        
        logger.info(f"WAKE WORD DETECTED: '{keyword}' (confidence: {confidence:.2f})")
        
        # Notify callbacks
        for callback in self._wake_word_callbacks:
            try:
                callback(result)
            except Exception as e:
                logger.error(f"Wake word callback error: {e}")
    
    async def stop_listening(self):
        """Stop listening for wake word."""
        async with self._lock:
            if not self._listening:
                return
            
            self._stop_event.set()
            self._listening = False
            
            # Terminate EI process
            if self._ei_process and self._ei_process.poll() is None:
                try:
                    self._ei_process.terminate()
                    await asyncio.sleep(0.5)
                    if self._ei_process.poll() is None:
                        self._ei_process.kill()
                except Exception as e:
                    logger.error(f"Error stopping EI process: {e}")
            
            # Wait for thread to finish
            if self._ei_thread and self._ei_thread.is_alive():
                self._ei_thread.join(timeout=2.0)
            
            logger.info("Wake word listening stopped")
    
    def get_latest_classifications(self) -> Dict[str, float]:
        """Get the most recent classification results."""
        return self._latest_classifications.copy()
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current status of the brick.
        
        Returns:
            Dictionary with status information
        """
        return {
            "initialized": self._initialized,
            "listening": self._listening,
            "running": self._running,
            "target_keyword": self.config.target_keyword,
            "confidence_threshold": self.config.confidence_threshold,
            "detection_count": self._detection_count,
            "session_id": self._session_id,
            "latest_classifications": self._latest_classifications,
        }
    
    async def shutdown(self):
        """
        Clean up resources and shutdown.
        
        This method should be called when the brick is no longer needed.
        """
        async with self._lock:
            if not self._initialized:
                return
            
            logger.info("Shutting down WakeWordEIBrick...")
            
            try:
                await self.stop_listening()
                self._running = False
                self._initialized = False
                
                # Clear callbacks
                self._wake_word_callbacks.clear()
                self._classification_callbacks.clear()
                
                logger.info("Shutdown complete")
                
            except Exception as e:
                logger.error(f"Error during shutdown: {e}")
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.shutdown()

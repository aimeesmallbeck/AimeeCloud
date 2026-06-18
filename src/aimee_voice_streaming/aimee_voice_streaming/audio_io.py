#!/usr/bin/env python3
"""Audio I/O module using sounddevice + numpy.

Provides non-blocking audio capture and playback with queue-based
threading for integration with ROS2/WebSocket loops.
"""

import logging
import queue
import threading
import time
from typing import Optional, Callable

import numpy as np

try:
    import sounddevice as sd
except ImportError:
    sd = None

logger = logging.getLogger(__name__)


class AudioCapture:
    """Capture audio from microphone using sounddevice callback."""

    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        block_duration_ms: int = 20,
        device_index: Optional[int] = None,
        dtype=np.int16,
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.block_size = int(sample_rate * block_duration_ms / 1000)
        self.device_index = device_index
        self.dtype = dtype
        self._queue: queue.Queue = queue.Queue(maxsize=100)
        self._stream = None
        self._running = False
        self._lock = threading.Lock()

    def start(self) -> bool:
        if sd is None:
            logger.error("sounddevice not installed. Cannot start audio capture.")
            return False
        with self._lock:
            if self._running:
                return True
            try:
                self._stream = sd.InputStream(
                    samplerate=self.sample_rate,
                    blocksize=self.block_size,
                    dtype=self.dtype,
                    channels=self.channels,
                    device=self.device_index if self.device_index >= 0 else None,
                    callback=self._callback,
                )
                self._stream.start()
                self._running = True
                logger.info(
                    f"Audio capture started: {self.sample_rate}Hz, "
                    f"{self.channels}ch, block={self.block_size}"
                )
                return True
            except Exception as e:
                logger.error(f"Failed to start audio capture: {e}")
                return False

    def stop(self):
        with self._lock:
            if not self._running:
                return
            self._running = False
            if self._stream:
                try:
                    self._stream.stop()
                    self._stream.close()
                except Exception as e:
                    logger.warning(f"Error stopping capture stream: {e}")
                self._stream = None
            logger.info("Audio capture stopped")

    def _callback(self, indata, frames, time_info, status):
        if status:
            logger.debug(f"Audio capture status: {status}")
        try:
            # indata is a numpy array; copy it
            arr = indata.copy()
            # If 2D with 1 channel, flatten it
            if arr.ndim > 1 and arr.shape[1] == 1:
                arr = arr.flatten()
            self._queue.put_nowait(arr)
        except queue.Full:
            # Drop oldest frame to avoid unbounded growth
            try:
                self._queue.get_nowait()
                self._queue.put_nowait(arr)
            except queue.Empty:
                pass

    def read_frame(self, timeout: float = 0.1) -> Optional[np.ndarray]:
        """Read one audio frame from the queue."""
        try:
            return self._queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def drain(self):
        """Clear the capture queue."""
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break


class AudioPlayback:
    """Playback audio to speaker using sounddevice callback."""

    def __init__(
        self,
        sample_rate: int = 24000,
        channels: int = 1,
        block_duration_ms: int = 20,
        device_index: Optional[int] = None,
        dtype=np.int16,
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.block_size = int(sample_rate * block_duration_ms / 1000)
        self.device_index = device_index
        self.dtype = dtype
        self._queue: queue.Queue = queue.Queue(maxsize=200)
        self._stream = None
        self._running = False
        self._lock = threading.Lock()
        self._silence = np.zeros((self.block_size, self.channels), dtype=self.dtype)

    def start(self) -> bool:
        if sd is None:
            logger.error("sounddevice not installed. Cannot start audio playback.")
            return False
        with self._lock:
            if self._running:
                return True
            try:
                self._stream = sd.OutputStream(
                    samplerate=self.sample_rate,
                    blocksize=self.block_size,
                    dtype=self.dtype,
                    channels=self.channels,
                    device=self.device_index if self.device_index >= 0 else None,
                    callback=self._callback,
                )
                self._stream.start()
                self._running = True
                logger.info(
                    f"Audio playback started: {self.sample_rate}Hz, "
                    f"{self.channels}ch, block={self.block_size}"
                )
                return True
            except Exception as e:
                logger.error(f"Failed to start audio playback: {e}")
                return False

    def stop(self):
        with self._lock:
            if not self._running:
                return
            self._running = False
            # Flush remaining audio
            time.sleep(0.1)
            if self._stream:
                try:
                    self._stream.stop()
                    self._stream.close()
                except Exception as e:
                    logger.warning(f"Error stopping playback stream: {e}")
                self._stream = None
            logger.info("Audio playback stopped")

    def _callback(self, outdata, frames, time_info, status):
        if status:
            logger.debug(f"Audio playback status: {status}")
        try:
            frame = self._queue.get_nowait()
            if frame.ndim == 1 and outdata.ndim == 2:
                frame = frame.reshape(-1, 1)
            
            if len(frame) >= len(outdata):
                outdata[:] = frame[: len(outdata)]
            else:
                outdata[: len(frame)] = frame
                outdata[len(frame) :] = 0
        except queue.Empty:
            outdata[:] = self._silence

    def write_frame(self, frame: np.ndarray) -> bool:
        """Queue an audio frame for playback."""
        try:
            self._queue.put_nowait(np.copy(frame))
            return True
        except queue.Full:
            logger.warning("Playback queue full, dropping frame")
            return False

    def write_silence(self, num_frames: int = 1):
        """Queue silence frames."""
        for _ in range(num_frames):
            self.write_frame(self._silence)

    def drain(self):
        """Clear the playback queue."""
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break

    @property
    def queue_size(self) -> int:
        return self._queue.qsize()

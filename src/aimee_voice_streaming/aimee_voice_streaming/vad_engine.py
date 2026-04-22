#!/usr/bin/env python3
"""Voice Activity Detection wrapper.

Supports webrtcvad (lightweight, no ML deps) as the default.
Silero VAD can be added later as an optional enhancement.
"""

import logging
import collections
from typing import Optional

import numpy as np

try:
    import webrtcvad
except ImportError:
    webrtcvad = None

logger = logging.getLogger(__name__)


class VADEngine:
    """Voice Activity Detection engine with smoothing."""

    def __init__(
        self,
        mode: int = 2,  # 0=normal, 1=low_bitrate, 2=aggressive, 3=very_aggressive
        sample_rate: int = 16000,
        frame_duration_ms: int = 20,
        padding_duration_ms: int = 300,
        silence_duration_ms: int = 500,
    ):
        self.mode = mode
        self.sample_rate = sample_rate
        self.frame_duration_ms = frame_duration_ms
        self.frame_size = int(sample_rate * frame_duration_ms / 1000)
        self.padding_frames = int(padding_duration_ms / frame_duration_ms)
        self.silence_frames = int(silence_duration_ms / frame_duration_ms)

        self._vad = None
        self._available = False

        if webrtcvad is None:
            logger.error("webrtcvad not installed. VAD will always return True.")
            self._available = False
        else:
            try:
                self._vad = webrtcvad.Vad(mode)
                self._available = True
                logger.info(f"webrtcvad initialized (mode={mode})")
            except Exception as e:
                logger.error(f"Failed to initialize webrtcvad: {e}")
                self._available = False

        # Ring buffer for prefix padding (keep audio before speech detected)
        self._ring_buffer: collections.deque = collections.deque(maxlen=self.padding_frames)
        self._triggered = False
        self._silence_count = 0
        self._speech_count = 0
        self._min_speech_frames = 3  # At least 60ms of speech to trigger

    def reset(self):
        """Reset VAD state."""
        self._ring_buffer.clear()
        self._triggered = False
        self._silence_count = 0
        self._speech_count = 0

    def process(self, frame: np.ndarray) -> tuple[bool, bool, list[np.ndarray]]:
        """Process one audio frame.

        Returns:
            (is_speech, speech_finished, buffered_frames)
            - is_speech: whether this frame contains speech
            - speech_finished: whether speech segment has ended
            - buffered_frames: prefix padding frames to prepend when speech starts
        """
        if not self._available or self._vad is None:
            # Fallback: assume all frames are speech
            return True, False, []

        # Ensure frame is the right size
        if len(frame) < self.frame_size:
            # Pad with silence
            padded = np.zeros(self.frame_size, dtype=frame.dtype)
            padded[: len(frame)] = frame.flatten()
            frame = padded
        else:
            frame = frame[: self.frame_size].flatten()

        # Convert to bytes (webrtcvad expects 16-bit PCM bytes)
        pcm_bytes = frame.astype(np.int16).tobytes()

        try:
            is_speech = self._vad.is_speech(pcm_bytes, self.sample_rate)
        except Exception as e:
            logger.debug(f"webrtcvad error: {e}")
            is_speech = False

        if not self._triggered:
            self._ring_buffer.append(np.copy(frame))
            if is_speech:
                self._speech_count += 1
                if self._speech_count >= self._min_speech_frames:
                    self._triggered = True
                    self._silence_count = 0
                    # Return buffered prefix frames
                    buffered = list(self._ring_buffer)
                    self._ring_buffer.clear()
                    return True, False, buffered
            else:
                self._speech_count = max(0, self._speech_count - 1)
            return False, False, []
        else:
            if is_speech:
                self._silence_count = 0
                return True, False, []
            else:
                self._silence_count += 1
                if self._silence_count >= self.silence_frames:
                    self._triggered = False
                    self._silence_count = 0
                    self._speech_count = 0
                    self._ring_buffer.clear()
                    return False, True, []
                return True, False, []  # Still in speech segment during silence gap

    @property
    def state(self) -> str:
        """Current VAD state for debugging."""
        return "triggered" if self._triggered else "idle"

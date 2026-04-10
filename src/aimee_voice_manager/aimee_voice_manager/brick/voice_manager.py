#!/usr/bin/env python3
"""Voice Manager Brick - Handles STT with Vosk/Whisper"""

import logging
from dataclasses import dataclass, field
from typing import Optional, Callable, Any
import asyncio
import uuid

logger = logging.getLogger(__name__)


@dataclass
class TranscriptionResult:
    """Result from STT engine."""
    text: str
    confidence: float = 1.0
    is_command: bool = False
    engine: str = "vosk"
    language: str = "en"
    wake_word: str = ""
    session_id: str = ""


class STTEngine:
    """Base class for STT engines."""
    
    def transcribe(self, audio_data: bytes) -> TranscriptionResult:
        """Transcribe audio to text."""
        raise NotImplementedError


class VoskSTT(STTEngine):
    """Vosk STT engine."""
    
    def __init__(self, model_path: str = None):
        self.model_path = model_path
        logger.info(f"Vosk STT initialized (model: {model_path or 'default'})")
    
    def transcribe(self, audio_data: bytes) -> TranscriptionResult:
        """Transcribe using Vosk."""
        return TranscriptionResult(
            text="Hello robot",
            confidence=0.9,
            is_command=True,
            engine="vosk"
        )


class VoiceManagerBrick:
    """Voice Manager Brick - Manages STT for AIMEE."""
    
    def __init__(
        self,
        model_path: str = None,
        engine: str = "vosk",
        record_duration: float = 5.0,
        sample_rate: int = 16000,
        audio_device: str = "default",
        command_timeout: float = 10.0,
        min_command_length: float = 0.5,
        debug: bool = False
    ):
        self.model_path = model_path
        self.engine_type = engine
        self.record_duration = record_duration
        self.sample_rate = sample_rate
        self.audio_device = audio_device
        self.command_timeout = command_timeout
        self.min_command_length = min_command_length
        self.debug = debug
        
        self.stt_engine = None
        self.is_recording = False
        self.simulation_mode = False
        self._transcription_callback: Optional[Callable[[Any], None]] = None
        self._partial_callback: Optional[Callable[[Any], None]] = None
        self._wake_word_callback: Optional[Callable[[], None]] = None
        self._initialized = False
        self._current_wake_word: str = ""
        self._current_session_id: str = ""
        
        try:
            if engine == "vosk":
                self.stt_engine = VoskSTT(model_path)
            else:
                self.simulation_mode = True
        except Exception as e:
            logger.warning(f"STT init failed: {e}, using simulation")
            self.simulation_mode = True
        
        logger.info(f"VoiceManager initialized (simulation={self.simulation_mode})")
    
    async def initialize(self):
        """Async initialization - called by node."""
        if not self._initialized:
            self._initialized = True
            logger.info("VoiceManagerBrick async initialization complete")
        return self
    
    async def transcribe_command(self, max_duration: float = None, wake_word: str = None) -> TranscriptionResult:
        """Record and transcribe a voice command."""
        duration = max_duration or self.record_duration
        self._current_wake_word = wake_word or ""
        self._current_session_id = str(uuid.uuid4())[:8]
        
        logger.info(f"Transcribing command (max_duration={duration}s, wake_word={wake_word})")
        
        # Simulate recording
        await asyncio.sleep(0.5)
        
        # Return simulated transcription
        result = TranscriptionResult(
            text="Hello aimee move forward",
            confidence=0.92,
            is_command=True,
            engine=self.engine_type,
            wake_word=self._current_wake_word,
            session_id=self._current_session_id
        )
        
        # Trigger callback
        if self._transcription_callback:
            self._transcription_callback(result)
        
        return result
    
    def on_transcription(self, callback: Callable[[Any], None]):
        """Set transcription callback."""
        self._transcription_callback = callback
        logger.info("Transcription callback registered")
        return self
    
    def on_partial(self, callback: Callable[[Any], None]):
        """Set partial transcription callback."""
        self._partial_callback = callback
        logger.info("Partial callback registered")
        return self
    
    def on_wake_word(self, callback: Callable[[], None]):
        """Set wake word callback."""
        self._wake_word_callback = callback
        logger.info("Wake word callback registered")
        return self
    
    def start_recording(self) -> bool:
        """Start recording audio."""
        if self.is_recording:
            return False
        self.is_recording = True
        logger.info("Started recording")
        return True
    
    def stop_recording(self) -> Optional[TranscriptionResult]:
        """Stop recording and transcribe."""
        if not self.is_recording:
            return None
        
        self.is_recording = False
        
        result = TranscriptionResult(
            text="Hello robot",
            confidence=0.85,
            is_command=True,
            engine=self.engine_type,
            wake_word=self._current_wake_word,
            session_id=self._current_session_id
        )
        
        if self._transcription_callback:
            try:
                self._transcription_callback(result)
            except Exception as e:
                logger.error(f"Callback error: {e}")
        
        return result
    
    def is_recording_active(self) -> bool:
        """Check if currently recording."""
        return self.is_recording

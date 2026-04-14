#!/usr/bin/env python3
"""Voice Manager Brick - Real continuous STT with Vosk"""

import array
import json
import logging
import math
import os
import subprocess
import threading
import time
from dataclasses import dataclass, field
from typing import Optional, Callable, Any, Dict, Set

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


class VoiceManagerBrick:
    """Voice Manager Brick - Continuous Vosk STT for AIMEE."""

    def __init__(
        self,
        model_path: str = None,
        engine: str = "vosk",
        record_duration: float = 5.0,
        sample_rate: int = 16000,
        audio_device: str = "dsnoop:1,0",
        command_timeout: float = 10.0,
        min_command_length: float = 0.5,
        debug: bool = False
    ):
        self.model_path = model_path or "/home/arduino/vosk-models/vosk-model-small-en-us-0.15"
        self.engine_type = engine
        self.record_duration = record_duration
        self.sample_rate = sample_rate
        self.audio_device = audio_device
        self.command_timeout = command_timeout
        self.min_command_length = min_command_length
        self.debug = debug

        # Audio energy gate: minimum RMS for audio to be considered speech
        self.energy_threshold = 120

        # Garbage words to suppress from ambient noise
        self.garbage_words: Set[str] = {"huh", "who", "um", "mm", "mhm", "uh", "eh", "hm", "hmm"}

        self._vosk_model = None
        self._recognizer = None
        self._arecord_proc = None
        self._listening = False
        self._initialized = False
        self._listen_thread: Optional[threading.Thread] = None
        self._shutdown_event = threading.Event()

        self._transcription_callback: Optional[Callable[[Any], None]] = None
        self._partial_callback: Optional[Callable[[Any], None]] = None

        if debug:
            logging.basicConfig(level=logging.DEBUG)

        logger.info(f"VoiceManager initialized: model={self.model_path}, device={self.audio_device}, energy_threshold={self.energy_threshold}")

    async def initialize(self):
        """Async initialization - load Vosk model."""
        if self._initialized:
            return self

        try:
            from vosk import Model, KaldiRecognizer
            logger.info(f"Loading Vosk model from {self.model_path}...")
            if not os.path.exists(self.model_path):
                raise RuntimeError(f"Vosk model not found at {self.model_path}")
            self._vosk_model = Model(self.model_path)
            self._recognizer = KaldiRecognizer(self._vosk_model, self.sample_rate)
            self._initialized = True
            logger.info("Vosk model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Vosk: {e}")
            raise

        return self

    def start_listening(self):
        """Start continuous listening in a background thread."""
        if self._listening:
            logger.warning("Already listening")
            return
        if not self._initialized:
            logger.error("Brick not initialized")
            return

        self._shutdown_event.clear()
        self._listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._listen_thread.start()
        self._listening = True
        logger.info("Started continuous listening")

    def stop_listening(self):
        """Stop continuous listening."""
        if not self._listening:
            return
        self._shutdown_event.set()
        if self._arecord_proc:
            try:
                self._arecord_proc.terminate()
                self._arecord_proc.wait(timeout=2)
            except Exception as e:
                logger.warning(f"Error stopping arecord: {e}")
            self._arecord_proc = None
        self._listening = False
        logger.info("Stopped listening")

    @staticmethod
    def _audio_energy(data: bytes) -> float:
        """Compute RMS energy of a S16_LE raw audio chunk."""
        if len(data) < 2:
            return 0.0
        try:
            samples = array.array('h', data)
            if len(samples) == 0:
                return 0.0
            sum_squares = sum(s * s for s in samples)
            rms = math.sqrt(sum_squares / len(samples))
            return rms
        except Exception:
            return 0.0

    def _is_garbage(self, text: str) -> bool:
        """Check if transcription is just noise garbage."""
        clean = text.lower().strip().rstrip('.').rstrip('?').rstrip('!')
        return clean in self.garbage_words

    def _listen_loop(self):
        """Background thread: stream audio from arecord to Vosk."""
        import json as _json

        cmd = [
            "arecord", "-D", self.audio_device,
            "-f", "S16_LE", "-r", str(self.sample_rate),
            "-c", "1", "-t", "raw"
        ]

        try:
            self._arecord_proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            logger.info(f"arecord started: {' '.join(cmd)}")
        except Exception as e:
            logger.error(f"Failed to start arecord: {e}")
            self._listening = False
            return

        # Create a fresh recognizer for this session
        from vosk import KaldiRecognizer
        recognizer = KaldiRecognizer(self._vosk_model, self.sample_rate)

        # Track whether current utterance has sufficient energy
        utterance_has_energy = False

        try:
            while not self._shutdown_event.is_set():
                data = self._arecord_proc.stdout.read(4000)
                if not data:
                    time.sleep(0.01)
                    continue

                energy = self._audio_energy(data)
                if energy >= self.energy_threshold:
                    utterance_has_energy = True

                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    result_dict = _json.loads(result)
                    text = result_dict.get("text", "").strip()

                    # Require either sufficient energy OR non-garbage content
                    # (protects short valid words like "yes/no" from being dropped,
                    #  but drops quiet noise hallucinations)
                    if text and len(text) >= self.min_command_length:
                        if self._is_garbage(text) and not utterance_has_energy:
                            logger.debug(f"Dropped garbage (quiet): {text}")
                        else:
                            logger.info(f"Transcription: {text}")
                            result_obj = TranscriptionResult(
                                text=text,
                                confidence=1.0,
                                is_command=True,
                                engine=self.engine_type,
                                wake_word="",
                                session_id=""
                            )
                            if self._transcription_callback:
                                try:
                                    self._transcription_callback(result_obj)
                                except Exception as cb_err:
                                    logger.error(f"Transcription callback error: {cb_err}")

                    # Reset for next utterance
                    utterance_has_energy = False

                elif self._partial_callback:
                    partial = recognizer.PartialResult()
                    partial_dict = _json.loads(partial)
                    partial_text = partial_dict.get("partial", "").strip()
                    if partial_text:
                        partial_result = TranscriptionResult(
                            text=partial_text,
                            confidence=0.5,
                            is_command=True,
                            engine=self.engine_type,
                            wake_word="",
                            session_id=""
                        )
                        try:
                            self._partial_callback(partial_result)
                        except Exception as cb_err:
                            logger.error(f"Partial callback error: {cb_err}")

        except Exception as e:
            logger.error(f"Listen loop error: {e}")
        finally:
            if self._arecord_proc:
                try:
                    self._arecord_proc.terminate()
                    self._arecord_proc.wait(timeout=2)
                except Exception:
                    pass
                self._arecord_proc = None
            self._listening = False
            logger.info("Listen loop ended")

    async def transcribe_command(self, max_duration: float = None, wake_word: str = None) -> TranscriptionResult:
        """Legacy API - not used in continuous mode."""
        logger.warning("transcribe_command called in continuous mode - returning empty")
        return TranscriptionResult(text="", confidence=0.0, is_command=False, engine=self.engine_type)

    def on_transcription(self, callback: Callable[[Any], None]):
        """Set transcription callback."""
        self._transcription_callback = callback
        return self

    def on_partial(self, callback: Callable[[Any], None]):
        """Set partial transcription callback."""
        self._partial_callback = callback
        return self

    def on_wake_word(self, callback: Callable[[], None]):
        """Legacy - no-op in continuous mode."""
        pass

    def start_recording(self) -> bool:
        """Legacy API."""
        self.start_listening()
        return True

    def stop_recording(self) -> Optional[TranscriptionResult]:
        """Legacy API."""
        self.stop_listening()
        return None

    def is_recording_active(self) -> bool:
        """Check if currently listening."""
        return self._listening

    def get_status(self) -> Dict[str, Any]:
        """Get current status."""
        return {
            "initialized": self._initialized,
            "engine": self.engine_type,
            "listening": self._listening,
            "model_path": self.model_path,
        }

    async def shutdown(self):
        """Clean up resources."""
        logger.info("Shutting down VoiceManagerBrick...")
        self.stop_listening()
        if self._listen_thread and self._listen_thread.is_alive():
            self._listen_thread.join(timeout=2.0)
        self._initialized = False
        logger.info("Shutdown complete")

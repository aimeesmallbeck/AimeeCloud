#!/usr/bin/env python3
"""Voice Manager Brick - Real continuous STT with Vosk"""

import array
import difflib
import json
import logging
import math
import os
import subprocess
import threading
import time
from dataclasses import dataclass, field
from typing import Optional, Callable, Any, Dict, Set, List

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
        energy_threshold: float = 80.0,
        debug: bool = False,
        whisper_enabled: bool = True,
        whisper_api_key: str = "",
        whisper_api_base_url: str = "https://api.openai.com/v1/audio/transcriptions",
    ):
        self.model_path = model_path or "/home/arduino/vosk-models/vosk-model-small-en-us-0.15"
        self.engine_type = engine
        self.record_duration = record_duration
        self.sample_rate = sample_rate
        self.audio_device = audio_device
        self.command_timeout = command_timeout
        self.min_command_length = min_command_length
        self.energy_threshold = energy_threshold
        self.debug = debug
        self.whisper_enabled = whisper_enabled
        self._whisper_api_key = whisper_api_key
        self._whisper_api_base_url = whisper_api_base_url
        self._online = False
        self._online_lock = threading.Lock()

        # Garbage words to suppress from ambient noise
        self.garbage_words: Set[str] = {"huh", "who", "um", "mm", "mhm", "uh", "eh", "hm", "hmm"}

        # TTS echo suppression state
        self._tts_active = False
        self._tts_text_history: List[str] = []
        self._tts_history_lock = threading.Lock()
        self._tts_similarity_threshold = 0.60
        self._tts_energy_boost = 3.5  # multiplier while TTS is speaking
        self._tts_mute_until = 0.0  # timestamp until which all transcription is muted

        self._vosk_model = None
        self._recognizer = None
        self._arecord_proc = None
        self._listening = False
        self._initialized = False
        self._listen_thread: Optional[threading.Thread] = None
        self._shutdown_event = threading.Event()

        self._transcription_callback: Optional[Callable[[Any], None]] = None
        self._partial_callback: Optional[Callable[[Any], None]] = None
        self._health_callback: Optional[Callable[[Dict[str, Any]], None]] = None

        if debug:
            logging.basicConfig(level=logging.DEBUG)

        logger.info(f"VoiceManager initialized: model={self.model_path}, device={self.audio_device}, energy_threshold={self.energy_threshold}, whisper_enabled={self.whisper_enabled}")

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

    @staticmethod
    def _kill_orphaned_arecord(audio_device: str):
        """Kill any existing arecord processes blocking the audio device."""
        import glob
        import os
        import signal
        import subprocess
        
        # Try to find the ALSA card/device number from the device string
        # e.g., 'plughw:2,0' -> card=2, device=0
        card = None
        device = None
        if audio_device.startswith("plughw:") or audio_device.startswith("hw:"):
            try:
                parts = audio_device.split(":", 1)[1].split(",")
                card = int(parts[0])
                device = int(parts[1])
            except Exception:
                pass
        
        # Method 1: check /proc/asound status files for owner_pid
        if card is not None and device is not None:
            status_paths = glob.glob(f"/proc/asound/card{card}/pcm{device}c/sub*/status")
            for path in status_paths:
                try:
                    with open(path) as f:
                        for line in f:
                            if line.startswith("owner_pid"):
                                pid_str = line.split(":", 1)[1].strip()
                                pid = int(pid_str)
                                if pid != os.getpid() and os.path.exists(f"/proc/{pid}"):
                                    logger.warning(f"Killing orphaned audio owner PID {pid}")
                                    try:
                                        os.kill(pid, signal.SIGKILL)
                                    except ProcessLookupError:
                                        pass
                                break
                except Exception:
                    pass
        
        # Method 2: pkill any arecord using the same device argument
        try:
            subprocess.run(
                ["pkill", "-9", "-f", f"arecord.*{audio_device}"],
                capture_output=True, timeout=2
            )
        except Exception:
            pass
        
        # Method 3: broad sweep of all arecord zombies older than this process
        try:
            own_start = os.stat(f"/proc/{os.getpid()}").st_ctime
            for entry in os.listdir("/proc"):
                if not entry.isdigit():
                    continue
                try:
                    pid = int(entry)
                    cmdline = open(f"/proc/{pid}/cmdline").read().replace("\x00", " ")
                    if "arecord" in cmdline:
                        proc_start = os.stat(f"/proc/{pid}").st_ctime
                        if proc_start < own_start:
                            logger.warning(f"Killing stale arecord PID {pid}")
                            os.kill(pid, signal.SIGKILL)
                except (ProcessLookupError, PermissionError):
                    continue
        except Exception:
            pass
    
    def set_online(self, online: bool):
        """Update online connectivity state for Whisper API fallback."""
        with self._online_lock:
            if self._online != online:
                self._online = online
                logger.info(f"Voice manager online state: {online} (Whisper API {'active' if online and self.whisper_enabled else 'inactive'})")

    def start_listening(self):
        """Start continuous listening in a background thread."""
        if self._listening:
            logger.warning("Already listening")
            return
        if not self._initialized:
            logger.error("Brick not initialized")
            return

        self._kill_orphaned_arecord(self.audio_device)
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

    def set_tts_active(self, active: bool):
        """Set TTS speaking state for echo suppression."""
        if active and not self._tts_active:
            logger.debug("TTS started — echo suppression active")
        if not active and self._tts_active:
            # Keep a mute window after TTS stops to catch trailing echo
            self._tts_mute_until = time.time() + 2.0
            logger.debug(f"TTS ended — post-TTS mute window until {self._tts_mute_until:.1f}")
        self._tts_active = active
        if not active:
            # Don't clear history immediately; let the mute window + similarity check handle it
            pass
        logger.debug(f"TTS active set to {active}")

    def set_tts_text(self, text: str):
        """Record TTS text being spoken for echo correlation."""
        normalized = self._normalize_for_echo(text)
        with self._tts_history_lock:
            self._tts_text_history.append(normalized)
            # Keep last few phrases
            while len(self._tts_text_history) > 5:
                self._tts_text_history.pop(0)
        logger.debug(f"Recorded TTS text: {text} -> {normalized}")

    @staticmethod
    def _normalize_for_echo(text: str) -> str:
        """Normalize text for echo comparison."""
        import re
        clean = text.lower().strip()
        clean = re.sub(r"[^a-z0-9\s]", "", clean)
        clean = re.sub(r"\s+", " ", clean).strip()
        # Common misheard variants
        clean = clean.replace("amy", "aimee")
        return clean

    def _is_tts_echo(self, text: str) -> bool:
        """Check if transcription is the robot hearing its own TTS."""
        clean = self._normalize_for_echo(text)

        # Hard mute window after TTS finishes (catches trailing echo/reverb)
        if time.time() < self._tts_mute_until:
            logger.debug(f"Dropped transcription in post-TTS mute window: {text}")
            return True

        if not self._tts_active and not self._tts_text_history:
            return False

        with self._tts_history_lock:
            for tts_text in self._tts_text_history:
                ratio = difflib.SequenceMatcher(None, clean, tts_text).ratio()
                if ratio >= self._tts_similarity_threshold:
                    logger.info(f"Dropped TTS echo (similarity {ratio:.2f}): {text}")
                    return True
        return False

    def _effective_energy_threshold(self) -> float:
        """Return energy threshold adjusted for TTS playback."""
        if self._tts_active:
            return self.energy_threshold * self._tts_energy_boost
        return self.energy_threshold

    def _listen_loop(self):
        """Background thread: stream audio from arecord to Vosk."""
        import json as _json

        cmd = [
            "arecord", "-D", self.audio_device,
            "-f", "S16_LE", "-r", str(self.sample_rate),
            "-c", "1", "-t", "raw"
        ]

        try:
            # Use DEVNULL for stderr to prevent pipe-buffer deadlock
            # if arecord writes lots of warnings.
            self._arecord_proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
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
        utterance_buffer = bytearray()

        try:
            loop_start = time.time()
            total_bytes = 0
            bytes_since_vosk = 0
            last_health_report = 0.0
            warned_no_data = False
            warned_silence = False
            warned_vosk_stuck = False
            zero_energy_streak = 0  # count consecutive zero-energy chunks

            while not self._shutdown_event.is_set():
                data = self._arecord_proc.stdout.read(4000)
                if not data:
                    # Check if arecord died
                    if self._arecord_proc.poll() is not None:
                        logger.error(f"arecord exited with code {self._arecord_proc.returncode}")
                        self._report_health(False, "arecord_died", f"arecord exited with code {self._arecord_proc.returncode}")
                        break
                    time.sleep(0.01)
                    continue

                utterance_buffer.extend(data)
                total_bytes += len(data)
                bytes_since_vosk += len(data)
                elapsed = time.time() - loop_start

                energy = self._audio_energy(data)

                # Health check: no audio data flowing at all
                if elapsed > 5.0 and not warned_no_data and total_bytes == 0:
                    warned_no_data = True
                    logger.error("Audio capture stall: arecord is running but has produced zero bytes")
                    self._report_health(False, "audio_stall", "Microphone detected but producing no audio data. Try power-cycling the USB device.")

                # Health check: audio buffers are all silence (zero energy)
                if energy == 0.0:
                    zero_energy_streak += 1
                    if not warned_silence and zero_energy_streak >= 125:
                        # 125 * 4000 bytes @ 16kHz mono S16_LE ~= 15 seconds of silence
                        warned_silence = True
                        logger.error("Audio capture silence flood: microphone is streaming zero-filled buffers. Power-cycle the USB device.")
                        self._report_health(False, "silence_flood", "Microphone is connected but streaming silence. Try power-cycling the USB device.")
                else:
                    zero_energy_streak = 0

                # Health check: Vosk hasn't accepted any audio for a long time (>30s)
                if elapsed > 30.0 and not warned_vosk_stuck and bytes_since_vosk > 480000:
                    # 480k bytes ~= 15 seconds of audio at 16kHz mono S16_LE
                    warned_vosk_stuck = True
                    logger.warning("Vosk has not accepted an utterance in 30+ seconds; microphone may be muted or ambient volume too low")
                    self._report_health(False, "vosk_stall", "Audio is flowing but Vosk has not recognized any speech in 30s. Check mic volume or mute switch.")

                # Periodic healthy heartbeat once real audio flows
                if total_bytes > 0 and energy > 0.0 and elapsed - last_health_report > 10.0:
                    last_health_report = elapsed
                    self._report_health(True, "", "Audio capture is healthy")

                effective_threshold = self._effective_energy_threshold()
                if energy >= effective_threshold:
                    utterance_has_energy = True

                if recognizer.AcceptWaveform(data):
                    bytes_since_vosk = 0  # reset on accepted utterance
                    result = recognizer.Result()
                    result_dict = _json.loads(result)
                    vosk_text = result_dict.get("text", "").strip()

                    final_text = vosk_text
                    engine_used = self.engine_type

                    with self._online_lock:
                        should_use_whisper = self._online and self.whisper_enabled and self._whisper_api_key

                    if should_use_whisper and utterance_has_energy and len(utterance_buffer) > 0:
                        whisper_text = self._transcribe_whisper_api(bytes(utterance_buffer))
                        if whisper_text:
                            final_text = whisper_text
                            engine_used = "whisper_api"

                    # Drop unconditional garbage; let non-garbage through
                    if final_text and len(final_text) >= self.min_command_length:
                        if self._is_garbage(final_text):
                            logger.debug(f"Dropped garbage: {final_text}")
                        elif self._is_tts_echo(final_text):
                            logger.debug(f"Dropped TTS echo: {final_text}")
                        else:
                            logger.info(f"Transcription ({engine_used}): {final_text}")
                            result_obj = TranscriptionResult(
                                text=final_text,
                                confidence=1.0,
                                is_command=True,
                                engine=engine_used,
                                wake_word="",
                                session_id=""
                            )
                            if self._transcription_callback:
                                try:
                                    self._transcription_callback(result_obj)
                                except Exception as cb_err:
                                    logger.error(f"Transcription callback error: {cb_err}")

                    # Reset for next utterance
                    utterance_buffer = bytearray()
                    utterance_has_energy = False

                elif self._partial_callback:
                    partial = recognizer.PartialResult()
                    partial_dict = _json.loads(partial)
                    partial_text = partial_dict.get("partial", "").strip()
                    if partial_text and self._is_garbage(partial_text):
                        partial_text = ""
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

    def _transcribe_whisper_api(self, audio_bytes: bytes) -> Optional[str]:
        """Send raw PCM audio to OpenAI Whisper API and return transcription text."""
        import io
        import wave
        import requests

        try:
            # Convert raw S16_LE mono PCM to WAV
            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)  # 16-bit = 2 bytes
                wf.setframerate(self.sample_rate)
                wf.writeframes(audio_bytes)
            wav_buffer.seek(0)

            url = self._whisper_api_base_url
            headers = {"Authorization": f"Bearer {self._whisper_api_key}"}
            files = {"file": ("utterance.wav", wav_buffer, "audio/wav")}
            data = {"model": "whisper-1", "language": "en", "response_format": "json"}

            resp = requests.post(url, headers=headers, files=files, data=data, timeout=10)
            resp.raise_for_status()
            text = resp.json().get("text", "").strip()
            logger.info(f"Whisper API transcription: '{text[:60]}...'")
            return text
        except Exception as e:
            logger.warning(f"Whisper API transcription failed: {e}")
            return None

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

    def on_health(self, callback: Callable[[Dict[str, Any]], None]):
        """Set health/diagnostics callback. Receives dict with 'healthy', 'issue', 'message'."""
        self._health_callback = callback
        return self

    def _report_health(self, healthy: bool, issue: str = "", message: str = ""):
        if self._health_callback:
            try:
                self._health_callback({"healthy": healthy, "issue": issue, "message": message})
            except Exception as e:
                logger.warning(f"Health callback error: {e}")

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

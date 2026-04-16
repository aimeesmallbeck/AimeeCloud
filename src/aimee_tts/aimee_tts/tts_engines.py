#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
TTS Engine adapters for AIMEE Robot.

Supports:
- Kokoro (via pykokoro or official kokoro package) — primary, offline
- gTTS (Google Text-to-Speech) — cloud fallback
"""

import logging
import os
import subprocess
import tempfile
import wave
from dataclasses import dataclass
from typing import List, Optional
from urllib import request, error

import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class TTSResult:
    success: bool = False
    audio_path: str = ""
    engine_used: str = ""
    duration_seconds: float = 0.0
    error_message: str = ""
    request_id: str = ""


class BaseTTSEngine:
    """Base class for TTS engines."""

    name: str = "base"
    available: bool = False
    voices: List[str] = []

    def generate(self, text: str, voice: Optional[str] = None, speed: float = 1.0, lang: str = "en") -> TTSResult:
        raise NotImplementedError


class PyKokoroEngine(BaseTTSEngine):
    """Kokoro TTS via pykokoro (lightweight, ONNX-based, no torch)."""

    name = "kokoro"
    voices = [
        "af_heart", "af_bella", "af_sarah", "af_nicole",
        "am_michael", "am_adam", "bf_emma", "bm_george"
    ]

    def __init__(self, default_voice: str = "af_heart", speed: float = 1.0, lang: str = "en-us"):
        from pykokoro import KokoroPipeline, PipelineConfig, GenerationConfig
        self._default_voice = default_voice
        self._speed = speed
        self._lang = lang
        self._config = PipelineConfig(
            voice=default_voice,
            generation=GenerationConfig(speed=speed),
        )
        self._pipe = KokoroPipeline(self._config)
        self.available = True
        logger.info(f"Kokoro (pykokoro) initialized with voice={default_voice}")

    def generate(self, text: str, voice: Optional[str] = None, speed: float = 1.0, lang: str = "en") -> TTSResult:
        voice = voice or self._default_voice

        try:
            # Recreate pipeline if voice or speed changed
            if voice != self._default_voice or speed != self._speed:
                from pykokoro import KokoroPipeline, PipelineConfig, GenerationConfig
                self._config = PipelineConfig(
                    voice=voice,
                    generation=GenerationConfig(speed=speed),
                )
                self._pipe = KokoroPipeline(self._config)
                self._default_voice = voice
                self._speed = speed

            result = self._pipe.run(text)
            audio = result.audio
            sample_rate = result.sample_rate

            # Save to WAV
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                audio_path = tmp.name

            if audio.dtype != np.int16:
                audio = (audio * 32767).astype(np.int16)

            with wave.open(audio_path, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(audio.tobytes())

            duration = len(audio) / float(sample_rate)
            return TTSResult(
                success=True,
                audio_path=audio_path,
                engine_used="kokoro",
                duration_seconds=duration,
            )
        except Exception as e:
            logger.error(f"Kokoro generation failed: {e}")
            return TTSResult(success=False, error_message=f"Kokoro failed: {e}")


class KokoroOfficialEngine(BaseTTSEngine):
    """Kokoro TTS via official hexgrad/kokoro package (requires torch)."""

    name = "kokoro"
    voices = [
        "af_heart", "af_bella", "af_sarah", "af_nicole",
        "am_michael", "am_adam", "bf_emma", "bm_george"
    ]

    def __init__(self, default_voice: str = "af_heart", lang_code: str = "a", speed: float = 1.0):
        from kokoro import KPipeline
        self._pipe = KPipeline(lang_code=lang_code)
        self._default_voice = default_voice
        self._speed = speed
        self.available = True
        logger.info(f"Kokoro (official) initialized with voice={default_voice}, lang_code={lang_code}")

    def generate(self, text: str, voice: Optional[str] = None, speed: float = 1.0, lang: str = "en") -> TTSResult:
        voice = voice or self._default_voice
        speed = speed if speed is not None else self._speed

        try:
            generator = self._pipe(text, voice=voice, speed=speed, split_pattern=r"\n+")
            audios = []
            for _gs, _ps, audio in generator:
                audios.append(audio)

            if not audios:
                return TTSResult(success=False, error_message="Kokoro produced no audio")

            combined = np.concatenate(audios)
            sample_rate = 24000

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                audio_path = tmp.name

            if combined.dtype != np.int16:
                combined = (combined * 32767).astype(np.int16)

            with wave.open(audio_path, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(combined.tobytes())

            duration = len(combined) / float(sample_rate)
            return TTSResult(
                success=True,
                audio_path=audio_path,
                engine_used="kokoro",
                duration_seconds=duration,
            )
        except Exception as e:
            logger.error(f"Kokoro official generation failed: {e}")
            return TTSResult(success=False, error_message=f"Kokoro failed: {e}")


class GTTSEngine(BaseTTSEngine):
    """Google Text-to-Speech engine (cloud fallback)."""

    name = "gtts"

    def __init__(self, lang: str = "en", tld: str = "com", slow: bool = False):
        try:
            from gtts import gTTS
            self.available = True
        except ImportError:
            self.available = False
            logger.warning("gTTS not installed")
            return

        self.gtts_lang = lang
        self.gtts_tld = tld
        self.gtts_slow = slow
        logger.info("gTTS engine initialized")

    def generate(self, text: str, voice: Optional[str] = None, speed: float = 1.0, lang: str = "en") -> TTSResult:
        if not self.available:
            return TTSResult(success=False, error_message="gTTS not available")

        try:
            from gtts import gTTS

            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                audio_path = tmp.name

            tts = gTTS(
                text=text,
                lang=self.gtts_lang,
                slow=self.gtts_slow,
                tld=self.gtts_tld,
            )
            tts.save(audio_path)

            # Convert MP3 to WAV for compatibility with pygame/aplay
            wav_path = audio_path.replace(".mp3", ".wav")
            try:
                subprocess.run(
                    [
                        "ffmpeg", "-y", "-i", audio_path,
                        "-ar", "24000", "-ac", "1", "-sample_fmt", "s16",
                        wav_path,
                    ],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                os.unlink(audio_path)
                audio_path = wav_path
            except Exception as e:
                logger.warning(f"ffmpeg MP3→WAV conversion failed: {e}, leaving MP3")

            word_count = len(text.split())
            duration = word_count * 0.15 / speed

            return TTSResult(
                success=True,
                audio_path=audio_path,
                engine_used="gtts",
                duration_seconds=duration,
            )
        except Exception as e:
            logger.error(f"gTTS generation failed: {e}")
            return TTSResult(success=False, error_message=f"gTTS failed: {e}")


class TTSEngineManager:
    """Manages TTS engines and fallback logic."""

    def __init__(
        self,
        default_engine: str = "kokoro",
        fallback_engine: str = "gtts",
        auto_fallback: bool = True,
        default_voice: str = "af_heart",
        kokoro_lang: str = "en-us",
        kokoro_speed: float = 1.0,
        gtts_lang: str = "en",
        gtts_tld: str = "com",
        gtts_slow: bool = False,
    ):
        self.default_engine = default_engine
        self.fallback_engine = fallback_engine
        self.auto_fallback = auto_fallback
        self.default_voice = default_voice
        self.kokoro_lang = kokoro_lang
        self.kokoro_speed = kokoro_speed
        self.gtts_lang = gtts_lang

        self._engines: dict[str, BaseTTSEngine] = {}
        self._init_engines(
            gtts_lang=gtts_lang,
            gtts_tld=gtts_tld,
            gtts_slow=gtts_slow,
        )

    def _init_engines(self, **kwargs):
        # Kokoro: prefer pykokoro, then official kokoro
        try:
            engine = PyKokoroEngine(
                default_voice=self.default_voice,
                speed=self.kokoro_speed,
                lang=self.kokoro_lang,
            )
            self._engines["kokoro"] = engine
            logger.info("Kokoro engine available (pykokoro)")
        except Exception as e:
            logger.warning(f"pykokoro not available: {e}")
            try:
                lang_code = "a" if self.kokoro_lang.startswith("en") else self.kokoro_lang[:1]
                engine = KokoroOfficialEngine(
                    default_voice=self.default_voice,
                    lang_code=lang_code,
                    speed=self.kokoro_speed,
                )
                self._engines["kokoro"] = engine
                logger.info("Kokoro engine available (official package)")
            except Exception as e2:
                logger.warning(f"Official kokoro not available: {e2}")

        # gTTS fallback
        try:
            engine = GTTSEngine(
                lang=kwargs.get("gtts_lang", "en"),
                tld=kwargs.get("gtts_tld", "com"),
                slow=kwargs.get("gtts_slow", False),
            )
            if engine.available:
                self._engines["gtts"] = engine
        except Exception as e:
            logger.warning(f"gTTS not available: {e}")

    def _is_online(self) -> bool:
        try:
            request.urlopen("https://www.google.com", timeout=3)
            return True
        except error.URLError:
            return False

    def select_engine(self, preferred: Optional[str] = None) -> str:
        if preferred and preferred in self._engines:
            return preferred

        if self.default_engine == "auto":
            if self._is_online() and "gtts" in self._engines:
                return "gtts"
            if "kokoro" in self._engines:
                return "kokoro"
            raise RuntimeError("No TTS engine available")

        if self.default_engine in self._engines:
            return self.default_engine

        if self.auto_fallback:
            for fallback in [self.fallback_engine, "kokoro", "gtts"]:
                if fallback in self._engines:
                    logger.info(f"Falling back to {fallback}")
                    return fallback

        raise RuntimeError(f"Engine {self.default_engine} not available")

    def generate(self, text: str, engine_name: Optional[str] = None, voice: Optional[str] = None, speed: float = 1.0) -> TTSResult:
        engine_name = self.select_engine(engine_name)
        engine = self._engines.get(engine_name)
        if not engine:
            return TTSResult(success=False, error_message=f"Engine {engine_name} not available")

        result = engine.generate(text, voice=voice, speed=speed)

        if not result.success and self.fallback_engine and self.fallback_engine != engine_name:
            fallback = self._engines.get(self.fallback_engine)
            if fallback:
                logger.info(f"Primary engine failed, trying fallback: {self.fallback_engine}")
                result = fallback.generate(text, voice=voice, speed=speed)

        return result

    def get_voices(self, engine_name: Optional[str] = None) -> List[str]:
        engine_name = self.select_engine(engine_name)
        engine = self._engines.get(engine_name)
        if engine:
            return engine.voices
        return []

    def health_status(self) -> dict:
        return {
            "engines": {name: eng.available for name, eng in self._engines.items()},
            "default_engine": self.default_engine,
            "fallback_engine": self.fallback_engine,
            "online": self._is_online(),
        }

#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
tts Brick - Text-to-Speech with gTTS and Piper local TTS support

This brick provides text-to-speech conversion with:
- gTTS (Google Text-to-Speech): High quality, requires internet
- Piper (Local neural TTS): Fast, offline, privacy-friendly
- pyttsx3 (Fallback): Always available, robotic quality
- Automatic fallback when offline

Features:
- Multiple TTS engine support
- Automatic offline detection and fallback
- Preemption support (interrupt current speech)
- Queue management for sequential playback
- Volume control
"""

import asyncio
import logging
import os
import subprocess
import tempfile
import time
import wave
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable, Dict, List, Optional, Any, Union
from urllib import request, error

import pygame
from arduino.app_utils import brick

# Configure logging
logger = logging.getLogger(__name__)


class TTSEngine(Enum):
    """Supported TTS engines."""
    GTTS = "gtts"           # Google TTS (cloud)
    PIPER = "piper"         # Piper local neural TTS
    PYTTSX3 = "pyttsx3"     # pyttsx3 local TTS
    AUTO = "auto"           # Auto-select based on availability


@dataclass
class TTSRequest:
    """TTS request."""
    text: str
    engine: Optional[str] = None  # Override default engine
    lang: str = "en"
    volume: float = 1.0
    speed: float = 1.0
    priority: int = 0  # Higher = more urgent
    request_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: float = field(default_factory=time.time)


@dataclass
class TTSResult:
    """TTS generation result."""
    success: bool = False
    audio_path: str = ""
    engine_used: str = ""
    duration_seconds: float = 0.0
    error_message: str = ""
    request_id: str = ""


class TTSBrickError(Exception):
    """Custom exception for TTSBrick errors."""
    pass


# Import uuid here to avoid issues
import uuid


@brick
class TTSBrick:
    """
    Text-to-Speech with gTTS and Piper local TTS support.
    
    This brick provides TTS conversion with multiple engines:
    - gTTS: High quality, requires internet (development default)
    - Piper: Local neural TTS, fast, offline (production target)
    - pyttsx3: Fallback, always available
    
    Features:
    - Automatic engine selection based on connectivity
    - Speech queue with priority support
    - Preemption (interrupt current speech)
    - Volume and speed control
    
    Attributes:
        default_engine: Default TTS engine (gtts, piper, pyttsx3, auto)
        fallback_engine: Fallback when primary fails
        auto_fallback: Automatically fallback when offline
        piper_model: Path to Piper ONNX model
        piper_config: Path to Piper config JSON
        gtts_lang: Language for gTTS
        volume: Default volume (0.0-1.0)
        speed: Default speed multiplier
        debug: Enable debug logging
        
    Example:
        >>> brick = TTSBrick(
        ...     default_engine="auto",
        ...     auto_fallback=True,
        ...     piper_model="~/.local/share/piper/en_US-lessac-medium.onnx"
        ... )
        >>> await brick.initialize()
        >>> 
        >>> # Simple speak
        >>> await brick.speak("Hello, I am AIMEE")
        >>> 
        >>> # With options
        >>> await brick.speak("Hello", engine="piper", volume=0.8)
        >>> 
        >>> await brick.shutdown()
    """
    
    def __init__(
        self,
        default_engine: str = "gtts",
        fallback_engine: str = "pyttsx3",
        auto_fallback: bool = True,
        piper_model: Optional[str] = None,
        piper_config: Optional[str] = None,
        piper_speaker_id: int = 0,
        gtts_lang: str = "en",
        gtts_tld: str = "com",
        gtts_slow: bool = False,
        volume: float = 1.0,
        speed: float = 1.0,
        use_pygame: bool = True,
        debug: bool = False,
        **kwargs
    ):
        """
        Initialize the TTSBrick.
        
        Args:
            default_engine: Default engine (gtts, piper, pyttsx3, auto)
            fallback_engine: Fallback engine on failure
            auto_fallback: Auto-switch to local when offline
            piper_model: Path to Piper ONNX model file
            piper_config: Path to Piper config JSON (auto-detected if None)
            piper_speaker_id: Speaker ID for multi-speaker models
            gtts_lang: Language code for gTTS
            gtts_tld: Top-level domain for gTTS accent
            gtts_slow: Slow speech for gTTS
            volume: Default volume (0.0-1.0)
            speed: Default speed multiplier
            use_pygame: Use pygame for audio playback
            debug: Enable debug logging
            **kwargs: Additional arguments
        """
        self.default_engine = TTSEngine(default_engine.lower())
        self.fallback_engine = TTSEngine(fallback_engine.lower())
        self.auto_fallback = auto_fallback
        
        # Piper configuration
        self.piper_model = piper_model
        self.piper_config = piper_config
        self.piper_speaker_id = piper_speaker_id
        
        # gTTS configuration
        self.gtts_lang = gtts_lang
        self.gtts_tld = gtts_tld
        self.gtts_slow = gtts_slow
        
        # Audio settings
        self.volume = max(0.0, min(1.0, volume))
        self.speed = speed
        self.use_pygame = use_pygame
        
        self.debug = debug
        
        # State
        self._initialized = False
        self._lock = asyncio.Lock()
        
        # Audio playback
        self._pygame_initialized = False
        self._current_audio_path: Optional[str] = None
        self._is_speaking = False
        self._preempt_event = asyncio.Event()
        
        # Queue for sequential playback
        self._speech_queue: asyncio.Queue = asyncio.Queue()
        self._queue_task: Optional[asyncio.Task] = None
        
        # Statistics
        self._speak_count = 0
        self._total_duration = 0.0
        
        # Engine availability
        self._gtts_available = False
        self._piper_available = False
        self._pyttsx3_available = False
        
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        
        logger.info(
            f"TTSBrick initialized: default={default_engine}, "
            f"fallback={fallback_engine}, auto_fallback={auto_fallback}"
        )
    
    async def initialize(self) -> "TTSBrick":
        """
        Initialize TTS engines and check availability.
        
        Returns:
            self for method chaining
        """
        async with self._lock:
            if self._initialized:
                return self
            
            try:
                # Check engine availability
                await self._check_engines()
                
                # Initialize audio playback
                if self.use_pygame:
                    await self._init_pygame()
                
                # Start queue processor
                self._queue_task = asyncio.create_task(self._process_queue())
                
                self._initialized = True
                logger.info("TTSBrick initialization complete")
                
            except Exception as e:
                logger.error(f"Initialization failed: {e}")
                raise TTSBrickError(f"Failed to initialize: {e}")
        
        return self
    
    async def _check_engines(self):
        """Check which TTS engines are available."""
        # Check gTTS
        try:
            from gtts import gTTS
            self._gtts_available = True
            logger.info("gTTS available")
        except ImportError:
            logger.warning("gTTS not installed")
        
        # Check Piper
        try:
            from piper import PiperVoice
            if self.piper_model and os.path.exists(self.piper_model):
                self._piper_available = True
                logger.info(f"Piper available: {self.piper_model}")
            else:
                logger.warning(f"Piper model not found: {self.piper_model}")
        except ImportError:
            logger.warning("Piper not installed")
        
        # Check pyttsx3
        try:
            import pyttsx3
            self._pyttsx3_available = True
            logger.info("pyttsx3 available")
        except ImportError:
            logger.warning("pyttsx3 not installed")
    
    async def _init_pygame(self):
        """Initialize pygame mixer."""
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self._pygame_initialized = True
            logger.info("Pygame mixer initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize pygame: {e}")
            self._pygame_initialized = False
    
    def _is_online(self) -> bool:
        """Check if internet is available."""
        try:
            request.urlopen('https://www.google.com', timeout=3)
            return True
        except:
            return False
    
    def _select_engine(self, preferred: Optional[str] = None) -> TTSEngine:
        """
        Select appropriate TTS engine.
        
        Args:
            preferred: Preferred engine override
            
        Returns:
            Selected TTSEngine
        """
        if preferred:
            return TTSEngine(preferred.lower())
        
        # If auto mode, select based on connectivity
        if self.default_engine == TTSEngine.AUTO:
            if self._is_online() and self._gtts_available:
                return TTSEngine.GTTS
            elif self._piper_available:
                return TTSEngine.PIPER
            elif self._pyttsx3_available:
                return TTSEngine.PYTTSX3
            else:
                raise TTSBrickError("No TTS engine available")
        
        # Check if default is available
        if self.default_engine == TTSEngine.GTTS and not self._is_online():
            if self.auto_fallback:
                logger.info("Offline, falling back to local TTS")
                if self._piper_available:
                    return TTSEngine.PIPER
                elif self._pyttsx3_available:
                    return TTSEngine.PYTTSX3
        
        if self.default_engine == TTSEngine.PIPER and not self._piper_available:
            if self.auto_fallback and self._pyttsx3_available:
                return TTSEngine.PYTTSX3
        
        return self.default_engine
    
    async def speak(
        self,
        text: str,
        engine: Optional[str] = None,
        volume: Optional[float] = None,
        speed: Optional[float] = None,
        priority: int = 0,
        block: bool = True
    ) -> TTSResult:
        """
        Convert text to speech and play.
        
        Args:
            text: Text to speak
            engine: TTS engine override
            volume: Volume override (0.0-1.0)
            speed: Speed override
            priority: Speech priority (higher = more urgent)
            block: Wait for speech to complete
            
        Returns:
            TTSResult with details
        """
        if not self._initialized:
            raise TTSBrickError("Brick not initialized")
        
        if not text or not text.strip():
            return TTSResult(success=False, error_message="Empty text")
        
        request = TTSRequest(
            text=text,
            engine=engine,
            volume=volume if volume is not None else self.volume,
            speed=speed if speed is not None else self.speed,
            priority=priority
        )
        
        if block:
            # Generate and play immediately
            return await self._speak_internal(request)
        else:
            # Add to queue
            await self._speech_queue.put(request)
            return TTSResult(success=True, request_id=request.request_id)
    
    async def _speak_internal(self, request: TTSRequest) -> TTSResult:
        """Internal speak implementation."""
        start_time = time.time()
        
        try:
            # Select engine
            engine = self._select_engine(request.engine)
            logger.info(f"Using TTS engine: {engine.value}")
            
            # Generate audio
            if engine == TTSEngine.GTTS:
                result = await self._generate_gtts(request)
            elif engine == TTSEngine.PIPER:
                result = await self._generate_piper(request)
            elif engine == TTSEngine.PYTTSX3:
                result = await self._generate_pyttsx3(request)
            else:
                raise TTSBrickError(f"Unsupported engine: {engine}")
            
            if not result.success:
                # Try fallback
                if self.fallback_engine != engine:
                    logger.info(f"Trying fallback engine: {self.fallback_engine.value}")
                    if self.fallback_engine == TTSEngine.GTTS:
                        result = await self._generate_gtts(request)
                    elif self.fallback_engine == TTSEngine.PIPER:
                        result = await self._generate_piper(request)
                    elif self.fallback_engine == TTSEngine.PYTTSX3:
                        result = await self._generate_pyttsx3(request)
            
            if result.success and result.audio_path:
                # Play audio
                await self._play_audio(result.audio_path, request.volume)
                
                # Update statistics
                self._speak_count += 1
                self._total_duration += result.duration_seconds
                
                # Cleanup temp file
                try:
                    os.unlink(result.audio_path)
                except:
                    pass
            
            return result
            
        except Exception as e:
            logger.error(f"Speak failed: {e}")
            return TTSResult(
                success=False,
                error_message=str(e),
                request_id=request.request_id
            )
    
    async def _generate_gtts(self, request: TTSRequest) -> TTSResult:
        """Generate audio using gTTS."""
        try:
            from gtts import gTTS
            
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                audio_path = tmp.name
            
            # Generate
            tts = gTTS(
                text=request.text,
                lang=request.lang,
                slow=self.gtts_slow,
                tld=self.gtts_tld
            )
            
            # Save in background thread (gTTS does HTTP request)
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, tts.save, audio_path)
            
            # Get duration (approximate)
            # gTTS produces MP3, we'd need to decode for exact duration
            # Rough estimate: ~0.15s per word
            word_count = len(request.text.split())
            duration = word_count * 0.15 / request.speed
            
            return TTSResult(
                success=True,
                audio_path=audio_path,
                engine_used="gtts",
                duration_seconds=duration,
                request_id=request.request_id
            )
            
        except Exception as e:
            logger.error(f"gTTS generation failed: {e}")
            return TTSResult(
                success=False,
                error_message=f"gTTS failed: {e}",
                request_id=request.request_id
            )
    
    async def _generate_piper(self, request: TTSRequest) -> TTSResult:
        """Generate audio using Piper."""
        try:
            from piper import PiperVoice
            
            if not self.piper_model or not os.path.exists(self.piper_model):
                raise TTSBrickError("Piper model not found")
            
            # Load voice model
            model_path = Path(self.piper_model)
            config_path = Path(self.piper_config) if self.piper_config else model_path.with_suffix('.onnx.json')
            
            voice = PiperVoice.load(str(model_path), str(config_path) if config_path.exists() else None)
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                audio_path = tmp.name
            
            # Synthesize
            with wave.open(audio_path, "wb") as wav_file:
                voice.synthesize(request.text, wav_file, speaker_id=self.piper_speaker_id)
            
            # Get duration
            with wave.open(audio_path, "rb") as wav:
                frames = wav.getnframes()
                rate = wav.getframerate()
                duration = frames / float(rate)
            
            return TTSResult(
                success=True,
                audio_path=audio_path,
                engine_used="piper",
                duration_seconds=duration / request.speed,
                request_id=request.request_id
            )
            
        except Exception as e:
            logger.error(f"Piper generation failed: {e}")
            return TTSResult(
                success=False,
                error_message=f"Piper failed: {e}",
                request_id=request.request_id
            )
    
    async def _generate_pyttsx3(self, request: TTSRequest) -> TTSResult:
        """Generate audio using pyttsx3."""
        try:
            import pyttsx3
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                audio_path = tmp.name
            
            # Initialize engine
            engine = pyttsx3.init()
            engine.setProperty('rate', int(150 * request.speed))
            engine.setProperty('volume', request.volume)
            
            # Save to file
            engine.save_to_file(request.text, audio_path)
            engine.runAndWait()
            
            # Get duration (approximate)
            word_count = len(request.text.split())
            duration = word_count * 0.15 / request.speed
            
            return TTSResult(
                success=True,
                audio_path=audio_path,
                engine_used="pyttsx3",
                duration_seconds=duration,
                request_id=request.request_id
            )
            
        except Exception as e:
            logger.error(f"pyttsx3 generation failed: {e}")
            return TTSResult(
                success=False,
                error_message=f"pyttsx3 failed: {e}",
                request_id=request.request_id
            )
    
    async def _play_audio(self, audio_path: str, volume: float):
        """Play audio file."""
        self._is_speaking = True
        self._current_audio_path = audio_path
        
        try:
            if self.use_pygame and self._pygame_initialized:
                await self._play_pygame(audio_path, volume)
            else:
                await self._play_aplay(audio_path, volume)
                
        finally:
            self._is_speaking = False
            self._current_audio_path = None
    
    async def _play_pygame(self, audio_path: str, volume: float):
        """Play audio using pygame."""
        try:
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play()
            
            # Wait for completion or preemption
            while pygame.mixer.music.get_busy():
                if self._preempt_event.is_set():
                    pygame.mixer.music.stop()
                    self._preempt_event.clear()
                    logger.info("Speech preempted")
                    break
                await asyncio.sleep(0.05)
                
        except Exception as e:
            logger.error(f"Pygame playback failed: {e}")
            # Fallback to aplay
            await self._play_aplay(audio_path, volume)
    
    async def _play_aplay(self, audio_path: str, volume: float):
        """Play audio using aplay (ALSA)."""
        try:
            # Note: aplay doesn't support volume control directly
            # Would need amixer or similar for volume
            proc = await asyncio.create_subprocess_exec(
                "aplay", audio_path,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            
            # Wait for completion or preemption
            while proc.returncode is None:
                if self._preempt_event.is_set():
                    proc.terminate()
                    self._preempt_event.clear()
                    logger.info("Speech preempted")
                    break
                await asyncio.sleep(0.05)
                
        except Exception as e:
            logger.error(f"aplay failed: {e}")
    
    async def _process_queue(self):
        """Process speech queue."""
        while True:
            try:
                request = await self._speech_queue.get()
                await self._speak_internal(request)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Queue processing error: {e}")
    
    async def preempt(self):
        """Preempt (interrupt) current speech."""
        if self._is_speaking:
            logger.info("Preempting current speech")
            self._preempt_event.set()
            
            # Also clear queue if desired
            # while not self._speech_queue.empty():
            #     try:
            #         self._speech_queue.get_nowait()
            #     except asyncio.QueueEmpty:
            #         break
    
    def is_speaking(self) -> bool:
        """Check if currently speaking."""
        return self._is_speaking
    
    def is_online(self) -> bool:
        """Check if internet is available."""
        return self._is_online()
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status."""
        return {
            "initialized": self._initialized,
            "default_engine": self.default_engine.value,
            "gtts_available": self._gtts_available,
            "piper_available": self._piper_available,
            "pyttsx3_available": self._pyttsx3_available,
            "is_online": self._is_online(),
            "is_speaking": self._is_speaking,
            "speak_count": self._speak_count,
            "total_duration": self._total_duration,
            "queue_size": self._speech_queue.qsize(),
        }
    
    async def shutdown(self):
        """Clean up resources."""
        async with self._lock:
            if not self._initialized:
                return
            
            logger.info("Shutting down TTSBrick...")
            
            try:
                # Preempt current speech
                await self.preempt()
                
                # Stop queue processor
                if self._queue_task:
                    self._queue_task.cancel()
                    try:
                        await self._queue_task
                    except asyncio.CancelledError:
                        pass
                
                # Quit pygame
                if self._pygame_initialized:
                    pygame.mixer.quit()
                
                self._initialized = False
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

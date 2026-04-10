# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
tts Brick for Aimee Robot

Text-to-Speech with gTTS and Piper local TTS support

Usage:
    from aimee_tts.brick.tts import TTSBrick, TTSEngine
    
    brick = TTSBrick(
        default_engine="auto",
        piper_model="~/.local/share/piper/en_US-lessac-medium.onnx"
    )
    await brick.initialize()
    
    # Speak with auto engine selection
    await brick.speak("Hello, I am AIMEE")
    
    # Force specific engine
    await brick.speak("Hello", engine="piper")
    
    await brick.shutdown()
"""

from .tts import TTSBrick, TTSRequest, TTSResult, TTSEngine, TTSBrickError

__all__ = ["TTSBrick", "TTSRequest", "TTSResult", "TTSEngine", "TTSBrickError"]
__version__ = "0.1.0"

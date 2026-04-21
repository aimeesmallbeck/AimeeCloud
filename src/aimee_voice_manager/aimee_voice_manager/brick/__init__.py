# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
voice_manager Brick for Aimee Robot

Voice Manager for continuous STT (Vosk)

Usage:
    from aimee_voice_manager.brick.voice_manager import VoiceManagerBrick
    
    brick = VoiceManagerBrick(
        engine="vosk",
        model_path="/path/to/model"
    )
    await brick.initialize()
    
    # Transcribe a command
    result = await brick.transcribe_command(wake_word="aimee")
    print(f"Heard: {result.text}")
    
    await brick.shutdown()
"""

from .voice_manager import VoiceManagerBrick, TranscriptionResult

__all__ = ["VoiceManagerBrick", "TranscriptionResult"]
__version__ = "0.1.0"

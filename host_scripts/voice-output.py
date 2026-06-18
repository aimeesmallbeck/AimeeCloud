#!/usr/bin/env python3
"""
Voice Output - Standalone TTS (Text-to-Speech) Process

Takes text from message bus via WebSocket, converts to speech, plays on speaker.
This is a standalone process - NOT part of App Lab (yet).

Usage:
    python3 voice-output.py [--mode real|simulated]
"""

import os
# Force ALSA for audio
os.environ['SDL_AUDIODRIVER'] = 'alsa'
os.environ['AUDIODEV'] = 'plughw:0,0'

import argparse
import json
import asyncio
import websockets
import time
import threading
import pygame
from gtts import gTTS

# Settings
WS_URL = "ws://localhost:8088"

# Track if TTS is currently playing
tts_lock = threading.Lock()
message_queue = asyncio.Queue()

# Mode state (mutable for config changes)
current_mode = ["simulated"]  # List so we can modify in nested function


def speak(text):
    """Use gTTS + pygame to speak."""
    try:
        tts = gTTS(text=text, lang="en")
        tts.save("/tmp/speak.mp3")
        
        pygame.mixer.pre_init(frequency=24000, size=-16, channels=1)
        pygame.mixer.init()
        pygame.mixer.music.load("/tmp/speak.mp3")
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        
        pygame.mixer.quit()
        print(f"Spoke: {text[:50]}...")
        
    except Exception as e:
        print(f"TTS error: {e}")


def speak_in_background(text):
    """Speak text in a background thread."""
    def _speak():
        try:
            tts = gTTS(text=text, lang="en")
            tts.save("/tmp/speak.mp3")
            
            pygame.mixer.pre_init(frequency=24000, size=-16, channels=1)
            pygame.mixer.init()
            pygame.mixer.music.load("/tmp/speak.mp3")
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            pygame.mixer.quit()
            print(f"[TTS] Finished: {text[:50]}...")
            
        except Exception as e:
            print(f"TTS error: {e}")
    
    thread = threading.Thread(target=_speak)
    thread.daemon = True
    thread.start()


def display_text(text):
    """Simulated mode - just print/display the text."""
    print(f"\n=== SPEAKER OUTPUT (SIMULATED) ===")
    print(f"Text: {text}")
    print("=" * 40)


async def handle_message(payload):
    """Handle incoming text message."""
    text = payload.get("text", "")
    
    if not text:
        return
    
    print(f"Received: {text}")
    
    mode = current_mode[0]
    if mode == "real":
        speak_in_background(text)
    else:
        display_text(text)


async def listen_for_messages():
    """Connect to WebSocket and listen for voice/output messages."""
    while True:
        try:
            async with websockets.connect(WS_URL) as ws:
                print(f"Connected to {WS_URL}")
                
                # Subscribe to voice output topics
                await ws.send(json.dumps({
                    "action": "subscribe",
                    "topic": "voice/output"
                }))
                await ws.send(json.dumps({
                    "action": "subscribe",
                    "topic": "tts"
                }))
                # Subscribe to config changes
                await ws.send(json.dumps({
                    "action": "subscribe",
                    "topic": "config/voice_output"
                }))
                
                print(f"Subscribed to voice/output and tts. Mode: {mode}")
                
                async for message in ws:
                    try:
                        data = json.loads(message)
                        topic = data.get("topic", "")
                        payload = data.get("payload", {})
                        
                        if topic == "config/voice_output":
                            # Handle mode change
                            new_mode = payload.get("mode", "simulated")
                            if new_mode in ["real", "simulated"]:
                                current_mode[0] = new_mode
                                print(f"Mode changed to: {current_mode[0]}")
                        
                        elif topic in ["voice/output", "tts"]:
                            await handle_message(payload)
                    
                    except json.JSONDecodeError:
                        continue
                    
        except Exception as e:
            print(f"Connection error: {e}")
            print("Retrying in 5 seconds...")
            await asyncio.sleep(5)


async def test_speak():
    """Test TTS speak."""
    print("\n=== TEST MODE ===")
    text = input("Enter text to speak: ").strip()
    if text:
        speak(text)


async def main():
    parser = argparse.ArgumentParser(description="Voice Output - TTS Speaker")
    parser.add_argument("--mode", choices=["real", "simulated"], default="simulated",
                        help="Output mode: real (speak audio) or simulated (display text)")
    parser.add_argument("--test", action="store_true",
                        help="Test TTS with manual input")
    args = parser.parse_args()
    
    # Set initial mode
    current_mode[0] = args.mode
    
    if args.test:
        await test_speak()
        return
    
    # Listen for messages via WebSocket
    await listen_for_messages()


if __name__ == "__main__":
    asyncio.run(main())
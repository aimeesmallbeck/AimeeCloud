#!/usr/bin/env python3
"""
Voice Input - Standalone Microphone to STT Process

Listens to microphone, transcribes with Vosk, publishes via WebSocket.
This is a standalone process - NOT part of App Lab (yet).

Usage:
    python3 voice-input.py [--continuous] [--simulate]
"""

import os
# Force ALSA for audio
os.environ['SDL_AUDIODRIVER'] = 'alsa'
os.environ['AUDIODEV'] = 'plughw:0,0'

import sys
import argparse
import json
import asyncio
import websockets
from vosk import Model, KaldiRecognizer

# Settings
MODEL_PATH = "/home/arduino/vosk-models/vosk-model-small-en-us-0.15"
WS_URL = "ws://localhost:8088"


async def load_model():
    """Load Vosk model once."""
    print(f"Loading Vosk model from {MODEL_PATH}...")
    model = Model(MODEL_PATH)
    print("Vosk ready!")
    return model


async def publish_via_ws(ws, text):
    """Publish transcription via WebSocket."""
    message = {
        "action": "publish",
        "topic": "voice/transcription",
        "payload": {
            "text": text,
            "confidence": 0.85,
            "source": "voice_input"
        },
        "source": "voice_input"
    }
    await ws.send(json.dumps(message))
    print(f"Published: {text}")


async def listen_once(model, ws):
    """Listen once and return transcribed text."""
    recognizer = KaldiRecognizer(model, 16000)
    
    # Use dsnoop for USB mic (device 0,0)
    import subprocess
    cmd = ["arecord", "-D", "dsnoop:0,0", "-f", "S16_LE", "-r", "16000", "-c", "1", "-t", "raw"]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print("Listening... (Speak now)")
    
    try:
        while True:
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
            
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_dict = json.loads(result)
                text = result_dict.get("text", "")
                
                if text:
                    print(f"Heard: {text}")
                    await publish_via_ws(ws, text)
                    return text
    
    except KeyboardInterrupt:
        print("\nInterrupted")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        process.terminate()
        process.wait()
    
    return ""


async def connect_and_listen(model, continuous=False):
    """Connect to WebSocket server and listen."""
    while True:
        try:
            async with websockets.connect(WS_URL) as ws:
                print(f"Connected to {WS_URL}")
                
                # Subscribe to topics if needed
                await ws.send(json.dumps({
                    "action": "subscribe",
                    "topic": "config/voice"
                }))
                
                if continuous:
                    # Continuous mode
                    await listen_continuous(model, ws)
                else:
                    # Single listen mode
                    text = await listen_once(model, ws)
                    if text:
                        print(f"\nFinal: {text}")
                
        except Exception as e:
            print(f"Connection error: {e}")
            print("Retrying in 5 seconds...")
            await asyncio.sleep(5)


async def listen_continuous(model, ws):
    """Continuous listening mode."""
    recognizer = KaldiRecognizer(model, 16000)
    
    import subprocess
    cmd = ["arecord", "-D", "dsnoop:0,0", "-f", "S16_LE", "-r", "16000", "-c", "1", "-t", "raw"]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print("Continuous listening mode. Press Ctrl+C to stop.")
    
    try:
        while True:
            data = process.stdout.read(4000)
            if len(data) == 0:
                continue
            
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_dict = json.loads(result)
                text = result_dict.get("text", "")
                
                if text:
                    print(f"Heard: {text}")
                    await publish_via_ws(ws, text)
    
    except KeyboardInterrupt:
        print("\nStopped")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        process.terminate()
        process.wait()


async def simulate_input():
    """Simulate voice input for testing."""
    print("\n=== SIMULATE MODE ===")
    print("Type text and press Enter to simulate voice transcription.")
    print("Press Ctrl+C to exit.")
    
    # Connect to WS for simulate mode too
    try:
        async with websockets.connect(WS_URL) as ws:
            print("Connected to message bus")
            
            try:
                while True:
                    text = input("You: ").strip()
                    if text:
                        print(f"Simulated Heard: {text}")
                        await publish_via_ws(ws, text)
            except KeyboardInterrupt:
                print("\nExited")
    except Exception as e:
        print(f"WS Error: {e}")


async def main():
    parser = argparse.ArgumentParser(description="Voice Input - Mic to STT")
    parser.add_argument("--continuous", action="store_true", help="Continuous listening mode")
    parser.add_argument("--simulate", action="store_true", help="Simulate input (text keyboard)")
    args = parser.parse_args()
    
    if args.simulate:
        await simulate_input()
        return
    
    # Load Vosk model
    model = await load_model()
    
    # Connect and listen
    await connect_and_listen(model, continuous=args.continuous)


if __name__ == "__main__":
    asyncio.run(main())
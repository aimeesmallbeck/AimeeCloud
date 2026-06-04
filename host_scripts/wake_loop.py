#!/usr/bin/env python3
"""Simple wake-on-sound voice assistant - listens continuously"""
import pygame
import time
import subprocess
import os
from faster_whisper import WhisperModel
from gtts import gTTS

# Load Whisper model once
print("Loading Whisper...")
whisper = WhisperModel("tiny.en", device="cpu", compute_type="int8")
print("Ready!")

# yzma chat command
YZMA_LIB = "/home/arduino/lib"
MODEL = "/home/arduino/models/Qwen2.5-0.5B-Instruct-Q4_K_M.gguf"
GO_BIN = "/home/arduino/go/pkg/mod/golang.org/toolchain@v0.0.1-go1.25.8.linux-arm64/bin/go"
YZMA_DIR = "/home/arduino/yzma"

def listen_and_respond():
    """Record, transcribe, respond"""
    print("Recording...")
    subprocess.run("arecord -D plughw:1 -f S16_LE -r 16000 -d 5 /tmp/wake_input.wav", 
                   shell=True, capture_output=True)
    
    # Transcribe
    print("Transcribing...")
    segments, _ = whisper.transcribe("/tmp/wake_input.wav")
    text = " ".join([s.text for s in segments]).strip()
    if not text:
        print("Nothing heard")
        return
    print(f"You said: {text}")
    
    # Get LLM response
    print("Thinking...")
    cmd = f"export YZMA_LIB={YZMA_LIB} && {GO_BIN} run {YZMA_DIR}/examples/chat/ -model {MODEL} -sys 'You are Aimee, a friendly robot. Keep replies short.' -p '{text}' -n 50"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=YZMA_DIR)
    response = result.stdout.strip()
    print(f"Aimee: {response}")
    
    # TTS
    print("Speaking...")
    tts = gTTS(text=response)
    tts.save("/tmp/wake_reply.mp3")
    
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("/tmp/wake_reply.mp3")
    pygame.mixer.music.play()
    time.sleep(5)

print("\n=== Voice assistant ready! ===")
print("Say something to start...")

# Simple loop - listen for audio, respond when sound detected
import numpy as np
try:
    while True:
        # Quick check audio level (very short recording)
        subprocess.run("arecord -D plughw:1 -f S16_LE -r 16000 -d 1 /tmp/check.wav -V mono", 
                       shell=True, capture_output=True)
        
        # Get file size as proxy for volume
        size = os.path.getsize("/tmp/check.wav")
        if size > 8000:  # threshold for speech
            print(f"Audio level: {size}")
            listen_and_respond()
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nExiting...")
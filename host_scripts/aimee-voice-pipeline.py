#!/usr/bin/env python3
"""Full voice pipeline triggered by wake word"""
import subprocess
import json
import time
import requests
from vosk import Model, KaldiRecognizer
import wave
from gtts import gTTS
import pygame

# Load Vosk model once (keep in memory)
print("Loading Vosk model...")
MODEL_PATH = "/home/arduino/vosk-models/vosk-model-en-us-0.22-lgraph"
model = Model(MODEL_PATH)
print("Model loaded!")

def run_pipeline():
    """Record, transcribe, respond, speak"""
    start_total = time.time()
    
    # 1. Record audio
    print("\n[1] Recording...")
    rec_start = time.time()
    subprocess.run([
        "arecord", "-D", "hw:1", "-f", "S16_LE", "-r", "16000", "-c", "1", "-d", "5", "/tmp/pipeline.wav"
    ], capture_output=True)
    print(f"    Recording: {time.time() - rec_start:.2f}s")
    
    # 2. Vosk STT
    print("[2] Transcribing...")
    stt_start = time.time()
    recognizer = KaldiRecognizer(model, 16000)
    wf = wave.open("/tmp/pipeline.wav", "rb")
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        recognizer.AcceptWaveform(data)
    transcript = json.loads(recognizer.FinalResult()).get("text", "")
    print(f"    Heard: [{transcript}] ({time.time() - stt_start:.2f}s)")
    
    if not transcript.strip():
        print("    No speech detected, skipping LLM")
        return
    
    # 3. SmolLM2 LLM
    print("[3] Getting response...")
    llm_start = time.time()
    try:
        resp = requests.post("http://localhost:8080/v1/chat/completions", json={
            "model": "SmolLM2-135M.Q4_K_M.gguf",
            "messages": [{"role": "user", "content": transcript}],
            "max_tokens": 50
        }, timeout=30)
        reply = resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"Error: {e}"
    print(f"    Reply: {reply[:100]}... ({time.time() - llm_start:.2f}s)")
    
    # 4. TTS + Playback
    print("[4] Speaking...")
    tts_start = time.time()
    tts = gTTS(text=reply)
    tts.save("/tmp/reply.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("/tmp/reply.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass
    print(f"    Spoken! ({time.time() - tts_start:.2f}s)")
    
    total = time.time() - start_total
    print(f"\n=== TOTAL TIME: {total:.2f}s ===")

if __name__ == "__main__":
    # Run once for testing
    run_pipeline()
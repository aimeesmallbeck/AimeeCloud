#!/usr/bin/env python3
"""
Vosk Server - Persistent STT service
Listens for audio and returns transcription
"""
from flask import Flask, request, jsonify
import json
from vosk import Model, KaldiRecognizer
import wave
import os

app = Flask(__name__)

# Load model once at startup
print("Loading Vosk model...")
MODEL_PATH = "/home/arduino/vosk-models/vosk-model-en-us-0.22-lgraph"
model = Model(MODEL_PATH)
print("Vosk server ready!")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    """Receive audio file, return transcription"""
    # Save uploaded audio
    with open("/tmp/vosk_server_input.wav", "wb") as f:
        f.write(request.data)
    
    # Transcribe
    recognizer = KaldiRecognizer(model, 16000)
    wf = wave.open("/tmp/vosk_server_input.wav", "rb")
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        recognizer.AcceptWaveform(data)
    
    result = json.loads(recognizer.FinalResult())
    return jsonify({"text": result.get("text", "")})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    print("Starting Vosk server on port 5000...")
    app.run(host="0.0.0.0", port=5000)
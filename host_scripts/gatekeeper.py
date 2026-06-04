#!/usr/bin/env python3
"""Gatekeeper Brick - Input → LLM → Output"""

import subprocess
import os

LLAMA_CLI = os.path.expanduser("~/lib/llama-cli")
MODEL_PATH = os.path.expanduser("~/models/Qwen2.5-0.5B-Instruct-Q4_K_M.gguf")
LLAMA_LIB = os.path.expanduser("~/lib")

def route_to_llm(prompt: str) -> str:
    if not os.path.exists(LLAMA_CLI):
        return f"Error: llama-cli not found"
    if not os.path.exists(MODEL_PATH):
        return f"Error: model not found"
    
    result = subprocess.run(
        [LLAMA_CLI, "-m", MODEL_PATH, "-p", prompt, "-n", "50"],
        env={**os.environ, "LD_LIBRARY_PATH": LLAMA_LIB},
        capture_output=True,
        text=True,
        timeout=180
    )
    
    if result.returncode != 0:
        return f"Error: {result.stderr}"
    return result.stdout.strip()

def speak(text: str):
    try:
        from gtts import gTTS
        import pygame, tempfile, time
        text = text.replace("\n", " ").strip()
        if not text:
            return
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            tts = gTTS(text=text, lang="en")
            tts.save(f.name)
            pygame.mixer.init()
            pygame.mixer.music.load(f.name)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            pygame.mixer.quit()
            os.unlink(f.name)
    except Exception as e:
        print(f"[TTS] {e}")

def process_input(text: str) -> str:
    if not text.strip():
        return ""
    response = route_to_llm(text)
    speak(response)
    return response

def main():
    print("Gatekeeper ready. Type quit to exit.")
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() in ("quit", "exit"):
                break
            response = process_input(user_input)
            print(f"<< {response}")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
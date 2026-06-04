from faster_whisper import WhisperModel
import sys

print("Loading Whisper model...")
model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
print("Transcribing...")

segments, info = model.transcribe("/tmp/test.wav", beam_size=5)
for segment in segments:
    print(segment.text)

print(f"Language: {info.language}, probability: {info.language_probability:.2f}")
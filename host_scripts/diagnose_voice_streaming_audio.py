#!/usr/bin/env python3
"""Diagnose voice streaming audio capture + VAD path.

Mimics what aimee_voice_streaming does, but prints debug info for every frame.
Use this to determine whether the issue is:
  - Microphone capture (no audio / low amplitude)
  - VAD not triggering (audio present but too quiet / VAD too aggressive)
  - WebSocket/cloud connection

Run inside the robot Docker container (where sounddevice/portaudio are available).
"""

import json
import logging
import os
import sys
import time
from pathlib import Path

import numpy as np

# Allow importing from the workspace
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "aimee_voice_streaming"))

from aimee_voice_streaming.audio_io import AudioCapture
from aimee_voice_streaming.vad_engine import VADEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Match voice_streaming.yaml defaults
SAMPLE_RATE = 16000
CHANNELS = 1
FRAME_DURATION_MS = 20
VAD_MODE = 2
VAD_SILENCE_MS = 500
VAD_PADDING_MS = 300


def amplitude_db(frame: np.ndarray) -> float:
    """Return RMS amplitude in dBFS."""
    if frame.size == 0:
        return -np.inf
    rms = np.sqrt(np.mean(frame.astype(np.float64) ** 2))
    if rms == 0:
        return -np.inf
    return 20.0 * np.log10(rms / 32768.0)


def main():
    device_index = int(os.getenv("AIMEE_AUDIO_DEVICE_INDEX", "-1"))
    duration_sec = float(os.getenv("AIMEE_DIAG_DURATION", "10"))

    logger.info(
        f"Diagnosing audio capture: device_index={device_index}, "
        f"sample_rate={SAMPLE_RATE}, channels={CHANNELS}, "
        f"duration={duration_sec}s"
    )

    capture = AudioCapture(
        sample_rate=SAMPLE_RATE,
        channels=CHANNELS,
        block_duration_ms=FRAME_DURATION_MS,
        device_index=device_index,
    )
    vad = VADEngine(
        mode=VAD_MODE,
        sample_rate=SAMPLE_RATE,
        frame_duration_ms=FRAME_DURATION_MS,
        padding_duration_ms=VAD_PADDING_MS,
        silence_duration_ms=VAD_SILENCE_MS,
    )

    if not capture.start():
        logger.error("FAILED to start audio capture. Check sounddevice/PortAudio/ALSA.")
        sys.exit(1)

    logger.info("Capture started. Speak now...")
    start_time = time.time()
    state = "idle"
    speech_frames = 0
    total_frames = 0
    db_values = []
    peak_max = 0

    try:
        while time.time() - start_time < duration_sec:
            frame = capture.read_frame(timeout=0.1)
            if frame is None:
                continue

            # Flatten to mono if needed
            if frame.ndim > 1:
                frame = frame[:, 0]

            total_frames += 1
            db = amplitude_db(frame)
            if not np.isinf(db):
                db_values.append(db)
            peak = np.max(np.abs(frame))
            if peak > peak_max:
                peak_max = int(peak)

            is_speech, speech_finished, prefix_frames = vad.process(frame)

            if is_speech and not (state == "listening"):
                state = "listening"
                logger.info(f"SPEECH STARTED  amp={db:.1f} dBFS  peak={peak}")
            elif speech_finished:
                state = "idle"
                logger.info(f"SPEECH ENDED    amp={db:.1f} dBFS  peak={peak}")

            if is_speech:
                speech_frames += 1
                logger.info(
                    f"  speech frame  amp={db:.1f} dBFS  peak={peak}  "
                    f"speech_frames={speech_frames}"
                )
            else:
                logger.debug(f"  silent frame  amp={db:.1f} dBFS  peak={peak}")

    except KeyboardInterrupt:
        logger.info("Interrupted")
    finally:
        capture.stop()

    db_min = min(db_values) if db_values else -np.inf
    db_max = max(db_values) if db_values else -np.inf
    db_mean = sum(db_values) / len(db_values) if db_values else -np.inf

    logger.info(
        f"Done. Captured {total_frames} frames, "
        f"{speech_frames} classified as speech ({speech_frames / max(total_frames, 1) * 100:.1f}%)."
    )
    logger.info(
        f"Amplitude stats over all captured frames: "
        f"peak_sample={peak_max}, min_dBFS={db_min:.1f}, max_dBFS={db_max:.1f}, mean_dBFS={db_mean:.1f}"
    )
    if speech_frames == 0:
        logger.warning(
            "No speech frames detected. Likely causes:\n"
            "  - Microphone gain too low (check alsamixer / Emeet hardware mute)\n"
            "  - Wrong audio device selected (set AIMEE_AUDIO_DEVICE_INDEX env var)\n"
            "  - VAD too aggressive for quiet/noisy audio (try VAD mode 1 or 0)\n"
            "  - ALSA dsnoop/sounddevice not opening the Emeet device correctly"
        )


if __name__ == "__main__":
    main()

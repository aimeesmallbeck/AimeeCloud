# Aimee Robot Deployment Guide

This directory contains scripts and configurations for deploying the Aimee Robot ROS2 stack to new Arduino UNO Q boards (or any ARM64 Debian-based system).

## Architecture

The Aimee robot runs entirely inside a **Docker container** based on `ros:humble-ros-base`. The host OS only needs Docker; ROS2 itself is encapsulated in the image.

```
┌─────────────────────────────────────────────┐
│  Arduino UNO Q Host OS (Debian, ARM64)      │
│  ├─ Docker daemon                           │
│  ├─ ALSA audio config (.asoundrc)           │
│  └─ Python pip packages (minimal)           │
│                                               │
│  ┌───────────────────────────────────────┐   │
│  │  Docker: aimee-robot:latest           │   │
│  │  ├─ ROS2 Humble (201+ packages)       │   │
│  │  ├─ Aimee workspace (/workspace)      │   │
│  │  ├─ LLM backend (llama-server)        │   │
│  │  ├─ Python deps (flask, vosk, etc.)   │   │
│  │  └─ System deps (ffmpeg, alsa, etc.)  │   │
│  └───────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

## Quick Start (New Board)

### 1. Run the Bootstrap Script

On a fresh UNO Q with network access:

```bash
curl -fsSL https://raw.githubusercontent.com/aimeesmallbeck/Aimee-Project/main/deploy/bootstrap.sh | bash
```

Or, if you have the repo cloned:

```bash
cd ~/aimee-robot-ws
bash deploy/bootstrap.sh
```

This will:
- Install Docker (if missing)
- Clone the Aimee workspace
- Create `.env` from template
- Build the Docker image
- Build the ROS2 workspace inside the container
- Install the systemd auto-start service

### 2. Configure Environment Variables

Edit `.env` and add your API keys:

```bash
nano ~/aimee-robot-ws/.env
```

Required for cloud features:
- `LEMONFOX_API_KEY` — For TTS and Whisper STT fallback ([get one free](https://www.lemonfox.ai/))

Optional:
- `AIMEE_CLOUD_ENDPOINT` — If self-hosting AimeeCloud
- `AIMEE_DEVICE_ID` — Unique identifier for this robot

### 3. Sync Models (from Board #1)

Large binary models are **not** tracked in git. If you have a source board with models already downloaded:

```bash
bash deploy/sync-models.sh arduino@10.0.0.156
```

This transfers:
- `models/` — LLM weights (Qwen2.5 .gguf files)
- `vosk-models/` — Speech recognition models
- `lib/` — Custom binaries (llama.cpp, etc.)
- `.arduino-bricks/models/` — Edge Impulse wake word model

### 4. Start the Robot

```bash
# Manual start
cd ~/aimee-robot-ws
docker compose up -d

# Or use systemd for auto-start on boot
sudo systemctl start aimee-robot
```

### 5. Verify

```bash
# View running nodes
docker compose exec aimee-robot bash -c "source install/setup.bash && ros2 node list"

# Open the monitor dashboard
# http://<board-ip>:8081
```

## Files Reference

| File | Purpose |
|------|---------|
| `Dockerfile` | Custom ROS2 image with all Aimee dependencies pre-installed |
| `docker-compose.yml` | Service definition with bind mounts, network, and env vars |
| `.env.example` | Template for secrets and configuration (copy to `.env`) |
| `deploy/bootstrap.sh` | One-shot provisioning script for fresh boards |
| `deploy/sync-models.sh` | rsync helper to copy models between boards |
| `systemd/aimee-robot.service` | Systemd unit for auto-starting on boot |

## Updating an Existing Board

```bash
cd ~/aimee-robot-ws
git pull origin main
docker compose up -d --build
```

## Troubleshooting

### Docker permission denied
Log out and back in after bootstrap, or run:
```bash
newgrp docker
```

### Out of memory during build
The UNO Q has 4GB RAM. If builds fail:
```bash
# Reduce parallel jobs
docker compose run --rm aimee-robot bash -c "colcon build --symlink-install --parallel-workers 1"
```

### Audio not working
Ensure `.asoundrc` exists and points to the correct card:
```bash
aplay -l  # List audio devices
```

## Security Notes

- **Never commit `.env` to git.** It contains API keys.
- The `.env.example` file contains no secrets and is safe to commit.
- All hardcoded API keys have been removed from source code; they are now injected via environment variables.

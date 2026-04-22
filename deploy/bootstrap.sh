#!/bin/bash
# Aimee Robot - New Board Bootstrap Script
# Run this on a fresh Arduino UNO Q to provision the entire ROS2 stack.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/aimeesmallbeck/Aimee-Project/main/deploy/bootstrap.sh | bash
#   # Or, if cloned locally:
#   bash deploy/bootstrap.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"
REPO_URL="https://github.com/aimeesmallbeck/AimeeCloud.git"
MODELS_SOURCE=""  # Set this to rsync from board #1, e.g. "arduino@10.0.0.156:/home/arduino/aimee-robot-ws/models"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# ─────────────────────────────── Step 1: System Prep ───────────────────────────────
log_info "Aimee Robot Bootstrap starting..."

ARCH=$(uname -m)
if [ "$ARCH" != "aarch64" ]; then
    log_warn "Architecture is $ARCH, expected aarch64 (Arduino UNO Q)"
fi

# Install Docker if missing
if ! command -v docker &> /dev/null; then
    log_info "Installing Docker..."
    sudo apt-get update
    sudo apt-get install -y docker.io docker-compose-plugin
    sudo usermod -aG docker "$USER"
    log_warn "Docker installed. You may need to log out and back in for group changes."
    log_warn "After re-login, re-run this script."
    exit 0
else
    log_info "Docker already installed."
fi

# Ensure user is in docker group
if ! groups "$USER" | grep -q '\bdocker\b'; then
    sudo usermod -aG docker "$USER"
    log_warn "Added $USER to docker group. Please log out and back in, then re-run."
    exit 0
fi

# ─────────────────────────────── Step 2: Clone Workspace ───────────────────────────────
if [ ! -d "$HOME/aimee-robot-ws" ]; then
    log_info "Cloning Aimee workspace to ~/aimee-robot-ws..."
    git clone "$REPO_URL" "$HOME/aimee-robot-ws"
    cd "$HOME/aimee-robot-ws"
else
    log_info "Workspace exists at ~/aimee-robot-ws. Pulling latest changes..."
    cd "$HOME/aimee-robot-ws"
    git pull origin main || true
fi

# ─────────────────────────────── Step 3: Environment Configuration ───────────────────────────────
if [ ! -f ".env" ]; then
    log_info "Creating .env from template..."
    cp .env.example .env
    log_warn "Please edit ~/aimee-robot-ws/.env and add your API keys before starting the robot."
fi

# ─────────────────────────────── Step 4: Audio Setup ───────────────────────────────
if [ ! -f "$HOME/.asoundrc" ]; then
    log_info "Creating default ALSA configuration..."
    cat > "$HOME/.asoundrc" << 'EOF'
pcm.!default {
    type plug
    slave.pcm "plughw:0,0"
}
ctl.!default {
    type hw
    card 0
}
EOF
fi

# ─────────────────────────────── Step 5: Model Sync (Optional) ───────────────────────────────
if [ -n "$MODELS_SOURCE" ]; then
    log_info "Syncing models from source board..."
    mkdir -p models vosk-models
    rsync -avz --progress "$MODELS_SOURCE/" models/ || log_warn "Model sync failed. You can run sync-models.sh later."
else
    log_warn "No MODELS_SOURCE set. Skipping model sync."
    log_warn "After bootstrap, run: bash deploy/sync-models.sh <source-board-ip>"
fi

# ─────────────────────────────── Step 6: Build Docker Image ───────────────────────────────
log_info "Building Aimee Docker image (this may take 10-20 minutes on first run)..."
docker compose build

# ─────────────────────────────── Step 7: Build ROS2 Workspace ───────────────────────────────
log_info "Building ROS2 workspace inside container..."
docker compose run --rm aimee-robot bash -c "
    source /opt/ros/humble/setup.bash &&
    cd /workspace &&
    rosdep install --from-paths src --ignore-src -y 2>/dev/null || true &&
    colcon build --symlink-install
"

# ─────────────────────────────── Step 8: Install Systemd Service ───────────────────────────────
log_info "Installing systemd service for auto-start on boot..."
sudo cp systemd/aimee-robot.service /etc/systemd/system/aimee-robot.service
sudo sed -i "s|/home/arduino|$HOME|g" /etc/systemd/system/aimee-robot.service
sudo systemctl daemon-reload
sudo systemctl enable aimee-robot.service

# ─────────────────────────────── Done ───────────────────────────────
echo ""
log_info "========================================"
log_info "Aimee Robot Bootstrap Complete!"
log_info "========================================"
echo ""
echo "Next steps:"
echo "  1. Edit ~/aimee-robot-ws/.env with your API keys"
echo "  2. If you skipped model sync, run: bash deploy/sync-models.sh <source-ip>"
echo "  3. Start the robot:     docker compose up -d"
echo "  4. View logs:           docker compose logs -f"
echo "  5. Open monitor:        http://$(hostname -I | awk '{print $1}'):8081"
echo "  6. Auto-start on boot:  sudo systemctl start aimee-robot"
echo ""

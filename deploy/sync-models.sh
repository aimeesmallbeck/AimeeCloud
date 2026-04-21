#!/bin/bash
# Aimee Robot - Model Synchronization Script
# Transfers large binary models from a source board to this board.
#
# Usage:
#   bash deploy/sync-models.sh <source-ip-or-host>
#   bash deploy/sync-models.sh arduino@10.0.0.156

set -e

SOURCE_HOST="${1:-}"
if [ -z "$SOURCE_HOST" ]; then
    echo "Usage: bash deploy/sync-models.sh <source-ip-or-host>"
    echo "Example: bash deploy/sync-models.sh arduino@10.0.0.156"
    exit 1
fi

WORKSPACE_DIR="$HOME/aimee-robot-ws"
SOURCE_BASE="$SOURCE_HOST:/home/arduino/aimee-robot-ws"

echo "Syncing models from $SOURCE_HOST..."

# Ensure directories exist
mkdir -p "$WORKSPACE_DIR/models"
mkdir -p "$WORKSPACE_DIR/vosk-models"
mkdir -p "$WORKSPACE_DIR/lib"
mkdir -p "$HOME/.arduino-bricks/models"
mkdir -p "$HOME/.config"

# Sync LLM and vision models
echo "  -> models/"
rsync -avz --progress "$SOURCE_BASE/models/" "$WORKSPACE_DIR/models/" || echo "    (models/ may be empty or host unreachable)"

# Sync Vosk models
echo "  -> vosk-models/"
rsync -avz --progress "$SOURCE_BASE/vosk-models/" "$WORKSPACE_DIR/vosk-models/" || echo "    (vosk-models/ may be empty or host unreachable)"

# Sync custom binaries (llama.cpp, etc.)
echo "  -> lib/"
rsync -avz --progress "$SOURCE_BASE/lib/" "$WORKSPACE_DIR/lib/" || echo "    (lib/ may be empty or host unreachable)"

# Sync Edge Impulse wake word model
echo "  -> .arduino-bricks/models/"
rsync -avz --progress "$SOURCE_HOST:/home/arduino/.arduino-bricks/models/" "$HOME/.arduino-bricks/models/" || echo "    (EI models may be empty or host unreachable)"

# Sync config files
echo "  -> config/"
rsync -avz --progress "$SOURCE_BASE/config/" "$WORKSPACE_DIR/config/" || echo "    (config/ may be empty or host unreachable)"

echo ""
echo "Model sync complete!"
echo "Run 'docker compose up -d' to start the robot."

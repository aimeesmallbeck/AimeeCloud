#!/bin/bash
# Aimee Robot - Push clean deployment code to public AimeeCloud repo
#
# Usage:
#   bash deploy/push-public.sh

set -e

cd "$HOME/aimee-robot-ws"

echo "Pushing clean deployment code to AimeeCloud (public)..."

# Ensure we're on main
git checkout main

# Push to public remote
git push public main

echo ""
echo "Public push complete!"
echo "View at: https://github.com/aimeesmallbeck/AimeeCloud"

#!/bin/bash
# Keep OBSBOT camera awake by sending periodic commands

echo "Keeping camera awake... Press Ctrl+C to stop"

while true; do
    # Send a tiny movement command every 10 seconds to keep it awake
    /workspace/obsbot_helper/obsbot_ctrl gimbal 1 0 0 > /dev/null 2>&1
    sleep 10
done

#!/bin/bash
# Aimee Robot Environment Setup Script
# Source this file to configure the ROS2 environment
# Usage: source ~/aimee-robot-ws/setup_env.sh

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# ROS2 Humble setup
if [ -f /opt/ros/humble/setup.bash ]; then
    source /opt/ros/humble/setup.bash
elif [ -f /usr/opt/ros/humble/setup.bash ]; then
    source /usr/opt/ros/humble/setup.bash
else
    echo "WARNING: ROS2 Humble setup not found!"
fi

export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
# Cyclone DDS configuration (replaced Fast DDS for Nav2 stability)


# Aimee Robot workspace
if [ -f "${SCRIPT_DIR}/install/setup.bash" ]; then
    source "${SCRIPT_DIR}/install/setup.bash"
fi

# Aimee Robot specific environment variables
export AIMEE_ROBOT_WS="${SCRIPT_DIR}"
export AIMEE_ROBOT_NAME="${AIMEE_ROBOT_NAME:-ron}"  # Default to 'ron'
export AIMEE_ROBOT_CONFIG="${SCRIPT_DIR}/config/robot_config.yaml"
export AIMEE_SKILLS_CONFIG="${SCRIPT_DIR}/config/skills_config.yaml"

# Model paths
export AIMEE_MODELS_DIR="${SCRIPT_DIR}/models"
export VOSK_MODEL_PATH="${AIMEE_MODELS_DIR}/vosk/vosk-model-small-en-us-0.15"
export LLM_MODEL_PATH="${AIMEE_MODELS_DIR}/llm/Qwen2.5-0.5B-Instruct-Q4_K_M.gguf"

# Edge Impulse wake word model
export EI_MODEL_PATH="/home/arduino/.arduino-bricks/models/custom-ei/model.eim"

# OBSBOT camera configuration
export OBSBOT_IP="${OBSBOT_IP:-192.168.5.1}"
export OBSBOT_PORT="${OBSBOT_PORT:-16284}"

# AimeeCloud configuration
export AIMEE_CLOUD_ENDPOINT="${AIMEE_CLOUD_ENDPOINT:-http://209.38.147.67:8089}"
export AIMEE_API_KEY="${AIMEE_API_KEY:-}"  # Set via environment or secrets

# Logging configuration
export RCUTILS_LOGGING_BUFFERED_STREAM=1
export RCUTILS_COLORIZED_OUTPUT=1
export RCUTILS_LOGGING_USE_STDOUT=0

# Console output format
export RCUTILS_CONSOLE_OUTPUT_FORMAT="[{severity}] [{name}]: {message}"

# Python path for bricks
export PYTHONPATH="${SCRIPT_DIR}/src:${PYTHONPATH}"

echo "=========================================="
echo "Aimee Robot Environment Configured"
echo "=========================================="
echo "Workspace: ${AIMEE_ROBOT_WS}"
echo "Robot Name: ${AIMEE_ROBOT_NAME}"
echo "DDS: Cyclone DDS (Nav2-stable)"
echo "RMW Implementation: ${RMW_IMPLEMENTATION}"
echo "=========================================="

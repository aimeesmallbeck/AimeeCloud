#!/bin/bash
source /opt/ros/humble/setup.bash
source /workspace/install/setup.bash

# Minimal robot bringup for SLAM testing
# Disables vision, voice, TTS, LLM, intent, skills, cloud, monitor to save CPU/RAM
ros2 launch aimee_bringup robot.launch.py \
  use_vision:=false use_voice:=false use_tts:=false use_llm:=false \
  use_intent:=false use_skills:=false use_cloud:=false use_monitor:=false \
  > /tmp/robot_minimal.log 2>&1 &
ROBOT_PID=$!
echo "Robot launch PID: $ROBOT_PID"

sleep 8

# Nav2 + SLAM
ros2 launch aimee_bringup nav2.launch.py slam:=True use_sim_time:=false \
  > /tmp/nav2_minimal.log 2>&1 &
NAV2_PID=$!
echo "Nav2 launch PID: $NAV2_PID"

wait $ROBOT_PID

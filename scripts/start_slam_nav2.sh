#!/bin/bash
source /opt/ros/humble/setup.bash
source /workspace/install/setup.bash

# Robot base + sensors (disable heavy software to save RAM)
ros2 launch aimee_bringup robot.launch.py \
  use_voice:=false use_llm:=false use_monitor:=false use_cloud:=false \
  > /tmp/robot.launch.log 2>&1 &
ROBOT_PID=$!
echo "Robot launch PID: $ROBOT_PID"

# Wait for base controller and lidar to initialize
sleep 8

# Nav2 + SLAM
ros2 launch aimee_bringup nav2.launch.py slam:=True use_sim_time:=false \
  > /tmp/nav2.launch.log 2>&1 &
NAV2_PID=$!
echo "Nav2 launch PID: $NAV2_PID"

# Keep script alive so docker exec -d does not reap children
wait $ROBOT_PID

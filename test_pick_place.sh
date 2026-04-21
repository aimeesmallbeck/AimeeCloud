#!/bin/bash
# Test script for pick/place without vision
# Runs inside the ROS2 Docker container

source /ros_entrypoint.sh
source /workspace/install/setup.bash

# Kill any stale ROS2 nodes to avoid topic collisions
echo "=== Cleaning up any stale nodes... ==="
ros2 daemon stop 2>/dev/null
sleep 1
ros2 daemon start 2>/dev/null
sleep 1

echo "=== Starting RoArm-M3 HTTP Driver ==="
ros2 run aimee_lerobot_bridge roarm_m3_http_driver \
    --ros-args -p arm_ip:=192.168.1.57 -p poll_rate:=5.0 &
DRIVER_PID=$!
sleep 3

echo "=== Starting PickPlace Server (test mode) ==="
ros2 run aimee_manipulation pick_place_server \
    --ros-args -p test_mode:=true &
SERVER_PID=$!
sleep 3

echo "=== Sending test goal: top_down pick/place ==="
# Use Python client instead of CLI for reliable long-running action handling
ros2 run aimee_manipulation test_pick_place_client \
    --ros-args -p object:=top_down -p enable_place:=true -p timeout:=120.0

EXIT_CODE=$?

echo "=== Test complete (exit code: $EXIT_CODE). Shutting down nodes... ==="
kill $SERVER_PID $DRIVER_PID 2>/dev/null
wait
exit $EXIT_CODE

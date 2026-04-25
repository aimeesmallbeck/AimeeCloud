#!/bin/bash
source /opt/ros/humble/setup.bash
source /workspace/install/setup.bash

# Launch aimee_nav with zero speed (no movement)
ros2 run aimee_nav aimee_nav_node \
  --ros-args \
  -p max_speed:=0.0 \
  -p rover_http_ip:='192.168.1.56' \
  -p grid_size_m:=8.0 \
  -p grid_resolution_m:=0.08 &
NODE_PID=$!

sleep 8

echo "=== Topics ==="
ros2 topic list | grep -E 'scan|odom|map|path|cmd_vel|goal'

echo ""
echo "=== TF Frames ==="
ros2 run tf2_ros tf2_frames 2>&1 | grep -E 'map|odom|base_link|base_laser'

echo ""
echo "=== LaserScan sample ==="
ros2 topic echo /scan --once 2>&1 | head -15

echo ""
echo "=== Map sample ==="
ros2 topic echo /map --once 2>&1 | head -15

kill $NODE_PID 2>/dev/null
sleep 1
kill -9 $NODE_PID 2>/dev/null
echo ""
echo "=== RVIZ CHECK COMPLETE ==="

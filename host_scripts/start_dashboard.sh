#!/bin/bash
# Quick start AIMEE Robot + ROS2 Management Dashboard

# Stop any existing container
docker rm -f aimee-robot 2>/dev/null

# Run combined core + dashboard in single container
# This ensures reliable DDS communication between nodes
docker run -d \
    --name aimee-robot \
    --privileged \
    --network host \
    -e RMW_IMPLEMENTATION=rmw_fastrtps_cpp \
    -e ROS_DOMAIN_ID=42 \
    -v /home/arduino/aimee-robot-ws:/workspace \
    -v /dev:/dev \
    -w /workspace \
    aimee-ros-dashboard:usb-cam \
    bash -c "
        source /opt/ros/humble/setup.bash
        source /workspace/install/setup.bash
        apt-get update -qq && apt-get install -y -qq ros-humble-usb-cam || true
        pip3 install -q opencv-python-headless
        ros2 launch aimee_bringup core.launch.py &
        tail -f /dev/null
    "

echo "AIMEE Robot starting..."
sleep 5
echo "Open browser to: http://192.168.1.100:8081"

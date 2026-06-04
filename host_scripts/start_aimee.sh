#!/bin/bash
# Quick launcher for AIMEE Robot

echo "🤖 Starting AIMEE Robot..."
echo "=========================="
echo ""

# Check if AIMEE workspace is built
if [ ! -d ~/aimee-robot-ws/install ]; then
    echo "📦 First run - building workspace..."
    echo "This may take 5-10 minutes..."
    echo ""
fi

# Run AIMEE in Docker
docker run -it --rm \
    --name aimee-robot \
    --privileged \
    --network host \
    -v /home/arduino/aimee-robot-ws:/workspace \
    -v /dev:/dev \
    -v /home/arduino/.asoundrc:/root/.asoundrc \
    -w /workspace \
    ros:humble-ros-base \
    bash -c "
        source /opt/ros/humble/setup.bash
        
        # Install tools if needed
        apt-get update -qq
        apt-get install -y -qq python3-colcon-common-extensions python3-rosdep python3-pip 2>/dev/null || true
        pip3 install -q --break-system-packages flask gtts pygame vosk aiohttp 2>/dev/null || true
        
        # Build if needed
        cd /workspace
        if [ ! -f install/setup.bash ]; then
            echo '🔨 Building AIMEE workspace...'
            colcon build --symlink-install 2>&1 | tail -20
        fi
        
        # Source and run
        source install/setup.bash
        
        clear
        echo '====================================='
        echo '🤖 AIMEE Robot - ROS2 Environment'
        echo '====================================='
        echo ''
        echo '📝 Available commands:'
        echo '  ros2 run aimee_test_dashboard dashboard_node'
        echo '  ros2 topic list'
        echo '  ros2 node list'
        echo ''
        echo '📱 Dashboard URL: http://localhost:5000'
        echo ''
        echo 'Press Ctrl+D to exit'
        echo '====================================='
        echo ''
        
        bash
    "

echo ""
echo "AIMEE session ended."

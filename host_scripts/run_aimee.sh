#!/bin/bash
# Run AIMEE Robot in ROS2 Docker container

# Check if docker daemon is running
if ! sudo docker info > /dev/null 2>&1; then
    echo "Starting Docker daemon..."
    sudo systemctl start docker
fi

# Run AIMEE workspace in Docker
sudo docker run -it --rm \
    --name aimee-robot \
    --privileged \
    --network host \
    -v /home/arduino/aimee-robot-ws:/workspace \
    -v /dev:/dev \
    -v /home/arduino/.asoundrc:/root/.asoundrc \
    -w /workspace \
    ros:humble-ros-base \
    bash -c "
        # Setup ROS2
        source /opt/ros/humble/setup.bash
        
        # Install colcon
        apt update && apt install -y python3-colcon-common-extensions python3-rosdep
        
        # Initialize rosdep if needed
        rosdep init 2>/dev/null || true
        rosdep update
        
        # Build workspace
        cd /workspace
        if [ ! -d install ]; then
            echo 'Building AIMEE workspace...'
            rosdep install --from-paths src --ignore-src -y
            colcon build --symlink-install
        fi
        
        source install/setup.bash
        echo 'AIMEE Robot Ready!'
        echo 'Try: ros2 run aimee_test_dashboard dashboard_node'
        bash
    "

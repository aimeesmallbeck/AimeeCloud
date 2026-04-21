#!/bin/bash
# Start the ROS2 Monitor Dashboard

echo "🔍 Starting AIMEE ROS2 Monitor Dashboard..."
echo ""

# Check if ROS2 is running
if ! docker exec aimee-robot pgrep -f "ros2" > /dev/null 2>&1; then
    echo "⚠️  Warning: ROS2 doesn't appear to be running"
    echo "   Start ROS2 first with: ros2 launch aimee_bringup core.launch.py"
    echo ""
fi

# Run the monitor node
docker exec -it aimee-robot bash -c "
    source /opt/ros/humble/setup.bash
    source /workspace/install/setup.bash
    ros2 run aimee_ros2_monitor monitor_node
"

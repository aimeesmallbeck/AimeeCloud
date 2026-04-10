#!/bin/bash
# AIMEE Robot Testing Session
# This script starts all components for testing

set -e

echo "========================================"
echo "🤖 AIMEE Robot - Testing Session"
echo "========================================"
echo ""

# Source environment
echo "📋 Sourcing environment..."
source ~/aimee-robot-ws/setup_env.sh
cd ~/aimee-robot-ws

echo ""
echo "🚀 Starting AIMEE components..."
echo ""

# Function to start a component in background
start_component() {
    local name=$1
    local command=$2
    echo "  Starting $name..."
    $command &
    sleep 2
}

# Start components
echo "1️⃣  Starting Test Dashboard..."
ros2 run aimee_test_dashboard dashboard_node &
DASHBOARD_PID=$!
sleep 3

echo ""
echo "========================================"
echo "✅ Dashboard started!"
echo "========================================"
echo ""
echo "📱 Open browser to: http://localhost:5000"
echo ""
echo "📝 Testing Checklist:"
echo "   [ ] Dashboard loads in browser"
echo "   [ ] ROS2 status shows connected"
echo "   [ ] Microphone test works"
echo "   [ ] Speaker test works"
echo "   [ ] TTS test works (simulation)"
echo "   [ ] LLM test works (simulation)"
echo "   [ ] Full pipeline test works"
echo ""
echo "⚠️  Skills default to SIMULATION mode"
echo "   Toggle to REAL only when ready for hardware"
echo ""
echo "Press Ctrl+C to stop all components"
echo ""

# Wait for interrupt
trap "echo 'Stopping...'; kill $DASHBOARD_PID 2>/dev/null; exit" INT
wait

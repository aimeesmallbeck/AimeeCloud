#!/bin/bash
# Setup udev rules for Aimee Robot USB devices
# Run with sudo when both rover and lidar are connected to identify them

RULES_FILE=/etc/udev/rules.d/99-aimee-robot.rules

echo "Creating udev rules for Aimee Robot..."

# LD19 Lidar (Silicon Labs CP210x UART Bridge)
# Verified ID: 10c4:ea60
cat > "$RULES_FILE" <<'EOF'
# Aimee Robot USB Serial Devices
# LD19 Lidar (CP210x)
SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", SYMLINK+="lidar", MODE="0666"

# Waveshare General Driver / Wave Rover (CH340) — uncomment after verifying with lsusb
# SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", SYMLINK+="rover", MODE="0666"
EOF

echo "Reloading udev rules..."
udevadm control --reload-rules
udevadm trigger

echo "Done. Rules written to $RULES_FILE"
echo ""
echo "Current USB serial devices:"
ls -l /dev/ttyUSB* /dev/ttyACM* 2>/dev/null || echo "  (none found)"
echo ""
echo "To verify rover USB ID, power it on and run: lsusb | grep -i waveshare"
echo "Then update $RULES_FILE with the correct idVendor/idProduct for the rover."

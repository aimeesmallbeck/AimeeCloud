#!/bin/bash
# Setup udev rules for Aimee Robot USB devices
# Both LD19 lidar and Wave Rover use CP210x chips (10c4:ea60), so we distinguish by serial.
#
# Verified serials (update these if hardware changes):
#   Wave Rover: 7a4ad02fc773ef11ade0c68c8fcc3fa0  -> /dev/aimee_rover
#   LD19 Lidar: 0001                               -> /dev/aimee_lidar
#
# Run with sudo when both devices are connected.

RULES_FILE=/etc/udev/rules.d/99-aimee-robot.rules

echo "Creating udev rules for Aimee Robot..."

cat > "$RULES_FILE" <<'EOF'
# Aimee Robot USB Serial Devices
# Wave Rover (CP210x)
SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", ATTRS{serial}=="7a4ad02fc773ef11ade0c68c8fcc3fa0", SYMLINK+="aimee_rover", MODE="0666"

# LD19 Lidar (CP210x)
SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", ATTRS{serial}=="0001", SYMLINK+="aimee_lidar", MODE="0666"
EOF

echo "Reloading udev rules..."
udevadm control --reload-rules
udevadm trigger

echo "Done. Rules written to $RULES_FILE"
echo ""
echo "Current USB serial devices:"
ls -l /dev/ttyUSB* /dev/aimee_* 2>/dev/null || echo "  (none found)"
echo ""
echo "To update serial numbers, run:"
echo "  udevadm info -a -n /dev/ttyUSB0 | grep serial"
echo "  udevadm info -a -n /dev/ttyUSB1 | grep serial"

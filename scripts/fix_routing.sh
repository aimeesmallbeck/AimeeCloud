#!/bin/bash
# Aimee Robot Network Routing Fix
# 
# Prevents OBSBOT USB RNDIS from hijacking default gateway
# Ensures Wi-Fi remains primary route for internet traffic

set -e

echo "[Aimee Routing] Configuring network routes..."

# Get primary Wi-Fi gateway (adjust interface name as needed)
WIFI_INTERFACE="wlan0"
USB_INTERFACE="usb0"

# Find Wi-Fi gateway
WIFI_GATEWAY=$(ip route show dev $WIFI_INTERFACE | grep default | awk '{print $3}' | head -n1)

if [ -z "$WIFI_GATEWAY" ]; then
    echo "[Aimee Routing] WARNING: Could not find Wi-Fi gateway"
    echo "[Aimee Routing] Checking current routes:"
    ip route show
    exit 0
fi

echo "[Aimee Routing] Wi-Fi Gateway: $WIFI_GATEWAY"

# Delete default route via USB if it exists (with lower metric)
ip route del default via 192.168.5.1 2>/dev/null || true
ip route del default dev $USB_INTERFACE 2>/dev/null || true

# Ensure default route is via Wi-Fi with high priority (low metric)
if ! ip route show | grep -q "default via $WIFI_GATEWAY"; then
    echo "[Aimee Routing] Adding default route via Wi-Fi"
    ip route add default via $WIFI_GATEWAY dev $WIFI_INTERFACE metric 100
fi

# Add specific route for OBSBOT (local subnet only)
if ip link show $USB_INTERFACE &>/dev/null; then
    echo "[Aimee Routing] Adding OBSBOT subnet route"
    ip route add 192.168.5.0/24 dev $USB_INTERFACE metric 800 2>/dev/null || true
fi

# Verify routing
echo "[Aimee Routing] Current routing table:"
ip route show

# Test connectivity
echo "[Aimee Routing] Testing connectivity..."
if ping -c 1 -W 2 8.8.8.8 &>/dev/null; then
    echo "[Aimee Routing] ✓ Internet connectivity OK"
else
    echo "[Aimee Routing] ✗ Internet connectivity FAILED"
fi

if ping -c 1 -W 2 192.168.5.1 &>/dev/null; then
    echo "[Aimee Routing] ✓ OBSBOT camera reachable"
else
    echo "[Aimee Routing] ⚠ OBSBOT camera not reachable (may be disconnected)"
fi

echo "[Aimee Routing] Configuration complete"

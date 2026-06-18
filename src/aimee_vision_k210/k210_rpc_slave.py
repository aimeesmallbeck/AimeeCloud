# K210 (WonderMV) RPC Slave Script
# Upload this to your K210 board using the MaixPy IDE (OpenMV Fork).
# This script enables the K210 to respond to image and detection requests from ROS.

import sensor, image, time, rpc, struct

# 1. Initialize Camera
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA) # 320x240
sensor.run(1) # Start camera
sensor.skip_frames(time=2000)

# 2. Initialize RPC over UART
# Most WonderMV/K210 modules use UART3 or the default Serial port.
# If connecting via USB cable, use rpc.rpc_usb_vcp_slave().
# If connecting via pins (UART), use rpc_uart_slave.
interface = rpc.rpc_uart_slave(baudrate=57600)

def get_image(data):
    """Captures a snapshot and returns it as a JPEG compressed byte array."""
    # quality=50 provides a good balance between size and speed for 115200 baud
    img = sensor.snapshot().compress(quality=50)
    return img

def get_detections(data):
    """
    Performs object detection and returns data as a packed byte array.
    Example here searches for red objects.
    """
    # Define color thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
    # This is an example for 'red'
    red_threshold = (30, 100, 15, 127, 15, 127)
    
    blobs = sensor.snapshot().find_blobs([red_threshold])
    
    packet = bytes()
    for b in blobs:
        # Pack as [x, y, w, h, id] (16-bit unsigned shorts)
        # b[0]=x, b[1]=y, b[2]=w, b[3]=h
        packet += struct.pack('<HHHHH', b[0], b[1], b[2], b[3], 1)
        
    return packet

# Register callbacks
interface.register_callback(get_image)
interface.register_callback(get_detections)

print("K210 RPC Slave Ready...")
while True:
    interface.loop()

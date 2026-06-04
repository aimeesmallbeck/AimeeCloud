#!/usr/bin/env python3
"""
Manual Arm Calibration via Direct ESP32 Serial
"""
import serial
import time
import sys

# Connect directly to the ESP32 via USB
try:
    ser = serial.Serial('/dev/ttyUSB0', 921600, timeout=1)
except Exception as e:
    print(f"Error opening /dev/ttyUSB0: {e}")
    print("Please ensure the USB cable is connected.")
    sys.exit(1)

def send_command(cmd):
    ser.write((cmd + '\n').encode('utf-8'))
    ser.flush()

def read_response():
    start = time.time()
    while time.time() - start < 1.0:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            if line:
                return line
    return None

def disable_torque():
    print("Disabling torque (motors will go limp)...")
    send_command("FREEZE")
    resp = read_response()
    if resp == "FROZEN":
        print("Torque disabled. You can now move the arm manually.")
    else:
        print(f"Failed to verify freeze command. Got: {resp}")

def poll_positions():
    print("\nReading positions. Press Ctrl+C to stop.")
    print("Format: Base | S_Driv | S_Drvn | Elbow | Wrist | Roll | Gripper (Raw 0-4095)")
    print("-" * 75)
    
    try:
        while True:
            # Clear input buffer
            while ser.in_waiting:
                ser.read(ser.in_waiting)
                
            send_command("READ")
            resp = read_response()
            
            if resp and resp.startswith("POS:<") and resp.endswith(">"):
                # Parse POS:<1,2,3,4,5,6,7>
                data_str = resp[5:-1]
                vals = data_str.split(',')
                if len(vals) == 7:
                    b, sd1, sd2, e, w, r, g = vals
                    print(f"\rB:{b:>4} | S1:{sd1:>4} | S2:{sd2:>4} | E:{e:>4} | W:{w:>4} | R:{r:>4} | G:{g:>4}", end="")
                else:
                    print(f"\rMalformed data: {resp}", end="")
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\n\nCalibration stopped.")

if __name__ == "__main__":
    print("Testing connection to ESP32 Custom Firmware...")
    send_command("PING")
    if read_response() == "PONG":
        print("Connected.")
        disable_torque()
        poll_positions()
    else:
        print("Could not get PONG response. Please check connection.")
    
    ser.close()

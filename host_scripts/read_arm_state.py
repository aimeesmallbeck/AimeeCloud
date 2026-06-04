#!/usr/bin/env python3
import serial
import time
import sys

def get_arm_state(action="read"):
    try:
        # Disable DTR/RTS to prevent ESP32 reset on open
        ser = serial.Serial('/dev/ttyUSB0', 921600, timeout=1, dsrdtr=False, rtscts=False)
        ser.setDTR(False)
        ser.setRTS(False)
        time.sleep(0.5)
    except Exception as e:
        print(f"ERROR: {e}")
        return

    def send(cmd):
        print(f"Sending: {cmd}")
        ser.write((cmd + '\n').encode('utf-8'))
        ser.flush()

    def receive():
        start = time.time()
        while time.time() - start < 2.0:
            if ser.in_waiting:
                try:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    if line: 
                        print(f"Received: {line}")
                        return line
                except Exception:
                    pass
        print("Timeout waiting for response.")
        return None

    if action == "freeze":
        send("FREEZE")
        resp = receive()
        if resp == "FROZEN":
            print("SUCCESS: Torque disabled.")
        else:
            print(f"ERROR: Failed to freeze. Got: {resp}")
    
    elif action == "read":
        while ser.in_waiting: ser.read(ser.in_waiting)
        send("READ")
        resp = receive()
        if resp and resp.startswith("POS:<") and resp.endswith(">"):
            print(f"DATA:{resp[5:-1]}")
        else:
            print(f"ERROR: Invalid response: {resp}")

    ser.close()

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "read"
    get_arm_state(action)

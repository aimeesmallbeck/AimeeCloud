import serial
import time

def reset_esp32(port='/dev/ttyUSB0', baud=921600):
    try:
        print(f"Opening {port} to reset ESP32...")
        ser = serial.Serial(port, baud, timeout=2.0)
        ser.dtr = True
        ser.rts = True
        time.sleep(0.1)
        ser.dtr = False
        ser.rts = False
        time.sleep(1.0)
        ser.reset_input_buffer()
        print("ESP32 Reset via DTR/RTS successful.")
        ser.close()
    except Exception as e:
        print(f"Error resetting ESP32: {e}")

if __name__ == '__main__':
    reset_esp32()

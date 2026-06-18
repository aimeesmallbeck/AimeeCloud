import serial
import time
import sys

def upload_file(port, local_path, remote_path):
    with open(local_path, 'rb') as f:
        content = f.read()

    ser = serial.Serial(port, 115200, timeout=1)
    
    # Hardware Reset
    print("Resetting board...")
    ser.dtr = True
    ser.rts = True
    time.sleep(0.1)
    ser.dtr = False
    ser.rts = False
    time.sleep(0.5)

    # Interrupt any running script
    print("Interrupting...")
    for _ in range(20):
        ser.write(b'\x03')
        time.sleep(0.05)
    
    time.sleep(0.5)
    ser.read_all()
    
    # Enter raw REPL
    print("Entering raw REPL...")
    ser.write(b'\x01')
    time.sleep(0.5)
    res = ser.read_all()
    if b'raw REPL; CTRL-B to exit' not in res:
        print(f"Failed to enter raw REPL: {res}")
        # Continue anyway, might have missed the string
    
    # Send command to open file for writing
    print(f"Opening {remote_path} for writing...")
    cmd = f"f = open('{remote_path}', 'wb')\n".encode()
    ser.write(cmd)
    time.sleep(0.2)
    
    # Write content in chunks
    print(f"Writing {len(content)} bytes...")
    chunk_size = 64
    for i in range(0, len(content), chunk_size):
        chunk = content[i:i+chunk_size]
        hex_data = chunk.hex()
        write_cmd = f"f.write(bytes.fromhex('{hex_data}'))\n".encode()
        ser.write(write_cmd)
        time.sleep(0.1)
        res = ser.read_all()
        if b'Traceback' in res:
            print(f"Error during write at {i}: {res}")
            return False

    ser.write(b"f.close()\n")
    time.sleep(0.2)
    print("File closed.")
    
    # Exit raw REPL and soft reset
    ser.write(b'\x02\x04')
    time.sleep(0.5)
    
    output = ser.read_all()
    print(f"Upload complete. Output: {output}")
    ser.close()
    return True

if __name__ == "__main__":
    port = sys.argv[1]
    local_path = sys.argv[2]
    remote_path = sys.argv[3]
    upload_file(port, local_path, remote_path)

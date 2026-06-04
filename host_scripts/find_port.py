import serial
import msgpack
import time
from io import BytesIO

for port in ["/dev/ttyS0", "/dev/ttyS1", "/dev/ttyS2", "/dev/ttyS3", "/dev/ttyMSM0"]:
    try:
        ser = serial.Serial(port, 115200, timeout=0.1)
        ser.reset_input_buffer()
        request = [0, 42, "ping_arm", []]
        ser.write(msgpack.packb(request))
        time.sleep(0.1)
        data = ser.read(1024)
        if data:
            print(f"Got data on {port}: {data}")
            try:
                unpacker = msgpack.Unpacker(BytesIO(data))
                for msg in unpacker:
                    print(f"Parsed: {msg}")
            except:
                pass
        ser.close()
    except Exception as e:
        print(f"Could not open {port}: {e}")

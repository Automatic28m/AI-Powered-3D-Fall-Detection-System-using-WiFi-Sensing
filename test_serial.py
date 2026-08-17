import serial
import time

PORT = '/dev/cu.usbmodem5B420199761'
BAUD_RATE = 921600

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=2)
    print(f"Listening to {PORT} for 5 seconds...")
    start = time.time()
    lines_received = 0
    while time.time() - start < 5:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(f"Data: {line[:50]}...")
                lines_received += 1
                if lines_received >= 5:
                    print("Successfully received data.")
                    break
    if lines_received == 0:
        print("Received 0 bytes. The ESP32 is completely silent.")
    ser.close()
except Exception as e:
    print(f"Error: {e}")

import serial
import time

ser = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=1)
print("CONNECTED")

s = "python"

for i in range(5):
    time.sleep(1)
    ser.write(s.encode('utf-8'))

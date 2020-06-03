import warnings
import serial
import serial.tools.list_ports
from serial import Serial
import time


data = {0,0,1,0,0,0,1,1,
        0,1,0,0,1,0,0,0,
        0,1,1,0,0,1,0,1,
        0,1,1,0,1,1,0,0,
        0,1,1,0,1,1,0,0,
        0,1,1,0,1,1,1,1,
        0,0,1,0,0,0,0,0,
        0,1,1,1,0,1,1,1,
        0,1,1,0,1,1,1,1,
        0,1,1,1,0,0,1,0,
        0,1,1,0,1,1,0,0,
        0,1,1,0,0,1,0,0,
        0,0,1,0,0,0,0,1,
        0,0,1,0,0,0,0,1,
        0,0,1,0,0,0,0,1,
        0,0,1,0,0,0,1,1,0}

dataLenght = len(data)
dataIndex = 0

ser = serial.Serial('/dev/cu.usbserial-14130', 115201, timeout=1)

print ('\n\n\n')


while True:
    ser.write(data[dataIndex])
    time.sleep(0.05)
    print(1)
    ser.write(b'1')
    time.sleep(0.05)
    print(0)

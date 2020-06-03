import warnings
import serial
import serial.tools.list_ports
from serial import Serial
import time


data = ["0","0","1","0","0","0","1","1",
        "0","1","0","0","1","0","0","0",
        "0","1","1","0","0","1","0","1",
        "0","1","1","0","1","1","0","0",
        "0","1","1","0","1","1","0","0",
        "0","1","1","0","1","1","1","1",
        "0","0","1","0","0","0","0","0",
        "0","1","1","1","0","1","1","1",
        "0","1","1","0","1","1","1","1",
        "0","1","1","1","0","0","1","0",
        "0","1","1","0","1","1","0","0",
        "0","1","1","0","0","1","0","0",
        "0","0","1","0","0","0","0","1",
        "0","0","1","0","0","0","0","1",
        "0","0","1","0","0","0","0","1",
        "0","0","1","0","0","0","1","1"]

dataLenght = len(data)
dataIndex = 0

dataRate = 0.05

ser = serial.Serial('/dev/cu.usbserial-14130', 115201, timeout=1)

print ('\n\n\n')

currentTime = time.time()
previousTime = time.time()

while True:
    currentTime = time.time()
    if(currentTime - previousTime > 0.05):
        previousTime = currentTime

        currentByte = bytes(data[dataIndex], encoding='utf-8')
        ser.write(currentByte)
        
        print(data[dataIndex])
        dataIndex+= 1
        if (dataIndex >= dataLenght):
            dataIndex = 0


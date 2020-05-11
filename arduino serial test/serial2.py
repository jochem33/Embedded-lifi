import warnings
import serial
import serial.tools.list_ports


print ('\n\nPYSERIAL\n')

sPort = '/dev/cu.usbserial-1420'

aSerialData = serial.Serial(sPort,9600)
 
while True:
    # print(aSerialData.inWaiting())
    if (aSerialData.inWaiting()>0):
        print(aSerialData)
        sData = aSerialData.readline()
        print(sData)

import warnings
import serial
import serial.tools.list_ports
from serial import Serial



print ('\n\n\n')

sPort = '/dev/cu.usbmodem141201'

aSerialData = serial.Serial(sPort,115201)

character = []
characterStr = ""


def synchronize(syncChar):
    print("\n__________________________________\nSynchronizing...")
    syncList = []
    synced = False
    while synced == False:
        if (aSerialData.inWaiting()>0):
            sData = aSerialData.readline()
            bit = str(sData)[2]
            syncList.append(bit)
            if(syncList[-8:] == syncChar and synced == False):
                print("Synchronized!\n__________________________________")
                synced = True
                text = ["\x00"]


text = ["\x00"]

print("Waiting for signal...\n")

synchronize(['0', '0', '1', '0', '0', '0', '1', '1'])


currentOkayCount = 0
totalOkayCount = 0


while True:
    if (aSerialData.inWaiting()>0):
        sData = aSerialData.readline()
        bit = str(sData)[2]
        character.append(bit)

        if (len(character) == 8):
            # print(characterStr.join(character), chr(int(characterStr.join(character), 2)))
            letter = chr(int(characterStr.join(character), 2))
            # print(letter)
            text.append(letter)
            character = []
            characterStr = ""

        if (len(text) >= 16):
            textStr = ""
            textStr = textStr.join(text)
            # if(textStr == "#Hello World!!##"):
            if(textStr[0] == "#" and textStr[-0] == "#"):
                currentOkayCount+= 1
                totalOkayCount+= 1

                file1 = open('output.txt', 'a') 
                file1.write(textStr) 
                file1.close() 

                print(textStr, currentOkayCount, totalOkayCount)
            else:
                synchronize(['0', '0', '1', '0', '0', '0', '1', '1'])
                text = ["\x00"]
                currentOkayCount = 0
            text = []



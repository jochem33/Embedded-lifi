import warnings
import serial
import serial.tools.list_ports
from serial import Serial

file1 = open('output.txt', 'w+') 
file1.write("") 
file1.close() 

lineEndChar = ['1', '0', '1', '0', '0', '1', '0', '1']
lineEndCharChar = "¥"

print ('\n\n\n')

sPort = '/dev/cu.usbmodem141201'

aSerialData = serial.Serial(sPort,115201)
9
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
            # print(bit)
            syncList.append(bit)
            # print(syncList[-8:])
            # if(syncList[-8:] == syncChar and syncList[-1] == syncChar and synced == False):
            if(syncList[-8:] == syncChar and synced == False):
                print("Synchronized!\n__________________________________")
                synced = True
                text = []


text = [""]

print("Waiting for signal...\n")

synchronize(lineEndChar)


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
            textStr = ""
            text.append(letter)
            textStr = textStr.join(text)
            print(textStr)
            character = []
            characterStr = ""

        if (len(text) >= 16):
            textStr = ""
            textStr = textStr.join(text)
            print("_" + textStr[-0] + "__" + textStr[0] + "_")
            if(textStr[0] == lineEndCharChar and textStr[-0] == lineEndCharChar):
                currentOkayCount+= 1
                totalOkayCount+= 1

                file1 = open('output.txt' + "\n", 'a') 
                file1.write(textStr) 
                file1.close() 

                print(textStr, currentOkayCount, totalOkayCount)
            else:
                synchronize(lineEndChar)
                text = [""]
                currentOkayCount = 0
            text = []



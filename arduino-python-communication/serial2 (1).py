import warnings
import serial
import serial.tools.list_ports


print ('\n\nPYSERIAL\n')

sPort = '/dev/cu.usbmodem141101'

aSerialData = serial.Serial(sPort,19200)

character = []
characterStr = ""
synced = False

print("Synchronizing...")

while True:
    if (aSerialData.inWaiting()>0):
        sData = aSerialData.readline()
        bit = str(sData)[2]
        character.append(bit)
        # if(character[-23:] == ['1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'] and synced == False):
        if(character[-8:] == ['0', '1', '0', '0', '1', '0', '0', '0'] and synced == False):
            print("Synchronized!")
            synced = True
            character = []

        if(synced):
            if (len(character) == 8):
                print(characterStr.join(character), chr(int(characterStr.join(character), 2)))
                character = []
                characterStr = ""




# while True:
#     # print(aSerialData.inWaiting())
#     if (aSerialData.inWaiting()>0):
#         # print(aSerialData, "a")
#         sData = aSerialData.readline()
#         # if len(str(sData)) > 6:
#         #     print(str(sData[-3]))
#         # else:
#         print(str(sData)[2])

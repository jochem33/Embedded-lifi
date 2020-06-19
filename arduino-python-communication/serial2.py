import warnings
import serial
import serial.tools.list_ports
from serial import Serial
import webbrowser
import os

filename = 'output.html'

file1 = open(filename, 'w+') 
file1.write("") 
file1.close() 

lineEndChar = ['1', '0', '1', '0', '0', '1', '0', '1']
lineEndCharChar = "¥"

print ('\n\n\n')

sPort = '/dev/cu.usbmodem141201'

aSerialData = serial.Serial(sPort,74880)

character = []
characterStr = ""

text = [""]
receiving = True

receivedChunks = {}

def synchronize(syncChar):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n__________________________________\nSynchronizing...")
    syncList = []
    synced = False
    while synced == False:
        if (aSerialData.inWaiting()>0):
            print(".", end="")
            sData = aSerialData.readline()
            bit = str(sData)[2]
            # print(bit)
            syncList.append(bit)
            if(syncList[-8:] == syncChar and synced == False):
                print("Synchronized!\n__________________________________")
                synced = True
                text = []


def integretyCheck(lastLineNum):
    if(len(receivedChunks) >= lastLineNum):
        print("integretycheck excellent")
        return(True)
    else:
        return(False)


print("Waiting for signal...\n")

synchronize(lineEndChar)


while receiving:
    if (aSerialData.inWaiting()>0):
        sData = aSerialData.readline()
        bit = str(sData)[2]
        character.append(bit)

        if (len(character) == 8):
            os.system('cls' if os.name == 'nt' else 'clear')
            letter = chr(int(characterStr.join(character), 2))
            # print(letter)
            textStr = ""
            text.append(letter)
            textStr = textStr.join(text)
            character = []
            characterStr = ""

            print("".join(text).replace("¥", ""))
            print("\n", receivedChunks.keys(), len(receivedChunks.keys()))
            print("\n", receivedChunks)
            

        if (len(text) >= 16):
            textStr = ""
            textStr = textStr.join(text)

            if(textStr[0] == lineEndCharChar and textStr[-0] == lineEndCharChar):
                lineNum = textStr[12:15]
                try:
                    lineNum = int(lineNum)
                    lineValid = True
                    print("Line OK")
                except ValueError:
                    print("Line invalid")
                    lineValid = False
                    synchronize(lineEndChar)
                
                if(lineValid):
                    if not(lineNum in receivedChunks):
                        print("New line")
                        receivedChunks[lineNum] = textStr[1:-4]

                    if("END" in textStr):
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("____ END ____", lineNum)
                        
                        integrety = integretyCheck(lineNum)

                        if(integrety):
                            finalFile = []
                            for i in range(lineNum):
                                # print(receivedChunks.get(i))
                                finalFile.append(receivedChunks.get(i, ""))
                            file1 = open(filename, 'a') 
                            file1.write(''.join(finalFile))
                            file1.close() 
                            receiving = False

                            webbrowser.open('file://' + os.path.realpath(filename))

                    
            else:
                synchronize(lineEndChar)
                text = [""]
            text = []



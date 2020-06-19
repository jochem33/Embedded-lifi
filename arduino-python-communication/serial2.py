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

aSerialData = serial.Serial(sPort,115201)

character = []
characterStr = ""

text = [""]
receiving = True

receivedChunks = {}

debugData = {"Synchronising": "NO",
            "syncTime":0,
            "text":"",
            "chunkValid":"",
            "newChunk":"NO"
            }


def printDebugData():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Synchronising: ", debugData["Synchronising"])
    print("syncTime: ", debugData["syncTime"])
    print("Received chunks: (", len(receivedChunks.keys()), ") ", receivedChunks.keys())
    print("Chunk valid: ", debugData["chunkValid"])
    print("New chunk: ", debugData["newChunk"])
    print("\n_________________________")
    print("Current chunk: ", debugData["text"])
    print("\n_________________________")
    print(str(receivedChunks).replace(",", "\n"))


def synchronize(syncChar):
    debugData["Synchronising"] = "YES"
    syncList = []
    synced = False
    syncTime = 0
    while synced == False:
        if (aSerialData.inWaiting()>0):
            debugData["syncTime"] = syncTime
            printDebugData()
            syncTime+=1
            # print(".", end="")
            sData = aSerialData.readline()
            bit = str(sData)[2]
            # print(bit)
            syncList.append(bit)
            debugData["syncTime"] = syncTime
            if(syncList[-8:] == syncChar and synced == False):
                if(syncList[-16:-8] == syncChar):
                    text = [lineEndCharChar]
                    print("Double syncchar!!!")
                else:
                    text = []
                debugData["Synchronising"] = "NO"
                synced = True


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
            letter = chr(int(characterStr.join(character), 2))
            # print(letter)
            textStr = ""
            text.append(letter)
            textStr = textStr.join(text)
            character = []
            characterStr = ""

            debugData["text"] = "".join(text).replace("¥", "=")

            printDebugData()
            

        if (len(text) >= 16):
            textStr = ""
            textStr = textStr.join(text)

            if(textStr[0] == lineEndCharChar and textStr[-0] == lineEndCharChar):
                lineNum = textStr[12:15]
                try:
                    lineNum = int(lineNum)
                    lineValid = True
                    debugData["chunkValid"] = "YES"
                except ValueError:
                    debugData["chunkValid"] = "NO"
                    lineValid = False
                    synchronize(lineEndChar)
                
                if(lineValid):
                    if not(lineNum in receivedChunks):
                        debugData["newChunk"] = "YES"
                        receivedChunks[lineNum] = textStr[1:-4]
                    else:
                            debugData["newChunk"] = "NO"

                    if("END" in textStr):
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
            if not(text == [lineEndCharChar]):
                text = []



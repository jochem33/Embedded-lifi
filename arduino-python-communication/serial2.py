import warnings
import serial
import serial.tools.list_ports
from serial import Serial
import webbrowser
import os


######## const setup ######
FILENAME = 'output.html'
LINE_END_CHAR = ['1', '0', '1', '0', '0', '1', '0', '1']
LINE_END_CHAR_CHAR = "¥"
sPort = '/dev/cu.usbmodem14201'
###########################



######## var setup ######
file1 = open(FILENAME, 'w+') 
file1.write("") 
file1.close() 


aSerialData = serial.Serial(sPort,115201)

character = []

text = [""]
receiving = True

receivedChunks = {}

debugData = {"Synchronising": "NO",
            "syncTime":0,
            "text":"",
            "chunkValid":"",
            "newChunk":"NO"
            }
###########################



######## printing all debuging information ######
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
###########################


######## function that looks for a syncchar in datastream ######
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
                    text = [LINE_END_CHAR_CHAR]
                    print("Double syncchar!!!")
                else:
                    text = []
                debugData["Synchronising"] = "NO"
                synced = True
###########################


######## function that checks if all chunks came in ######
def integretyCheck(lastLineNum):
    if(len(receivedChunks) >= lastLineNum):
        print("integretycheck excellent")
        return(True)
    else:
        return(False)
###########################



# first synchronisation
print("Waiting for signal...\n")
synchronize(LINE_END_CHAR)


# main loop
while receiving:
    # if serial data is found
    if (aSerialData.inWaiting()>0):

        # get bits and put them in character list
        sData = aSerialData.readline()
        bit = str(sData)[2]
        character.append(bit)

        # if 8 bits in character list
        if (len(character) == 8):
            #convert from binary to letter
            letter = chr(int("".join(character), 2))
            text.append(letter)
            character = []

            #update debug data
            debugData["text"] = "".join(text).replace("¥", "=")
            printDebugData()
        
            if not(text[0] == LINE_END_CHAR_CHAR):
                text = []
                synchronize(LINE_END_CHAR)

        if (len(text) >= 16):
            textStr = ""
            textStr = textStr.join(text)

            if(textStr[0] == LINE_END_CHAR_CHAR and textStr[-0] == LINE_END_CHAR_CHAR):
                lineNum = textStr[12:15]
                try:
                    lineNum = int(lineNum)
                    lineValid = True
                    debugData["chunkValid"] = "YES"
                except ValueError:
                    debugData["chunkValid"] = "NO"
                    lineValid = False
                    synchronize(LINE_END_CHAR)
                
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
                                finalFile.append(receivedChunks.get(i, ""))
                            file1 = open(FILENAME, 'a') 
                            file1.write(''.join(finalFile))
                            file1.close() 
                            receiving = False #end main loop

                            webbrowser.open('file://' + os.path.realpath(FILENAME))

                    
            else:
                synchronize(LINE_END_CHAR)
            if not(text == [LINE_END_CHAR_CHAR]):
                text = []



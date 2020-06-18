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

firstFileLines = []
secondFileLines = []

incorrectLines = []
# firsttransmit = True

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
            # print(syncList[-8:])
            # if(syncList[-8:] == syncChar and syncList[-1] == syncChar and synced == False):
            if(syncList[-8:] == syncChar and synced == False):
                print("Synchronized!\n__________________________________")
                synced = True
                text = []


# def integretyCheck():
#     incorrectLines = []

#     if(firstFileLines == secondFileLines):
#         print("integretycheck excellent")
#         return(True, incorrectLines)
#     else:
#         if(len(firstFileLines) > len(secondFileLines)):
#             shortestList = secondFileLines
#         else:
#             shortestList = firstFileLines

#         for i in range (len(shortestList)):
#             if not (firstFileLines[i] == secondFileLines [i]):
#                 incorrectLines.append(i)
#         return(False, incorrectLines)

def integretyCheck(lastLineNum):
    if(len(receivedChunks) == lastLineNum):
        print("integretycheck excellent")
        return(True)
    else:
        return(False)

text = [""]

print("Waiting for signal...\n")

synchronize(lineEndChar)

receiving = True

while receiving:
    if (aSerialData.inWaiting()>0):
        sData = aSerialData.readline()
        bit = str(sData)[2]
        character.append(bit)

        if (len(character) == 8):
            os.system('cls' if os.name == 'nt' else 'clear')
            # print(characterStr.join(character), chr(int(characterStr.join(character), 2)))
            letter = chr(int(characterStr.join(character), 2))
            # print(letter)
            textStr = ""
            text.append(letter)
            textStr = textStr.join(text)
            # print(textStr)
            character = []
            characterStr = ""
            # if(firsttransmit):
            #     print("true\n" + ''.join(firstFileLines), end="")
            # else:
            #     print("false\n" + ''.join(secondFileLines), end="")
            print("".join(text).replace("¥", ""))
            print("\n", receivedChunks.keys())
            print("\n", receivedChunks)
            

        if (len(text) >= 16):
            textStr = ""
            textStr = textStr.join(text)

            if(textStr[0] == lineEndCharChar and textStr[-0] == lineEndCharChar):
                lineNum = textStr[12:15]
                try:
                    lineNum = int(lineNum)
                    lineValid = True
                    print("Line valid")
                except ValueError:
                    print("Line invalid")
                    lineValid = False
                
                if(lineValid):
                    if not(lineNum in receivedChunks):
                        receivedChunks[lineNum] = textStr[1:-4]

                    if("</html>" in textStr):
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("____ END ____")
                        
                        integrety = integretyCheck(lineNum)

                        if(integrety):
                            file1 = open(filename, 'a') 
                            file1.write(''.join(''.join(receivedChunks.values()))) 
                            file1.close() 
                            receiving = False

                            webbrowser.open('file://' + os.path.realpath(filename))

                    
            else:
                synchronize(lineEndChar)
                text = [""]
            text = []



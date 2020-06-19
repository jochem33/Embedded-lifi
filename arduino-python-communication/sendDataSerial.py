import warnings
import serial
import serial.tools.list_ports
from serial import Serial
import time


######## const setup ######
dataRate = 0.05
chunkIndex = 0
dataIndex = 0
lineEndChar = "10100101"
lineEndCharChar = "¥"
writingLine = True
wholeLineLenght = 16 * 8

###########################



######## data setup ######
print("___________ Reading File ___________")

file1 = open('input.txt', 'r') 
fileContent = file1.read()
file1.close()

# fileContentWithLineEnd = lineEndCharChar + (lineEndCharChar * 2).join(fileContent[i:i + 11] for i in range(0, len(fileContent), 11)) + lineEndCharChar

# fileContentWithLineEndAndNumber = "".join(fileContentWithLineEnd[i:i + 13]+ (3 - len(str(int(i/11)))) * "0" + str(int(i/11)) for i in range(0, len(fileContentWithLineEnd), 13))

fileContentWithLineEndAndNumber = lineEndCharChar + (lineEndCharChar * 2).join(fileContent[i:i + 11]+ (3 - len(str(int(i/11)))) * "0" + str(int(i/11)) for i in range(0, len(fileContent), 11)) + lineEndCharChar


print(fileContentWithLineEndAndNumber)

binFile = "".join(f"{ord(i):08b}" for i in fileContentWithLineEndAndNumber)
binFile = binFile.replace(" ", "")

print(binFile)

binChucksListWithLineEnd = [binFile[i:i+wholeLineLenght] for i in range(0, len(binFile), wholeLineLenght)]

dataLenght = len(binChucksListWithLineEnd)
##########################



######## serial setup ######
ser = serial.Serial('/dev/cu.usbserial-1420', 74880, timeout=1)
############################



######## time setup #######
currentTime = time.time()
previousTime = time.time()
############################


print("\n\n\n ___________ Starting ___________")
while True:
    while writingLine == True:
        currentTime = time.time()
        if(currentTime - previousTime > 0.05):
            previousTime = currentTime

            currentByte = bytes(binChucksListWithLineEnd[chunkIndex][dataIndex], encoding='utf-8')
            ser.write(currentByte)
            
            # print(binChucksListWithLineEnd[chunkIndex][dataIndex])
            dataIndex+= 1
            if (dataIndex >= wholeLineLenght):
                dataIndex = 0
                writingLine = False
    
    writingLine = True
    chunkIndex+= 1
    if (chunkIndex >= dataLenght - 1):
        chunkIndex = 0
        print("\n___________ Restarting ___________")


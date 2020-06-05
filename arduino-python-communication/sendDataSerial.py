import warnings
import serial
import serial.tools.list_ports
from serial import Serial
import time

######## const setup ######
dataRate = 0.05
chunkIndex = 0
dataIndex = 0
lineEndChar = "01011111"
writingLine = True
wholeLineLenght = 16 * 8

###########################



######## data setup ######
print("___________ Reading File ___________")

file1 = open('input.html', 'r') 
fileContent = file1.read()
file1.close()

binFile = ' '.join(format(ord(x), 'b') for x in fileContent)
binFile = binFile.replace(" ", "")
lineLenght = 14 * 8

binChucksList = [binFile[i:i+lineLenght] for i in range(0, len(binFile), lineLenght)]
# binChucksListWithLineEnd = [lineEndChar + '{0}' + lineEndChar.format(element) for element in binChucksList]
binChucksListWithLineEnd = [lineEndChar + element + lineEndChar for element in binChucksList]

# print(binChucksList)

dataLenght = len(binChucksListWithLineEnd)
##########################



######## serial setup ######
ser = serial.Serial('/dev/cu.usbserial-14120', 115201, timeout=1)
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
    
    print("\n", lineEndChar + "_____ \n" + binChucksList[chunkIndex] + "\n _____" + lineEndChar)

    writingLine = True
    chunkIndex+= 1
    if (chunkIndex >= dataLenght - 1):
        chunkIndex = 0
        print("\n___________ Restarting ___________")


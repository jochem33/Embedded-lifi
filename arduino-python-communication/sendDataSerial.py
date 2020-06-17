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
writingLine = True
wholeLineLenght = 16 * 8

###########################



######## data setup ######
print("___________ Reading File ___________")

# file1 = open('input.txt', 'r') 
# fileContent = file1.read()
# file1.close()

# binFile = ' '.join(format(ord(x), 'b') for x in fileContent)
# binFile = binFile.replace(" ", "")
binFile = "001111000010000101000100010011110100001101010100010110010101000001000101001000000110100001110100011011010110110000111110000010100011110001101000011101000110110101101100001111100000101000100000001000000010000000100000001111000110100001100101011000010110010000111110000010100010000000100000001000000010000000100000001000000010000000100000001111000111010001101001011101000110110001100101001111100101010001100101011100110111010001110011011010010111010001100101001111000010111101110100011010010111010001101100011001010011111000001010001000000010000000100000001000000011110000101111011010000110010101100001011001000011111000001010001000000010000000100000001000000011110001100010011011110110010001111001001111100000101000100000001000000010000000100000001000000010000000100000001000000011110001101000001100010011111001001000011001010110000101100100011010010110111001100111001111000010111101101000001100010011111000001010001000000010000000100000001000000010000000100000001000000010000000111100011100000011111001001000011001010110110001101100011011110010000001010111011011110111001001101100011001000010000100111100001011110111000000111110000010100010000000100000001000000010000000111100001011110110001001101111011001000111100100111110000010100011110000101111011010000111010001101101011011000011111000001010"
print(binFile)
lineLenght = 14 * 8

binChucksList = [binFile[i:i+lineLenght] for i in range(0, len(binFile), lineLenght)]
# binChucksListWithLineEnd = [lineEndChar + '{0}' + lineEndChar.format(element) for element in binChucksList]
binChucksListWithLineEnd = [lineEndChar + element + lineEndChar for element in binChucksList]

# print(binChucksList)

dataLenght = len(binChucksListWithLineEnd)
##########################



######## serial setup ######
ser = serial.Serial('/dev/cu.usbserial-1420', 115201, timeout=1)
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


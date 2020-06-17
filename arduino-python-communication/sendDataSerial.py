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
binFile = "00100000001000000010000000100000001000000010000000100000001000000010000000100000001000000010000000100000001000000010000000100000001000000011110000100001010001000100111101000011010101000101100101010000010001010010000001101000011101000110110101101100001111100000101000111100011010000111010001101101011011000011111000001010001000000010000000100000001000000011110001101000011001010110000101100100001111100000101000100000001000000010000000100000001000000010000000100000001000000011110001110100011010010111010001101100011001010011111001010100011001010111001101110100011100110110100101110100011001010011110000101111011101000110100101110100011011000110010100111110000010100010000000100000001000000010000000111100001011110110100001100101011000010110010000111110000010100010000000100000001000000010000000111100011000100110111101100100011110010011111000001010001000000010000000100000001000000010000000100000001000000010000000111100011010000011000100111110010010000110010101100001011001000110100101101110011001110011110000101111011010000011000100111110000010100010000000100000001000000010000000100000001000000010000000100000001111000111000000111110010010000110010101101100011011000110111100100000010101110110111101110010011011000110010000100001001111000010111101110000001111100000101000100000001000000010000000100000001111000010111101100010011011110110010001111001001111100000101000111100001011110110100001110100011011010110110000111110000010100011110000101111011010000111010001101101011011000011111000001010"
print(binFile)
lineLenght = 14 * 8

binChucksList = [binFile[i:i+lineLenght] for i in range(0, len(binFile), lineLenght)]

lastLineLenght = len(binChucksList[-1])/8
print(lastLineLenght)
binChucksList[-1] = binChucksList[-1] + "00100000" * int(lineLenght - lastLineLenght)

lastLineLenght = len(binChucksList[-1])/8
print(lastLineLenght)

binChucksListWithLineEnd = [lineEndChar + element + lineEndChar for element in binChucksList]

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


from scipy.io import wavfile as wav
from scipy.fftpack import fft
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plot

from os import listdir
from os.path import isfile, join, exists


def distanceOfTwoArrays(first, second):
    res = 0
    smallArray = first
    largeArray = second
    if len(first) > len(second):
        smallArray = second
        largeArray = first
    
    for i in range(len(largeArray) - len(smallArray)):
        smallArray.append(0)

    for i in range(len(largeArray)):
        res += (smallArray[i] - largeArray[i])

    return res


if (not exists('learned')):
    print("error: no learned data found!")
    exit()

# Read learned data
print("Reading learned data")
leadrnedgFilesDirectory = 'learned/'
learnedFiles = listdir(leadrnedgFilesDirectory)
knowledge = {}
for learnedFile in learnedFiles:
    path = join(leadrnedgFilesDirectory, learnedFile)
    word = learnedFile[0:-4]
    file = open(path, 'r')
    for line in file.readlines():
        if word in knowledge:
            knowledge[word].append(int(line))
        else:
            knowledge[word] = [int(line)]
print("Finished")

p1 = []
p2 = []
for i in range(500):
    p1.append(knowledge['yes'][i])
    p2.append(knowledge['no'][i])
plot.plot(p1, 'b', label='yes')
plot.plot(p2, 'r', label='no')
plot.legend()

plot.show()


# rate, data = wav.read('file.wav')
rate, data = wav.read('train/no10.wav')
FourierTransformOfData = np.fft.fft(data, 44100)

# Convert fourier transform complex number to integer numbers
for i in range(len(FourierTransformOfData)):
    FourierTransformOfData[i] = int(np.absolute(FourierTransformOfData[i]))

minimumDistanceKey = ""
minimumDistanceValue = -1
for word in knowledge.keys():
    temp = distanceOfTwoArrays(FourierTransformOfData, knowledge[word])
    if (temp < minimumDistanceValue or minimumDistanceValue == -1):
        minimumDistanceValue = temp
        minimumDistanceKey = word

print(minimumDistanceKey)
print(distanceOfTwoArrays(FourierTransformOfData, knowledge['yes']))
print(distanceOfTwoArrays(FourierTransformOfData, knowledge['no']))

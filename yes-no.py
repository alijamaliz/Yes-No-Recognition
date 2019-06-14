from scipy.io import wavfile as wav
from scipy.fftpack import fft
from scipy.signal import argrelextrema
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plot

from os import listdir
from os.path import isfile, join, exists

effectiveRange = 600

def isSignalMortal(signal):
    section1 = 0
    for i in range(0, int(len(signal) / 3)):
        section1 += signal[i]
    section2 = 0
    for i in range(int(len(signal) / 3), int(2 * len(signal) / 3)):
        section2 += signal[i]
    section3 = 0
    for i in range(int(2 * len(signal) / 3), len(signal)):
        section3 += signal[i]
    if (section1 > section2 and section2 > section3 and section1):
        if (signalFirstPeakValue(signal) > 10000):
            return True;
    return False;

def signalFirstPeakValue(signal):
    res = 0
    for i in range(0, int(len(signal) / 6)):
        if (signal[i] > res):
            res = signal[i]
    return res

def energyOfSignal(signal):
    res = 0
    for i in range(0, len(signal)):
        res += signal[i]**2
    return res

def signalExtermasCount(signal):
    greater = len(argrelextrema(np.asarray(limitedFourierTransformOfData), np.greater)[0])
    less = len(argrelextrema(np.asarray(limitedFourierTransformOfData), np.less)[0])
    return greater + less

def recogniseYesNo(signal): 
    if (isSignalMortal(signal)):
        if (signalFirstPeakValue(signal) > 100000):
            return True
        else:
            return False
    else:
        if (energyOfSignal(limitedFourierTransformOfData) > 10000000000): 
            return False
        else:
            if (signalExtermasCount(limitedFourierTransformOfData) < 300):
                return False
            else:
                return True

correctAnswers = 0
trainingFilesDirectory = 'train/'
trainingFiles = listdir(trainingFilesDirectory)
index = 1
for file in trainingFiles:
    path = join(trainingFilesDirectory, file)
    if isfile(path) and 'wav' in path:
        rate, data = wav.read(path)
        data = np.array(data,dtype='int')
        FourierTransformOfData = np.fft.fft(data, 44100)
        FourierTransformOfData[0] = 0
        for i in range(effectiveRange):
            FourierTransformOfData[i] = int(np.absolute(FourierTransformOfData[i]))

        limitedFourierTransformOfData = []
        for i in range(effectiveRange):
            limitedFourierTransformOfData.append(FourierTransformOfData[i])

        word = ''.join([i for i in file[0:-5] if not i.isdigit()]) # Extract word from file name
        recognised = ""
        if (recogniseYesNo(limitedFourierTransformOfData)):
            recognised = "yes"
        else:
            recognised = "no"
        if (recognised == word):
            correctAnswers += 1
        print('{}: \033[93m{}\033[0m -> \033[92m{}\033[0m -> {}'.format(index, path, word, recognised))
        index += 1

print ('Number of correct recognitions: {} ({}%)'.format(correctAnswers, (correctAnswers / (index - 1)) * 100))
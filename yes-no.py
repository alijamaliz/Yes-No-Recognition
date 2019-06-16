from scipy.io import wavfile as wav
from scipy.fftpack import fft
from scipy.signal import argrelextrema
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plot

from os import listdir
from os.path import isfile, join, exists

effectiveRange = 1500

FORMAT = pyaudio.paInt16 # format of sampling 16 bit int
CHANNELS = 1 # number of channels it means number of sample in every sampling
RATE = 20000 # number of sample in 1 second sampling
CHUNK = 1000 # length of every chunk
RECORD_SECONDS = 0.2 # time of recording in seconds
WAVE_OUTPUT_FILENAME = "file.wav" # file name
TOTAL_RECORD_SECONDS = 2

audio = pyaudio.PyAudio()

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
    energy1 = energyOfSignal(signal[0:1000])
    energy2 = energyOfSignal(signal[1000:-1])
    if (energy1 / energy2 > 100):
        return False
    else:
        return True

last2SecondsData = []
while (True):
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    # stop Recording
    stream.stop_stream()
    stream.close()

    # storing voice
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    rate, data = wav.read('file.wav')
    if len(last2SecondsData) == TOTAL_RECORD_SECONDS * RATE:
        last2SecondsData = last2SecondsData[len(data) - 1:-1]
    last2SecondsData.extend(data)

    if len(last2SecondsData) == TOTAL_RECORD_SECONDS * RATE:
        FourierTransformOfData = np.fft.fft(data, int(TOTAL_RECORD_SECONDS * RATE))
        # FourierTransformOfData[0] = 0
        for i in range(effectiveRange):
            FourierTransformOfData[i] = int(np.absolute(FourierTransformOfData[i]))

        limitedFourierTransformOfData = []
        for i in range(effectiveRange):
            limitedFourierTransformOfData.append(np.real(FourierTransformOfData[i]))

        recognised = ""

        if (np.average(limitedFourierTransformOfData) > 200000):
            if (recogniseYesNo(limitedFourierTransformOfData)):
                recognised = "yes"
            else:
                recognised = "no"
            print("\033[93mListening:\033[0m",  "\033[92m{}\033[0m".format(recognised), "        ", end='\r')
        else:
            print("\033[93mListening: ...          \033[0m", end='\r')

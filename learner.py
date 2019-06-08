import sys
from scipy.io import wavfile as wav
from os import listdir, mkdir
from os.path import isfile, join, exists
import numpy as np
import matplotlib.pyplot as plot

def sumTwoArrays(first, second):
    res = []
    smallArray = first
    largeArray = second
    if len(first) > len(second):
        smallArray = second
        largeArray = first
    
    for i in range(len(smallArray)):
        res.append(smallArray[i] + largeArray[i])
    
    for i in range(len(largeArray) - len(smallArray)):
        res.append(largeArray[len(smallArray) + i])
    return res

# Collect data from files
sumOfAll = {}
countOfAll = {}
trainingFilesDirectory = 'train/'
trainingFiles = listdir(trainingFilesDirectory)
index = 1
for file in trainingFiles:
    path = join(trainingFilesDirectory, file)
    if isfile(path) and 'wav' in path:
        rate, data = wav.read(path)
        data = np.array(data,dtype='int')
        FourierTransformOfData = np.fft.fft(data, 44100)
        for i in range(len(FourierTransformOfData)):
            FourierTransformOfData[i] = int(np.absolute(FourierTransformOfData[i]))
        word = ''.join([i for i in file[0:-5] if not i.isdigit()]) # Reeconize word
        print('{}: \033[93m{}\033[0m -> \033[92m{}\033[0m'.format(index, path, word))
        index += 1
        if (word in sumOfAll):
            # The word is already in sumOfAll dictionary
            sumOfAll[word] = sumTwoArrays(FourierTransformOfData, sumOfAll[word])
            countOfAll[word] += 1
            pass
        else:
            sumOfAll[word] = FourierTransformOfData
            countOfAll[word] = 1

# Log all learned words
index = 1
print('\nTotal learned items:')
for word in countOfAll.keys():
    print('{}: \033[93m{}\033[0m -> \033[92m{} time(s)\033[0m'.format(index, word, countOfAll[word]))
    index += 1

# Find average signal for each word
knowledge = {}
for key in sumOfAll.keys():
    knowledge[key] = [i / countOfAll[key] for i in sumOfAll[key]]

# Write files
if (not exists('learned')):
    mkdir('learned')
for word in knowledge.keys():
    f = open("learned/{}.txt".format(word), "w")
    for item in knowledge[word]:
        f.write('{}\n'.format(str(int(item))))
    f.close()

p1 = []
p2 = []
for i in range(500):
    p1.append(knowledge['yes'][i])
    p2.append(knowledge['no'][i])
plot.plot(p1, 'b', label='yes')
plot.plot(p2, 'r', label='no')
plot.legend()

plot.show()
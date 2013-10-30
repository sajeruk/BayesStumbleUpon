__author__ = 'TORIAS'
import random
trainSize = 5000

workingDir = 'D:/Development/Projects/SDA/O-course/hometask1/data/test/'

def split(sourceFilename, trainFilename, testFilename):
    with open(workingDir + sourceFilename, 'r') as f:
        allSamples = f.readlines()
    random.shuffle(allSamples)

    with open(workingDir + trainFilename, 'w') as f:
        f.writelines(allSamples[:trainSize])
    with open(workingDir + testFilename, 'w') as f:
        f.writelines(allSamples[trainSize:])

if __name__ == '__main__':
    split('train.txt','trainSamples.txt', 'testSamples.txt')
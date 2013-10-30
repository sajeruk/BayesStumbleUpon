from __future__ import division
from collections import defaultdict
from math import log
from math import exp
from sklearn import metrics

workingDir = 'D:/Development/Projects/SDA/O-course/hometask1/data/test/'
trimDown = 10000
trimUp = 17
minLen = 3

def train(samples):
    classes, freq = defaultdict(lambda : 0), defaultdict(lambda : 0)
    for line, label in samples:
        classes[label] += 1
        for word in line:
            freq[label, word] += 1
    words = [x[1] for x in freq.keys()]
    words = set(words)
    if trimUp > 0:
        freq = dict([(w, freq[w])
                 for w in sorted(freq, key = freq.get)][trimDown : -trimUp])

    return (classes, freq, len(words), sum(freq.values()))

def getFeatures(sample):
    return [item for item in sample
    if len(item) > minLen]


def classify(classifier, feats):
    classes, freqs, corpusLen, totalLen = classifier
    logs = [log(classes[cl] / len(classes)) +
    sum(log((freqs.get((cl, word), 0) + 1) / (totalLen + corpusLen))
    for word in feats) for cl in classes]
    if logs[0] - logs[1] > 600:
        return 0.0
    elif logs[1] - logs[0] > 600:
        return 1.0
    else:
        posProb = 1 / (1 + exp(logs[0] - logs[1]))
        return posProb


def test(actual, expected):
    fpr, tpr, thresholds = metrics.roc_curve(expected, actual, pos_label=1)
    auc = metrics.auc(fpr,tpr)
    print "roc-curve accuracy:", auc

def crossValidation(data):
    return 0

def writeToFile(filename, data):
    with open(workingDir + filename, 'w') as f:
        f.write('urlid,label\n')
        for urlid, label in data:
            f.write(str(urlid) + ',' + str(label) + '\n')

def main(trainFile, testFile, outputFile = '',testResult = True):
    #read samples first
    trainSamples = []
    testSamples = []
    testId = []
    with open(workingDir + trainFile, 'r') as f:
        trainSamples = f.readlines()
    with open(workingDir + testFile, 'r') as f:
        testSamples = f.readlines()
    #now select feaures
    trainSamples = [line.replace(',', '').
               replace(';', '').replace('.', '').
                replace('}', '').replace('{', '').
                replace('\\', '').replace('/', '').
               split() for line in trainSamples]



    features = [(getFeatures(line[3:]), int(line[2])) for line in trainSamples]
    #change 2 to 3 and 1 to 2
    testItems = [line.replace(',', '').
               replace(';', '').replace('.', '').
                replace('}', '').replace('{', '').
                replace('\\', '').replace('/', '').
               split() for line in testSamples]
    testId = [line[0] for line in testItems]
    #then train classifier
    classifier = train(features)

    #then check your answer
    actual = [classify(classifier, getFeatures(line[3:])) # 2 to 3
                for line in testItems]
    #print len([x for x in actual if abs(x[0] - x[1]) < 0.9])
    if testResult:
        expected = map (int, [line[2] for line in testItems]) # 1 to 2
        test(actual, expected)
    else:
        writeToFile(outputFile, zip(testId, actual))

if __name__ == '__main__':
    main('trainSamples.txt', 'testSamples.txt')
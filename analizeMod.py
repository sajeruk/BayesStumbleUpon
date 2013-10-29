from __future__ import division
import random
from collections import defaultdict
from math import log

workingDir = 'D:/Development/Projects/SDA/O-course/hometask1/data/'

def train(samples):
    classes = []
    freq = []
    return (classes, freq)

def getFeatures(sample):
    return [item for item in sample
    if len(item) > 3]


def classify(classifier, feats):
    return 1

def test(actual, expected):
    tp = fp = tn = fn = 0
    for i in xrange(len(actual)):
        if actual[i] == 1 and expected[i] == 1:
            tp += 1
        elif actual[i] == 1 and expected[i] == 0:
            fp += 1
        elif actual[i] == 0 and expected[i] == 1:
            fn += 1
        elif actual[i] == 0 and expected[i] == 0:
            tn += 1
    print 'tp: {0}, fp: {1}, tn: {2}, fn: {3}'.format(tp, fp, tn, fn)
    print 'total true', tp + tn
    print 'total false', fp + fn
    if tp > 0:
        print 'precision =', tp / (tp + fp)
    if tp > 0:
        print 'recall =', tp / (tp + fn)

def crossValidation(data):
    return 0

if __name__ == '__main__':
    #read samples first
    trainSamples = []
    testSamples = []
    with open(workingDir + 'trainSamples.txt', 'r') as f:
        trainSamples = f.readlines()
    with open(workingDir + 'testSamples.txt', 'r') as f:
        testSamples = f.readlines()
    #now select feaures
    samples = [line.replace(',', '').
               replace(';', '').replace('.', '').
               split() for line in trainSamples]
    features = [(getFeatures(line[2:]), int(line[1])) for line in samples]
    #then train classifier
    classifier = train(features)
    #then check your answer
    expected = map (int, [line.split()[1] for line in testSamples])
    actual = [classify(classifier, getFeatures(line.split()))
                for line in testSamples]
    test(actual, expected)
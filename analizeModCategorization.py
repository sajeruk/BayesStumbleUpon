#doesn't work good enough
from __future__ import division
from collections import defaultdict
from math import log
from sklearn import metrics

workingDir = 'D:/Development/Projects/SDA/O-course/hometask1/data/test/'
trimDown = 5000
trimUp = 19
minLen = 2
categories = ('?', 'arts_entertainment', 'business', 'computer_internet',
                'culture_politics', 'gaming', 'health', 'law_crime',
                'recreation', 'religion', 'science_technology', 'sports')


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
    ret = max(classes.keys(), key = lambda cl: log(classes[cl] / len(classes)) +
    sum(log((freqs.get((cl, word), 0) + 1) / (totalLen + corpusLen))
    for word in feats))
    return ret

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
    if tp > 0:
        print 'quality = ', (tp + tn) / (tp + tn + fp + fn)
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
               split() for line in trainSamples]

    samples = defaultdict()
    for theme in categories:
        samples[theme] = [doc for doc in trainSamples if doc[1] == theme]
    features = defaultdict()
    for theme in categories:
        features[theme] = [(getFeatures(line[3:]), int(line[2])) for line in
        samples.get(theme)] #change 2 to 3 and 1 to 2
    testItems = [line.replace(',', '').
               replace(';', '').replace('.', '').
               split() for line in testSamples]
    testId = [line[0] for line in testItems]
    #then train classifier
    classifier = defaultdict()
    for theme in categories:
        classifier[theme] = train(features[theme])
    #then check your answer
    actual = [classify(classifier[line[1]], getFeatures(line[3:])) # 2 to 3
                for line in testItems]
    if testResult:
        expected = map (int, [line[2] for line in testItems]) # 1 to 2
        test(actual, expected)
    else:
        writeToFile(outputFile, zip(testId, actual))

if __name__ == '__main__':
    main('trainSamples.txt', 'testSamples.txt')
import sys
import os

inputFile, qFile, eFile, outputFile, extra = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(ROOT_PATH, inputFile)
OUTPUT_PATH = os.path.join(ROOT_PATH, outputFile)
Q_PATH = os.path.join(ROOT_PATH, qFile)
E_PATH = os.path.join(ROOT_PATH, eFile)


def readInput():
    with open(INPUT_PATH, 'r', encoding="utf8") as f:
        return f.read().splitlines()


def readTrainData(PATH, dic):
    with open(PATH, 'r') as f:
        for line in f:
            (key, value) = line.split('\t')
            dic[key] = value
            if ' ' not in key:
                tags.insert(0, key)


def writeToFile(data):
    with open(OUTPUT_PATH, 'W', encoding="uft8") as f:
        f.write("\n".join(str(i) for i in data))


def getQ(t1, t2, t3):
    p1 = transitions[t1] / numWords
    p2 = transitions[t1 + " " + t2] / transitions[t1]
    p3 = transitions[t1 + " " + t2 + " " + t3] / transitions[t1 + " " + t2]
    return p3*0.9 + p2*0.09 + p1*0.01


def getE(x, y):
    return emissions[x + " " + y]/transitions[y]


def greedyChoice(sentence, tagSet):
    tagSet.insert(0, "start")
    tagSet.insert(0, "start")
    trajectory = [0 for i in range(len(sentence))]
    for j, x in enumerate(sentence):
        temp = 0
        for k, y in enumerate(tagSet[2:]):
            tagProbability = getE(x, y) * getQ(tagSet[k], tagSet[k+1], y)
            if temp < tagProbability:
                temp = tagProbability
                trajectory[j] = y
    return trajectory


def runTagger(sentences, tagSet):
    results = [[]]
    for j, i in enumerate(sentences):
        results[j] = greedyChoice(i, tagSet)
    writeToFile(results)


def readFiles():
    sentences = readInput()
    readTrainData(Q_PATH, transitions)
    readTrainData(Q_PATH, emissions)
    return len(emissions.keys()), sentences


transitions = {}
emissions = {}
tags = []
numWords, sentences = readFiles()
runTagger(sentences, tags)

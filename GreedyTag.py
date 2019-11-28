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


def readTransitions():
    with open(Q_PATH, 'r') as f:
        for line in f:
            (key, value) = line.split('\t')
            transitions[key] = float(value.rstrip())
            if ' ' not in key:
                tags.insert(0, key)
        sumValues = sum(transitions.values())
        tempDic = dict(transitions)
        for i in tempDic.keys():
            if i.count(' ') == 0:
                transitions["start start " + i] = transitions[i]
                transitions["start " + i] = transitions[i]
            else:
                if i.count(' ') == 1:
                    transitions["start " + i] = transitions[i]
        transitions["start"] = sumValues
        transitions["start start"] = sumValues


def readEmissions():
    with open(E_PATH, 'r') as f:
        for line in f:
            (key, value) = line.split('\t')
            emissions[key] = float(value.rstrip())


def writeToFile(given, data):
    with open(OUTPUT_PATH, 'w') as f:
        resultList = []
        for k, i in enumerate(given):
            sentence, tagger = i.split(), data[k].split()
            result = []
            for m, j in enumerate(sentence):
                result.append("/".join([j, tagger[m]]))
            resultList.append(" ".join(pair for pair in result))
        f.write("\n".join(str(i) for i in resultList))


def getQ(t1, t2, t3):
    p1 = transitions[t1] / numWords
    try:
        p2 = transitions[t1 + " " + t2] / transitions[t1]
    except: p2 = 0
    try:
        p3 = transitions[t1 + " " + t2 + " " + t3] / transitions[t1 + " " + t2]
    except: p3 = 0
    return p3*0.9 + p2*0.09 + p1*0.01


def getE(x, y):
    try:
        return emissions[x + " " + y] / transitions[y]
    except:
        return 0


def greedyChoice(sentence, tagSet):
    trajectory = ""
    for j, x in enumerate(sentence):
        temp, tag = 0, tagSet[2]
        for k, y in enumerate(tagSet[2:]):
            tagProbability = getE(x, y) * getQ(tagSet[k], tagSet[k+1], y)
            if temp < tagProbability:
                temp, tag = tagProbability, y
        trajectory = " ".join([trajectory, tag])
    return trajectory


def runTagger(sentences, tagSet):
    results = []
    tagSet.insert(0, "start")
    tagSet.insert(0, "start")
    for j, i in enumerate(sentences):
        results.append(greedyChoice(i.split(), tagSet))
    print("done")
    writeToFile(sentences, results)


def readFiles():
    sentences = readInput()
    readTransitions()
    readEmissions()
    return len(emissions.keys()), sentences


def runTest():
    path = os.path.join(ROOT_PATH, "ass1-tagger-dev")
    with open(OUTPUT_PATH, 'r', encoding="utf8") as f:
        arr1 = f.read().split()
    with open(path, 'r', encoding="utf8") as f:
        arr2 = f.read().split()
    count = 0
    for j, i in enumerate(arr1):
        if i == arr2[j]:
            count += 1
    print("accuracy is: " + str(float(count)/float(len(arr2))))


transitions = {}
emissions = {}
tags = []

numWords, sentences = readFiles()
runTagger(sentences, tags)
runTest()
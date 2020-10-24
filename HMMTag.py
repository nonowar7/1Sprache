import sys
import os
from collections import deque
import numpy as np
import math

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


def getQ(t1, t2, t3):
    p1 = transitions[t1] / numTags
    try:
        p2 = transitions[t3 + " " + t1] / transitions[t3]
    except: p2 = 0
    try:
        p3 = transitions[t2 + " " + t3 + " " + t1] / transitions[t2 + " " + t3]
    except: p3 = 0
    return p3*0.9 + p2*0.09 + p1*0.01


def getE(x, y):
    try:
        return emissions[x + " " + y] / transitions[y]
    except:
        return 0


def initialize(sentence, pointers, tagSet, probabilities):

    probabilities[(0, "start", "start")] = 1


    for i in tagSet[2:]:
        probabilities[(1, "start", i)] = getQ(i, "start", "start")*getE(sentence[1], i)*probabilities[(0, "start", "start")]

    for i in tagSet[2:]:
        for j in tagSet[2:]:
            probabilities[(2, i, j)] = getQ(j, i, "start") * getE(sentence[2], j) * probabilities[(1, "start", i)]

    return probabilities


def viterbi(sentence, tagSet):

    tags = []
    probabilities = {}
    pointers = {}
    probabilities[(0, "start", "start")] = 1

    def S(k):
        if k in (-1, 0):
            return {"start"}
        else:
            return tagSet

    for k in range(1, len(sentence)+1):
        for u in S(k-1):
            for v in S(k):
                best, tag = 0, None
                for w in S(k-2):
                    if getE(sentence[k-1], v) != 0:
                        probability = probabilities[(k-1, w, u)]*getE(sentence[k-1], v)*getQ(w, u, v)
                        if best < probability:
                            best, tag = probability, w
                probabilities[(k, u, v)] = best
                pointers[(k, u, v)] = tag

    print(probabilities)
    best = 0
    bestU, bestV = None, None
    n = len(sentence)
    for u in S(n-1):
        for v in S(n):
            probability = probabilities[(n, u, v)]*getQ(u, v, "end")
            if best < probability:
                best = probability
                bestU = u
                bestV = v

    tags = deque()
    tags.append(bestV)
    tags.append(bestU)

    for i, k in enumerate(range(n-2, 0, -1)):
        print(i)
        print(k)
        tags.append(pointers[(k+2, tags[i+1], tags[i])])
    tags.reverse()
    print(tags)
    return tags


def runTagger(sentences, tagSet):
    results = []
    results.append(viterbi(sentences[1].split(), tagSet))
    print("done")
    writeToFile([sentences[1]], results)


def readFiles():
    sentences = readInput()
    readTransitions()
    readEmissions()
    return len(emissions.keys()), sentences


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


transitions = {}
emissions = {}
tags = []

numTags, sentences = readFiles()
runTagger(sentences, tags)


'''
   print("got here2")
    tags = []
    tags.append(pointers[0, 0, 0])
    t = str(np.char.decode(tags[0], encoding='utf8'))
    tags.append(pointers[1, 1, myD[t]])

    print("got here3")
    for i in range(0, len(sentence)-2):
        tagA = str(np.char.decode(tags[i], encoding='utf8'))
        tagB = str(np.char.decode(tags[i+1], encoding='utf8'))
        tags.append(pointers[i+2, myD[tagA], myD[tagB]])

    trajectory = " ".join(str(np.char.decode(i, encoding='utf8')) for i in tags)
    print("got here4")

'''
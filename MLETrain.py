from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import sys
import os

fileName, eFile, qFile = sys.argv[1], sys.argv[2], sys.argv[3]
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
TRAIN_PATH = os.path.join(ROOT_PATH, fileName)
sentences = []


def readTrain():
    with open(TRAIN_PATH, 'r', encoding="utf8") as f:
        global sentences
        sentences = f.read().splitlines()


def extractWordsAndTags():
    e, q = [], []
    for i in sentences:
        emissions, transitions = [], []
        sentence = i.split(" ")
        for j in sentence:
            pair = j.split("/")
            emissions.append(pair[0])
            transitions.append(pair[1])
        e.append(" ".join(emissions))
        q.append(" ".join(transitions))
    return e, q


def countTransmissions(tagSet):
    vec = CountVectorizer(lowercase=False, ngram_range=(1, 3))

    a = vec.fit_transform(tagSet).toarray()
    print(vec.get_feature_names())
    return a


def countEmissions(wordSet):
    vec = CountVectorizer(lowercase=False)
    return vec.fit_transform(wordSet).toarray()


'''
def saveToFile(fileName, data):

    path = os.path.join(ROOT_PATH, fileName)
    with open(path, 'a', encoding="utf8") as f:
        f.write()
'''

readTrain()
words, tags = extractWordsAndTags()
countTags = countTransmissions([tags[0]])
countWords = countEmissions(words)

#saveToFile(eFile, countWords)
#saveToFile(qFile, countTags)
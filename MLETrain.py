from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import sys
import os

fileName = sys.argv[1]
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


def countTransmission(str):
    vec = CountVectorizer(ngram_range=(1, 3))
    counter = vec.fit_transform(str).toarray()
    print(vec.get_feature_names())
    print(counter)


readTrain()
words, tags = extractWordsAndTags()
print(tags[0])
countTransmission([tags[0]])

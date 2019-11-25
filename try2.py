
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import re
import sys
import os

fileName, eFile, qFile = sys.argv[1], sys.argv[2], sys.argv[3]
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
TRAIN_PATH = os.path.join(ROOT_PATH, fileName)
Q_PATH = os.path.join(ROOT_PATH, qFile)
E_PATH = os.path.join(ROOT_PATH, eFile)


def readTrain():
    with open(TRAIN_PATH, 'r', encoding="utf8") as f:
        return f.read().splitlines()


def removeTransitions(txt):
    return re.sub(r'(/.+?(\s|$))', ' ', txt).rstrip()


def removeEmissions(txt):
    return re.sub(r'(^|\s).+?(/)', ' ', txt).strip()


def countTransmissions(tagsSet):
    vec = CountVectorizer(lowercase=False, ngram_range=(1, 3), preprocessor=removeEmissions)
    values = vec.fit_transform(tagsSet).sum(axis=0).A1
    names = vec.get_feature_names()
    return dict(zip(names, values))


def countEmissions(wordsSet):
    vec = CountVectorizer(lowercase=False, preprocessor=removeTransitions)
    values = (vec.fit_transform(wordsSet)).sum(axis=0).A1
    names = vec.get_feature_names()
    return dict(zip(names, values))


def saveToFile(filePath, data):
    path = os.path.join(ROOT_PATH, filePath)
    with open(path, 'w', encoding="utf8") as f:
        f.write('\n'.join('\t'.join((key, str(data[key]))) for key in data))


# need to count for 1 char?

sentences = readTrain()
transitions = countTransmissions(sentences)
emissions = countEmissions(sentences)
saveToFile(Q_PATH, transitions)
saveToFile(E_PATH, emissions)
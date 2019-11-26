
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import re
import sys
import os


fileName, qFile, eFile = sys.argv[1], sys.argv[2], sys.argv[3]
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
TRAIN_PATH = os.path.join(ROOT_PATH, fileName)
Q_PATH = os.path.join(ROOT_PATH, qFile)
E_PATH = os.path.join(ROOT_PATH, eFile)


def readFile(PATH):
    with open(PATH, 'r', encoding="utf8") as f:
        return f.read().splitlines()


def removeEmissions(txt):
    return re.sub(r'(^|\s).+?(/)', ' ', txt).strip()


def countTransmissions(tagsSet):
    vec = CountVectorizer(lowercase=False, ngram_range=(1,3), preprocessor=removeEmissions)
    values = vec.fit_transform(tagsSet).sum(axis=0).A1
    names = vec.get_feature_names()
    return dict(zip(names, values))


def countEmissions(wordsSet):
    vec = CountVectorizer(lowercase=False, token_pattern=r"(?u)\b[a-zA-Z0-9_._,_''_'_!_?_/]{1,}\b")
    values = vec.fit_transform(wordsSet).sum(axis=0).A1
    names = vec.get_feature_names()
    names = [re.sub("/", " ", s) for s in names]
    return dict(zip(names, values))


def saveToFile(filePath, data):
    path = os.path.join(ROOT_PATH, filePath)
    with open(path, 'w', encoding="utf8") as f:
        f.write('\n'.join('\t'.join((key, str(data[key]))) for key in data))


def runTrain():
    sentences = readFile(TRAIN_PATH)
    saveToFile(Q_PATH, countTransmissions(sentences))
    saveToFile(E_PATH, countEmissions(sentences))


runTrain()
# need to count for 1 char?
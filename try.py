
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import re
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


def removeEmissions(txt):
    arr = txt.split()
    print(str(' '.join((re.split('/|//', i)[-1]) for i in arr)))
    return str(' '.join((re.split('/|//', i)[-1]) for i in arr))


def countTransmissions(tagsSet):
    vec = CountVectorizer(lowercase=False, preprocessor=removeEmissions)
    values = vec.fit_transform(tagsSet).sum(axis=0).A1
    names = vec.get_feature_names()
    return dict(zip(names, values))


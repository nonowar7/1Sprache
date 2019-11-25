
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import re
import sys
import os

fileName, eFile, qFile = sys.argv[1], sys.argv[2], sys.argv[3]
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
TRAIN_PATH = os.path.join(ROOT_PATH, fileName)
sentences = []


'''
def removeTransitions(txt):
    return re.sub(r'(/.+?(\s|$))', ' ', txt).rstrip()
'''


def removeEmissions(txt):
    return re.sub(r'(^|\s).+?(/)', ' ', txt).strip()



def readTrain():
    with open(TRAIN_PATH, 'r', encoding="utf8") as f:
        global sentences
        sentences = f.read().splitlines()


def removeTransitions(txt):
    return [(re.sub(r'(/.+?(\s|$))', ' ', sentence)).rstrip() for sentence in txt]


def removeEmissions(txt):
    return [(re.sub(r'(^|\s).+?(/)', ' ', sentence)).strip() for sentence in txt]


def countTransmissions(tagsSet):
    vec = CountVectorizer(lowercase=False, ngram_range=(1, 3))
    a = vec.fit_transform(tagsSet)
    return a


def countEmissions(wordsSet):
    vec = CountVectorizer(lowercase=False)
    a = vec.fit_transform(wordsSet)
    print(vec.get_feature_names())
    return a


readTrain()
countTags = countTransmissions(sentences)
countWords = countEmissions(sentences)

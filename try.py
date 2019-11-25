
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import re
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


def removeTransitions(txt):
    return [(re.sub(r'(/.+?(\s|$))', ' ', sentence)).rstrip() for sentence in txt]


def removeEmissions(txt):
    return [(re.sub(r'(^|\s).+?(/)', ' ', sentence)).strip() for sentence in txt]


def countTransmissions(tagsSet):
    vec = CountVectorizer(lowercase=False, ngram_range=(1, 3))
    a = vec.fit_transform(tagsSet).toarray()
    print(vec.vocabulary_)
    print(vec.get_feature_names())
    return a


def countEmissions(wordsSet):
    vec = CountVectorizer(lowercase=False)
    a = vec.fit_transform(wordsSet).toarray()
    print(vec.vocabulary_)
    print(vec.get_feature_names())
    return a

'''
def saveToFile(fileName, data):

    path = os.path.join(ROOT_PATH, fileName)
    with open(path, 'a', encoding="utf8") as f:
        f.write()
'''

readTrain()
tags = removeEmissions(sentences)
words = removeTransitions(sentences)
print(words[1])
print(tags[1])
countTags = countTransmissions([tags[1]])
countWords = countEmissions([words[1]])
print(np.sum(countTags))
print(np.sum(countWords))
#saveToFile(eFile, countWords)
#saveToFile(qFile, countTags)

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
ssss = "aa/bb cc/dd ee/ff"
print(re.sub(r'(^|\s).+?(/)', ' ', ssss))
'''


def readTrain():
    with open(TRAIN_PATH, 'r', encoding="utf8") as f:
        global sentences
        sentences = f.read().splitlines()


def removeTransitions(txt):
    return [(re.sub(r'(/.+?(\s|$))', ' ', sentence)).rstrip() for sentence in txt]


def removeEmissions(txt):
    return [(re.sub(r'(^|\s).+?(/)', ' ', sentence)).strip() for sentence in txt]


'''
def countTransmissions(tagSet):
    vec = CountVectorizer(lowercase=False, ngram_range=(1, 3), analyzer=removeTransitions)
    a = vec.fit_transform(tagSet).toarray()
    print(vec.get_feature_names())
    return a


def countEmissions(wordSet):
    vec = CountVectorizer(lowercase=False)
    return vec.fit_transform(wordSet).toarray()

'''
'''
def saveToFile(fileName, data):

    path = os.path.join(ROOT_PATH, fileName)
    with open(path, 'a', encoding="utf8") as f:
        f.write()
'''

readTrain()
print(removeTransitions(sentences))
#countTags = countTransmissions([tags[0]])
#countWords = countEmissions(words)

#saveToFile(eFile, countWords)
#saveToFile(qFile, countTags)
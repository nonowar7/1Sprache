

trajectory = []
probs = []

def initialize(X, Y):
    trajectory = [[0 for x in range(X)] for y in Y]
    probs = trajectory

def viterbi(sentence, tagSet):
    x = len(sentence)
    y = len(tagSet)
    initialize(x, y)
    for i in sentence:
        for u in tagSet:
            temp = 0
                for j in probs[i]:
                    if (temp < )



'''
Created on Apr 26, 2017

@author: Chamee PC
'''
from difflib import SequenceMatcher

import enchant
import pandas as pd
from collections import Counter
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import re, collections
import string

if __name__ == '__main__':
    pass

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / N

def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


document_text = ""
# document = str(open('docA.txt','r')
correctTest = ""
# correctTest = str(open('docB.txt','r',encoding='utf8'))
document_text = document_text.lower()
correctTest = correctTest.lower()

for singleword in document_text.split():
    # singleComment = singleComment.replace("\"","")
    # re.sub('[^A-Za-z]+', '', singleword)
    languageReferance = enchant.Dict("en_US")
    if not (languageReferance.check(singleword)):
        # print(singleword + " false")
        # print(correction(singleword))
        document_text = document_text.replace(singleword, correction(singleword))
        # print(singleword + "-" + correction(singleword))

print(correctTest)
print(document_text)

wordOfOriginalText = document_text.count(" ") + 1
textCount = correctTest.count(" ") + 1
print(wordOfOriginalText)
print(textCount)

# Get Similarity ratio between two words
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def findAccuracy(text, correctText):
    text = re.sub(r'[^A-Za-z\d\s]', '', text)
    text = ''.join([i for i in text if not i.isdigit()])

    correctText = re.sub(r'[^A-Za-z\d\s]', '', correctText)
    correctText = ''.join([i for i in correctText if not i.isdigit()])

    countText = text.count(" ") + 1
    countCorrectText = correctText.count(" ") + 1

    splittedText = text.split()
    splittedOriginal = correctText.split()
    accuracyVal = 0
    count = 0

    if splittedText.__len__() == splittedOriginal.__len__():
        while count < splittedOriginal.__len__():
            val = similar(splittedText[count],splittedOriginal[count])
            print(splittedText[count] + "-" + splittedOriginal[count])
            if val == 1:
                accuracyVal += 1
            count += 1

    return accuracyVal/countCorrectText

accuracy = findAccuracy(document_text,correctTest)
print(accuracy)


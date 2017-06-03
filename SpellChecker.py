'''
Created on Apr 26, 2017

@author: Chamee PC
'''
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

#MongoDB Connection
client = MongoClient()
try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("Server available")
except ConnectionFailure:
    print("Server not available")

#Get data connection from mongoDB collection
try:
    db = client.reviewData
    collection = db.reviewData
    TripAdvisorData = pd.DataFrame(list(collection.find().limit(500)))
except ConnectionFailure:
    print("Fail to retrieve data")

# get Comments in
commentList = TripAdvisorData["Comment"]
commentList = commentList.tolist()

purifiedComments = []
purifiedList = pd.DataFrame()

# String purifying
for singleComment in commentList:

    singleComment = str(singleComment)

    #Remove first two characters in comment b' or b"
    singleComment = singleComment[2:]

    #Remove last character from a comment
    singleComment = singleComment[:-1]

    singleComment = singleComment.replace("\\'", "'").replace("\\n", " ")

    singleComment = re.sub('[!@#$.,:?"]', ' ', singleComment)

    purifiedComments.append(singleComment)
    # print(singleComment)
    # print(" ")


purifiedList["Comments"] = purifiedComments

purifiedList.to_csv(r'c:\data\pandas.txt', header=None, index=None, sep=' ', mode='a')

document_text = open('c:\data\pandas.txt', 'r')

text_string = document_text.read().lower()
text_string.rstrip("\n")

freqs = Counter(text_string.split())

print(freqs)

for singleword in freqs:
    singleComment = singleComment.replace("\"","")
    re.sub('[^A-Za-z]+', '', singleword)
    languageReferance = enchant.Dict("en_US")
    if(languageReferance.check(singleword)):
        print(singleword + " true")
    else:
        print(singleword + " false")
        print(correction(singleword))


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
    languageReferance = enchant.Dict("en_US")
    if(languageReferance.check(singleword)):
        print(singleword + "true")
    else:
        print(singleword + "false")
        print(languageReferance.suggest(input))


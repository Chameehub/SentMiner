import csv
import nltk
import random
import pandas as pd
import numpy as np


# ================================== Input Data filtering ======================================
# ==============================================================================================
# with open('questions.csv', encoding="utf8") as f:
#     reader = csv.DictReader(f)
#     raw_questions = [row['question'] for row in reader]
#
# thefile = open('purifiedData.txt', 'w')
# for question in raw_questions:
#     sep = '(A)'
#     question = question.split(sep, 1)[0]
#
#     sep = 'A.'
#     question = question.split(sep, 1)[0]
#
#     sep = '1.'
#     question = question.split(sep, 1)[0]
#
#     sep = '\n\n A'
#     question = question.split(sep, 0)[0]
#     print(question)
#
#     thefile.write("%s\n" % question)
#=================================================================================================

# get question data set
# with open('questionsDos.csv') as f:
#     reader = csv.DictReader(f)
#     raw_questions = [row['question'] for row in reader]
    # print(raw_questions)

# Get Questions to dataFrame
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

rawDataQuestion = pd.read_csv('questionsDos.csv')

# Get sentence into DatFrame
rawDataSentence = pd.read_csv('sentenceList.csv')

rawData = pd.concat([rawDataSentence,rawDataQuestion], ignore_index='true')


rawData = rawData.reindex(np.random.permutation(rawData.index))

rawData['label_num']  = rawData.type.map({'question':0, 'sentence':1})
print(rawData)

# how to define X and y (from the data) for use with COUNTVECTORIZER
X = rawData.data
y = rawData.label_num
print(X.shape)
print(y.shape)

# split X and y into training and testing sets
from sklearn.cross_validation import train_test_split
#randon stste apecify the rondonm allocation(=1 give the same result at the same time)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)


# instantiate the vectorizer
vect = CountVectorizer()

# vect = TfidfVectorizer(min_df=5,max_df = 0.8,sublinear_tf=True,use_idf=True)

print(X_train)

X_train_dtm = vect.fit_transform(X_train)

print(X_train_dtm)

X_test_dtm = vect.transform(X_test)
X_test_dtm

from sklearn import svm

svm = svm.SVC()
# train the model using X_train_dtm
svm.fit(X_train_dtm, y_train)

# make class predictions for X_test_dtm
y_pred_class = svm.predict(X_test_dtm)


# calculate accuracy of class predictions
from sklearn import metrics
print("The Accuracy of the predection is")
print(metrics.accuracy_score(y_test, y_pred_class))


# print the confusion matrix
print(metrics.confusion_matrix(y_test, y_pred_class))



#
# # get Sentence dataset
# with open('sentenceList.csv') as sentence:
#     sentReader = csv.DictReader(sentence)
#     raw_sentence = [row['sentence'] for row in sentReader]
#     # print(raw_sentence)

# # Create list with questions and sentences
# inputDataSetQnA = ([(question, 'question') for question in raw_questions] + [(sentence, 'sentence') for sentence in raw_sentence])
#
# # Shuffle Questions and Sentences
# random.shuffle(inputDataSetQnA)
#
# # Create training and test dataset
# train_set, test_set = inputDataSetQnA[500:], inputDataSetQnA[:500]
#
# # Creating data frames
# trainDataFrame = pd.DataFrame(columns=('text', 'type'))
# testDataFrame = pd.DataFrame()
# for trainSingle in train_set:
#     trainDataFrame['text'] = trainSingle[0]
#     trainDataFrame['type'] = trainSingle[1]
#
# for testSingle in test_set:
#     testDataFrame['text'] = testSingle[0]
#     testDataFrame['type'] = testSingle[1]


# print(trainDataFrame)

# classifier = nltk.NaiveBayesClassifier.train(train_set)

# print(nltk.classify.accuracy(classifier, test_set))

# print(train_set)
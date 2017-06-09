import csv
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cross_validation import train_test_split
import pandas as pd
import numpy as np
from sklearn import svm

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

# Get Questions to dataFrame
rawDataQuestion = pd.read_csv('questionsDos.csv')

# Get sentence into DatFrame
rawDataSentence = pd.read_csv('sentenceList.csv')

# Merge two data sets
rawData = pd.concat([rawDataSentence,rawDataQuestion], ignore_index='true')

# Shuffle whole dataset
rawData = rawData.reindex(np.random.permutation(rawData.index))

# Create type_num data column according to type of the data
# if data type = question => 0
# if data type = sentence => 1
rawData['type_num']  = rawData.type.map({'question':0, 'sentence':1})
print(rawData)

# Define X and y (from the data) for use with COUNTVECTORIZER
# X => data
# Y => type_num
X = rawData.data
y = rawData.type_num
print(X.shape)
print(y.shape)

# split X and y into training and testing sets
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


## regression.py implements logistic regression on the topic distribution of the users against their assigned gender. Results include correlation coefficients between gender and each topic, as well as classification error through 5-fold cross validation. 
## Author: Ana-Andreea Stoica
## Date: December 12, 2018

import pandas as pd 
import csv 
import numpy as np 
import statsmodels.api as sm
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.cross_validation import train_test_split

# read the data in pandas, set the gender as the dependent variable and the topic assignments as the independent ones; regress
data = pd.read_csv('users_and_topics100_matrixformbin.csv', header=0)
y = ['gender']
data_final_vars=data.columns.values.tolist()
y = ['gender']
X = [i for i in data_final_vars if i not in y]
X = data[X]
y = data[y]

# perform 5-fold cross validation to test the accuracy of the classifier
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
logreg = LogisticRegression()
logreg.fit(X_train, y_train)
y_pred = logreg.predict(X_test)

# print the accuracy of logistic regression
print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))

# find the confusino matrix for the predictions
confusion_matrix = confusion_matrix(y_test, y_pred)
print(confusion_matrix)

# fit logistic regression to the whole dataset to obtain correlation coefficients between each topic and gender
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())

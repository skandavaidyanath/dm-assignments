# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 13:36:51 2019

@author: Skanda
"""

import pandas as pd
import nummpy as np
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from sklearn.model_selection import train_test_split
import operator


def distance(x, y):
    count = 0
    for i in range(len(x)):
        if x[i] == y[i]:
            count += 1
    return len(x) - count


def main():
    data = pd.read_csv('nursery.data', header=None)
    le = LabelEncoder()
    data = data.apply(le.fit_transform)
    output_classes = le.classes_  #the inverse operation of label encoding to give the results at the end
    X = data.iloc[:,:8]
    y = data.iloc[:,8]
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2)
    k = 100
    index = 1
    y_preds = []
    for test_row in X_test:
        i = 0
        distances = {}
        for train_row in X_train:
            distances[i] = distance(list(test_row), list(train_row))
            i =  i + 1
        sorted_distances = sorted(distances.items(), key=operator.itemgetter(1))[:k]
        candidates = []
        for tup in sorted_distances:
            candidates.append(y_train[tup[0]])
        candidates = np.array(candidates)
        y_preds.append(np.bincount(candidates).argmax())
        print(index)
    
    '''
    Need to find accuracy and confusion matrix etc.
    '''
        
        
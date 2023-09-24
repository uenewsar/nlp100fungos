# -*- coding: utf-8 -*-

'''
55. 混同行列の作成
52で学習したロジスティック回帰モデルの混同行列（confusion matrix）を，学習データおよび評価データ上で作成せよ．

'''

import csv
import numpy as np
import pickle
from tabulate import tabulate
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from q51 import NLTKWrapper, create_features
from q52 import get_num_dict    
from q54 import read_feature_label    


def conv_dict_to_simple_list(fn):
    
    # obj consists of {str: id, str: id, ...}
    with open(fn, 'r', encoding='utf-8') as fr:
        obj = eval(fr.read())

    # get max id and make initial list
    ret = [None] * (max(obj.values()) + 1)
    # assign
    for (ek, ei) in obj.items():
        assert(ret[ei] is None)
        ret[ei] = ek
        
    return ret
    


def main():


    # load classification model
    fn = 'data/logistic_regression_model.pickle'
    print('loading model from {}'.format(fn))
    with open(fn, 'rb') as fr:
        clf = pickle.load(fr)

    # get number of features
    num_feat = get_num_dict('data/feature_dictionary.txt')


    # read label
    labels = conv_dict_to_simple_list('data/label_dictionary.txt')
    print(labels)
    print('class id to label')
    for (ei, el) in enumerate(labels):
        print(' {} {}'.format(ei, el))

    '''
    training data
    '''
    # read data
    (x, y) = read_feature_label('data/train.feature.txt', num_feat)
    # predict
    y_pred = clf.predict(x)
    # obtain confusion matrix
    print('training data')
    print(confusion_matrix(y, y_pred))
    
    '''
    validation data
    '''
    # read data
    (x, y) = read_feature_label('data/valid.feature.txt', num_feat)
    # predict
    y_pred = clf.predict(x)
    # obtain confusion matrix
    print('validation data')
    print(confusion_matrix(y, y_pred))
    
    
    '''
    test data
    '''
    # read data
    (x, y) = read_feature_label('data/test.feature.txt', num_feat)
    # predict
    y_pred = clf.predict(x)
    # obtain confusion matrix
    print('test data')
    print(confusion_matrix(y, y_pred))

    
    

if __name__=='__main__':
    main()

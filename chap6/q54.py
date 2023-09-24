# -*- coding: utf-8 -*-

'''
54. 正解率の計測
52で学習したロジスティック回帰モデルの正解率を，学習データおよび評価データ上で計測せよ．
'''

import csv
import numpy as np
import pickle
from tabulate import tabulate
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from q51 import NLTKWrapper, create_features
from q52 import get_num_dict    

def read_feature_label(fn, num_dict_id):

    obj = []
    with open(fn, 'r') as fr:
        cr = csv.reader(fr, delimiter='\t')
        # format: label \t feature vector
        for e in cr:
            obj.append({
                'label': int(e[0]),
                'feature': eval(e[1])
            })

    x = np.zeros( (len(obj), num_dict_id) )
    y = np.zeros( (len(obj),), dtype=np.int32)

    for i in range(len(obj)):
        y[i] = obj[i]['label']
        for (ek, ev) in obj[i]['feature'].items():
            x[i][ek] = ev

    return (x, y)


def main():

    # get number of features
    num_feat = get_num_dict('data/feature_dictionary.txt')

    # load classification model
    fn = 'data/logistic_regression_model.pickle'
    print('loading model from {}'.format(fn))
    with open(fn, 'rb') as fr:
        clf = pickle.load(fr)

    '''
    training data
    '''
    # read data
    (x, y) = read_feature_label('data/train.feature.txt', num_feat)
    # predict
    y_pred = clf.predict(x)
    # calc accuracy
    print('training data accuracy   {}'.format(accuracy_score(y, y_pred)))
    
    '''
    validation data
    '''
    # read data
    (x, y) = read_feature_label('data/valid.feature.txt', num_feat)
    # predict
    y_pred = clf.predict(x)
    # calc accuracy
    print('validation data accuracy {}'.format(accuracy_score(y, y_pred)))
    
    '''
    test data
    '''
    # read data
    (x, y) = read_feature_label('data/test.feature.txt', num_feat)
    # predict
    y_pred = clf.predict(x)
    # calc accuracy
    print('test data accuracy       {}'.format(accuracy_score(y, y_pred)))

    

if __name__=='__main__':
    main()

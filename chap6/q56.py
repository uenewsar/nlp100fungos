# -*- coding: utf-8 -*-

'''
56. 適合率，再現率，F1スコアの計測
52で学習したロジスティック回帰モデルの適合率，再現率，F1スコアを，評価データ上で計測せよ．
カテゴリごとに適合率，再現率，F1スコアを求め，カテゴリごとの性能をマイクロ平均（micro-average）とマクロ平均（macro-average）で統合せよ．
'''

import json
import csv
import numpy as np
import pickle
from tabulate import tabulate
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from q52 import get_num_dict    
from q54 import read_feature_label    
from q55 import conv_dict_to_simple_list


def conv_class_id2label(obj, labels):
    ret = [labels[x] for x in obj]
    return ret
    

def calc_micro_metrics(gold, pred, labels):
    '''
    caculate micro metrics (precision, recall, f1, and accuracy) by myself 
    it just reconfirms accyracy, precision, recall, and f1 become the same
    '''

    assert(len(gold)==len(pred))
    mat = {}
    for el in labels:
        mat[el] = {'tp': 0, 'fp': 0, 'fn': 0}
    
    for (eg, ep) in zip(gold, pred):
        
        if eg==ep:
            mat[eg]['tp'] += 1
        else:
            mat[eg]['fn'] += 1
            mat[ep]['fp'] += 1

    for (el, eo) in mat.items():
        eo['precision']= eo['tp'] / (eo['tp'] + eo['fp'])
        eo['recall'] = eo['tp'] / (eo['tp'] + eo['fn'])
        eo['f1-score'] = 2 * eo['precision'] * eo['recall'] / (eo['precision'] + eo['recall'])


    # calculate micro metrics
    tp = fp = fn = 0
    for (el, eo) in mat.items():
        tp += eo['tp']
        fp += eo['fp']
        fn += eo['fn']

    micro = {}
    micro['precision'] = tp / (tp + fp)
    micro['recall'] = tp / (tp + fn)
    micro['f1-score'] = 2 * micro['precision'] * micro['recall'] / (micro['precision'] + micro['recall'])

    # calculate accuracy
    cor = 0
    for (eg, ep) in zip(gold, pred):
        if eg==ep:
            cor += 1
    micro['accuracy'] = cor / len(gold)

    print('micro metrics')
    print(json.dumps(micro, indent=2))

    
        
    
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

    '''
    training data
    '''
    # read data
    (x, y) = read_feature_label('data/train.feature.txt', num_feat)
    # predict
    y_pred = clf.predict(x)

    # convert class id to class label
    y_pred = conv_class_id2label(y_pred, labels)
    y = conv_class_id2label(y, labels)
    
    # calculate performance
    print('----\ntraining data\n----')
    print('macro metrics')
    print(json.dumps(classification_report(y, y_pred, output_dict=True), indent=2))
    calc_micro_metrics(y, y_pred, labels)

    '''
    validation data
    '''
    # read data
    (x, y) = read_feature_label('data/valid.feature.txt', num_feat)
    # predict
    y_pred = clf.predict(x)

    # convert class id to class label
    y_pred = conv_class_id2label(y_pred, labels)
    y = conv_class_id2label(y, labels)

    # obtain confusion matrix
    # calculate performance
    print('----\nvalidation data\n----')
    print('macro metrics')
    print(json.dumps(classification_report(y, y_pred, output_dict=True), indent=2))
    calc_micro_metrics(y, y_pred, labels)
    
    '''
    test data
    '''
    # read data
    (x, y) = read_feature_label('data/test.feature.txt', num_feat)
    # predict
    y_pred = clf.predict(x)
    # convert class id to class label
    y_pred = conv_class_id2label(y_pred, labels)
    y = conv_class_id2label(y, labels)

    # calculate performance
    print('----\ntest data\n----')
    print('macro metrics')
    print(json.dumps(classification_report(y, y_pred, output_dict=True), indent=2))
    calc_micro_metrics(y, y_pred, labels)
    
    

if __name__=='__main__':
    main()

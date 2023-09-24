# -*- coding: utf-8 -*-

'''
54. 正解率の計測Permalink
52で学習したロジスティック回帰モデルの正解率を，学習データおよび評価データ上で計測せよ．
'''

import csv
import numpy as np
import pickle
from tabulate import tabulate
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from q51 import NLTKWrapper, create_features
    
def read_data(fn):
    '''
    Read data in CSV
    '''
    ret = []
    with open(fn, 'r') as fr:
        cr = csv.reader(fr, delimiter='\t')
        # format: category \t feature vector
        for e in cr:
            ret.append({
                'category': e[0],
                'feature': eval(e[1])
            })
    return ret

def get_num_dict_id(fn):
    with open(fn, 'r', encoding='utf-8') as fr:
        obj = eval(fr.read())
    return max(list(obj.values()))+1


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


def do_predict(sentences, nltk_wrapper, feat_dict, label_dict, clf):
    # convert sentence to features
    (feat, _) = create_features(sentences, nltk_wrapper=nltk_wrapper, feat_dict=feat_dict)
    num_dict_id = max(feat_dict.values())+1

    # convert features to a matrix
    x = np.zeros( (len(feat), num_dict_id) )
    for i in range(len(feat)):
        for (ek, ev) in feat[i].items():
            x[i][ek] = ev

    # predict probabilities of classes
    y = clf.predict_proba(x)

    
    # convert label-probabilities
    id2label = {}
    for (el, ei) in label_dict.items():
        assert(ei not in id2label)
        id2label[ei] = el
    ret = []
    for ey in y:
        tmp = []
        for i in range(len(ey)):
            tmp.append( (id2label[i], ey[i]) )
        tmp = sorted(tmp, key=lambda x: -x[1])
        ret.append(tmp)
    
    return ret
    


def main():

    # read dictionaries
    with open('data/feature_dictionary.txt', 'r', encoding='utf-8') as fr:
        feat_dict = eval(fr.read())
    num_feat = max(feat_dict.values())+1
    with open('data/label_dictionary.txt', 'r', encoding='utf-8') as fr:
        label_dict = eval(fr.read())

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

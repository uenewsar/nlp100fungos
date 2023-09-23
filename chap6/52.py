# -*- coding: utf-8 -*-

'''
52. 学習
51で構築した学習データを用いて，ロジスティック回帰モデルを学習せよ．
'''

import csv
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression

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
    

def main():

    # read training data
    train = read_data('train.feature.txt')
    # get num of feature from dictionary
    num_dict_id = get_num_dict_id('feature_dictionary.txt')

    # read training data and convert to numpy array
    (x, y) = read_feature_label('train.feature.txt', num_dict_id)

    # train classifier model
    print('training model ...')
    clf = LogisticRegression(random_state=42, solver='liblinear').fit(x, y)

    # save model
    fn = 'logistic_regression_model.pickle'
    print('saving model to {}'.format(fn))
    with open(fn, 'wb') as fr:
        pickle.dump(clf, fr)
        

if __name__=='__main__':
    main()

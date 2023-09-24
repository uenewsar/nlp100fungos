# -*- coding: utf-8 -*-

'''
57. 特徴量の重みの確認
52で学習したロジスティック回帰モデルの中で，重みの高い特徴量トップ10と，重みの低い特徴量トップ10を確認せよ．
'''

import numpy as np
import pickle
from tabulate import tabulate
from q55 import conv_dict_to_simple_list

    
def main():

    # load classification model
    fn = 'data/logistic_regression_model.pickle'
    print('loading model from {}'.format(fn))
    with open(fn, 'rb') as fr:
        clf = pickle.load(fr)

    # read feature dictionary as list
    feat_list = conv_dict_to_simple_list('data/feature_dictionary.txt')
    
    # get feature weight
    # NOTE: importance is indicated by absolute values of the weights
    weights = np.abs(clf.coef_[0])

    # construct feat vs. weight
    obj = []
    assert(len(feat_list)==len(weights))
    for (ef, ew) in zip(feat_list, weights):
        obj.append( (ef, ew) )

    # sort by weight's descending order
    obj = sorted(obj, key=lambda x: -x[1])

    # show top-10 and bottom-10
    print('top 10')
    print(tabulate(obj[:10], headers=['feature', 'weight']))
    print('bottom 10')
    print(tabulate(obj[-10:], headers=['feature', 'weight']))

    # show only 1-gram
    for i in range(len(obj)-1, -1, -1):
        ngram = eval(obj[i][0])
        assert(type(ngram) is list)
        if len(ngram)>1:
            del(obj[i])

    print('showing only 1-gram')
    print('top 10')
    print(tabulate(obj[:10], headers=['feature', 'weight']))
    print('bottom 10')
    print(tabulate(obj[-10:], headers=['feature', 'weight']))
    
        
if __name__=='__main__':
    main()

# -*- coding: utf-8 -*-

'''
58. 正則化パラメータの変更
ロジスティック回帰モデルを学習するとき，正則化パラメータを調整することで，学習時の過学習（overfitting）の度合いを制御できる．異なる正則化パラメータでロジスティック回帰モデルを学習し，学習データ，検証データ，および評価データ上の正解率を求めよ．実験の結果は，正則化パラメータを横軸，正解率を縦軸としたグラフにまとめよ．
'''

import csv
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.metrics  import accuracy_score
from tabulate import tabulate
from matplotlib import pyplot
    
from q52 import read_data, get_num_dict, read_feature_label


def evaluate(feat_label, clf, num_feat):
    # data
    (x, y) = feat_label
    # predict
    y_pred = clf.predict(x)
    # get accuracy
    return accuracy_score(y, y_pred)
    


def main():

    # get num of feature from dictionary
    num_feat = get_num_dict('data/feature_dictionary.txt')

    # read training/validation/test data and convert to numpy array
    train_feat_label = read_feature_label('data/train.feature.txt', num_feat)
    valid_feat_label = read_feature_label('data/valid.feature.txt', num_feat)
    test_feat_label = read_feature_label('data/test.feature.txt', num_feat)
    

    res = []
    for c in [1e-4, 2e-4, 5e-4, 1e-3, 2e-3, 5e-3, 1e-2, 2e-2, 5e-2, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50]:
        # strength of normalization
    
        '''
        train classifier model
        '''
        print('training model ...')
        # NOTE LogisticRegression argument must be inverse of strength of normalization
        clf = LogisticRegression(random_state=42, solver='liblinear', C=1/c).fit(train_feat_label[0], train_feat_label[1])

        '''
        evaluate
        '''
        print('evaluating ...')
        # training data
        acc_train = evaluate(train_feat_label, clf, num_feat)
        # validation data
        acc_valid = evaluate(valid_feat_label, clf, num_feat)
        # test data
        acc_test = evaluate(test_feat_label, clf, num_feat)

        print(c, acc_train, acc_valid, acc_test)
        res.append( (c, acc_train, acc_valid, acc_test) )
        

    # show accuracies in table
    print('accuracies')
    print(tabulate(res, headers=['c', 'train', 'valid', 'test']))

    # show accuracies in graph
    pyplot.plot([x[0] for x in res], [x[1] for x in res], label='train')
    pyplot.plot([x[0] for x in res], [x[2] for x in res], label='valid')
    pyplot.plot([x[0] for x in res], [x[3] for x in res], label='test')
    pyplot.xscale('log')
    pyplot.xlabel('C (Normalization Strength)')
    pyplot.ylabel('Accuracy')
    pyplot.legend()
    # save graph to a pdf file
    pyplot.savefig('data/graph_q58.pdf')
    #pyplot.show()

    
if __name__=='__main__':
    main()

# -*- coding: utf-8 -*-

'''
86. 単語ベクトルの表示
85で得た単語の意味ベクトルを読み込み，
"United States"のベクトルを表示せよ．ただし，
"United States"は内部的には"United_States"と表現されていることに注意せよ．
'''

import sys
import pickle

## main
w2v_fn = 'w2v.pickle'

# read word-vector data from outcome of 85
sys.stderr.write(' reading word-vector ...\n')
with open(w2v_fn, 'rb') as fr:
    word2vector = pickle.load(fr)
sys.stderr.write(' ok\n')

# get vector of "United States" = "United_States"
print('word vector of "United_States":')
print(word2vector['United_States'])

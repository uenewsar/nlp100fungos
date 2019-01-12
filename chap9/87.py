# -*- coding: utf-8 -*-

'''
87. 単語の類似度
85で得た単語の意味ベクトルを読み込み，"United States"と
"U.S."のコサイン類似度を計算せよ．ただし，"U.S."は内部的に
"U.S"と表現されていることに注意せよ．

'''

import pickle
import sys
import numpy as np

def cos_sim(v1, v2):
    if np.linalg.norm(v1)==0.0 or np.linalg.norm(v2)==0.0:
        return 0.0
    else:
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

## main
w2v_fn = 'w2v.pickle'

# read word-vector data from outcome of 85
sys.stderr.write(' reading word-vector ...\n')
with open(w2v_fn, 'rb') as fr:
    word2vector = pickle.load(fr)
sys.stderr.write(' ok\n')


print('cosine similarity between "United_States" and "U.S":')
print(cos_sim(word2vector['United_States'], word2vector['U.S']))

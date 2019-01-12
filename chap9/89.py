# -*- coding: utf-8 -*-

'''
89. 加法構成性によるアナロジー
85で得た単語の意味ベクトルを読み込み，
vec("Spain") - vec("Madrid") + vec("Athens")を計算し，
そのベクトルと類似度の高い10語とその類似度を出力せよ．
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

# get word similarities from "Spain"-"Madrid"+"Athens"
target = word2vector['Spain'] - word2vector['Madrid'] + word2vector['Athens']
similarity = {}
for e in word2vector.keys():
    similarity[e] = cos_sim(target, word2vector[e])

print('top 10 words having high similarity with "Spain"-"Madrid"+"Athens":')
cnt = 0
for word, sim in sorted(similarity.items(), key=lambda x: -x[1]):
    print(' {} : {}'.format(word, sim))
    cnt += 1
    if cnt==10:
        break

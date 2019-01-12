# -*- coding: utf-8 -*-

'''
85. 主成分分析による次元圧縮
84で得られた単語文脈行列に対して，主成分分析を適用し，
単語の意味ベクトルを300次元に圧縮せよ．

NOTE: if you use Python 3.6 or older, it fails to save word-vector file
because it exceeds 4-GB size and Python 3.6 or older has the problem to fail
saveing such a big file.
Please use Python 3.7 or later as this problem has been already fixed and
you can successfully save the word-vector file.
'''


import pickle
import sys
from scipy import sparse
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD
import numpy as np
import os

def get_word_vector(svd, word_idx, n_words):
    inp = sparse.lil_matrix( (1, n_words) )
    inp[0, word_idx] = 1.0
    ret = svd.transform(inp)[0]
    return ret

## main
np.random.seed(123)

ppmi_fn = 'ppmi.pickle'
w2v_fn = 'w2v.pickle'

# read outcome of 84
sys.stderr.write(' reading PPMI ...\n')
with open(ppmi_fn, 'rb') as fr:
    (word2idx, idx2word, Xtc) = pickle.load(fr)
sys.stderr.write(' ok\n')

sys.stderr.write(' doing PCA (SVD) ...\n')
# use SVD instead of PCA because sparse matrix cannot be applicable in PCA.
# SVD is also an alternative of PCA.
# this process takes several tens of minutes.
svd = TruncatedSVD(n_components=300)
svd.fit(Xtc)
sys.stderr.write(' ok ...\n')

sys.stderr.write(' making word-vector ...\n')

# make eye matrix to get each of word vector.
# NOTE: sparse matrix makes it very fast
n_words = len(word2idx)
inp = sparse.eye(n_words)
# get vectors
res = svd.transform(inp)

# convert it to word-vector dictionary
word2vector = {}
for i in range(n_words):
    if (i+1) % 100000 == 0:
        sys.stderr.write(' {}/{}\n'.format(i+1, n_words))
    word2vector[idx2word[i]] = res[i]
# write word-vector into a file
sys.stderr.write(' writing word-vector ...\n')
with open(w2v_fn, 'wb') as fw:
    pickle.dump( word2vector, fw )
sys.stderr.write(' ok\n')


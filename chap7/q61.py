# -*- coding: utf-8 -*-

'''
61. 単語の類似度
“United States”と”U.S.”のコサイン類似度を計算せよ．
'''

import gensim

from numpy import dot 
from numpy.linalg import norm 


def main():

    # Before executing this script,
    # 1. Download "GoogleNews-vectors-negative300.bin.gz".
    # 2. Unzip it with the command below.
    #  $ gzip -d GoogleNews-vectors-negative300.bin.gz

    # word word2vec model
    w2v = gensim.models.KeyedVectors.load_word2vec_format(
        'GoogleNews-vectors-negative300.bin',
        binary=True
    )

    # get vector of "United_States"
    vec_united_states = w2v['United_States']

    # get vector of "U.S."
    vec_us = w2v['U.S.']

    # calculate cosine similarity
    cos_sim = dot(vec_united_states, vec_us) / (norm(vec_united_states) * norm(vec_us))
    print(cos_sim) 

if __name__=='__main__':
    main()

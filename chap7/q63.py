# -*- coding: utf-8 -*-

'''
63. 加法構成性によるアナロジ
"Spain"の単語ベクトルから"Madrid"のベクトルを引き，"Athens"のベクトルを足したベクトルを計算し，そのベクトルと類似度の高い10語とその類似度を出力せよ．
'''

import gensim
from tqdm import tqdm
from numpy import dot 
from numpy.linalg import norm 


def calc_cos_sim(a, b):
    # calculate cosine similarity
    return dot(a, b) / (norm(a) * norm(b))
    

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
    
    # get vector of target
    target_vec = w2v["Spain"] - w2v["Madrid"] + w2v["Athens"]
    
    # calculate cosine similarities between "United_States" and all the phrases in the model
    cos_sim = {}
    for ep in tqdm(w2v.index_to_key):
        cos_sim[ep] = calc_cos_sim(target_vec, w2v[ep])

    # sort cosine similarity in descending order
    sorted_cos_sim = sorted(cos_sim.items(), key = lambda x: -x[1])
    # show top 10 similar phrases
    for i in range(10):
        print(sorted_cos_sim[i])


if __name__=='__main__':
    main()

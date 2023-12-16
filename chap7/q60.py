# -*- coding: utf-8 -*-

'''
第7章: 単語ベクトル
60. 単語ベクトルの読み込みと表示Permalink
Google Newsデータセット（約1,000億単語）での学習済み単語ベクトル（300万単語・フレーズ，300次元）をダウンロードし，"United States"の単語ベクトルを表示せよ．ただし，"United States"は内部的には"United_States"と表現されていることに注意せよ．
'''

import gensim

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
    # show vector of "United_States"
    print(w2v['United_States'])

if __name__=='__main__':
    main()

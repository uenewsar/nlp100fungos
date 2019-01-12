# -*- coding: utf-8 -*-

'''
83. 単語／文脈の頻度の計測
82の出力を利用し，以下の出現分布，および定数を求めよ．
 f(t,c): 単語tと文脈語cの共起回数
 f(t,∗): 単語tの出現回数
 f(∗,c): 文脈語cの出現回数
 N: 単語と文脈語のペアの総出現回数
'''

import pickle
import sys

def write_res(word2idx, idx2word, ftc, ft, fc, N, fn):
    with open(fn, 'wb') as fw:
        pickle.dump( (word2idx, idx2word, ftc, ft, fc, N), fw )


## main
# read outcome of 82
fr = open('context.txt', 'r', encoding='utf-8')

# initialize variables
# f(t,c)
ftc = {}
# f(t,*)
ft = {}
# f(*,c)
fc = {}
# N
N = 0

# word id - word
# word - word id
idx2word = {}
word2idx = {}

for line in fr:

    # there are some cases that line doesn't have two colums, so use strip (not rstrip)
    # to remove all unnecessary spaces
    line = line.strip()
    # split to words
    tab = line.split('\t')
    if len(tab) != 2:
        continue

    t = tab[0]
    c = tab[1]

    # register word id
    if t not in word2idx:
        word2idx[t] = len(word2idx)
        idx2word[ word2idx[t] ] = t
    if c not in word2idx:
        word2idx[c] = len(word2idx)
        idx2word[ word2idx[c] ] = c

    # convert to word id
    t = word2idx[t]
    c = word2idx[c]

    # count f(t,c)
    if t not in ftc:
        ftc[t] = {}
    if c not in ftc[t]:
        ftc[t][c] = 0
    ftc[t][c] += 1

    # count f(t,*)
    if t not in ft:
        ft[t] = 0
    ft[t] += 1

    # count f(*,c)
    if c not in fc:
        fc[c] = 0
    fc[c] += 1

    N += 1
    if N % 10000000 == 0:
        sys.stderr.write(' N={}\n'.format(N))
    #if N % 100000000 == 0:
    #    break
                             


fr.close()

# write final result
sys.stderr.write(' writing final result ...\n')
write_res(word2idx, idx2word, ftc, ft, fc, N, 'context_count.pickle')
sys.stderr.write(' end\n')

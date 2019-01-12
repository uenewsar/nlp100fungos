# -*- coding: utf-8 -*-

'''
84. 単語文脈行列の作成
83の出力を利用し，単語文脈行列Xを作成せよ．
ただし，行列Xの各要素Xtcは次のように定義する．
- f(t,c)>=10ならば，Xtc = PPMI(t,c) = max {log (N*f(t,c)/(f(t,*)*f(*,c))), 0}
- f(t,c)<10ならば，Xtc = 0
ここで，PPMI(t,c)はPositive Pointwise Mutual Information（正の相互情報量）と
呼ばれる統計量である．なお，行列Xの行数・列数は数百万オーダとなり，
行列のすべての要素を主記憶上に載せることは無理なので注意すること．
幸い，行列Xのほとんどの要素は0になるので，非0の要素だけを書き出せばよい．
'''

import pickle
import sys
from scipy import sparse
import numpy as np

## main
cc_fn = 'context_count.pickle'
ppmi_fn = 'ppmi.pickle'

# read outcome of 83
sys.stderr.write(' reading context count information ...\n')
with open(cc_fn, 'rb') as fr:
    (word2idx, idx2word, ftc, ft, fc, N) = pickle.load(fr)
sys.stderr.write(' ok\n')

# make sparse matrix
Xtc = sparse.lil_matrix( (len(word2idx), len(word2idx) ))

# search all the elements where f(t,c)>=10
cnt = 0
for t in ftc.keys():

    cnt += 1
    if cnt % 10000 == 0:
        sys.stderr.write(' t order = {}/{}\n'.format(cnt, len(ftc)))

    for c in ftc[t].keys():
        if ftc[t][c] < 10:
            # Xtc = 0
            continue

        # calc PPMI(t, c) = max{log (N*f(t,c)/(f(t,*)*f(*,c))), 0}
        if t not in ft:
            raise Exception('error t={} is not found in ft.'.format(t))
        if c not in fc:
            raise Exception('error c={} is not found in fc.'.format(c))

        tmp = float(N) * ftc[t][c] / ft[t] / fc[c]
        tmp = np.log(tmp)
        if tmp < 0.0:
            tmp = 0.0
        Xtc[t, c] = tmp

# write final result
sys.stderr.write(' writing final result ...\n')
with open(ppmi_fn, 'wb') as fw:
    pickle.dump( (word2idx, idx2word, Xtc), fw )
sys.stderr.write(' end\n')

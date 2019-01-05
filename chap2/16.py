# -*- coding: utf-8 -*-

'''
16. ファイルをN分割する
自然数Nをコマンドライン引数などの手段で受け取り，
入力のファイルを行単位でN分割せよ．同様の処理をsplitコマンドで実現せよ．

shell commands:
[I don't know how to do that with using "split" command.]
'''

import sys
n = int(sys.argv[1])
fr = open('hightemp.txt', 'r', encoding='utf-8')
buf = []
for e in fr:
    e = e.rstrip()
    buf.append(e)
fr.close()

outp = {}
for i in range(len(buf)):
    idx = int(float(i) / len(buf) * n)
    if idx not in outp:
        outp[idx] = []
    outp[idx].append(buf[i])

for idx in sorted(outp.keys()):
    with open('out16_{}.txt'.format(idx), 'w', encoding='utf-8') as fw:
        for e in outp[idx]:
            fw.write('{}\n'.format(e))

# -*- coding: utf-8 -*-

'''
15. 末尾のN行を出力
自然数Nをコマンドライン引数などの手段で受け取り，
入力のうち末尾のN行だけを表示せよ．確認にはtailコマンドを用いよ．

shell commands:
tail -n 10 hightemp.txt
'''

import sys
n = int(sys.argv[1])

fr = open('hightemp.txt', 'r', encoding='utf-8')
buf = []
for e in fr:
    e = e.rstrip()
    buf.append(e)
fr.close()

for i in range(-n,0):
    print(buf[i])


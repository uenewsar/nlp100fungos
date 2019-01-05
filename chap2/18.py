# -*- coding: utf-8 -*-

'''
18. 各行を3コラム目の数値の降順にソート
各行を3コラム目の数値の逆順で整列せよ
（注意: 各行の内容は変更せずに並び替えよ）．
確認にはsortコマンドを用いよ
（この問題はコマンドで実行した時の結果と合わなくてもよい）．

shell commands:
sort -k3,3gr -k2,2 hightemp.txt
'''

buf = []
fr = open('hightemp.txt', 'r', encoding='utf-8')
for e in fr:
    e = e.rstrip()
    words = e.split('\t')
    buf.append(words)
fr.close()

# In order to cope with the case where several lines
# have the same value in column no.2, I use column no.1
# as a second sorting key.
buf.sort(key=lambda x:(-float(x[2]), x[1]))

for e in buf:
    print('\t'.join(e))

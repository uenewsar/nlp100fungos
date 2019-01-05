# -*- coding: utf-8 -*-

'''
17. １列目の文字列の異なり
1列目の文字列の種類（異なる文字列の集合）を求めよ．
確認にはsort, uniqコマンドを用いよ．

cat hightemp.txt | cut -f 1 | sort | uniq | wc -l
'''


fr = open('hightemp.txt', 'r', encoding='utf-8')
buf = {}
for e in fr:
    e = e.rstrip()
    word = e.split('\t')[0]
    buf[word] = 1
fr.close()

print(len(buf))

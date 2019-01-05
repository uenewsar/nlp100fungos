# -*- coding: utf-8 -*-

'''
19. 各行の1コラム目の文字列の出現頻度を求め，出現頻度の高い順に並べる
各行の1列目の文字列の出現頻度を求め，その高い順に並べて表示せよ．
確認にはcut, uniq, sortコマンドを用いよ．

shell commands:
cat hightemp.txt | cut -f1 | sort | uniq -c | sort -k1,1gr -k2,2
'''

fr = open('hightemp.txt', 'r', encoding='utf-8')
buf = {}
for e in fr:
    e = e.rstrip()
    word = e.split('\t')[0]
    if word not in buf:
        buf[word] = 0
    buf[word] += 1
fr.close()

# In order to cope with the case where frequencies of several keys
# are same, I use column no.1 as the second sorting key.
for k, v in sorted(buf.items(), key=lambda x:(-x[1],x[0])):
    print('%4d %s' % (v, k))

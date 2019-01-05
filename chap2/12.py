# -*- coding: utf-8 -*-

'''
12. 1列目をcol1.txtに，2列目をcol2.txtに保存
各行の1列目だけを抜き出したものをcol1.txtに，
2列目だけを抜き出したものをcol2.txtとしてファイルに保存せよ．
確認にはcutコマンドを用いよ．

shell commands:
cut -f 1 < hightemp.txt > col1_sh.txt
cut -f 2 < hightemp.txt > col2_sh.txt
'''

import re

fr = open('hightemp.txt', 'r', encoding='utf-8')
fw1 = open('col1.txt', 'w', encoding='utf-8')
fw2 = open('col2.txt', 'w', encoding='utf-8')
for e in fr:
    e = e.rstrip()
    tab = e.split('\t')
    fw1.write('{}\n'.format(tab[0]))
    fw2.write('{}\n'.format(tab[1]))
fr.close()
fw1.close()
fw2.close()

# -*- coding: utf-8 -*-

'''
13. col1.txtとcol2.txtをマージ
12で作ったcol1.txtとcol2.txtを結合し，
元のファイルの1列目と2列目をタブ区切りで並べたテキストファイルを作成せよ．
確認にはpasteコマンドを用いよ．

shell commands:
cut -f 1 < hightemp.txt > col1_sh.txt
cut -f 2 < hightemp.txt > col2_sh.txt
paste col1_sh.txt col2_sh.txt > col3_sh.txt
'''

import re

# same as no.12 (start)
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
# same as no.12 (end)

col1 = []
fr = open('col1.txt', 'r', encoding='utf-8')
for e in fr:
    col1.append(e.rstrip())

col2 = []
fr = open('col2.txt', 'r', encoding='utf-8')
for e in fr:
    col2.append(e.rstrip())

fw = open('col3.txt', 'w', encoding='utf-8')
for i in range(len(col1)):
    fw.write('{}\t{}\n'.format(col1[i], col2[i]))
fw.close()

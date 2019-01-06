# -*- coding: utf-8 -*-

'''
70. データの入手・整形
文に関する極性分析の正解データを用い，以下の要領で正解データ
（sentiment.txt）を作成せよ．
1. rt-polarity.posの各行の先頭に"+1 "という文字列を追加する
  （極性ラベル"+1"とスペースに続けて肯定的な文の内容が続く）
2. rt-polarity.negの各行の先頭に"-1 "という文字列を追加する
  （極性ラベル"-1"とスペースに続けて否定的な文の内容が続く）
3. 上述1と2の内容を結合（concatenate）し，行をランダムに並び替える
sentiment.txtを作成したら，正例（肯定的な文）の数と負例（否定的な文）の数を確認せよ．

shell commands:
$ python3 70.py
$ grep -E '^\+1' sentiment.txt | wc -l
5331
$ grep -E '^\-1' sentiment.txt | wc -l
5331
'''

import random

def read_data(fn, label):
    # the encoding of these data are 'latin-1'
    fr = open(fn, 'r', encoding='latin-1')
    buf = []
    for e in fr:
        e = e.rstrip()
        buf.append('{} {}'.format(label, e))
    fr.close()
    return buf

## main
# fix seed of random
random.seed(12345)

buf = read_data('rt-polaritydata/rt-polarity.pos', '+1')
buf += read_data('rt-polaritydata/rt-polarity.neg', '-1')
random.shuffle(buf)

fw = open('sentiment.txt', 'w', encoding='utf-8')
for e in buf:
    fw.write('{}\n'.format(e))
fw.close()

# -*- coding: utf-8 -*-

# 37. 頻度上位10語
# 出現頻度が高い10語とその出現頻度をグラフ（例えば棒グラフなど）で表示せよ．

def read_text():

    buf = []
    fr = open('neko.txt.mecab', 'r', encoding='utf-8')
    sentence = []
    for e in fr:
        # e.g.
        # 生れ  \t 動詞,自立,*,*,一段,連用形,生れる,ウマレ,ウマレ
        # 表層形\t 品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音
        e = e.rstrip()
        if e=='EOS':
            # end of one sentence
            if len(sentence)>0:
                buf.append(sentence)
                sentence = []
            continue

        word = {}

        tmp = e.split('\t')
        word['surface'] = tmp[0]

        tmp = tmp[1].split(',')
        word['base'] = tmp[6]
        word['pos'] = tmp[0]
        word['pos1'] = tmp[1]

        sentence.append(word)

    fr.close()

    return buf


# main
buf = read_text()
word2freq = {}
for es in buf:
    for ew in es:
        if ew['surface'] not in word2freq:
            word2freq[ew['surface']] = 0
        word2freq[ew['surface']] += 1

top10 = sorted(word2freq.items(), key=lambda x: -x[1])[:10]
for (k, v) in top10:
    print('{} {}'.format(k, v))


# to show Japanese characters in matplotlib,
# it is necesary to specify Japanse-applicable fonts in your system.
# see https://openbook4.me/sections/1674
import matplotlib
matplotlib.rcParams['font.family'] = 'AppleGothic'

import matplotlib.pyplot as plt

plt.bar([e[0] for e in top10], [e[1] for e in top10])
plt.show()

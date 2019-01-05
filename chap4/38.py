# -*- coding: utf-8 -*-

# 38. ヒストグラム
# 単語の出現頻度のヒストグラム（横軸に出現頻度，
# 縦軸に出現頻度をとる単語の種類数を棒グラフで表したもの）を描け．

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

# make histogram
hist = {}
for ew in word2freq.keys():
    val = word2freq[ew]
    if val not in hist:
        hist[val] = 0
    hist[val] += 1


import matplotlib.pyplot as plt
plt.bar([x for x in sorted(hist.keys())], [hist[x] for x in sorted(hist.keys())])
plt.xscale("log")
plt.yscale("log")
plt.show()

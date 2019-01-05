# -*- coding: utf-8 -*-

# 39. Zipfの法則
# 単語の出現頻度順位を横軸，その出現頻度を縦軸として，両対数グラフをプロットせよ．

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

# sort words by descending order of word frequency
srt_w2f = sorted(word2freq.items(), key=lambda x: -x[1])

import matplotlib.pyplot as plt

plt.scatter(range(1, len(srt_w2f)+1), [y[1] for y in srt_w2f])
plt.xscale("log")
plt.yscale("log")
plt.show()

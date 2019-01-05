# -*- coding: utf-8 -*-

# 32. 動詞の原形
# 動詞の原形をすべて抽出せよ．

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
dup = {}
num = 1
for es in buf:
    for ew in es:
        if ew['pos']=='動詞':
            if ew['base'] not in dup:
                dup[ew['base']] = 1
                print('{} {}'.format(num, ew['base']))
                num += 1
 



# -*- coding: utf-8 -*-

# 35. 名詞の連接
# 名詞の連接（連続して出現する名詞）を最長一致で抽出せよ．

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
    tmp = []
    for i in range(len(es)):
        if es[i]['pos']=='名詞':
            # store noun to buffer
            tmp.append(es[i]['surface'])

        if es[i]['pos']!='名詞' or i==len(es)-1:
            # end of nouns, or end of sentence
            if len(tmp) > 1:
                # buffer has two or more nouns in a row
                meishi = ' '.join(tmp)
                if meishi not in dup:
                    dup[meishi] = 1
                    print('{} {}'.format(num, meishi))
                    num += 1
            tmp = []


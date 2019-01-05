# -*- coding: utf-8 -*-

# 34. 「AのB」
# 2つの名詞が「の」で連結されている名詞句を抽出せよ．

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
    for i in range(len(es)-2):
        if es[i]['pos']!='名詞':
            continue
        if es[i+1]['surface']!='の' or es[i+1]['pos']!='助詞':
            continue
        if es[i+2]['pos']!='名詞':
            continue

        meishiku = es[i]['surface'] + es[i+1]['surface'] + es[i+2]['surface']
        if meishiku not in dup:
            dup[meishiku] = 1
            print('{} {}'.format(num, meishiku))
            num += 1





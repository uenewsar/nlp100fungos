# -*- coding: utf-8 -*-

'''
40. 係り受け解析結果の読み込み（形態素）
形態素を表すクラスMorphを実装せよ．
このクラスは表層形（surface），基本形（base），
品詞（pos），品詞細分類1（pos1）をメンバ変数に
持つこととする．さらに，CaboChaの解析結果
（neko.txt.cabocha）を読み込み，各文をMorph
オブジェクトのリストとして表現し，3文目の形態素列を表示せよ．
'''

import re

class Morph(object):

    def __init__(self):
        self.surface = None
        self.base = None
        self.pos = None
        self.pos1 = None

    def echo(self):
        ret = 'surface={} base={} pos={} pos1={}'.format(
            self.surface, self.base, self.pos, self.pos1
            )
        return ret

def read_parsed():

    '''
    * 0 2D 0/0 -0.764522
    　	記号,空白,*,*,*,*,　,　,　
    * 1 2D 0/1 -0.764522
    吾輩	名詞,代名詞,一般,*,*,*,吾輩,ワガハイ,ワガハイ
    は	助詞,係助詞,*,*,*,*,は,ハ,ワ
    * 2 -1D 0/2 0.000000
    猫	名詞,一般,*,*,*,*,猫,ネコ,ネコ
    で	助動詞,*,*,*,特殊・ダ,連用形,だ,デ,デ
    ある	助動詞,*,*,*,五段・ラ行アル,基本形,ある,アル,アル
    。	記号,句点,*,*,*,*,。,。,。
    EOS
    '''

    buf = []
    fr = open('neko.txt.cabocha', 'r', encoding='utf-8')
    sentence = []
    for e in fr:
        e = e.rstrip()
        if e=='EOS':
            # end of one sentence
            if len(sentence)>0:
                buf.append(sentence)
                sentence = []
            continue

        if re.search(r'^\*', e):
            continue

        morph = Morph()

        tmp = e.split('\t')
        morph.surface = tmp[0]

        tmp = tmp[1].split(',')
        morph.base = tmp[6]
        morph.pos = tmp[0]
        morph.pos1 = tmp[1]

        sentence.append(morph)

    fr.close()

    return buf


# main
buf = read_parsed()
for e in buf[2]:
    print(e.echo())

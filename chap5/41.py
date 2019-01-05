# -*- coding: utf-8 -*-

'''
41. 係り受け解析結果の読み込み（文節・係り受け）

40に加えて，文節を表すクラスChunkを実装せよ．
このクラスは形態素（Morphオブジェクト）のリスト（morphs），
係り先文節インデックス番号（dst），係り元文節インデックス
番号のリスト（srcs）をメンバ変数に持つこととする．さらに，
入力テキストのCaboChaの解析結果を読み込み，１文をChunk
オブジェクトのリストとして表現し，8文目の文節の文字列と
係り先を表示せよ．第5章の残りの問題では，ここで作った
プログラムを活用せよ．
'''

import re

class Chunk(object):

    def __init__(self):
        self.morphs = None
        self.dst = None
        self.srcs = None

    def echo(self):
        ret = 'dst={} srcs={} [{}]'.format(self.dst, self.srcs, [e.echo() for e in self.morphs])
        return ret


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
    chunk = None

    for e in fr:
        e = e.rstrip()
        if e=='EOS':
            # end of previous chunk (maybe)
            if chunk is not None:
                sentence.append(chunk)
                chunk = None

            # end of one sentence
            if len(sentence)>0:

                # make srcs
                for i in range(len(sentence)):
                    for j in range(len(sentence)):
                        if i==j:
                            continue
                        if sentence[j].dst == i:
                            # if chunk i is source of chunk j
                            if sentence[i].srcs is None:
                                sentence[i].srcs = []
                            sentence[i].srcs.append(j)
 
                buf.append(sentence)
                sentence = []

            continue

        if re.search(r'^\*', e):
            # end of previous chunk
            if chunk is not None:
                sentence.append(chunk)

            # start of a chank
            # make new chunk
            chunk = Chunk()
            # register destination id
            tmp = e.split(' ')[2]
            tmp = re.sub(r'D', '', tmp)
            if int(tmp) != -1:
                chunk.dst = int(tmp)
            # init morphs
            chunk.morphs = []
            continue

        # morph
        e_morph = Morph()
        tmp = e.split('\t')
        e_morph.surface = tmp[0]

        tmp = tmp[1].split(',')
        e_morph.base = tmp[6]
        e_morph.pos = tmp[0]
        e_morph.pos1 = tmp[1]

        chunk.morphs.append(e_morph)

    fr.close()

    return buf


# main
buf = read_parsed()
for i in range(len(buf[7])):
    print('{} {}'.format(i, buf[7][i].echo()))

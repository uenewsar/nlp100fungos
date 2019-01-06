# -*- coding: utf-8 -*-

'''
48. 名詞から根へのパスの抽出

文中のすべての名詞を含む文節に対し，その文節から構文木の
根に至るパスを抽出せよ．ただし，構文木上のパスは以下の
仕様を満たすものとする．
- 各文節は（表層形の）形態素列で表現する
- パスの開始文節から終了文節に至るまで，各文節の表現を
  "->"で連結する

「吾輩はここで始めて人間というものを見た」という文
（neko.txt.cabochaの8文目）から，次のような出力が得られる
はずである．

  吾輩は -> 見た
  ここで -> 始めて -> 人間という -> ものを -> 見た
  人間という -> ものを -> 見た
  ものを -> 見た
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

def delete_symbols(inp):
    ret = re.sub(r'[　。、]', '', inp)
    return ret
    

## main
buf = read_parsed()

for es in buf:
    # es ... a sentence
    for i in range(len(es)):
        # es[i] ... a chunk

        # if chunk has no destination, skip
        if es[i].dst is None:
            continue

        # if chunk does not have noun, skip
        flag = False
        for em in es[i].morphs:
            if em.pos=='名詞':
                flag = True
                break
        if flag is False:
            continue
        
        # track chain
        chain = []
        idx = i
        while True:
            # get surface
            surface = ''.join([x.surface for x in es[idx].morphs])
            chain.append(surface)
            
            # if this is terminal, end.
            if es[idx].dst is None:
                break
            # update chunk id
            idx = es[idx].dst

        # delete symbols
        chain = [delete_symbols(e) for e in chain]
        # if one or more surface is "", skip
        flag = False
        for e in chain:
            if e=='':
                flag = True
                break
        if flag:
            continue

        # output
        print(' -> '.join(chain))

    # add a blank line between two sentences
    print()

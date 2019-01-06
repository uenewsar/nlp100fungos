# -*- coding: utf-8 -*-

'''
45. 動詞の格パターンの抽出

今回用いている文章をコーパスと見なし，日本語の述語が取りうる格を
調査したい．動詞を述語，動詞に係っている文節の助詞を格と考え，
述語と格をタブ区切り形式で出力せよ． ただし，出力は以下の仕様を
満たすようにせよ．
- 動詞を含む文節において，最左の動詞の基本形を述語とする
- 述語に係る助詞を格とする
- 述語に係る助詞（文節）が複数あるときは，すべての助詞を
  スペース区切りで辞書順に並べる

「吾輩はここで始めて人間というものを見た」という例文
（neko.txt.cabochaの8文目）を考える．この文は「始める」と「見る」
の２つの動詞を含み，「始める」に係る文節は「ここで」，「見る」に
係る文節は「吾輩は」と「ものを」と解析された場合は，次のような
出力になるはずである．
  始める  で
  見る    は を

このプログラムの出力をファイルに保存し，以下の事項をUNIXコマンドを用いて確認せよ．
- コーパス中で頻出する述語と格パターンの組み合わせ
- 「する」「見る」「与える」という動詞の格パターン
  （コーパス中で出現頻度の高い順に並べよ）

shell commands:
python3 45.py > foo.txt


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

        # search chunk which have src
        if es[i].srcs is None or len(es[i].srcs)==0:
            continue
        
        # search most-left verb, and extract its base
        base = None
        for ew in es[i].morphs:
            if ew.pos == '動詞':
                base = ew.base
                break
        if base is None:
            continue

        # extract particles in src
        particles = []
        for esrc in es[i].srcs:
           for ew in es[esrc].morphs:
               if ew.pos == '助詞':
                   particles.append(ew.surface)

        if len(particles)==0:
            continue

        # output
        print('{}\t{}'.format(base, ' '.join(particles)))

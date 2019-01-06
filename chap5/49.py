# -*- coding: utf-8 -*-

'''
49. 名詞間の係り受けパスの抽出

文中のすべての名詞句のペアを結ぶ最短係り受けパスを抽出せよ．
ただし，名詞句ペアの文節番号がiとj（i<j）のとき，
係り受けパスは以下の仕様を満たすものとする．

- 問題48と同様に，パスは開始文節から終了文節に至るまでの
  各文節の表現（表層形の形態素列）を"->"で連結して表現する
- 文節iとjに含まれる名詞句はそれぞれ，XとYに置換する

また，係り受けパスの形状は，以下の2通りが考えられる．

- 文節iから構文木の根に至る経路上に文節jが存在する場合:
  文節iから文節jのパスを表示
- 上記以外で，文節iと文節jから構文木の根に至る経路上で共通
  の文節kで交わる場合: 文節iから文節kに至る直前のパスと文節j
  から文節kに至る直前までのパス，文節kの内容を"|"で連結して表示

例えば，「吾輩はここで始めて人間というものを見た。」という文
（neko.txt.cabochaの8文目）から，次のような出力が得られるはずである．
  Xは | Yで -> 始めて -> 人間という -> ものを | 見た
  Xは | Yという -> ものを | 見た
  Xは | Yを | 見た
  Xで -> 始めて -> Y
  Xで -> 始めて -> 人間という -> Y
  Xという -> Y
'''

import sys
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
    
def pos_has(chunk, pos):
    for e in chunk.morphs:
        if e.pos==pos:
            return True
    return False


def cat_surface(morphs, convert_noun=None, delete_words_after_noun=False):

    if convert_noun is not None:
        # convert last noun to specified character
        tmp = []
        idx = len(morphs)-1
        while idx>=0:
            if morphs[idx].pos=='名詞':
                # add specified character as noun's surface
                tmp.append(convert_noun)
                break
            else:
                if delete_words_after_noun is False:
                    # doesn't include any words after nouns
                    tmp.append(morphs[idx].surface)
                idx -= 1

        if len(tmp)==0:
            # for just in case
            raise Exception('unexpected error.')

        return ''.join(reversed(tmp))

    elif delete_words_after_noun:
        # delete any words after last noun
        # search idx of last noun
        last_noun_idx = None
        for i in range(len(morphs)-1, -1, -1):
            if morphs[i].pos=='名詞':
                last_noun_idx = i
                break

        if last_noun_idx is not None:
            # cat surface from 0 to (last_noun_idx)
            return ''.join([morphs[i].surface for i in range(last_noun_idx+1)])
        else:
            # no nouns, so the same process as normal
            return ''.join([e.surface for e in morphs])

    else:
        # normal
        return ''.join([e.surface for e in morphs])



def make_str_for_direct_path(chunks, chk_str):

    buf = []
    for i in range(len(chk_str)):
        chk_idx = chk_str[i]
        if i==0:
            # first chunk -> convert noun to "X"
            buf.append(cat_surface(chunks[chk_idx].morphs, convert_noun='X'))
        elif i==len(chk_str)-1:
            # last chunk -> convert noun to "Y", and get rid of all words after "Y"
            buf.append(cat_surface(chunks[chk_idx].morphs, convert_noun='Y', delete_words_after_noun=True))
        else:
            # normal
            buf.append(cat_surface(chunks[chk_idx].morphs))

    return ' -> '.join(buf)
            

def get_path_to_root(chunks, idx):

    ret = {}
    i = idx

    while True:
        if chunks[i].dst is None:
            break
        i = chunks[i].dst
        ret[i] = 1
    
    # for just in case
    if len(ret)==0:
        raise Exception('unexpected error')

    return ret



def get_chk_meet(chunks, idx_x, idx_y):

    # search the chunk where x and y eventually meets each other
    
    # enumerate all the chunks after x or y
    aft_x = get_path_to_root(chunks, idx_x)
    aft_y = get_path_to_root(chunks, idx_y)

    # extract AND
    idx_and = {}
    for e in aft_x.keys():
        if e in aft_y:
            idx_and[e] = 1

    if len(idx_and)==0:
        raise Exception('unexpected error')

    # get minimum idx from AND, and it is the chunk number where x and y firstly meet.
    return min(idx_and.keys())
    
 
def make_path_to_one_step_before_of_goal(chunks, idx_start, idx_goal):

    ret = []
    i = idx_start
    while i != idx_goal:
        ret.append(i)
        i = chunks[i].dst
    return ret

def make_str_for_indirect_connection(chunks, idx_x, idx_y, idx_meet):

    # make list from idx_x to one step before of idx_meet
    chk_x = make_path_to_one_step_before_of_goal(chunks, idx_x, idx_meet)
    chk_y = make_path_to_one_step_before_of_goal(chunks, idx_y, idx_meet)

    # make string
    surface_x = []
    for i in range(len(chk_x)):
        if i==0:
            surface_x.append(cat_surface(chunks[chk_x[i]].morphs, convert_noun='X'))
        else:
            surface_x.append(cat_surface(chunks[chk_x[i]].morphs))

    surface_y = []
    for i in range(len(chk_y)):
        if i==0:
            surface_y.append(cat_surface(chunks[chk_y[i]].morphs, convert_noun='Y'))
        else:
            surface_y.append(cat_surface(chunks[chk_y[i]].morphs))

    surface_meet = cat_surface(chunks[idx_meet].morphs)

    return '{} | {} | {}'.format(' -> '.join(surface_x), ' -> '.join(surface_y), surface_meet)





def process_for_a_chunk_pair(chunks, idx_x, idx_y):

    # search direct path from x to y, and make chunk string
    chk_str = []
    i = idx_x
    flag = False
    while True:
        chk_str.append(i)
        if i==idx_y:
            # found direct path
            flag = True
            break           
        if chunks[i].dst is None:
            # not found
            break
        i = chunks[i].dst

    if flag:
        # direct path was found, so make string for it
        ret = make_str_for_direct_path(chunks, chk_str)
        return ret

    # in the case of indirect connection between x, y

    # search the chunk where x and y eventually meets each other
    idx_meet = get_chk_meet(chunks, idx_x, idx_y)
    # do process for case of indirect connection
    ret = make_str_for_indirect_connection(chunks, idx_x, idx_y, idx_meet)
    return ret


def process_for_one_sentence(chunks):

    # enumerate all chunks having noun
    chk_noun = []
    for i in range(len(chunks)):
        if pos_has(chunks[i], '名詞'):
            chk_noun.append(i)

    # test all "noun phrase" pairs
    for idx_x in range(len(chk_noun)-1):
        for idx_y in range(idx_x+1, len(chk_noun)):
            ret = process_for_a_chunk_pair(chunks, chk_noun[idx_x], chk_noun[idx_y])

            ret = delete_symbols(ret)
            print(ret)

## main
buf = read_parsed()
for es in buf:
    # es ... a sentence
    process_for_one_sentence(es)

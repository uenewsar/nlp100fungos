# -*- coding: utf-8 -*-

'''
47. 機能動詞構文のマイニング

動詞のヲ格にサ変接続名詞が入っている場合のみに着目したい．
46のプログラムを以下の仕様を満たすように改変せよ．
- 「サ変接続名詞+を（助詞）」で構成される文節が動詞に係る場合
  のみを対象とする
- 述語は「サ変接続名詞+を+動詞の基本形」とし，文節中に複数の
  動詞があるときは，最左の動詞を用いる
- 述語に係る助詞（文節）が複数あるときは，すべての助詞を
  スペース区切りで辞書順に並べる
- 述語に係る文節が複数ある場合は，すべての項をスペース区切り
  で並べる（助詞の並び順と揃えよ）

例えば「別段くるにも及ばんさと、主人は手紙に返事をする。」という
文から，以下の出力が得られるはずである．
  返事をする      と に は        及ばんさと 手紙に 主人は

このプログラムの出力をファイルに保存し，以下の事項をUNIXコマンドを用いて確認せよ．
- コーパス中で頻出する述語（サ変接続名詞+を+動詞）
- コーパス中で頻出する述語と助詞パターン


shell commands:
python3 47.py > foo.txt 
cut -f1 foo.txt | sort | uniq -c | sort -nr | head -n 10
cut -f1,2 foo.txt | sort | uniq -c | sort -nr | head -n 10
'''

import re
from operator import itemgetter

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
        verb_base = None
        for ew in es[i].morphs:
            if ew.pos == '動詞':
                verb_base = ew.base
                break
        if verb_base is None:
            continue

        particles = []
        chunks_with_particles = []
        pre_verb = []

        # extract particles in src, and corresponding chunks
        for esrc in es[i].srcs:

            # check サ変接続名詞+を
            flag = False
            for j in range(len(es[esrc].morphs)):
                if flag is False and j>0 and es[esrc].morphs[j-1].pos=='名詞' and es[esrc].morphs[j-1].pos1=='サ変接続' and es[esrc].morphs[j].pos=='助詞' and es[esrc].morphs[j].surface=='を':
                    # add as pre-verb
                    pre_verb.append(es[esrc].morphs[j-1].surface + es[esrc].morphs[j].surface)
                    # this chunk must be no longer investigated
                    flag = True
                    break
            
            if flag is True:
                continue

            # check 助詞 from last morph to top morph in each chunk
            for j in range(len(es[esrc].morphs)-1, -1, -1):
                if es[esrc].morphs[j].pos == '助詞':
                    particles.append(es[esrc].morphs[j].surface)
                    tmp = ''.join([x.surface for x in es[esrc].morphs])
                    tmp = delete_symbols(tmp)
                    chunks_with_particles.append(tmp)
                    break


        if len(pre_verb)==0:
            # there is no サ変接続名詞+を, so skip
            continue

        if len(particles)==0:
            # there is no chunks relating to サ変接続名詞+を+動詞 chunk, so skip
            continue

        # sort by "dictionary order" of particles
        '''
        # for debug
        sys.stderr.write('verb_base:{}\n'.format(verb_base))
        sys.stderr.write('pre_verb:{}\n'.format(pre_verb))
        sys.stderr.write('chunks_with_particles:{}\n'.format(chunks_with_particles))
        '''
        tmp = zip(particles, chunks_with_particles)
        tmp = sorted(tmp, key=itemgetter(0))
        (particles, chunks_with_particles) = zip(*tmp)

        # output
        for ep in pre_verb:
            print('{}{}\t{}\t{}'.format(ep, verb_base, ' '.join(particles), ' '.join(chunks_with_particles)))

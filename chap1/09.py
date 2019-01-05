# -*- coding: utf-8 -*-

# 09. Typoglycemia
# スペースで区切られた単語列に対して，各単語の先頭と末尾の文字は残し，
# それ以外の文字の順序をランダムに並び替えるプログラムを作成せよ．
# ただし，長さが４以下の単語は並び替えないこととする．
# 適当な英語の文（例えば"I couldn't believe that I
#  could actually understand what I was reading : 
#  the phenomenal power of the human mind ."）
# を与え，その実行結果を確認せよ．

import random

def proc(inp):

    if len(inp)<=4:
        return inp

    bos = inp[0]
    eos = inp[-1]

    middle = inp[1:-1]
    middle = list(middle)
    random.shuffle(middle)

    return '{}{}{}'.format(bos, ''.join(middle), eos)

str = "I couldn't believe that I could actually understand what I was reading : the phenomenal power of the human mind ."

words = str.split(' ')
for i in range(len(words)):
    words[i] = proc(words[i])

print(' '.join(words))

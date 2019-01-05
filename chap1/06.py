# -*- coding: utf-8 -*-

# 06. 集合
# "paraparaparadise"と"paragraph"に含まれる文字bi-gramの集合を，
# それぞれ, XとYとして求め，XとYの和集合，積集合，差集合を求めよ．
# さらに，'se'というbi-gramがXおよびYに含まれるかどうかを調べよ．


def make_n_gram(seq, n):

    n_gram = []

    for i in range(len(seq)-n+1):
        buf = []
        for j in range(n):
            buf.append(seq[i+j])
        n_gram.append('/'.join(buf))

    return n_gram

stc_x = "paraparaparadise"
stc_y = "paragraph"

ngram_x = set(make_n_gram(list(stc_x), 2))
print('ngram_x: {}'.format(ngram_x))
ngram_y = set(make_n_gram(list(stc_y), 2))
print('ngram_y: {}'.format(ngram_y))

# union: x+y
union = set(list(ngram_x) + list(ngram_y))
print('union: {}'.format(union))

# intesection: x*y
intersection = []
for e in ngram_x:
    if e in ngram_y:
        intersection.append(e)
print('intesection: {}'.format(intersection))

# difference: x-y
diff_xmy = []
for e in ngram_x:
    if e not in ngram_y:
        diff_xmy.append(e)
print('difference x-y: {}'.format(diff_xmy))

# difference: y-x
diff_ymx = []
for e in ngram_y:
    if e not in ngram_x:
        diff_ymx.append(e)
print('difference y-x: {}'.format(diff_ymx))

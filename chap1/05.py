# -*- coding: utf-8 -*-

# 05. n-gram
# 与えられたシーケンス（文字列やリストなど）からn-gramを作る関数を作成せよ．この関数を用い，"I am an NLPer"という文から単語bi-gram，文字bi-gramを得よ．

def make_n_gram(seq, n):

    n_gram = []

    for i in range(len(seq)-n+1):
        buf = []
        for j in range(n):
            buf.append(seq[i+j])
        n_gram.append('/'.join(buf))

    return n_gram

stc = "I am an NLPer"

words = stc.split(' ')

word_2_gram = make_n_gram(words, 2)
print("word 2-gram: {}".format(word_2_gram))

word_1_gram = make_n_gram(words, 1)
print("word 1-gram: {}".format(word_1_gram))

char = list(stc)

char_2_gram = make_n_gram(char, 2)
print("char 2-gram: {}".format(char_2_gram))

char_1_gram = make_n_gram(char, 1)
print("char 1-gram: {}".format(char_1_gram))

# -*- coding: utf-8 -*-

'''
71. ストップワード
英語のストップワードのリスト（ストップリスト）を
適当に作成せよ．さらに，引数に与えられた単語
（文字列）がストップリストに含まれている場合は真，
それ以外は偽を返す関数を実装せよ．
さらに，その関数に対するテストを記述せよ．
'''

import random

# from https://gist.github.com/sebleier/554280
stop_words = {
    "i", "me", "my", "myself", "we", "our",
    "ours", "ourselves", "you", "your", "yours",
    "yourself", "yourselves", "he", "him", "his", "himself",
    "she", "her", "hers", "herself", "it", "its",
    "itself", "they", "them", "their", "theirs", "themselves",
    "what", "which", "who", "whom", "this", "that",
    "these", "those", "am", "is", "are", "was",
    "were", "be", "been", "being", "have", "has",
    "had", "having", "do", "does", "did", "doing",
    "a", "an", "the", "and", "but", "if",
    "or", "because", "as", "until", "while", "of",
    "at", "by", "for", "with", "about", "against",
    "between", "into", "through", "during", "before", "after",
    "above", "below", "to", "from", "up", "down",
    "in", "out", "on", "off", "over", "under",
    "again", "further", "then", "once", "here", "there",
    "when", "where", "why", "how", "all", "any",
    "both", "each", "few", "more", "most", "other",
    "some", "such", "no", "nor", "not", "only",
    "own", "same", "so", "than", "too", "very",
    "s", "t", "can", "will", "just", "don", "should",
    "now"}

def is_stop_word(inp):
    if inp in stop_words:
        return True
    else:
        return False

def test():

    def _test(inp):
        return '{} -> {}'.format(inp, is_stop_word(inp))
    
    print(_test('hello'))
    print(_test('having'))
    print(_test('another'))
    print(_test('other'))

test()

# -*- coding: utf-8 -*-

# 04. 元素記号
# "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."という文を単語に分解し，1, 5, 6, 7, 8, 9, 15, 16, 19番目の単語は先頭の1文字，それ以外の単語は先頭に2文字を取り出し，取り出した文字列から単語の位置（先頭から何番目の単語か）への連想配列（辞書型もしくはマップ型）を作成せよ．

stc = "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."
idx = [1, 5, 6, 7, 8, 9, 15, 16, 19]

word2idx = {}

words = stc.split(' ')
for i in range(len(words)):

    if i+1 in idx:
        extracted = words[i][:1]
    else:
        extracted = words[i][:2]

    word2idx[extracted] = i+1

for k,v in word2idx.items():
    print('{} {}'.format(k, v))

                 

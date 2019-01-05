# -*- coding: utf-8 -*-

'''
11. タブをスペースに置換
タブ1文字につきスペース1文字に置換せよ．
確認にはsedコマンド，trコマンド，もしくはexpandコマンドを用いよ．

shell commands:
tr '\t' ' ' < hightemp.txt 
'''

import re
with open('hightemp.txt', 'r', encoding='utf-8') as fr:
    for e in fr:
        e = e.rstrip()
        e = re.sub(r'\t', ' ', e)
        print(e)

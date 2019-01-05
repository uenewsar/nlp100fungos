# -*- coding: utf-8 -*-

'''
10. 行数のカウント
行数をカウントせよ．確認にはwcコマンドを用いよ．

shell commands
wc hightemp.txt
'''

with open('hightemp.txt', 'r', encoding='utf-8') as fr:
    i = 0
    for e in fr:
        i += 1
print(i)

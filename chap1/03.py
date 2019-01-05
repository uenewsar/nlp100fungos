# -*- coding: utf-8 -*-

# 03. 円周率
# "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."という文を単語に分解し，各単語の（アルファベットの）文字数を先頭から出現順に並べたリストを作成せよ．

import re

a = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."
a = re.sub(r'[^0-9a-zA-Z ]+', '', a)
b = a.split(' ')
c = [len(e) for e in b]
print(c)
for i in range(len(b)):
    print('{} {}'.format(c[i], b[i]))


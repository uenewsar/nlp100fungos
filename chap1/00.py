# -*- coding: utf-8 -*-

# 00. 文字列の逆順
# 文字列"stressed"の文字を逆に（末尾から先頭に向かって）並べた文字列を得よ．

a = "stressed"
b = [a[i] for i in range(len(a)-1, -1, -1)] 
b = ''.join(b)
print(b)

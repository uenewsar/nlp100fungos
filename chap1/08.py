# -*- coding: utf-8 -*-

# 08. 暗号文
# 与えられた文字列の各文字を，以下の仕様で変換する関数cipherを実装せよ．
#  英小文字ならば(219 - 文字コード)の文字に置換
#  その他の文字はそのまま出力
# この関数を用い，英語のメッセージを暗号化・復号化せよ．

import re
def cipher(inp):

    out = []

    for e in list(inp):
        if re.search('^[a-z]+$', e):
            out.append(chr(219-ord(e)))
        else:
            out.append(e)

    return ''.join(out)

print(cipher('Hello I\'m going to 123.'))

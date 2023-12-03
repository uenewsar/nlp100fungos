# -*- coding: utf-8 -*-

"""
27. 内部リンクの除去
26の処理に加えて，テンプレートの値からMediaWikiの内部リンクマークアップを除去し，テキストに変換せよ

[[記事名]] -> 記事名
[[記事名|表示文字]] -> 表示文字
[[記事名#節名|表示文字]] -> 表示文字
"""

import re
import pprint


def process(inp):

    while True:
        # ''''斜体と強調'''''
        m = re.search(r"''''([^']+?)''''", inp)
        if m:
            inp = inp[:m.span()[0]] + m.group(1) + inp[m.span()[1]:]
            continue
        # '''強調'''
        m = re.search(r"'''([^']+?)'''", inp)
        if m:
            inp = inp[:m.span()[0]] + m.group(1) + inp[m.span()[1]:]
            continue
        # ''他との区別''
        m = re.search(r"''([^']+?)''", inp)
        if m:
            inp = inp[:m.span()[0]] + m.group(1) + inp[m.span()[1]:]
            continue

        # [[記事名|表示文字]] -> 表示文字
        # [[記事名#節名|表示文字]] -> 表示文字
        m = re.search(r"\[\[[^\|\[\]]+?\|([^\]\[]+?)\]\]", inp)
        if m:
            inp = inp[:m.span()[0]] + m.group(1) + inp[m.span()[1]:]
            continue
        # [[記事名]] -> 記事名
        m = re.search(r"\[\[([^\]\[\|]+?)\]\]", inp)
        if m:
            inp = inp[:m.span()[0]] + m.group(1) + inp[m.span()[1]:]
            continue

        break

    return inp


def main():

    obj = {}
    
    with open('uk.txt', 'r', encoding='utf-8') as fr:
        flag = 0
        for el in fr:
            el = el.rstrip()
            if el=='':
                continue
            
            if flag == 0:
                if el == '{{基礎情報 国':
                    flag = 1
            elif flag == 1:
                if el == '}}':
                    break
                m = re.search(r'^\|([^=]+)=(.+)$', el)
                if m:
                    key = m.group(1).strip()
                    value = m.group(2).strip()
                    assert(key not in obj)

                    # post process
                    org_value = value
                    value = process(value)
                    if value != org_value:
                        print('changed from "{}"'.format(org_value))
                        print('        to   "{}"'.format(value))
                    obj[key] = value

    pprint.pprint(obj)
        
if __name__=='__main__':
    main()

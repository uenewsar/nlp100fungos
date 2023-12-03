# -*- coding: utf-8 -*-

"""
26. 強調マークアップの除去
25の処理時に，テンプレートの値からMediaWikiの強調マークアップ（弱い強調，強調，強い強調のすべて）を除去してテキストに変換せよ

''他との区別''
'''強調'''
''''斜体と強調'''''
"""

import re
import pprint


def process(inp):

    while True:
        m = re.search(r"''''([^']+?)''''", inp)
        if m:
            inp = inp[:m.span()[0]] + m.group(1) + inp[m.span()[1]:]
            continue
        m = re.search(r"'''([^']+?)'''", inp)
        if m:
            inp = inp[:m.span()[0]] + m.group(1) + inp[m.span()[1]:]
            continue
        m = re.search(r"''([^']+?)''", inp)
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
                        print('changed from "{}" to "{}"'.format(org_value, value))
                    obj[key] = value

    pprint.pprint(obj)
                
                
if __name__=='__main__':
    main()

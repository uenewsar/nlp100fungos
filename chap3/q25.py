# -*- coding: utf-8 -*-

'''
25. テンプレートの抽出
記事中に含まれる「基礎情報」テンプレートのフィールド名と値を抽出し，辞書オブジェクトとして格納せよ．
'''

import re
import pprint

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
                    # not sure how much we must do post-processing on values
                    value = m.group(2).strip()
                    assert(key not in obj)
                    obj[key] = value

    pprint.pprint(obj)
                
                
if __name__=='__main__':
    main()

# -*- coding: utf-8 -*-

'''
22. カテゴリ名の抽出
記事のカテゴリ名を（行単位ではなく名前で）抽出せよ．
'''

import re
    
def main():
    PTN = re.compile(r'^\[\[Category\:([^\|]+).*\]\]')
    with open('uk.txt', 'r', encoding='utf-8') as fr:
        for line in fr:
            line = line.rstrip()
            m = PTN.search(line)
            if m:
                print(m.group(1))
                
if __name__=='__main__':
    main()

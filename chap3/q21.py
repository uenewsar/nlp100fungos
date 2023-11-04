# -*- coding: utf-8 -*-

'''
21. カテゴリ名を含む行を抽出
記事中でカテゴリ名を宣言している行を抽出せよ．
'''

import re
    
def main():
    PTN = re.compile(r'^\[\[Category\:.+\]\]')
    with open('uk.txt', 'r', encoding='utf-8') as fr:
        for line in fr:
            line = line.rstrip()
            if PTN.search(line):
                print(line)
                
if __name__=='__main__':
    main()

# -*- coding: utf-8 -*-

'''
23. セクション構造
記事中に含まれるセクション名とそのレベル（例えば”== セクション名 ==”なら1）を表示せよ．

'''

import re
    
def main():
    PTN = re.compile(r'^(=+)(.+?)(=+)$')
    with open('uk.txt', 'r', encoding='utf-8') as fr:
        for line in fr:
            line = line.rstrip()
            m = PTN.search(line)
            if m:
                beginning_equals = m.group(1)
                last_equals = m.group(3)
                if beginning_equals==last_equals:
                    print('{} {}'.format(len(beginning_equals)-1, m.group(2).strip()))
                
if __name__=='__main__':
    main()

# -*- coding: utf-8 -*-

'''
81. 複合語からなる国名への対処

英語では，複数の語の連接が意味を成すことがある．
例えば，アメリカ合衆国は"United States"，イギリスは"United Kingdom"と
表現されるが，"United"や"States"，"Kingdom"という単語だけでは，
指し示している概念・実体が曖昧である．そこで，コーパス中に
含まれる複合語を認識し，複合語を1語として扱うことで，
複合語の意味を推定したい．しかしながら，複合語を正確に
認定するのは大変むずかしいので，ここでは複合語からなる
国名を認定したい．
インターネット上から国名リストを各自で入手し，80のコーパス中に
出現する複合語の国名に関して，スペースをアンダーバーに置換せよ．
例えば，"United States"は"United_States"，"Isle of Man"は
"Isle_of_Man"になるはずである．

I got country list from
https://en.wikipedia.org/wiki/List_of_sovereign_states
'''

import re
import sys
from tqdm import tqdm


def main():
    
    # read country list
    country_list = []
    fr = open('country_list.txt', 'r', encoding='utf-8')
    for line in fr:
        line = line.rstrip()
        if re.search(r'^#', line):
            continue
        if re.search(r' ', line):
            country_list.append(line)
    fr.close()
    
    # sort by descending length
    country_list.sort(key=len)
    country_list.reverse()

    # make replaced sentence
    tmp = []
    for e in country_list:
        tmp.append( (e, re.sub(r' ', '_', e)) )
    country_list = tmp

    PTN1 = re.compile(r'^ ')
    PTN2 = re.compile(r' $')

    fw = open('text2.txt', 'w', encoding='utf-8')

    with open('text.txt', 'r', encoding='utf-8') as fr:
        for line in tqdm(fr):
            line = line.rstrip()

            # replace
            line = ' {} '.format(line)
            for (src, dst) in country_list:
                # str.replace process is much faster than regexp process
                #line = re.sub(re.escape(' {} '.format(src)), ' {} '.format(dst), line)
                line = line.replace(' {} '.format(src), ' {} '.format(dst))
            line = PTN1.sub('', line)
            line = PTN2.sub('', line)
        
            fw.write(line + '\n')

    fw.close()


if __name__=='__main__':
    main()

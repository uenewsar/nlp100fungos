# -*- coding: utf-8 -*-

'''
82. 文脈の抽出
81で作成したコーパス中に出現するすべての単語tに関して，
単語tと文脈語cのペアをタブ区切り形式ですべて書き出せ．
ただし，文脈語の定義は次の通りとする．
- ある単語tの前後d単語を文脈語cとして抽出する
  （ただし，文脈語に単語tそのものは含まない）
- 単語tを選ぶ度に，文脈幅dは{1,2,3,4,5}の範囲でランダムに決める．
'''

import re
import sys
import random

## main
# fix random seed for reproducing same results
random.seed(123)
# read outcome of 81
fr = open('text2.txt', 'r', encoding='utf-8')
# output file storing word vs. context
fw = open('context.txt', 'w', encoding='utf-8')
cnt = 0
for line in fr:

    cnt += 1
    if cnt % 10000 == 0:
        sys.stderr.write(' {}\n'.format(cnt))

    line = line.rstrip()

    # split to words
    words = line.split(' ')

    for i in range(len(words)):
        # i ... word idx in focusing
        
        # d ... window length (1-5)
        d = random.randint(1, 5)

        # enumerate context words prior to target word
        for j in range(1, d+1):
            idx = i-j
            if idx<0:
                continue
            fw.write('{}\t{}\n'.format(words[i], words[i-j]))

        # enumerate context words after the target word
        for j in range(1, d+1):
            idx = i+j
            if idx>=len(words):
                continue
            fw.write('{}\t{}\n'.format(words[i], words[i+j]))

fw.close()
fr.close()


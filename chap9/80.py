# -*- coding: utf-8 -*-

'''
第9章: ベクトル空間法 (I)
enwiki-20150112-400-r10-105752.txt.bz2は，2015年1月12日時点の
英語のWikipedia記事のうち，約400語以上で構成される記事の中から，
ランダムに1/10サンプリングした105,752記事のテキストをbzip2形式
で圧縮したものである．このテキストをコーパスとして，単語の意味
を表すベクトル（分散表現）を学習したい．第9章の前半では，
コーパスから作成した単語文脈共起行列に主成分分析を適用し，単語
ベクトルを学習する過程を，いくつかの処理に分けて実装する．
第9章の後半では，学習で得られた単語ベクトル（300次元）を用い，
単語の類似度計算やアナロジー（類推）を行う．

なお，問題83を素直に実装すると，大量（約7GB）の主記憶が必要になる．
メモリが不足する場合は，処理を工夫するか，1/100サンプリングの
コーパスenwiki-20150112-400-r100-10576.txt.bz2を用いよ．

80. コーパスの整形
文を単語列に変換する最も単純な方法は，空白文字で単語に区切る
ことである． ただ，この方法では文末のピリオドや括弧などの記号が
単語に含まれてしまう． そこで，コーパスの各行のテキストを空白文字で
トークンのリストに分割した後，各トークンに以下の処理を施し，
単語から記号を除去せよ．
- トークンの先頭と末尾に出現する次の文字を削除: .,!?;:()[]'"
- 空文字列となったトークンは削除
以上の処理を適用した後，トークンをスペースで連結してファイルに保存せよ．
'''

import re
import bz2
import sys
from tqdm import tqdm


def main():

    fw = open('text.txt', 'w', encoding='utf-8')

    PTN1 = re.compile(r'^[\.\,\!\?\;\:\(\)\[\]\'\"]+')
    PTN2 = re.compile(r'[\.\,\!\?\;\:\(\)\[\]\'\"]+$')


    with bz2.open("enwiki-20150112-400-r10-105752.txt.bz2", "rt", encoding="utf_8") as fr:
        for line in tqdm(fr):
        
            line = line.rstrip()
            words = line.split(' ')
            buf = []
            for e in words:
                #e = re.sub(r'^[\.\,\!\?\;\:\(\)\[\]\'\"]+', '', e)
                #e = re.sub(r'[\.\,\!\?\;\:\(\)\[\]\'\"]+$', '', e)
                e = PTN1.sub('', e)
                e = PTN2.sub('', e)
                if e != '':
                    buf.append(e)

            if len(buf) > 0:
                fw.write(' '.join(buf) + '\n')

    fw.close()

if __name__=='__main__':
    main()


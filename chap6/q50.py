# -*- coding: utf-8 -*-

'''
第6章: 機械学習

本章では，Fabio Gasparetti氏が公開しているNews Aggregator Data Setを用い，
ニュース記事の見出しを「ビジネス」「科学技術」「エンターテイメント」
「健康」のカテゴリに分類するタスク（カテゴリ分類）に取り組む．
(https://archive.ics.uci.edu/ml/datasets/News+Aggregator)

50. データの入手・整形
News Aggregator Data Setをダウンロードし、以下の要領で学習データ
（train.txt），検証データ（valid.txt），評価データ（test.txt）を作成せよ．

1. ダウンロードしたzipファイルを解凍し，readme.txtの説明を読む．
2. 情報源（publisher）が”Reuters”, “Huffington Post”, “Businessweek”, “Contactmusic.com”, “Daily Mail”の事例（記事）のみを抽出する．
3. 抽出された事例をランダムに並び替える．
4. 抽出された事例の80%を学習データ，残りの10%ずつを検証データと評価データに分割し，それぞれtrain.txt，valid.txt，test.txtというファイル名で保存する．ファイルには，１行に１事例を書き出すこととし，カテゴリ名と記事見出しのタブ区切り形式とせよ（このファイルは後に問題70で再利用する）．
学習データと評価データを作成したら，各カテゴリの事例数を確認せよ．
'''

import re
import os
import subprocess
import csv
import random
import collections
from pprint import pprint

def exec_command(cmd):
    print(cmd)
    proc = subprocess.Popen(cmd, shell=True)
    proc.communicate()

    
def download_and_unzip_dataset():

    url = 'https://archive.ics.uci.edu/static/public/359/news+aggregator.zip'
    filename = 'news+aggregator.zip'
    dirname = re.sub(r'\..+$', '', filename)
    if not os.path.isdir(dirname):
        if not os.path.isfile(filename):
            # download zip
            exec_command('wget {}'.format(url))
        # unzip
        exec_command('unzip {} -d {}'.format(filename, dirname))
    

        
def read_news():

    fn = 'news+aggregator/newsCorpora.csv'

    pub2cnt = {
        'Reuters': 0,
        'Huffington Post': 0,
        'Businessweek': 0,
        'Contactmusic.com': 0,
        'Daily Mail': 0
    }

    ret = []

    with open(fn, 'r') as fr:
        cr = csv.reader(fr, delimiter='\t')
        # FORMAT: ID \t TITLE \t URL \t PUBLISHER \t CATEGORY \t STORY \t HOSTNAME \t TIMESTAMP
        for e in cr:
            # check publisher
            if e[3] not in pub2cnt:
                continue
            pub2cnt[e[3]] += 1
            # extract category and title
            ret.append( [e[4], e[1]])

    print('number of articles of publishers')
    pprint(pub2cnt)
            
    return ret


def write_csv(obj, fn, categories):

    cat2num = {}
    for e in categories:
        cat2num[e] = 0

    with open(fn, 'w') as fw:
        cw = csv.writer(fw, delimiter='\t')
        # category \t title
        for e in obj:
            cw.writerow(e)
            cat2num[e[0]] += 1

    # show number of items of categories
    print(fn)
    print(' total number of items: {}'.format(len(obj)))
    print(' number of items of categories:\n  {}'.format(cat2num))
    
        
def main():
    # download dataset from Web
    download_and_unzip_dataset()
    # read dataset
    obj = read_news()
    # count categories
    cat2num = collections.defaultdict(int)
    for e in obj:
        cat2num[e[0]] += 1
    cat2num = dict(cat2num)
    
    print('number of items of categories:')
    print(' {}'.format(cat2num))
    
    # shuffle order
    random.seed(42)
    random.shuffle(obj)
    
    # write training data
    write_csv(obj[0 : int(len(obj)*0.8)], 'train.txt', list(cat2num.keys()))
    write_csv(obj[int(len(obj)*0.8) : int(len(obj)*0.9)], 'valid.txt', list(cat2num.keys()))
    write_csv(obj[int(len(obj)*0.9) : ], 'test.txt', list(cat2num.keys()))
    

if __name__=='__main__':
    main()

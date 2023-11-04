# -*- coding: utf-8 -*-

'''
第3章: 正規表現
Wikipediaの記事を以下のフォーマットで書き出したファイルjawiki-country.json.gzがある．
1行に1記事の情報がJSON形式で格納される
各行には記事名が”title”キーに，記事本文が”text”キーの辞書オブジェクトに格納され，そのオブジェクトがJSON形式で書き出される
ファイル全体はgzipで圧縮される
以下の処理を行うプログラムを作成せよ．

20. JSONデータの読み込み
Wikipedia記事のJSONファイルを読み込み，「イギリス」に関する記事本文を表示せよ．
問題21-29では，ここで抽出した記事本文に対して実行せよ．
'''

import subprocess
import os
import gzip
import json
    
    
def exec_command(cmd):
    print(cmd)
    proc = subprocess.Popen(cmd, shell=True)
    proc.communicate()

def download_dataset(url):
    filename = url.split('/')[-1]
    if not os.path.isfile(filename):
        # download file
        exec_command('wget {}'.format(url))
        
def main():

    url = 'https://nlp100.github.io/data/jawiki-country.json.gz'
    download_dataset(url)
    filename = url.split('/')[-1]

    body = None
    
    with gzip.open(filename, 'rt') as fr:        
        for line in fr:
            obj = json.loads(line.rstrip())
            if obj['title']=='イギリス':
                body = obj['text']
                break

    assert(body is not None)
    with open('uk.txt', 'w', encoding='utf-8') as fw:
        fw.write(body)

if __name__=='__main__':
    main()
    print('SUCCESSFULLY ENDED')

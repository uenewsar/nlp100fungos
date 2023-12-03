# -*- coding: utf-8 -*-

'''
29. 国旗画像のURLを取得するPermalink
テンプレートの内容を利用し，国旗画像のURLを取得せよ．（ヒント: MediaWiki APIのimageinfoを呼び出して，ファイル参照をURLに変換すればよい）
'''

import re
import requests


def process(inp):

    while True:
        # ''''斜体と強調'''''
        m = re.search(r"''''([^']+?)''''", inp)
        if m:
            inp = inp[:m.span()[0]] + m.group(1) + inp[m.span()[1]:]
            continue
        # '''強調'''
        m = re.search(r"'''([^']+?)'''", inp)
        if m:
            inp = inp[:m.span()[0]] + m.group(1) + inp[m.span()[1]:]
            continue
        # ''他との区別''
        m = re.search(r"''([^']+?)''", inp)
        if m:
            inp = inp[:m.span()[0]] + m.group(1) + inp[m.span()[1]:]
            continue

        # [[ファイル:Wikipedia-logo-v2-ja.png|thumb|説明文]] -> 説明文
        m = re.search(r"\[\[ファイル:[^\|]+\|[^\|]+\|([^\]]+?)\]\]", inp)
        if m:
            inp = inp[:m.span()[0]] + m.group(1) + inp[m.span()[1]:]
            continue
       

        # [[記事名|表示文字]] -> 表示文字
        # [[記事名#節名|表示文字]] -> 表示文字
        m = re.search(r"\[\[[^\|\[\]]+?\|([^\]\[]+?)\]\]", inp)
        if m:
            inp = inp[:m.span()[0]] + m.group(1) + inp[m.span()[1]:]
            continue
        # [[記事名]] -> 記事名
        m = re.search(r"\[\[([^\]\[\|]+?)\]\]", inp)
        if m:
            inp = inp[:m.span()[0]] + m.group(1) + inp[m.span()[1]:]
            continue

        break

    return inp


def get_field(obj, field):
    # find field and return it

    if type(obj) is dict:
        if field in obj and type(obj[field]) is str:
            return obj[field]
        else:
            for ek in obj.keys():
                if type(obj[ek]) is dict or type(obj[ek]) is list:
                    ret = get_field(obj[ek], field)
                    if ret is not None:
                        return ret
            return None
    elif type(obj) is list:
        for ei in obj:
            if type(ei) is dict or type(ei) is list:
                ret = get_field(ei, field)
                if ret is not None:
                    return ret
        return None
    else:
        return None    


def get_url(fn):
    #curl -v --get --data-urlencode "action=query" --data-urlencode "format=json" --data-urlencode "prop=imageinfo" --data-urlencode "iiprop=url"  --data-urlencode "titles=ファイル:Flag of the United Kingdom.svg" https://ja.wikipedia.org/w/api.php

    url = 'https://ja.wikipedia.org/w/api.php'
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url",
        "titles": "ファイル:{}".format(fn)
    }
    res = requests.get(url, params=params).json()
    return get_field(res, 'url')




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
                    value = process(value)
                    obj[key] = value

    # get URL
    url = get_url(obj['国旗画像'])
    print(url)
    

         
if __name__=='__main__':
    main()

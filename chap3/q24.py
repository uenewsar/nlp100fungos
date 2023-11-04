# -*- coding: utf-8 -*-

'''
24. ファイル参照の抽出
記事から参照されているメディアファイルをすべて抜き出せ．
'''

import re


def check_extension(filename, extensions):
    for ee in extensions:
        if filename.endswith(ee):
            return True
    return False


def extract_basic_info(obj, extensions):

    ret = []
    
    for el in obj.split('\n'):
        el = el.rstrip()
        if el=='':
            continue

        m = re.search(r'^\|[^=]+=(.+)$', el)
        if not m:
            continue
        tgt = m.group(1).strip()

        if check_extension(tgt, extensions):
            ret.append(tgt)

    #print(ret)
    return ret


def extract_normal(obj, extensions):

    ret = []

    while True:
        m = re.search(r'^[\s\S]*?(\[\[[\s\S]*)$', obj)
        if not m:
            break
        obj = m.group(1)

        m = re.search(r'^\[\[(.+?)\]\]([\s\S]*)$', obj)
        assert(m)
        obj = m.group(2)

        tgt = m.group(1)
        # delete "|" and after
        tgt = re.sub(r'\|.+$', '', tgt)

        # extract after ":"
        m = re.search(r':([^:]+)$', tgt)
        if not m:
            continue
        tgt = m.group(1)

        # check extension
        if check_extension(tgt, extensions):
            ret.append(tgt)

    #print(ret)
    return ret


        
def extract_gallery(obj, extensions):
    '''
    <gallery>...</gallery>
    '''

    m = re.search(r'<gallery>([\s\S]+)<\/gallery>', obj)
    if not m:
        return []

    ret = []
    tgt = m.group(1)
    for el in tgt.split('\n'):
        el = el.strip()
        if el=='':
            continue
        el = re.sub(r'\|.*$', '', el).strip()

        if check_extension(el, extensions):
            ret.append(el)

    #print(ret)
    return ret

    
def main():

    extensions = [
        "tiff", "tif", "png", "gif", "jpg", "jpeg", "webp", "xcf", "pdf", "mid", "ogg", "ogv",
        "svg", "djvu", "oga", "flac", "opus", "wav", "webm", "mp3", "midi", "mpg", "mpeg"
    ]
    extensions = extensions + [x.upper() for x in extensions]
    extensions = ['.{}'.format(x) for x in extensions]
        
    with open('uk.txt', 'r', encoding='utf-8') as fr:
        obj = fr.read()

    # extract normal media file reference
    ret = extract_normal(obj, extensions)

    # extract like "|国旗画像 = Flag of the United Kingdom.svg"
    ret.extend(extract_basic_info(obj, extensions))
    
    # extract <gallery> ... </gallery>
    ret.extend(extract_gallery(obj, extensions))

    # output
    for (i, e) in enumerate(ret):
        print('{} {}'.format(i+1, e))

                
if __name__=='__main__':
    main()

# -*- coding: utf-8 -*-

'''
72. 素性抽出
極性分析に有用そうな素性を各自で設計し，
学習データから素性を抽出せよ．素性としては，
レビューからストップワードを除去し，各単語を
ステミング処理したものが最低限のベースライン
となるであろう．
'''

import re
import sys
from stemming.porter2 import stem

# from https://gist.github.com/sebleier/554280
stop_words = {
    "i", "me", "my", "myself", "we", "our",
    "ours", "ourselves", "you", "your", "yours",
    "yourself", "yourselves", "he", "him", "his", "himself",
    "she", "her", "hers", "herself", "it", "its",
    "itself", "they", "them", "their", "theirs", "themselves",
    "what", "which", "who", "whom", "this", "that",
    "these", "those", "am", "is", "are", "was",
    "were", "be", "been", "being", "have", "has",
    "had", "having", "do", "does", "did", "doing",
    "a", "an", "the", "and", "but", "if",
    "or", "because", "as", "until", "while", "of",
    "at", "by", "for", "with", "about", "against",
    "between", "into", "through", "during", "before", "after",
    "above", "below", "to", "from", "up", "down",
    "in", "out", "on", "off", "over", "under",
    "again", "further", "then", "once", "here", "there",
    "when", "where", "why", "how", "all", "any",
    "both", "each", "few", "more", "most", "other",
    "some", "such", "no", "nor", "not", "only",
    "own", "same", "so", "than", "too", "very",
    "s", "t", "can", "will", "just", "don", "should",
    "now"}

class Instance(object):
    # class to store one instance of training/evaluation data
    def __init__(self):
        self.label = None
        self.sentence = None
        self.words = None
        self.feat = None
        self.feat_vec = None

def create_feat(org_words):

    # make unigram and bigram feat

    # to aviid changing original memory
    words = list(org_words)

    # delete symbol tokens
    tmp = []
    for e in words:
        if not re.search(r'^[^0-9a-zA-Z]+$', e):
            # if it is NOT only-symbol word
            tmp.append(e)
    words = tmp

    # stemming
    for i in range(len(words)):
        words[i] = stem(words[i])
    
    # assign flag to stop words
    for i in range(len(words)):
        if is_stop_word(words[i]):
            words[i] = '__stop__'
    
    feat = {}

    # add BOS and EOS
    words.insert(0, 'BOS')
    words.append('EOS')

    ## make unigram
    for i in range(len(words)):
        if words[i] == '__stop__':
            continue
        feat[words[i]] = 1

    ## make bigram
    for i in range(len(words)-1):
        if words[i] == '__stop__' or words[i+1] == '__stop__':
            continue
        feat['{}_{}'.format(words[i], words[i+1])] = 1

    # no matter how much one feature exist in one sentence,
    # the value of feature is set to 1.

    # debug
    #sys.stderr.write('[{}]\n  -> [{}]\n'.format(' '.join(org_words), ' '.join(sorted(feat.keys()))))
    return feat


def read_data(fn):

    data = []
    fr = open(fn, 'r', encoding='utf-8')
    for e in fr:
        e = e.rstrip()

        # delete duplicated space
        e = re.sub(r' +', ' ', e)
        # lower
        e = e.lower()
        
        tab = e.split(' ')
        # label -> [0]
        label = int(tab[0])
        # words -> [1, 2, ...]
        words = tab[1:]

        # sentence
        sentence = ' '.join(tab[1:])

        ins = Instance()
        ins.label = label
        ins.words = words
        ins.sentence = sentence
        data.append(ins)

    fr.close()

    return data

def is_stop_word(inp):
    if inp in stop_words:
        return True
    else:
        return False

# main
data = read_data('sentiment.txt')
for e in data:
    e.feat = create_feat(e.words)
# creat feat vs. freq
feat2freq = {}
for e in data:
    for ef in e.feat:
        if ef not in feat2freq:
            feat2freq[ef] = 0
        feat2freq[ef] += 1
# delete singleton and make feat to be used
feat2id = {}
for k, v in feat2freq.items():
    if v>1:
        feat2id[k] = len(feat2id)
    else:
        #print('{} is deleted.'.format(k))
        pass
# make feature vector
for ed in data:
    vec = [0.0] *  len(feat2id)
    to_be_del = []
    for ef in ed.feat.keys():
        if ef in feat2id:
            vec[feat2id[ef]] = 1.0
        else:
            to_be_del.append(ef)
    # add feature vector
    ed.feat_vec = vec
    # delete unregistered feature
    for ef in to_be_del:
        del(ed.feat[ef])


for ed in data:
    print('sentence: {}'.format(ed.sentence))
    print(' -> feat: {}'.format(' '.join(sorted(ed.feat.keys()))))



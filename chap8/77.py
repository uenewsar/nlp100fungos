# -*- coding: utf-8 -*-

'''
77. 正解率の計測
76の出力を受け取り，予測の正解率，正例に関する適合率，
再現率，F1スコアを求めるプログラムを作成せよ．
'''

import re
import sys
import numpy as np
import stemming.porter2
from sklearn.linear_model import LogisticRegression

# as stemming.porter2.stem is a little bit slow, use cache.
stem_cache = {}
def stem(inp):
    if inp not in stem_cache:
        stem_cache[inp] = stemming.porter2.stem(inp)
    return stem_cache[inp]

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

def create_feat(org_words, feat2id=None):

    # make unigram and bigram feat

    # to avoid changing original memory
    words = list(org_words)

    # delete symbol tokens
    tmp = []
    for e in words:
        if not re.search(r'^[^0-9a-zA-Z]+$', e):
            # use if the word is NOT only-symbol word
            tmp.append(e)
    words = tmp

    # stemming
    for i in range(len(words)):
        words[i] = stem(words[i])
    
    # assign flag for showing stop words
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

    # if each feature is not defined in feat2id, delete
    vec = None
    if feat2id is not None:
        tmp = {}
        for ef in feat.keys():
            if ef in feat2id:
                tmp[ef] = 1
        feat = tmp

        # also make feature vector
        vec = [0.0] * len(feat2id)
        for ef in feat.keys():
            vec[feat2id[ef]] = 1.0


    # debug
    #sys.stderr.write('[{}]\n  -> [{}]\n'.format(' '.join(org_words), ' '.join(sorted(feat.keys()))))
    return (feat, vec)



def normalize_stc(inp):

    # delete duplicated space
    inp = re.sub(r' +', ' ', inp)
    # lower
    inp = inp.lower()

    return inp


def read_data(fn):

    data = []
    fr = open(fn, 'r', encoding='utf-8')
    for e in fr:
        e = e.rstrip()

        e = normalize_stc(e)

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


def make_feat_to_be_used(data):

    # from raw features, extract actual features to be used.

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

    return feat2id

## main
data = read_data('sentiment.txt')

# first, makes all possible features
for e in data:
    (e.feat, _) = create_feat(e.words)

# make actual features to be used
feat2id = make_feat_to_be_used(data)

#for e in sorted(feat2id.keys()):
#    print('{} {}'.format(e, feat2id[e]))
#exit()

# make feature vector
for ed in data:
    (ed.feat, ed.feat_vec) = create_feat(ed.words, feat2id)

## train
x = []
y = []
for ed in data:
    x.append(ed.feat_vec)
    y.append(ed.label)
lr = LogisticRegression(solver='liblinear')
lr.fit(x, y)

## evaluation in training data, with evaluation of acciracies
# regard "positive polarity" as "positive"
mat = {'TP':0, 'FN':0, 'FP':0, 'TN':0}
cor = 0
for ed in data:
        
    est_label = lr.predict([ed.feat_vec])[0]
    est_prob = lr.predict_proba([ed.feat_vec])[0][np.where(lr.classes_==est_label)][0]

    if est_label==ed.label:
        cor += 1

    if est_label==1 and ed.label==1:
        mat['TP'] += 1
    elif est_label==1 and ed.label==-1:
        mat['FP'] += 1
    elif est_label==-1 and ed.label==1:
        mat['FN'] += 1
    elif est_label==-1 and ed.label==-1:
        mat['TN'] += 1
    else:
        raise Exception('error')

print(' accuracy: {}'.format(float(cor)/len(data)))
precision = float(mat['TP']) / (mat['TP']+mat['FP'])
print('precision: {}'.format(precision))
recall = float(mat['TP']) / (mat['TP']+mat['FN'])
print('   recall: {}'.format(recall))
print('       f1: {}'.format( 2 * precision * recall / (precision + recall) ))

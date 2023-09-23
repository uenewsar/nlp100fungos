# -*- coding: utf-8 -*-

'''
51. 特徴量抽出
学習データ，検証データ，評価データから特徴量を抽出し，それぞれtrain.feature.txt，valid.feature.txt，test.feature.txtというファイル名で保存せよ． なお，カテゴリ分類に有用そうな特徴量は各自で自由に設計せよ．記事の見出しを単語列に変換したものが最低限のベースラインとなるであろう．

Policy
I use 1-gram, 2-gram, and 3-gram features after light normalization and stemming

'''

import re
import csv
import collections
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
from tqdm import tqdm

class NLTKWrapper(object):
    '''
    User NLTK functionalities
    '''
    def __init__(self):
        # read stopwords
        nltk.download('stopwords')
        self.stopwords = set(stopwords.words('english'))
        # load porter stemmer
        self.stemmer = PorterStemmer()

    def is_stopword(self, inp):
        assert(type(inp) is str)
        return inp in self.stopwords

    def stem(self, inp):
        return self.stemmer.stem(inp)
    

def read_csv(fn):
    '''
    Read csv file
    Return:
      List of items. One item is a dictionary containing "category" and "title" keys
    '''
    
    ret = []
    with open(fn, 'r') as fr:
        cr = csv.reader(fr, delimiter='\t')
        # format: category \t title
        for e in cr:
            ret.append({
                'category': e[0],
                'title': e[1]
            })
    return ret


def write_csv(obj, fn):

    with open(fn, 'w') as fw:
        cw = csv.writer(fw, delimiter='\t')
        # category \t feature vector
        for e in obj:
            cw.writerow([e['label'], str(e['feature'])])


            
def create_ngrams(words, order):
    ret = []
    for i in range(len(words)-order+1):
        ret.append(list(words[i:i+order]))
    return ret    


def conv_sent_to_feat_vect(inp, nltk_wrapper=None):
    '''
    Convert one sentence to feature vector
    '''

    '''
    Normalize the sentence
    Note it is designed by looking at actual data
    '''
    # delete top/end spaces
    inp = inp.strip()
    # delete last periods like "..."
    inp = re.sub(r'[ \.]+$', '', inp)
    # delete last number with parenthesis like (1), (2)
    inp = re.sub(r' *\([0-9]+\) *$', '', inp)
    # delete double quotation
    inp = re.sub(r'"', '', inp)
    # delete single quotation if it is in starting or ending position of word
    inp = re.sub(r' \'', ' ', inp)
    inp = re.sub(r'^\'', '', inp)
    inp = re.sub(r'\' ', ' ', inp)
    inp = re.sub(r'\'$', '', inp)
    # delete ',', ':', ';'
    inp = re.sub(r'[,:;]', '', inp)
    # replace '-' to a space
    inp = re.sub(r'\-', ' ', inp)

    # normalize spaces
    inp = inp.strip()
    inp = re.sub(r' +', ' ', inp)

    # lowering
    inp = inp.lower()

    # split to words
    words = inp.split(' ')

    # add beginning of sencence (BOS) and end of sentence (EOS) special words
    words = ['BOS'] + words + ['EOS']

    '''
    create 1, 2, and 3 grams
    '''
    ngrams = create_ngrams(words, order=1)
    ngrams += create_ngrams(words, order=2)
    ngrams += create_ngrams(words, order=3)
    
    '''
    if a stopword is included in ngrams, delete them
    '''
    if nltk_wrapper is not None:
        tmp = []
        for en in ngrams:
            flag = True
            for ew in en:
                if nltk_wrapper.is_stopword(ew):
                    flag = False
                    break
            if flag:
                tmp.append(en)
        ngrams = tmp

    '''
    apply stemmer
    '''
    if nltk_wrapper is not None:
        tmp = []
        for en in ngrams:
            tmp2 = []
            for ew in en:
                if ew != 'BOS' and ew != 'EOS':
                    tmp2.append(nltk_wrapper.stem(ew))
                else:
                    tmp2.append(ew)
            tmp.append(tmp2)

        #print('  {}\n-> {}'.format(ngrams, tmp))
        ngrams = tmp

    return ngrams
    
        
    
def delete_singleton(obj):

    feat2cnt = collections.defaultdict(int)
    for es in obj:
        for ef in es:
            assert(type(ef) is list)
            feat2cnt[str(ef)] += 1

    num_singleton = 0
    for ef in feat2cnt.keys():
        if feat2cnt[ef] == 1:
            num_singleton += 1

    print('{} singletons are found out of {} features'.format(num_singleton, len(feat2cnt)))
    print('deleting sigletons ...')
    
    ret = []
    for es in tqdm(obj):
        tmp = []
        for ef in es:
            if feat2cnt[str(ef)] > 1:
                tmp.append(ef)
        ret.append(tmp)
    
    return ret
    

        
def create_featrures(obj, nltk_wrapper=None, feat_dict=None, create_feat_dict=False):

    if feat_dict is None and create_feat_dict is False:
        raise Exception('error: create_feat_dict must be True when feat_dict is None')
    
    ret = []
    print('converting sentences to features ...')
    for e in tqdm(obj):
        ret.append(conv_sent_to_feat_vect(e['title'], nltk_wrapper=nltk_wrapper))
    obj = ret

    if create_feat_dict:
        '''
        create feature dictionary
        '''
        # delete singleton
        obj = delete_singleton(obj)
        
        # create featur-to-id dictionary (i.e. feature dictionary)
        feat_dict = {}
        for es in obj:
            for ef in es:
                if str(ef) not in feat_dict:
                    feat_dict[str(ef)] = len(feat_dict)
        print('{} features are registered to dictionary'.format(len(feat_dict)))


    '''
    delete unknown feature
    '''
    tmp = []
    num_del = 0
    num_total = 0
    for es in obj:
        tmp2 = []
        num_total += len(es)
        for ef in es:
            if str(ef) in feat_dict:
                tmp2.append(ef)
            else:
                num_del += 1
        tmp.append(tmp2)
    print('{} out of {} features are deleted due to unknown feature'.format(num_del, num_total))
    obj = tmp
        
    '''
    conver to feature vector
    '''
    ret = []
    for es in obj:
        tmp = collections.defaultdict(int)
        for ef in es:
            tmp[feat_dict[str(ef)]] += 1
        ret.append(dict(tmp))
    
    return (ret, feat_dict)



def add_feat_to_data(obj, feat, label_dict):
    assert(len(obj)==len(feat))
    for (eo, ef) in zip(obj, feat):
        eo['feature'] = ef
        eo['label'] = label_dict[eo['category']]
    return obj
    
    
    
def main():

    nltk_wrapper = NLTKWrapper()
    
    '''
    training data
    '''
    # read
    print('processing training data')
    train = read_csv('train.txt')
    # create feature and feature dictionary
    (feat, feat_dict)  = create_featrures(
        train,
        nltk_wrapper=nltk_wrapper,
        create_feat_dict=True
    )

    # create label dictionary
    tmp = set()
    for e in train:
        tmp.add(e['category'])
    tmp = sorted(list(tmp))
    label_dict = {}
    for e in tmp:
        label_dict[e] = len(label_dict)

    train = add_feat_to_data(train, feat, label_dict)
    write_csv(train, 'train.feature.txt')

    # store label dictionary
    with open('label_dictionary.txt', 'w', encoding='utf-8') as fw:
        fw.write(str(label_dict))
    # store feature dictionary
    with open('feature_dictionary.txt', 'w', encoding='utf-8') as fw:
        fw.write(str(feat_dict))

    
    '''
    validation data
    '''
    print('processing validation data')
    valid = read_csv('valid.txt')
    (feat, _)  = create_featrures(valid, nltk_wrapper=nltk_wrapper, feat_dict=feat_dict)
    valid = add_feat_to_data(valid, feat, label_dict)
    write_csv(valid, 'valid.feature.txt')
    
    '''
    test data
    '''
    print('processing test data')
    test = read_csv('test.txt')
    # create feature and feature dictionary
    (feat, _)  = create_featrures(test, nltk_wrapper=nltk_wrapper, feat_dict=feat_dict)
    test = add_feat_to_data(test, feat, label_dict)
    write_csv(test, 'test.feature.txt')

    

if __name__=='__main__':
    main()

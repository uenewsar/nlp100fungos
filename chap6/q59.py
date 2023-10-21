# -*- coding: utf-8 -*-

'''
59. ハイパーパラメータの探索
学習アルゴリズムや学習パラメータを変えながら，カテゴリ分類モデルを学習せよ．
検証データ上の正解率が最も高くなる学習アルゴリズム・パラメータを求めよ．
また，その学習アルゴリズム・パラメータを用いたときの評価データ上の正解率を求めよ．
'''

from sklearn.linear_model import LogisticRegression
from sklearn.metrics  import accuracy_score
from tabulate import tabulate
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from tqdm import tqdm
import random
import queue
import threading
    
from q52 import read_data, get_num_dict, read_feature_label

class Predictor(object):
    
    def __init__(self, param):
        self.clf = None
        self.transformer = None
        if param['model_type'] == 'svm_linear':
            self.model = LinearSVC(
                C = 1/param['c'],
                random_state=42,
                dual='auto'
            )
        elif param['model_type'] == 'logistic_regression':
            self.model = LogisticRegression(
                random_state = 42,
                solver = 'liblinear',
                C = 1/param['c']
            )
        elif param['model_type'] == 'random_forest':
            self.model = RandomForestClassifier(
                random_state=42,
                criterion = param['criterion'],
                n_estimators = param['n_estimators'],
            )
        else:
            raise Exception()
        

    def train(self, x, y):

        #self.transformer = preprocessing.StandardScaler()
        #self.transformer.fit(x)
        #self.clf = self.model.fit(self.transformer.transform(x), y)
        self.clf = self.model.fit(x, y)


    def evaluate(self, feat_label):
        # data
        (x, y) = feat_label
        # predict
        #y_pred = self.clf.predict(self.transformer.transform(x))
        y_pred = self.clf.predict(x)
        # get accuracy
        return accuracy_score(y, y_pred)
        

def do_process(idx, q2p, q2m, train_feat_label, valid_feat_label, test_feat_label, num_feat):

    while True:
        model_type = q2p.get()
        if model_type is None:
            break
        
        print('thread {}, train model type {}'.format(idx, model_type))

        '''
        train classifier model
        '''
        clf = Predictor(model_type)
        clf.train(train_feat_label[0], train_feat_label[1])

        '''
        evaluate
        '''
        print('thread {}, evaluate model type {}'.format(idx, model_type))
        # training data
        acc_train = clf.evaluate(train_feat_label)
        # validation data
        acc_valid = clf.evaluate(valid_feat_label)
        # test data
        acc_test = clf.evaluate(test_feat_label)

        res = {
            'model_type': model_type,
            'acc_train': acc_train,
            'acc_valid': acc_valid,
            'acc_test': acc_test
        }
        print('thread {}, send evaluation result {}'.format(idx, res))
        q2m.put(res)

    
    
def main():

    random.seed(42)

    '''
    make model_types array
    '''
    model_types = []
    # SVM linear
    c = [0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5]
    for ec in c:
        model_types.append( {'model_type': 'svm_linear', 'c': ec} )
    # Logistic Regression
    for ec in c:
        model_types.append( {'model_type': 'logistic_regression', 'c': ec} )
    # Random Forest
    for ec in ['gini', 'entropy', 'log_loss']:
        for en in [10, 20, 50]:
            model_types.append( {'model_type': 'random_forest', 'criterion': ec, 'n_estimators': en} )

    # get num of feature from dictionary
    num_feat = get_num_dict('data/feature_dictionary.txt')
    # read training/validation/test data and convert to numpy array
    train_feat_label = read_feature_label('data/train.feature.txt', num_feat)
    valid_feat_label = read_feature_label('data/valid.feature.txt', num_feat)
    test_feat_label = read_feature_label('data/test.feature.txt', num_feat)

    # too slow, so use multi-thread
    num_threads = 4
    q2p = queue.Queue()
    q2m = queue.Queue()
    threads = []
    for i in range(num_threads):
        h = threading.Thread(target=do_process, args=(i, q2p, q2m, train_feat_label, valid_feat_label, test_feat_label, num_feat,))
        h.daemon = True
        h.start()

    # send model_types
    for em in model_types:
        q2p.put(em)

    # wait results
    best = None
    res = []
    pbar = tqdm(total=len(model_types), ascii=True)
    while len(res)<len(model_types):
        eres = q2m.get()
        res.append(eres)
        if best is None or best['acc_valid'] < eres['acc_valid']:
            print(' outperformed the previous best')
            best = eres
        pbar.update(1)

    pbar.close()
    print('best in validation: {}'.format(best))

    # top 10 models
    res = sorted(res, key=lambda x: -x['acc_valid'])
    res = res[:10]
    print('top 10 models')
    print(tabulate([ (x['model_type'], x['acc_valid'], x['acc_test']) for x in res], headers=['model_type', 'valid', 'test']))

    
if __name__=='__main__':
    main()

#-*-coding:utf-8-*-

import numpy as np
import pandas as pd
import MeCab
from collections import Counter
from sklearn.model_selection import KFold, cross_validate, GridSearchCV
from sklearn.svm import LinearSVC

def text2word_list(text):
    chasen_list = MeCab.Tagger("-Ochasen").parse(text).splitlines()
    word_list = []
    for chasen in chasen_list:
        cha_list = chasen.split("\t")
        if len(cha_list) >= 3:
            hinshi = cha_list[3].split('-')[0]
            #if hinshi == "名詞" or hinshi == "動詞":
                #word_list.append(cha_list[0])#そのまま
            word_list.append(cha_list[2])#原型
    return word_list

#文を入力
df = pd.read_csv('./data/app_review_sentiment.csv')

#単語インデックス辞書を作る
all_word = []
for text in list(df['text']):
    all_word += text2word_list(text)
word2index = {}
for i, (w, c) in enumerate(Counter(all_word).most_common()):
    if c >= 3:
        word2index[w] = i
        max_index = i

#データセットを作る
y = np.array(df['sentiment'])

X = np.zeros((len(df['text']), max_index+1))
for i, text in enumerate(list(df['text'])):
    for word in text2word_list(text):
        if word in word2index:
            X[i][word2index[word]] = 1

#グリッドサーチをする
param = [{'C': [0.1, 1, 10, 100, 1000]}]
clf = GridSearchCV(
        LinearSVC(),
        param,
        cv=5)

#5分割交差検定をする
clf.fit(X, y)
C = clf.best_params_['C']
kfold = KFold(n_splits = 5, shuffle = True, random_state = 0)
model = LinearSVC(C=C)
results = cross_validate(model, X, y, cv = kfold, scoring = 'accuracy')
print("5-fold Cross Validation 平均 Accuracy: %.2f" % (results['test_score'].mean()))
print(results)



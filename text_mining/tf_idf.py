#-*-coding:utf-8-*- 

import sys
import re
import MeCab
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer

#テキストから空白文字を除去する
def remove_space(text):
    text = re.sub(' ','',text)
    text = re.sub('\u3000','',text)
    text = re.sub('\n','',text)
    text = re.sub('\t','',text)
    text = re.sub('\r','',text)
    return text

#テキストを文のリストにする
def text2sentence_list(text):
    #text = re.sub('[，,]','、',text)
    #text = re.sub('[．.]','。',text)
    sentence_list = re.split('。|\n', text)
    while '' in sentence_list:
        sentence_list.remove('')
    return sentence_list

#テキストにおける文の長さに関する情報を出力する
def show_len_str_dist(len_str_array):
    print('長さの平均', len_str_array.mean())
    print('長さの分散', len_str_array.var())
    print('長さの標準偏差', len_str_array.std())

    plt.rcParams['font.family'] = 'AppleGothic'
    plt.figure()
    plt.title('文字数')
    plt.xlabel('長さ')
    plt.ylabel('頻度')
    plt.hist(len_str_array, color='blue', bins=40)
    plt.show()

#テキストを単語にする
def text2word_list(text):
    chasen_list = MeCab.Tagger("-Ochasen").parse(text).splitlines()
    word_list = []
    for chasen in chasen_list:
        cha_list = chasen.split("\t")
        if len(cha_list) >= 3:
            hinshi = cha_list[3].split('-')[0]
            if hinshi == "名詞" or  hinshi == "形容詞":
                #word_list.append(cha_list[0])#そのまま
                word_list.append(cha_list[2])#原型
    return word_list

#単語のリストから不要単語を除去する
def remove_symbol(word_list):
    new_word_list = []
    for word in word_list:
        word = re.sub('[，,]','、',word)
        word = re.sub('[．.]','。',word)
        len_ja = len(re.findall('[0-9a-zA-Zぁ-んァ-ヶ一-龥々ー、。]', word))
        #len_ja = len(re.findall('[a-zA-Zぁ-んァ-ヶ一-龥々ー、。]', word))   
        if len(word) != (len_ja):
            continue
        new_word_list.append(word)
    return new_word_list

#特徴語抽出
def extract_feature_words(terms, tfidfs, i, n):
    tfidf_array = tfidfs[i]
    top_n_idx = tfidf_array.argsort()[-n:][::-1]
    words = [terms[idx] for idx in top_n_idx]
    return words
                                        
if __name__ == '__main__':

    text_list = []
    for num in range(5,10):
        with open("data/abe201"+str(num)+".txt","r") as fread:
            text_list.append(fread.readlines())
            
    #単語の分析
    for i, text in enumerate(text_list):
        text = remove_space("".join(text))###テキストの変なスペースをなくす
        word_list = text2word_list(text)###単語のリストに変換
        word_list = remove_symbol(word_list)###記号除去
        text_list[i] = " ".join(word_list)###空白で結合
        
    vectorizer = TfidfVectorizer(use_idf=True, token_pattern=u'(?u)\\b\\w+\\b')
    features = vectorizer.fit_transform(np.array(text_list))
    terms = vectorizer.get_feature_names()
    tfidfs = features.toarray()
    
    zip_list = []
    for i in range(5):
        zip_list.append(extract_feature_words(terms, tfidfs, i, 50))

    pd.set_option('display.unicode.east_asian_width', True)
    print(pd.DataFrame(zip_list).T)
    

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

    plt.rcParams['font.family'] = 'IPAexGothic'
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
            #if hinshi == "名詞":# or hinshi == "動詞":
                #word_list.append(cha_list[0])#そのまま
            word_list.append(cha_list[2])#原型
    return word_list

#単語のリストから不要単語を除去する
def remove_symbol(word_list):
    new_word_list = []
    for word in word_list:
        word = re.sub('[，,]','、',word)
        word = re.sub('[．.]','。',word)
        #len_ja = len(re.findall('[0-9a-zA-Zぁ-んァ-ヶ一-龥々ー、。]', word))
        len_ja = len(re.findall('[a-zA-Zぁ-んァ-ヶ一-龥々ー、。]', word))   
        if len(word) != (len_ja):
            continue
        new_word_list.append(word)
    return new_word_list

if __name__ == '__main__':

    with open("data/abe2019.txt","r") as fread:
        text_list = fread.readlines()#[10:15]

    df = pd.read_csv('./data/sentimental_dict.csv')
    sentiment_dict = {}
    for word, value in zip(list(df['kanji']),list(df['value'])):
        if value >= 0.3 or value <= -0.3: 
            sentiment_dict[word] = value

    text = "".join(text_list)
    text = remove_space(text)

    #文の分析
    sentence_list = text2sentence_list(text)
    score_list = [0] * len(sentence_list)
    for i, sentence in enumerate(sentence_list):
        word_list = text2word_list(sentence)
        word_list = remove_symbol(word_list)
        for word in word_list:
            if word in sentiment_dict:
                score_list[i] += sentiment_dict[word]
    for sentence, value in zip(sentence_list, score_list):
        print(sentence, value)

            

#-*-coding:utf-8-*-

import pandas as pd
import MeCab

#感情辞書を作る
word2pn = {}

#乾研感情辞書(同士)
with open('./sentiment_dict/wago.121808.pn.txt', 'r') as f:
    sentiment_word_list = [s.strip() for s in f.readlines()]
for sent_word in sentiment_word_list:
    try:
        pn, word = sent_word.split('\t')
    except ValueError:
        continue

    if " " in sent_word:
        continue

    if pn.split('（')[0] == 'ポジ':
        pn = 1
    else:
        pn = -1

    word2pn[word] = pn

#乾研感情辞書(名詞)
df = pd.read_table('./sentiment_dict/pn.csv.m3.120408.trim', names=["word","pn","detail"])
for w, pn in zip(list(df['word']), list(df['pn'])):
    if pn == 'p':
        pn = 1
    elif pn == 'n':
        pn = -1
    else:
        continue    
    word2pn[w] = pn

#奥村研感情辞書
df = pd.read_csv('./sentiment_dict/okumura_dict.csv')
for w, pn in zip(list(df['kanji']),list(df['value'])):
    if -0.8 < pn < 0.8:
        continue
    if w in word2pn:
        continue
    if pn <= -0.8:
        pn = -1
    if 0.8 <= pn:
        pn = 1
    word2pn[w] = pn
for w, pn in zip(list(df['hira']),list(df['value'])):
    if -0.8 < pn < 0.8:
        continue
    if w in word2pn:
        continue
    if pn <= -0.8:
        pn = -1
    if 0.8 <= pn:
        pn = 1
    word2pn[w] = pn

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
df = pd.read_csv('./data/app_review.csv')

text_list = []
for text in list(df['content']):
    text_list.append(text)

#感情付与
text_sentiment_list = []
for text in text_list:
    word_list = text2word_list(text)

    senti = 0
    count = 0
    for word in word_list:
        if word in word2pn:
            senti += word2pn[word]
            count += 1

    ave_senti = 0
    if count != 0:
        ave_senti = senti / count

    text_sentiment_list.append((text, round(ave_senti, 1)))
[print(s,'\t',t) for t,s in text_sentiment_list]

#辞書の単語数
p = 0
n = 0
for w,pn in word2pn.items():
    if pn == 1:
        p += 1
    elif pn == -1:
        n += 1
print(p,n)

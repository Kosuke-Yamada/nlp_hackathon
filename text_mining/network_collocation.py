#-*-coding:utf-8-*- 
import sys
import re
import MeCab
from collections import Counter
import numpy as np
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
            if hinshi == "名詞":# or hinshi == "動詞":
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

#nグラムを作成する．flag_lastをyesにすることで文末表現のみに出来る．
def make_ngram(word_list,n,flag_last):
    new_word_list = []
    for i in range(len(word_list[:1-n])):
        new_word = ""
        for j in range(n):
            new_word += word_list[i+j-1]
        flag_pass = 0
        if flag_last == "yes":
            if new_word[-1] not in re.findall('[、。]', new_word):
                flag_pass = 1
        for j in range(len(new_word)-1):
            if len(re.findall('[、。]', new_word[j])) == 1 and len(re.findall('[、。]', new_word[j+1])) == 1:
                flag_pass = 1
                break
        if flag_pass == 1:
            continue
        new_word_list.append(new_word)
    return new_word_list

#単語の共起ネットワークを表示する．
def make_collocation_network(sentence_list, num_word, min_edge):
    
    sentence_words_list = []
    for sentence in sentence_list:
        word_list = text2word_list(sentence)
        word_list = remove_symbol(word_list)
        sentence_words_list.append(word_list)

    word_count_list = Counter(itertools.chain.from_iterable(sentence_words_list)).most_common(num_word)
    used_word_dict = {w:c for w,c in word_count_list}

    word_edges = []
    for sentence_words in sentence_words_list:
        for word0, word1 in itertools.combinations(sentence_words, 2):
            if word0 not in list(used_word_dict):
                continue
            if word1 not in list(used_word_dict):
                continue
            if word0 == word1:
                continue
            word_edges.append((word0, word1))
    word_edges_count_dict = Counter(word_edges)
    
    g = nx.Graph()
    vertices_list = []
    for (node0, node1), count in word_edges_count_dict.items():
        if count < min_edge:
            continue
        g.add_edge(node0, node1, weight=count)
        vertices_list.append(node0)
        vertices_list.append(node1)
    vertices_list = list(set(vertices_list))
    #g.add_nodes_from([(w, {"count":c}) for w,c in used_word_dict.items() if w in vertices_list]) 

    return g

#共起ネットワークの値を出力
def show_stats_net(g):
    print('頂点の数', len(g.nodes))
    print('辺の数', len(g.edges))

    #次元数
    deg_list = [(w, i, d) for i,(w,d) in enumerate(sorted(g.degree(), key=lambda x: -x[1]))]
    #中心性
    deg_cen_list = [(w, i, round(c,2)) for i,(w,c) in enumerate(sorted(nx.degree_centrality(g).items(), key=lambda x: -x[1]))]                    
    clo_cen_list = [(w, i, round(c,2)) for i,(w,c) in enumerate(sorted(nx.closeness_centrality(g).items(), key=lambda x: -x[1]))]
    bet_cen_list = [(w, i, round(c,2)) for i,(w,c) in enumerate(sorted(nx.betweenness_centrality(g).items(), key=lambda x: -x[1]))]
    eig_cen_list = [(w, i, round(c,2)) for i,(w,c) in enumerate(sorted(nx.eigenvector_centrality_numpy(g).items(), key=lambda x: -x[1]))]
    pg_list = [(w, i, round(c,2)) for i,(w,c) in enumerate(sorted(nx.pagerank(g).items(), key=lambda x: -x[1]))]

    print('次元中心性','\t\t','近接中心性','\t\t','媒介中心性','\t\t','固有ベクトル中心性','\t','ページランク')
    for c1, c2, c3, c4, c5 in zip(deg_cen_list, clo_cen_list, bet_cen_list, eig_cen_list, pg_list):
        print(c1,'\t',c2,'\t',c3,'\t',c4,'\t',c5)
                                        
if __name__ == '__main__':

    with open("data/abe2019.txt","r") as fread:
        text_list = fread.readlines()#[10:15]

    text = "".join(text_list)
    text = remove_space(text)

    #文の分析
    sentence_list = text2sentence_list(text)
    #len_sentence_array = np.array([len(v) for v in sentence_list])
    #show_len_str_dist(len_sentence_array)
    #cnt_dict = Counter(len(x) for x in sentence_list)
    #print(cnt_dict)

    #共起ネットワークの作成
    g = make_collocation_network(sentence_list, 500,3)
    #a = nx.nx_agraph.to_agraph(g)
    #a.node_attr['color'] = 'blue'
    #a.edge_attr['color'] = 'red'
    #a.layout()
    #a.draw('a.png')

    nx.nx_agraph.view_pygraphviz(g, prog='fdp')
    #show_stats_net(g)
    
    #単語の分析
    #word_list = text2word_list(text)
    #word_list = remove_symbol(word_list)
    #word_list = make_ngram(word_list,3,"no")
    #print(Counter(word_list))
    

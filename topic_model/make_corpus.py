#-*-coding:utf-8-*-
import sys
import re
import MeCab
import codecs as cd
import gensim
from gensim import corpora, models, similarities
import neologdn

#テキストから空白文字を除去する
def remove_space(text):
    text = re.sub(' ','',text)
    text = re.sub('\u3000','',text)
    text = re.sub('\n','',text)
    text = re.sub('\t','',text)
    text = re.sub('\r','',text)
    return text

#テキストを単語にする
def text2word_list(text):
    text = neologdn.normalize(text)#####
    chasen_list = MeCab.Tagger("-Ochasen").parse(text).splitlines()
    word_list = []
    for chasen in chasen_list:
        cha_list = chasen.split("\t")
        if len(cha_list) >= 3:
            hinshi = cha_list[3].split('-')[0]
            if hinshi == "名詞" or hinshi == "動詞":
                word_list.append(cha_list[2])#原型
    return word_list

#単語のリストから不要単語を除去する
def remove_symbol(word_list):
    new_word_list = []
    for word in word_list:
        word = re.sub('[，,]','、',word)
        word = re.sub('[．.]','。',word)
        #len_ja = len(re.findall('[a-zA-Zぁ-んァ-ヶ一-龥々ー、。]', word))
        len_ja = len(re.findall('[ぁ-んァ-ヶ一-龥々ー]', word))
        if len(word) != (len_ja):
            continue
        new_word_list.append(word)
    return new_word_list

if __name__ == '__main__':

    file_name = './data/summarize.txt'
    file = cd.open(file_name, 'r', 'utf-8')
    lines = file.readlines()

    all_word_list = []
    for i, line in enumerate(lines):
        print(i,len(line))
        line = remove_space(line)
        word_list = text2word_list(line)
        word_list = remove_symbol(word_list)

        # データを連結
        all_word_list += [word_list]

    # 辞書作成
    dictionary = corpora.Dictionary(all_word_list)
    dictionary.filter_extremes(no_below=10, no_above=0.3)
    dictionary.save_as_text('./data/summarize_dict.txt')
    
    # コーパスを作成
    corpus = [dictionary.doc2bow(text) for text in all_word_list]
    corpora.MmCorpus.serialize('./data/summarize_cop.mm', corpus)

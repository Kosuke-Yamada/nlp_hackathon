import gensim
from janome.tokenizer import Tokenizer
from gensim import corpora, models, similarities

dictionary = gensim.corpora.Dictionary.load_from_text('./data/summarize_dict.txt')
corpus = corpora.MmCorpus('./data/summarize_cop.mm')

topic_N = 10
lda = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=topic_N, id2word=dictionary)

#for i in range(topic_N):
#        print('TOPIC:', i, '__', lda.print_topic(i))

for i in range(topic_N):
    print("\n")
    print("="*80)
    print("TOPIC {0}\n".format(i))
    topic = lda.show_topic(i)
    for t in topic:
        print("{0:20s}{1}".format(t[0], t[1]))


topic_label = [
    "人生",
    "地名",
    "男",
    "フォロー",
    "動画",
    "戦い",
    "ブログ",
    "温度",
    "イベント",
    "映画"
]

target_record = 0 # 分析対象のドキュメントインデックス

print("\n\n")
for topics_per_document in lda[corpus[target_record]]:
   print("{0:30s}{1}".format(topic_label[topics_per_document[0]], topics_per_document[1]))

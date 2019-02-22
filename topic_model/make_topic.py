import gensim
from janome.tokenizer import Tokenizer
from gensim import corpora, models, similarities

dictionary = gensim.corpora.Dictionary.load_from_text('./data/summarize_dict.txt')
corpus = corpora.MmCorpus('./data/summarize_cop.mm')

topic_N = 5
lda = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=topic_N, id2word=dictionary)

for i in range(topic_N):
        print('TOPIC:', i, '__', lda.print_topic(i))

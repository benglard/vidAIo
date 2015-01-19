from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel
from app.lib.nlp.stop_words import ENGLISH_STOP_WORDS as stop_words
from nltk import RegexpTokenizer

"""Online latent dirichlet allocation for topic modeling"""

def topic_list(text):
    print 'Topic modeling...'

    tokenizer = RegexpTokenizer('\w+')
    document = []
    for token in tokenizer.tokenize(text):
        word = token.lower()
        if word not in stop_words:
            document.append(word)
    documents = [document]

    dic = Dictionary(documents)
    corpus = [ dic.doc2bow(doc) for doc in documents ]

    lda = LdaModel(corpus, num_topics=5)

    topics = [
        dic[int(id)]
        for topic in lda.show_topics(formatted=False)
        for prob, id in topic
    ][:5]

    print topics
    return topics
from numpy import dot
from numpy.linalg import norm
from nltk import RegexpTokenizer
from app.lib.nlp.stop_words import ENGLISH_STOP_WORDS as stop_words

def preprocess(documents):
    tokenizer = RegexpTokenizer('\w+')
    processed = []
    for doc in documents:
        string = ' '.join(
            token.lower()
            for token in tokenizer.tokenize(doc)
            if token.lower() not in stop_words
        )
        processed.append(string)
    return processed
            
def get_unique_words(documents):
    unique = set()
    for doc in documents:
        for word in doc.split(' '):
            unique.add(word)
    return list(unique)

def cos(v1, v2):
    return dot(v1, v2) / (norm(v1) * norm(v2))
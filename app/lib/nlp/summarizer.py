from app.lib.nlp.lexrank import LexRank
from nltk import sent_tokenize

def summarize(text):
    print 'Summarizing...'

    docs = sent_tokenize(text)
    eig = sorted(enumerate(LexRank(docs).pagerank()), reverse=True)
    
    if len(docs) < 5:
        summary = ' '.join(docs)
    else:
        summary = ' '.join(docs[idx] for idx, val in eig[:5])

    print summary
    return summary
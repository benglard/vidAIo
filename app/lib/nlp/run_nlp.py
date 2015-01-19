from app.lib.nlp.get_transcript import *
from app.lib.nlp.graph import *
from app.lib.nlp.ner import *
from app.lib.nlp.topics import *
from app.lib.nlp.summarizer import *
from nltk import sent_tokenize

def get_time_item(text, item):
    sentences = sent_tokenize(text)
    for i, sent in enumerate(sentences):
        if item in sent.split(' '):
            return i * 5
    return 5 * len(sentences)

def nlp(filename):
    text = get_transcript(filename)        # use google speech api to get transcript

    if text:
        keywords = TextGraph(text).keywords()  # get keywords
        ner = named_entities(text)             # get named entities
        topics = topic_list(text)              # get topics
        summary = summarize(text)              # generate summary

    return {
        'transcript': text,
        'keywords': [ 
            {'word': word, 'time': get_time_item(text, word)}
            for word in keywords 
        ],
        'ner': [ 
            {'word': word, 'time': get_time_item(text, word)}
            for word in ner 
        ],
        'topics': [ 
            {'word': word, 'time': get_time_item(text, word)}
            for word in topics 
        ],
        'summary': summary
    }


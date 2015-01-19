import nltk

"""Extract named entities"""
     
def extract_entity_names(t):
    entity_names = []
    
    if hasattr(t, 'node') and t.node:
        if t.node == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))
                
    return entity_names

def named_entities(text):
    print 'Extracting named entities...'

    sentences = nltk.sent_tokenize(text)
    tokenized_sentences = [ nltk.word_tokenize(sentence) for sentence in sentences ]
    tagged_sentences = [ nltk.pos_tag(sentence) for sentence in tokenized_sentences ]
    chunked_sentences = nltk.batch_ne_chunk(tagged_sentences, binary=True)

    entity_names = []
    for tree in chunked_sentences:    
        entity_names.extend(extract_entity_names(tree))
     
    results = set(entity_names)
    print results
    return results
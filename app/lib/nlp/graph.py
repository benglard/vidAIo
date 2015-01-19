from collections import defaultdict
from nltk import RegexpTokenizer
from random import sample
from app.lib.nlp.stop_words import ENGLISH_STOP_WORDS as stop_words

class Node(object):
    
    """Class for representing nodes in the text graph."""
 
    def __init__(self, node_id):
        self.node_id = node_id
        self.edges = defaultdict(lambda: 0)
 
    def __str__(self):
        return '{} {}'.format(self.node_id, self.edges)
 
    __repr__ = __str__
 
    def add_edge(self, node_id):
        self.edges[node_id] += 1
 
    def edge_weight(self, node_id):
        return self.edges[node_id]
 
    @property
    def degree(self):
        return len(self.edges)
 
class TextGraph(object):
    
    """
    A graph can be built up from a piece of text if distinct words
    are considered to be the nodes of the graph, and two nodes n1 and n2 
    are adjacent in the graph if word n2 appears directly after word n1. 
    Since the same word may appear after another word more than a 
    single time in a piece of text, this becomes a weighted graph, with 
    the weights equaling the number of times n2 appears after n1.
    """
 
    def __init__(self, text):
        print 'Extracting keywords...'

        self.text = text
        self.graph = defaultdict(lambda: 0)
        self.tokenizer = RegexpTokenizer('\w+')
        self.make_graph()
 
    def make_graph(self):
        last_word = ''
        for word in self.tokenizer.tokenize(self.text):
            word = word.lower()

            if word in stop_words:
                continue

            if word not in self.graph:
                self.graph[word] = Node(word)
            if last_word != '':
                self.graph[last_word].add_edge(self.graph[word].node_id)
            last_word = word
  
    def keywords(self):
        """Random walk based keyword extraction"""
        
        keys = defaultdict(lambda: 0)
        steps = len(self.graph)
        current = None
        for n in xrange(steps):
            if current is None:
                current = sample(self.graph, 1)[0]
            else:
                edges = self.graph.get(current).edges
                if len(edges) >= 1:
                    current = sample(edges, 1)[0]
                else:
                    current = sample(self.graph, 1)[0]
 
            keys[current] += 1
        results = list(sorted(keys, key=keys.get, reverse=True))[:5]
        print results
        return results
from app.lib.nlp.tfidf import TFIDF
from numpy import *
from utilities import cos

class LexRank(object):

    """
    LexRank takes a tfidf matrix as input, computes the 
    cos similarities between all sentences and then 
    applies pagerank to the matrix.

    Like Google ranking webpages, we can use this to 
    rank the importance of sentences, and can thus use
    LexRank for summarization.
    """ 

    def __init__(self, documents):
        self.documents = documents
        self.N = len(self.documents)
        self.tfidf = TFIDF(self.documents)
        self.make_matrix()

    def make_matrix(self):
        self.matrix = zeros((self.N, self.N)
        for i in xrange(self.N):
            for j in xrange(self.N):
                self.matrix[i, j] = self.matrix[j, i] = cos(
                    self.tfidf.matrix[i], self.tfidf.matrix[j]
                )

    def pagerank(self, d=0.85, epsilon=0.0001):
        v = ones(self.N) / self.N
        last_v = ones(self.N) * inf
        M_hat = (d * self.matrix) + ((1 - d) / self.N) * ones((self.N, self.N))
        while linalg.norm(v - last_v) > epsilon:
            last_v = v
            v = dot(M_hat, v)
        return v
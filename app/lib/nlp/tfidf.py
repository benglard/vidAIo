from utilities  import *
from numpy import zeros, log

class TFIDF(object):

    """
    Creates a matrix representation of text where the
    rows -> documents / columns -> words and a row/col
    entry equals the term frequency of the word of that
    col in the doc of that row multiplied by the inverse
    document frequency, given by log(#docs/#docs with that word)
    """

    def __init__(self, documents):
        self.documents = preprocess(documents)
        self.make_matrix()

    def make_matrix(self):
        self.words = get_unique_words(self.documents)
        self.num_docs = len(self.documents)
        self.num_words = len(self.words)

        self.matrix = zeros((self.num_docs, self.num_words))
        for d in xrange(self.num_docs):
            self.matrix[d, :] = self.make_vector(self.documents[d])

        self.transform()

    def make_vector(self, document):
        vector = zeros(self.num_words)
        for word in document.split(' '):
            try: vector[self.words.index(word)] += 1
            except ValueError: continue
        return vector   

    def transform(self):
        for col in xrange(self.num_words):
            count = float(self.matrix.sum(axis=0)[col])
            idf = log(self.num_words / count)
            self.matrix[:, col] *= idf

    def query(self, search, sort=False):
        vector = self.make_vector(preprocess([search])[0])
        sims = [ cos(vector, row) for row in self.matrix ]
        if sort:
            return sorted(enumerate(sims), key=lambda x: x[1], reverse=True)
        else:
            return sims
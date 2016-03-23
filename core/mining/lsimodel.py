from gensim import corpora, models, similarities


class LSImodel(object):
    def __init__(self):
        self.names = []
        self.texts = []
        self.corpus = []

        self.lsi = None
        self.index = None
        self.tfidf = None
        self.dictionary = None
        self.corpus_tfidf = None

    def setup(self, names, texts):
        self.names = names
        self.texts = texts
        self.silencer(2, 100)
        self.set_dictionary()
        self.set_corpus()
        self.set_tfidf()
        self.set_lsimodel()

    def set_dictionary(self):
        self.dictionary = corpora.Dictionary(self.texts)
        
    def set_corpus(self):
        for text in self.texts:
            self.corpus.append(self.dictionary.doc2bow(text))

    def set_tfidf(self):
        self.tfidf = models.TfidfModel(self.corpus)
        self.corpus_tfidf = self.tfidf[self.corpus]

    def set_lsimodel(self, topics=100):
        self.lsi = models.LsiModel(self.corpus_tfidf, id2word=self.dictionary, num_topics=topics)
        self.index = similarities.MatrixSimilarity(self.lsi[self.corpus])

    def silencer(self, minimum, maximum):
        count_dict = {}
        for text in self.texts:
            for word in text:
                if word not in count_dict:
                    count_dict[word] = 1
                else:
                    count_dict[word] += 1

        token_once = {}
        for word in count_dict:
            if count_dict[word] < minimum or count_dict[word] > maximum:
                token_once[word] = count_dict[word]
        self.texts = [[word for word in text if word not in token_once] for text in self.texts]

    def probability(self, doc):
        vec_bow = self.dictionary.doc2bow(jieba.cut(doc, cut_all=False))
        vec_lsi = self.lsi[vec_bow]
        sims = sorted(enumerate(self.index[vec_lsi]), key=lambda item: -item[1])
        return sims

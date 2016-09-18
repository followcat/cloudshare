import os
import ujson

from gensim import corpora, models

import core.outputstorage


class LSImodel(object):

    names_save_name = 'lsi.names'
    model_save_name = 'lsi.model'
    corpu_dict_save_name = 'lsi.dict'
    corpus_save_name = 'lsi.corpus'
    texts_save_name = 'lsi.texts'
    most_save_name = 'lsi.most'

    def __init__(self, savepath, no_above=1./8, topics=100, slicer=None):
        self.path = savepath
        self.topics = topics
        self.no_above = no_above
        if slicer:
            self.slicer = slicer
        else:
            self.slicer = lambda x:x.split('\n')
        self.names = []
        self._texts = []
        self._corpus = []

        self.lsi = None
        self.tfidf = None
        self.dictionary = None
        self.corpus_tfidf = None

    def update(self, svccv_list):
        added = False
        for svc_cv in svccv_list:
            for name in svc_cv.names():
                if name not in self.names:
                    doc = svc_cv.getmd(name)
                    self.add(name, doc)
                    added = True
        if added:
            self.save()
        return added

    def build(self, svccv_list):
        names = []
        texts = []
        for svc_cv in svccv_list:
            for data in svc_cv.datas():
                name, doc = data
                names.append(name)
                texts.append(doc)
        if len(names) > 10:
            self.setup(names, texts)
            return True
        return False

    def setup(self, names, texts):
        self.names = names
        self.texts = self.slicer(texts)
        self.set_dictionary()
        self.set_corpus()
        self.set_tfidf()
        self.set_lsimodel()

    def save(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        with open(os.path.join(self.path, self.names_save_name), 'w') as f:
            ujson.dump(self.names, f)
        with open(os.path.join(self.path, self.corpus_save_name), 'w') as f:
            ujson.dump(self.corpus, f)
        with open(os.path.join(self.path, self.texts_save_name), 'w') as f:
            ujson.dump(self.texts, f)
        self.lsi.save(os.path.join(self.path, self.model_save_name))
        self.dictionary.save(os.path.join(self.path, self.corpu_dict_save_name))

    def load(self):
        with open(os.path.join(self.path, self.names_save_name), 'r') as f:
            self.names = ujson.load(f)
        self.lsi = models.LsiModel.load(os.path.join(self.path, self.model_save_name))
        self.dictionary = corpora.dictionary.Dictionary.load(os.path.join(self.path,
                                                             self.corpu_dict_save_name))

    def add(self, name, document):
        text = self.slicer(document)
        self.names.append(name)
        self.texts.append(text)
        if self.dictionary is None:
            self.set_dictionary()
        corpu = self.dictionary.doc2bow(text)
        self.corpus.append(corpu)
        tfidf = models.TfidfModel(self.corpus)
        corpu_tfidf = tfidf[[corpu]]
        if self.lsi is None:
            self.lsi = models.LsiModel(corpu_tfidf, id2word=self.dictionary,
                            num_topics=self.topics, power_iters=6, extra_samples=300)
        else:
            self.lsi.add_documents(corpu_tfidf)

    def set_dictionary(self):
        self.dictionary = corpora.Dictionary(self.texts)
        self.dictionary.filter_extremes(no_below=int(len(self.names)*0.005),
                                        no_above=self.no_above)

    def set_corpus(self):
        for text in self.texts:
            self.corpus.append(self.dictionary.doc2bow(text))

    def set_tfidf(self):
        self.tfidf = models.TfidfModel(self.corpus)
        self.corpus_tfidf = self.tfidf[self.corpus]

    def set_lsimodel(self):
        self.lsi = models.LsiModel(self.corpus_tfidf, id2word=self.dictionary,
                                   num_topics=self.topics, power_iters=6, extra_samples=300)

    def probability(self, doc):
        texts = self.slicer(doc)
        vec_bow = self.dictionary.doc2bow(texts)
        vec_lsi = self.lsi[vec_bow]
        return vec_lsi

    @property
    def corpus(self):
        corpus_path = os.path.join(self.path, self.corpus_save_name)
        if os.path.exists(corpus_path) and not self._corpus:
            with open(corpus_path, 'r') as f:
                try:
                    self._corpus = ujson.load(f)
                except ValueError:
                    self._corpus = []
        return self._corpus

    @corpus.setter
    def corpus(self, value):
        self._corpus = value

    @property
    def texts(self):
        texts_path = os.path.join(self.path, self.texts_save_name)
        if os.path.exists(texts_path) and not self._texts:
            with open(texts_path, 'r') as f:
                try:
                    self._texts = ujson.load(f)
                except ValueError:
                    self._texts = []
        return self._texts

    @texts.setter
    def texts(self, value):
        self._texts = value

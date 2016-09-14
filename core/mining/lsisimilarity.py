import os
import ujson

from gensim import similarities


class LSIsimilarity(object):

    names_save_name = 'lsi.names'
    matrix_save_name = 'lsi.matrix'
    corpus_save_name = 'lsi.corpus'

    def __init__(self, savepath, lsi_model):
        self.path = savepath
        self.names = []
        self._corpus = []

        self.lsi_model = lsi_model
        self.index = None

    def update(self, svccv_list):
        added = False
        for svc_cv in svccv_list:
            for name in svc_cv.names():
                if name not in self.names:
                    doc = svc_cv.getmd(name)
                    self.add(name, doc)
                    added = True
        self.set_index()
        return added

    def build(self, svccv_list):
        names = []
        texts = []
        for svc_cv in svccv_list:
            for data in svc_cv.datas():
                name, doc = data
                names.append(name)
                texts.append(doc)
        if len(names) > 0:
            self.setup(names, texts)
            return True
        return False

    def setup(self, names, texts):
        self.names = names
        self.set_corpus(texts)
        self.set_index()

    def save(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        with open(os.path.join(self.path, self.names_save_name), 'w') as f:
            ujson.dump(self.names, f)
        with open(os.path.join(self.path, self.corpus_save_name), 'w') as f:
            ujson.dump(self.corpus, f)
        self.index.save(os.path.join(self.path, self.matrix_save_name))

    def load(self):
        with open(os.path.join(self.path, self.names_save_name), 'r') as f:
            self.names = ujson.load(f)
        self.index = similarities.Similarity.load(os.path.join(self.path,
                                                        self.matrix_save_name))

    def add(self, name, document):
        assert(self.lsi_model.dictionary)
        text = self.lsi_model.slicer(document)
        self.names.append(name)
        corpu = self.lsi_model.dictionary.doc2bow(text)
        self.corpus.append(corpu)

    def set_corpus(self, texts):
        for text in self.lsi_model.slicer(texts):
            self.corpus.append(self.lsi_model.dictionary.doc2bow(text))

    def set_index(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.index = similarities.Similarity(os.path.join(self.path, "similarity"),
                                             self.lsi_model.lsi[self.corpus], self.lsi_model.topics)

    def probability(self, doc):
        results = []
        vec_lsi = self.lsi_model.probability(doc)
        if self.index is not None:
            sims = sorted(enumerate(abs(self.index[vec_lsi])), key=lambda item: item[1], reverse=True)
            results = map(lambda x: (os.path.splitext(self.names[x[0]])[0], str(x[1])), sims)
        return results

    def probability_by_id(self, doc, id):
        if id not in self.names:
            return None
        index = self.names.index(id)
        vec_lsi = self.lsi_model.probability(doc)
        result = abs(self.index[vec_lsi][index])
        return (id, str(result))

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

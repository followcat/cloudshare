import os
import pickle

import utils.cutword
from gensim import similarities


class LSIsimilarity(object):

    names_save_name = 'lsi.names'
    matrix_save_name = 'lsi.matrix'
    corpus_save_name = 'lsi.corpus'

    def __init__(self, savepath, lsi_model):
        self.corpus = []
        self.path = savepath
        self.names = []
        self.corpus = []

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
        corpus = []
        for svc_cv in svccv_list:
            for data in svc_cv.datas():
                name, doc = data
                names.append(name)
                words = utils.cutword.chs_lsisim(doc)
                corpus.append(self.lsi_model.dictionary.doc2bow(words))
        if len(names) > 0:
            self.setup(names, corpus)
            return True
        return False

    def setup(self, names, corpus):
        self.names = names
        self.set_corpus(corpus)
        self.set_index()

    def save(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        with open(os.path.join(self.path, self.names_save_name), 'w') as f:
            pickle.dump(self.names, f)
        with open(os.path.join(self.path, self.corpus_save_name), 'w') as f:
            pickle.dump(self.corpus, f)
        self.index.save(os.path.join(self.path, self.matrix_save_name))

    def load(self):
        with open(os.path.join(self.path, self.names_save_name), 'r') as f:
            self.names = pickle.load(f)
        with open(os.path.join(self.path, self.corpus_save_name), 'r') as f:
            self.corpus = pickle.load(f)
        self.index = similarities.Similarity.load(os.path.join(self.path,
                                                        self.matrix_save_name))

    def add(self, name, document):
        assert(self.lsi_model.dictionary)
        text = self.lsi_model.slicer(document)
        self.names.append(name)
        corpu = self.lsi_model.dictionary.doc2bow(text)
        self.corpus.append(corpu)

    def set_corpus(self, corpus):
        self.corpus = corpus

    def set_index(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.index = similarities.Similarity(os.path.join(self.path, "similarity"),
                                             self.lsi_model.lsi[self.corpus], self.lsi_model.topics)

    def probability(self, doc):
        results = []
        if self.index is None:
            return results
        vec_lsi = self.lsi_model.probability(doc)
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


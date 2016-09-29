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
        corpus = []
        for svc_cv in svccv_list:
            for data in svc_cv.datas():
                name, doc = data
                names.append(name)
                words = self.lsi_model.slicer(doc)
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
            ujson.dump(self.names, f)
        with open(os.path.join(self.path, self.corpus_save_name), 'w') as f:
            ujson.dump(self.corpus, f)
        self.index.save(os.path.join(self.path, self.matrix_save_name))
        self.clear()

    def clear(self):
        self.corpus = None

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

    def add_documents(self, names, documents):
        assert(self.lsi_model.dictionary)
        assert len(names) == len(documents)
        corpus = []
        for name, document in zip(names, documents):
            text = self.lsi_model.slicer(document)
            self.names.append(name)
            corpu = self.lsi_model.dictionary.doc2bow(text)
            corpus.append(corpu)
        self.set_index()

    def set_corpus(self, corpus):
        self.corpus = corpus

    def set_index(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.index = similarities.Similarity(os.path.join(self.path, "similarity"),
                                             self.lsi_model.lsi[self.corpus], self.lsi_model.topics)

    def probability(self, doc):
        """
            >>> from tests.test_model import *
            >>> from webapp.settings import *
            >>> jd_service = SVC_PRJ_MED.jobdescription
            >>> sim = SVC_MIN.sim['medical']['medical']
            >>> (PERFECT, GOOD, MEDIUM, POOR)
            (100, 50, 25, 0)
            >>> assert kgr_percentage('9bbc45a81e4511e6b7066c3be51cefca', jd_service, sim, percentage=PERFECT)
            >>> assert kgr_percentage('cb3a4d820ab011e691ce6c3be51cefca', jd_service, sim, percentage=PERFECT)
            >>> assert kgr_percentage('f12cd9fc1b3011e6a5286c3be51cefca', jd_service, sim, percentage=PERFECT)
            >>> assert kgr_percentage('d09227ca0b5d11e6b01c6c3be51cefca', jd_service, sim, percentage=PERFECT)
            >>> assert kgr_percentage('4a9f2d9c0b4f11e6877a6c3be51cefca', jd_service, sim, percentage=PERFECT)
            >>> assert kgr_percentage('7cadbda40b5d11e699956c3be51cefca', jd_service, sim, percentage=PERFECT)
            >>> assert kgr_percentage('d10df4940b4f11e69d676c3be51cefca', jd_service, sim, percentage=PERFECT)
            >>> assert kgr_percentage('046ad1040b5511e6bd4d6c3be51cefca', jd_service, sim, percentage=PERFECT)
            >>> assert kgr_percentage('542330f40d0011e69e136c3be51cefca', jd_service, sim, percentage=PERFECT)
            >>> assert kgr_percentage('d652742841a211e68dc34ccc6a30cd76', jd_service, sim, percentage=PERFECT)
            >>> assert kgr_percentage('098a91ca0b4f11e6abf46c3be51cefca', jd_service, sim, percentage=66)
            >>> assert kgr_percentage('9b48f97653e811e6af534ccc6a30cd76', jd_service, sim, percentage=GOOD)
            >>> assert kgr_percentage('e9f415f653e811e6945a4ccc6a30cd76', jd_service, sim, percentage=GOOD)
            >>> assert kgr_percentage('be97722a0cff11e6a3e16c3be51cefca', jd_service, sim, percentage=MEDIUM)
            >>> assert kgr_percentage('e290dd36428a11e6b2934ccc6a30cd76', jd_service, sim, percentage=33)
            >>> assert kgr_percentage('80ce049a320711e6ac1f4ccc6a30cd76', jd_service, sim, percentage=MEDIUM)
            >>> assert kgr_percentage('b73ac9621cd811e694e76c3be51cefca', jd_service, sim, percentage=POOR)
            >>> assert kgr_percentage('48dc231c0b5d11e6b89e6c3be51cefca', jd_service, sim, percentage=POOR)
            >>> assert kgr_percentage('e3bd422a2d6411e6b5296c3be51cefca', jd_service, sim, percentage=POOR)
            >>> assert kgr_percentage('437958560b5b11e6aaa86c3be51cefca', jd_service, sim, percentage=POOR)
            >>> assert kgr_percentage('a9a20a84473211e6a6934ccc6a30cd76', jd_service, sim, percentage=POOR)
            >>> assert kgr_percentage('fb2ac1c80b4d11e6adce6c3be51cefca', jd_service, sim, percentage=POOR)
            >>> assert kgr_percentage('048b4bc60d0011e6be436c3be51cefca', jd_service, sim, percentage=POOR)
            >>> assert kgr_percentage('06fdc0680b5d11e6ae596c3be51cefca', jd_service, sim, percentage=POOR)
            >>> assert kgr_percentage('57317f820cfe11e681466c3be51cefca', jd_service, sim, percentage=POOR)
            >>> assert kgr_percentage('684605740b4e11e6ba746c3be51cefca', jd_service, sim, percentage=POOR)
            >>> assert kgr_percentage('763199560a9411e6a7936c3be51cefca', jd_service, sim, percentage=POOR)
            >>> assert kgr_percentage('8c43b5343c4511e680994ccc6a30cd76', jd_service, sim, percentage=POOR)

        HHMT new:
            >>> assert kgr_percentage('2fe1c53a231b11e6b7096c3be51cefca', jd_service, sim, cvs=['3hffapdz', '2x5wx4aa'], percentage=POOR)
            >>> assert kgr_percentage('06fdc0680b5d11e6ae596c3be51cefca', jd_service, sim, cvs=['2hw11q81', '8z3fxnr7', 'ltpyt2hp'], percentage=POOR)
            >>> assert kgr_percentage('2898a70a3f6111e6b68d4ccc6a30cd76', jd_service, sim, cvs=['mjm6vl3k'], percentage=POOR)
            >>> assert kgr_percentage('437958560b5b11e6aaa86c3be51cefca', jd_service, sim, cvs=['hy24julz'], percentage=POOR)
            >>> assert kgr_percentage('48dc231c0b5d11e6b89e6c3be51cefca', jd_service, sim, cvs=['ohapy8ge'], percentage=POOR)
            >>> assert kgr_percentage('7858d9aa636411e6815f4ccc6a30cd76', jd_service, sim, cvs=['o3fjv894', '59c102os', '8y5nqhoc'], percentage=POOR)
            >>> assert kgr_percentage('6cadbda40b5d11e699956c3be51cefca', jd_service, sim, cvs=['dpaxyqns'], percentage=POOR)
            >>> assert kgr_percentage('7cadbda40b5d11e699956c3be51cefca', jd_service, sim, cvs=['uqototc6', 'fs60ntrm', 'wbrnwrob'], percentage=33)
            >>> assert kgr_percentage('def2a4120b5c11e691246c3be51cefca', jd_service, sim, cvs=['0p2unnwd', 'o0njv8te'], percentage=POOR)
            >>> assert kgr_percentage('9df8a1b20b4f11e686a56c3be51cefca', jd_service, sim, cvs=['rt9qa1gf', 'py6d1c0k'], percentage=POOR)
            >>> assert kgr_percentage('5c2a203a596011e6bb374ccc6a30cd76', jd_service, sim, cvs=['18utt3gq', 'k0hov59f'], percentage=GOOD)
            >>> assert kgr_percentage('542330f40d0011e69e136c3be51cefca', jd_service, sim, cvs=['nbdsjvzx'], percentage=PERFECT)
            >>> assert kgr_percentage('046ad1040b5511e6bd4d6c3be51cefca', jd_service, sim, cvs=['cfvpiab7', 'pc42qr9a'], percentage=GOOD)

        FKJY new:
            >>> assert kgr_percentage('07ea1a8018be11e684026c3be51cefca', jd_service, sim, cvs=['cn64i09t', 'fxetvyzc', 'kgmp7dpg', 'u5dh7ozn', 'xt7613fa'], percentage=int(float(2)/5*100))
            >>> assert kgr_percentage('2fe1c53a231b11e6b7096c3be51cefca', jd_service, sim, cvs=['3hffapdz', '2x5wx4aa'], percentage=POOR)
            >>> assert kgr_percentage('ae31247274c811e6b6b54ccc6a30cd76', jd_service, sim, cvs=['2sh48rjp'], percentage=POOR)
            >>> assert kgr_percentage('5b2f8548320611e6b4e84ccc6a30cd76', jd_service, sim, cvs=['cfimev64', 'ko5luqyi', '0x4zpslk'], percentage=int(float(1)/3*100))
            >>> assert kgr_percentage('78df9d86555f11e6abad4ccc6a30cd76', jd_service, sim, cvs=['5ziy6c80', '6y0a1a75', '80clrjqi', 'rlb3jau0', 'sbip7deq', 'uwbvmsod', '68oojytn'], percentage=int(float(1)/7*100))
            >>> assert kgr_percentage('80ce049a320711e6ac1f4ccc6a30cd76', jd_service, sim, cvs=['nvujsh0u'], percentage=POOR)
            >>> assert kgr_percentage('cce2a5be547311e6964f4ccc6a30cd76', jd_service, sim, cvs=['qfgwkkhg', 'nji2v4s7', 'qssipwf9'], percentage=POOR)
            >>> assert kgr_percentage('d33a669c313511e69edc4ccc6a30cd76', jd_service, sim, cvs=['csa46gdd', 'fahayhk8'], percentage=POOR)
        """
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

# -*- coding: utf-8 -*-
import os
import ujson

import core.outputstorage
from gensim import similarities


class LSIsimilarity(object):

    names_save_name = 'lsi.names'
    matrix_save_name = 'lsi.matrix'

    def __init__(self, name, savepath, lsi_model):
        self._namesindex = dict()
        self.name = name
        self.path = savepath
        self.names = []

        self.lsi_model = lsi_model
        self.index = None

    def update(self, gen, numbers=5000):
        result = False
        names = []
        documents = []
        number = 0
        if self.index is None:
            self.set_index([])
        for name, doc in gen:
            if self.exists(name) is True:
                continue
            names.append(name)
            documents.append(doc)
            number += 1
            if number%numbers == 0:
                self.add_documents(names, documents)
                result = True
                names = list()
                documents = list()
        if number%numbers != 0:
            self.add_documents(names, documents)
            result = True
        return result

    def build(self, gen, numbers=5000):
        return self.update(gen, numbers=numbers)

    def save(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        with open(os.path.join(self.path, self.names_save_name), 'w') as f:
            ujson.dump(self.names, f)
        self.index.save(os.path.join(self.path, self.matrix_save_name))

    def exists(self, id):
        return id in self.ids

    def load(self):
        with open(os.path.join(self.path, self.names_save_name), 'r') as f:
            self.names = ujson.load(f)
        self.index = similarities.Similarity.load(os.path.join(self.path,
                                                  self.matrix_save_name))

    def add_documents(self, ids, documents):
        assert(self.lsi_model.lsi.id2word)
        assert len(ids) == len(documents)
        names = list()
        corpus = list()
        for id, document in zip(ids, documents):
            if self.exists(id) is True:
                 continue
            text = self.lsi_model.slicer(document, id=id)
            corpu = self.lsi_model.lsi.id2word.doc2bow(text)
            names.append(id)
            corpus.append(corpu)
        if names and corpus:
            modelcorpus = self.lsi_model.lsi[corpus]
            self.index.add_documents(modelcorpus)
            self.names.extend(names)
            self.ids = self.names

    def set_index(self, modelcorpus):
        self.index = similarities.Similarity(os.path.join(self.path, "similarity"),
                                             modelcorpus, self.lsi_model.topics)

    def probability(self, doc, top=None, minimum=0):
        """
            >>> from tests.test_model import *
            >>> from webapp.settings import *
            >>> from tests.multi_models import *
            >>> import core.mining.lsimodel
            >>> jd_service = SVC_PRJ_MED.jobdescription
            >>> names = list(test_cv_svc.ids)
            >>> texts = [SVC_CV_REPO.getmd(n) for n in names]
            >>> path = 'tests/lsisim/model'
            >>> model = build_lsimodel(path, SVC_MIN.lsi_model['medical'].slicer, names, texts, no_above=1./3, extra_samples=300)
            >>> sim_path = 'tests/lsisim/sim'
            >>> origin = count_in[0]
            >>> sim = build_sim(sim_path, model, [test_cv_svc])
            >>> (PERFECT, GOOD, POOR, BAD)
            (100, 50, 25, 0)
            >>> assert kgr_perfect('9bbc45a81e4511e6b7066c3be51cefca', jd_service, sim)
            >>> assert kgr_perfect('cb3a4d820ab011e691ce6c3be51cefca', jd_service, sim)
            >>> assert kgr_perfect('f12cd9fc1b3011e6a5286c3be51cefca', jd_service, sim)
            >>> assert kgr_perfect('d09227ca0b5d11e6b01c6c3be51cefca', jd_service, sim)
            >>> assert kgr_perfect('4a9f2d9c0b4f11e6877a6c3be51cefca', jd_service, sim)
            >>> assert kgr_good('7cadbda40b5d11e699956c3be51cefca', jd_service, sim)
            >>> assert kgr_perfect('d10df4940b4f11e69d676c3be51cefca', jd_service, sim)
            >>> assert kgr_perfect('046ad1040b5511e6bd4d6c3be51cefca', jd_service, sim)
            >>> assert kgr_perfect('542330f40d0011e69e136c3be51cefca', jd_service, sim)
            >>> assert kgr_perfect('d652742841a211e68dc34ccc6a30cd76', jd_service, sim)
            >>> assert kgr_perfect('098a91ca0b4f11e6abf46c3be51cefca', jd_service, sim)
            >>> assert kgr_perfect('9b48f97653e811e6af534ccc6a30cd76', jd_service, sim)
            >>> assert kgr_perfect('e9f415f653e811e6945a4ccc6a30cd76', jd_service, sim)
            >>> assert kgr_poor('be97722a0cff11e6a3e16c3be51cefca', jd_service, sim)
            >>> assert kgr_perfect('e290dd36428a11e6b2934ccc6a30cd76', jd_service, sim)
            >>> assert kgr_good('80ce049a320711e6ac1f4ccc6a30cd76', jd_service, sim)
            >>> assert kgr_perfect('b73ac9621cd811e694e76c3be51cefca', jd_service, sim)
            >>> assert kgr_good('48dc231c0b5d11e6b89e6c3be51cefca', jd_service, sim)
            >>> assert kgr_good('e3bd422a2d6411e6b5296c3be51cefca', jd_service, sim)
            >>> assert kgr_bad('437958560b5b11e6aaa86c3be51cefca', jd_service, sim)
            >>> assert kgr_bad('a9a20a84473211e6a6934ccc6a30cd76', jd_service, sim)
            >>> assert kgr_percentage('fb2ac1c80b4d11e6adce6c3be51cefca', jd_service, sim, percentage=int(float(1)/3*100))
            >>> assert kgr_bad('048b4bc60d0011e6be436c3be51cefca', jd_service, sim)
            >>> assert kgr_bad('06fdc0680b5d11e6ae596c3be51cefca', jd_service, sim)
            >>> assert kgr_bad('57317f820cfe11e681466c3be51cefca', jd_service, sim)
            >>> assert kgr_bad('684605740b4e11e6ba746c3be51cefca', jd_service, sim)
            >>> assert kgr_perfect('763199560a9411e6a7936c3be51cefca', jd_service, sim)
            >>> assert kgr_bad('8c43b5343c4511e680994ccc6a30cd76', jd_service, sim)

        HHMT new:
            >>> assert kgr_percentage('06fdc0680b5d11e6ae596c3be51cefca', jd_service, sim, cvs=['2hw11q81', '8z3fxnr7', 'ltpyt2hp'], percentage=int(float(1)/3*100))
            >>> assert kgr_bad('2898a70a3f6111e6b68d4ccc6a30cd76', jd_service, sim, cvs=['mjm6vl3k'])
            >>> assert kgr_bad('437958560b5b11e6aaa86c3be51cefca', jd_service, sim, cvs=['hy24julz'])
            >>> assert kgr_perfect('48dc231c0b5d11e6b89e6c3be51cefca', jd_service, sim, cvs=['ohapy8ge'])
            >>> assert kgr_perfect('7858d9aa636411e6815f4ccc6a30cd76', jd_service, sim, cvs=['o3fjv894'])
            >>> assert kgr_percentage('7cadbda40b5d11e699956c3be51cefca', jd_service, sim, cvs=['dpaxyqns', '59c102os', '8y5nqhoc', 'uqototc6', 'fs60ntrm', 'wbrnwrob'], percentage=int(float(2)/6*100))
            >>> assert kgr_bad('def2a4120b5c11e691246c3be51cefca', jd_service, sim, cvs=['0p2unnwd', 'o0njv8te'])
            >>> assert kgr_good('9df8a1b20b4f11e686a56c3be51cefca', jd_service, sim, cvs=['rt9qa1gf', 'py6d1c0k'])
            >>> assert kgr_bad('5c2a203a596011e6bb374ccc6a30cd76', jd_service, sim, cvs=['18utt3gq', 'k0hov59f'])
            >>> assert kgr_perfect('542330f40d0011e69e136c3be51cefca', jd_service, sim, cvs=['nbdsjvzx'])
            >>> assert kgr_good('046ad1040b5511e6bd4d6c3be51cefca', jd_service, sim, cvs=['cfvpiab7', 'pc42qr9a'])

        FKJY new:
            >>> assert kgr_percentage('07ea1a8018be11e684026c3be51cefca', jd_service, sim, cvs=['cn64i09t', 'fxetvyzc', 'kgmp7dpg', 'u5dh7ozn', 'xt7613fa'], percentage=int(float(1)/5*100))
            >>> assert kgr_good('2fe1c53a231b11e6b7096c3be51cefca', jd_service, sim, cvs=['3hffapdz', '2x5wx4aa'])
            >>> assert kgr_bad('ae31247274c811e6b6b54ccc6a30cd76', jd_service, sim, cvs=['2sh48rjp'])
            >>> assert kgr_bad('5b2f8548320611e6b4e84ccc6a30cd76', jd_service, sim, cvs=['cfimev64', 'ko5luqyi', '0x4zpslk'])
            >>> assert kgr_bad('5b2f8548320611e6b4e84ccc6a30cd76', jd_service, sim, cvs=['cfimev64', 'ko5luqyi', '0x4zpslk'], index_service=SVC_INDEX, filterdict={'expectation_places': ['长沙'.decode('utf-8')]})
            >>> assert kgr_percentage('78df9d86555f11e6abad4ccc6a30cd76', jd_service, sim, cvs=['5ziy6c80', '6y0a1a75', '80clrjqi', 'rlb3jau0', 'sbip7deq', 'uwbvmsod', '68oojytn'], percentage=int(float(1)/7*100))
            >>> assert kgr_percentage('78df9d86555f11e6abad4ccc6a30cd76', jd_service, sim, cvs=['5ziy6c80', '6y0a1a75', '80clrjqi', 'rlb3jau0', 'sbip7deq', 'uwbvmsod', '68oojytn'], index_service=SVC_INDEX, filterdict={'expectation_places': ['长沙'.decode('utf-8')]}, percentage=int(float(2)/7*100))
            >>> assert kgr_bad('80ce049a320711e6ac1f4ccc6a30cd76', jd_service, sim, cvs=['nvujsh0u'])
            >>> assert kgr_bad('cce2a5be547311e6964f4ccc6a30cd76', jd_service, sim, cvs=['qfgwkkhg', 'nji2v4s7', 'qssipwf9'])
            >>> assert kgr_percentage('cce2a5be547311e6964f4ccc6a30cd76', jd_service, sim, cvs=['qfgwkkhg', 'nji2v4s7', 'qssipwf9'], index_service=SVC_INDEX, filterdict={'expectation_places': ['长沙'.decode('utf-8')]}, percentage=int(float(2)/3*100)) #FIXME ranks {'qssipwf9': 37, 'nji2v4s7': 25, 'qfgwkkhg': 7}
            >>> assert kgr_good('d33a669c313511e69edc4ccc6a30cd76', jd_service, sim, cvs=['csa46gdd', 'fahayhk8'])

        IBA new:
            >>> assert kgr_bad('4f2d032e53e911e685e24ccc6a30cd76', jd_service, sim, cvs=['x4dy5bzu', 'i1xm7sml'])
            >>> assert kgr_percentage('86119050313711e69b804ccc6a30cd76', jd_service, sim, cvs=['dpaxyqns', 'kf9sxzox', '5o4tiazc', 'n2ae2kyt', 'hieheubl', 'jc496tc2', 'hieheubl', 'rzcqg8m3'], percentage=int(float(1)/8*100))
            >>> assert kgr_percentage('9b48f97653e811e6af534ccc6a30cd76', jd_service, sim, cvs=['6r03u6so', '8fq1dwq3', 'dg2n5hqa'], percentage=int(float(1)/3*100))
            >>> assert kgr_perfect('e3bd422a2d6411e6b5296c3be51cefca', jd_service, sim, cvs=['qsfmtebc'])
            >>> assert kgr_percentage('e9f415f653e811e6945a4ccc6a30cd76', jd_service, sim, cvs=['fv51hvdy', 'je7d0xeg', 'v0gcrsow', 'sjk41azl', 'f280mmdm', 'cla50bo5'], percentage=int(float(1)/6*100))
            >>> count_in[0] - origin
            60
        """
        self.num_best = None
        p = self.base_probability(doc, top=top, minimum=minimum)
        results = map(lambda x: (self.names[x[0]], str(x[1])), p)
        return results

    def probability_by_ids(self, doc, ids, top=10000):
        indexs = [self.namesindex[id] for id in ids if id in self.namesindex]
        vectors = [self.index.vector_by_id(pos) for pos in indexs]
        ms = similarities.MatrixSimilarity(vectors, num_features=self.index.num_features)
        ms.num_best = top
        vec_lsi = self.lsi_model.probability(doc)
        probability = ms[vec_lsi]
        results = map(lambda x: (self.names[indexs[x[0]]], str(x[1])), probability)
        return results

    def probability_by_id(self, doc, id):
        if self.exists(id) is False:
            return None
        index = self.names.index(id)
        vec_lsi = self.lsi_model.probability(doc)
        result = abs(self.index[vec_lsi][index])
        return (os.path.splitext(id)[0], str(result))

    def base_probability(self, doc, top=None, minimum=0):
        if top is None:
            top = len(self.index)
        elif top < 1:
            top = int(len(self.index)*top)
        top = top if top > minimum else minimum
        results = []
        self.num_best = top
        vec_lsi = self.lsi_model.probability(doc)
        result = self.index[vec_lsi]
        self.num_best = None
        return result

    @property
    def namesindex(self):
        if len(self._namesindex) != len(self.names):
            self._namesindex.update(dict([(self.names[index], index)
                                    for index in xrange(len(self._namesindex), len(self.names))]))
        return self._namesindex

    @property
    def num_best(self):
        return self.index.num_best

    @num_best.setter
    def num_best(self, value):
        self.index.num_best = value

    @property
    def ids(self):
        return self.namesindex.keys()

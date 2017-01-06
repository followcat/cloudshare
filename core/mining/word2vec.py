# -*- coding: utf-8 -*-

import os
import ujson

import jieba.posseg

from gensim.models import Word2Vec


class Doc2Vecmodel(object):

    names_save_name = 'word2vec.names'
    model_save_name = 'word2vec.model'
    texts_save_name = 'word2vec.texts'


    def __init__(self, savepath, size=100, sample=0, window=6, iter=1, workers=1, slicer=None, config=None):
        if config is None:
            config = {}
        self.path = savepath
        self.size = size
        self.iter = iter
        self.config = {
            'size': size,
            'workers': workers,
            'iter': iter,
            'sample': sample,
        }
        self.config.update(config)
        if slicer:
            self.slicer = slicer
        else:
            self.slicer = lambda x:x.split(' ')
        self.sample = sample
        self.workers = workers
        self.window = window
        self.names = []
        self._texts = []

        self.word2vec = None


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
        if len(names) > 5:
            self.setup(names, texts)
            return True
        return False

    def build_from_names(self, svccv_list, names):
        texts = []
        if len(names) < 6:
            return False
        for name in names:
            for svc_cv in svccv_list:
                if svc_cv.exists(name):
                    doc = svc_cv.getmd(name)
                    texts.append(doc)
                    break
            else:
                raise Exception("Not exists name: " + name)
        self.setup(names, texts)
        return True

    def build_from_words(self, svccv_list, words):
        names = []
        words = []
        for svc_cv in svccv_list:
            for data in svc_cv.datas():
                name, doc = data
                for word in words:
                    if word in doc:
                        names.append(name)
                        texts.append(doc)
                        break
        if len(names) > 5:
            self.setup(names, texts)
            return True
        return False

    def setup(self, names, texts):
        self.names = names
        self.texts = self.slicer(texts)
        self.set_word2vec_model()

    def getconfig(self, param):
        result = False
        if param in self.config:
            result = self.config[param]
        return result

    def save(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        with open(os.path.join(self.path, self.names_save_name), 'w') as f:
            ujson.dump(self.names, f)
        with open(os.path.join(self.path, self.texts_save_name), 'w') as f:
            ujson.dump(self.texts, f)
        self.word2vec.save(os.path.join(self.path, self.model_save_name))

    def load(self):
        with open(os.path.join(self.path, self.names_save_name), 'r') as f:
            self.names = ujson.load(f)
        self.word2vec = Word2Vec.load(os.path.join(self.path, self.model_save_name))

    def set_word2vec_model(self):
        self.word2vec = Word2Vec(self.texts,
                          size=self.size,
                          window=self.window,
                          min_count=0,
                          iter=self.iter,
                          workers=self.workers)

    def most_similar(self, doc, num_words=5):
        re_words = []
        words = self.slicer(doc)
        for word in words:
            re_words.append(word)
            try:
                re_words.extend([w[0] for w in self.word2vec.most_similar(word, topn=num_words)])
            except KeyError:
                continue
        return re_words

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

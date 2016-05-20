import re
import os
import pickle

import jieba.posseg

from gensim import corpora, models, similarities


class LSImodel(object):

    names_save_name = 'lsi.names'
    model_save_name = 'lsi.model'
    matrix_save_name = 'lsi.matrix'
    corpu_dict_save_name = 'lsi.dict'
    corpus_save_name = 'lsi.corpus'
    texts_save_name = 'lsi.texts'
    most_save_name = 'lsi.most'

    def __init__(self, topics=100):
        self.topics = topics
        self.names = []
        self.texts = []
        self.corpus = []
        self.token_most = {}

        self.lsi = None
        self.index = None
        self.tfidf = None
        self.dictionary = None
        self.corpus_tfidf = None

    def build(self, svc_cv):
        names = []
        texts = []
        for data in svc_cv.datas():
            name, doc = data
            names.append(name.md)
            text = [word.word for word in jieba.posseg.cut(doc) if word.flag != 'x']
            texts.append(text)
        if len(names) > 0:
            self.setup(names, texts)
            return True
        return False

    def setup(self, names, texts):
        self.names = names
        self.texts = texts
        self.silencer()
        self.set_dictionary()
        self.set_corpus()
        self.set_tfidf()
        self.set_lsimodel()

    def save(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, self.names_save_name), 'w') as f:
            pickle.dump(self.names, f)
        with open(os.path.join(path, self.corpus_save_name), 'w') as f:
            pickle.dump(self.corpus, f)
        with open(os.path.join(path, self.texts_save_name), 'w') as f:
            pickle.dump(self.texts, f)
        with open(os.path.join(path, self.most_save_name), 'w') as f:
            pickle.dump(self.token_most, f)
        self.lsi.save(os.path.join(path, self.model_save_name))
        self.dictionary.save(os.path.join(path, self.corpu_dict_save_name))
        self.index.save(os.path.join(path, self.matrix_save_name))

    def load(self, path):
        with open(os.path.join(path, self.names_save_name), 'r') as f:
            self.names = pickle.load(f)
        with open(os.path.join(path, self.corpus_save_name), 'r') as f:
            self.corpus = pickle.load(f)
        with open(os.path.join(path, self.texts_save_name), 'r') as f:
            self.texts = pickle.load(f)
        with open(os.path.join(path, self.most_save_name), 'r') as f:
            self.token_most = pickle.load(f)
        self.lsi = models.LsiModel.load(os.path.join(path, self.model_save_name))
        self.dictionary = corpora.dictionary.Dictionary.load(os.path.join(path,
                                                             self.corpu_dict_save_name))
        self.index = similarities.Similarity.load(os.path.join(path,
                                                        self.matrix_save_name))

    def add(self, name, document):
        self.names.append(name)
        data = re.sub(ur'[\n- /]+' ,' ' , document)
        seg = [word.word for word in jieba.posseg.cut(data) if word.flag != 'x']
        text = [word for word in seg if word not in self.token_most]
        self.texts.append(text)
        if self.dictionary is None:
            self.dictionary = corpora.Dictionary(self.texts)
        corpu = self.dictionary.doc2bow(text)
        self.corpus.append(corpu)
        tfidf = models.TfidfModel(self.corpus)
        corpu_tfidf = tfidf[[corpu]]
        if self.lsi is None:
            self.lsi = models.LsiModel(corpu_tfidf, id2word=self.dictionary,
                            num_topics=self.topics, power_iters=6, extra_samples=300)
        else:
            self.lsi.add_documents(corpu_tfidf)
        self.index = similarities.Similarity("similarity", self.lsi[self.corpus], self.topics)

    def set_dictionary(self):
        self.dictionary = corpora.Dictionary(self.texts)
        
    def set_corpus(self):
        for text in self.texts:
            self.corpus.append(self.dictionary.doc2bow(text))

    def set_tfidf(self):
        self.tfidf = models.TfidfModel(self.corpus)
        self.corpus_tfidf = self.tfidf[self.corpus]

    def set_lsimodel(self):
        self.lsi = models.LsiModel(self.corpus_tfidf, id2word=self.dictionary,
                                   num_topics=self.topics, power_iters=6, extra_samples=300)
        self.index = similarities.Similarity("similarity", self.lsi[self.corpus], self.topics)

    def silencer(self):
        count_dict = {}
        count_all = 0
        for text in self.texts:
            for word in text:
                if word not in count_dict:
                    count_dict[word] = 1
                else:
                    count_dict[word] += 1
                count_all += 1
        for word in count_dict:
            if count_dict[word] > count_all*0.2:
                self.token_most[word] = count_dict[word]
        self.texts = [[word for word in text if word not in self.token_most]
                        for text in self.texts]

    def probability(self, doc):
        texts = [word.word for word in jieba.posseg.cut(doc) if word.flag != 'x']
        vec_bow = self.dictionary.doc2bow(texts)
        vec_lsi = self.lsi[vec_bow]
        sims = sorted(enumerate(self.index[vec_lsi]), key=lambda item: -item[1])
        return sims

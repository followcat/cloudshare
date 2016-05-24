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

    def __init__(self, savepath, no_above=1./8, topics=100):
        self.path = savepath
        self.topics = topics
        self.no_above = no_above
        self.names = []
        self.texts = []
        self.corpus = []

        self.lsi = None
        self.index = None
        self.tfidf = None
        self.dictionary = None
        self.corpus_tfidf = None

    def update(self, svc_cv):
        added = False
        for data in svc_cv.datas():
            name, doc = data
            if name.md not in self.names:
                self.add(name.md, doc)
                added = True
        if added:
            self.save()

    def build(self, svc_cv):
        names = []
        texts = []
        for data in svc_cv.datas():
            name, doc = data
            names.append(name.md)
            texts.append(doc)
        if len(names) > 0:
            self.setup(names, texts)
            return True
        return False

    def setup(self, names, texts):
        self.names = names
        self.texts = self.silencer(texts)
        self.set_dictionary()
        self.set_corpus()
        self.set_tfidf()
        self.set_lsimodel()

    def save(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        with open(os.path.join(self.path, self.names_save_name), 'w') as f:
            pickle.dump(self.names, f)
        with open(os.path.join(self.path, self.corpus_save_name), 'w') as f:
            pickle.dump(self.corpus, f)
        with open(os.path.join(self.path, self.texts_save_name), 'w') as f:
            pickle.dump(self.texts, f)
        self.lsi.save(os.path.join(self.path, self.model_save_name))
        self.dictionary.save(os.path.join(self.path, self.corpu_dict_save_name))
        self.index.save(os.path.join(self.path, self.matrix_save_name))

    def load(self):
        with open(os.path.join(self.path, self.names_save_name), 'r') as f:
            self.names = pickle.load(f)
        with open(os.path.join(self.path, self.corpus_save_name), 'r') as f:
            self.corpus = pickle.load(f)
        with open(os.path.join(self.path, self.texts_save_name), 'r') as f:
            self.texts = pickle.load(f)
        self.lsi = models.LsiModel.load(os.path.join(self.path, self.model_save_name))
        self.dictionary = corpora.dictionary.Dictionary.load(os.path.join(self.path,
                                                             self.corpu_dict_save_name))
        self.index = similarities.Similarity.load(os.path.join(self.path,
                                                        self.matrix_save_name))

    def add(self, name, document):
        text = self.silencer([document])[0]
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
        self.index = similarities.Similarity(os.path.join(self.path, "similarity"),
                                             self.lsi[self.corpus], self.topics)

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
        self.index = similarities.Similarity(os.path.join(self.path, "similarity"),
                                             self.lsi[self.corpus], self.topics)

    def silencer(self, texts):
        FLAGS = ['x', # spaces
                 'm', # number and date
                 'ns', # city and country
                ]
        LINE = re.compile(ur'[\n- /]+')
        BHTTP = re.compile(ur'\(https?:\S*\)')
        HTTP = re.compile(ur'https?:\S*(?=\s)')
        WWW = re.compile('www\.[\.\w]+')
        EMAIL = re.compile('\w+@[\.\w]+')
        SHORT = re.compile('(([A-Z]\d{0,2})|([a-z]{1,4})|[\d\.]{1,11})$')
        selected_texts = []
        for text in texts:
            text = HTTP.sub('\n', BHTTP.sub('\n', LINE.sub(' ', text)))
            text = WWW.sub('', EMAIL.sub('', text))
            doc = [word.word for word in jieba.posseg.cut(text) if word.flag not in FLAGS]
            out = []
            for d in doc:
                if d.istitle():
                    # Can make it match SHORT later for skip (eg 'Ltd' ...)
                    d = d.lower()
                if not SHORT.match(d):
                    # Even out tools and brands (eg 'CLEARCASE' vs 'clearcase')
                    d = d.lower()
                    out.append(d)
            selected_texts.append(out)
        return selected_texts

    def probability(self, doc):
        texts = self.silencer([doc])[0]
        vec_bow = self.dictionary.doc2bow(texts)
        vec_lsi = self.lsi[vec_bow]
        sims = sorted(enumerate(abs(self.index[vec_lsi])), key=lambda item: item[1], reverse=True)
        return sims

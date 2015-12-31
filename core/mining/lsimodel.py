import os
import re
import glob
import jieba
import random

from gensim import corpora, models, similarities


class LSImodel(object):
    def __init__(self, directory):
        self.dir = directory
        self.names = []
        self.datas = []
        self.texts = []
        self.corpus = []
        self.set_data()

        self.lsi = None
        self.index = None
        self.tfidf = None
        self.dictionary = None
        self.corpus_tfidf = None

    def setup(self, dictionary=None):
        self.silencer(2, 100)
        self.set_dictionary(dictionary)
        self.set_corpus()
        self.set_tfidf()
        self.set_lsimodel()

    def set_data(self):
        def elt(s):
            return s
        for pathfile in glob.glob(os.path.join(self.dir, '*.md')):
            if os.path.isfile(pathfile):
                data = open(pathfile, 'rb').read()
                data = re.sub(ur'[\n- /]+' ,' ' , data)
                path, name = pathfile.split('/')
                self.names.append(name)
                self.datas.append(data)
                seg = filter(lambda x: len(x) > 0, map(elt, jieba.cut(data, cut_all=False)))
                self.texts.append(seg)

    def set_dictionary(self, dictionary=None):
        if dictionary is None:
            self.dictionary = corpora.Dictionary(self.texts)
        else:
            self.dictionary = dictionary

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

    def random_doc(self):
        name = random.choice(os.listdir(self.dir))
        data = open(os.path.join(self.dir, name), 'rb').read()
        return name, data

    def probability(self, doc):
        vec_bow = self.dictionary.doc2bow(jieba.cut(doc, cut_all=False))
        vec_lsi = self.lsi[vec_bow]
        sims = sorted(enumerate(self.index[vec_lsi]), key=lambda item: -item[1])
        return sims

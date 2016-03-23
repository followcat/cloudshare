import os
import pickle

import jieba

from gensim import corpora, models, similarities


class LSImodel(object):

    names_save_name = 'lsi.names'
    model_save_name = 'lsi.model'
    matrix_save_name = 'lsi.matrix'
    corpu_dict_save_name = 'lsi.dict'
    corpus_save_name = 'lsi.corpus'
    texts_save_name = 'lsi.texts'
    once_save_name = 'lsi.once'

    def __init__(self):
        self.names = []
        self.texts = []
        self.corpus = []
        self.token_once = {}

        self.lsi = None
        self.index = None
        self.tfidf = None
        self.dictionary = None
        self.corpus_tfidf = None

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
        with open(os.path.join(path, self.once_save_name), 'w') as f:
            pickle.dump(self.token_once, f)
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
        with open(os.path.join(path, self.once_save_name), 'r') as f:
            self.token_once = pickle.load(f)
        self.lsi = models.LsiModel.load(os.path.join(path, self.model_save_name))
        self.dictionary = corpora.dictionary.Dictionary.load(os.path.join(path,
                                                             self.corpu_dict_save_name))
        self.index = similarities.MatrixSimilarity.load(os.path.join(path,
                                                        self.matrix_save_name))

    def add(self, documents, minimum=0, maximum=100):
        def elt(s):
            return s
        count_dict = {}
        for name in documents:
            self.names.append(name)
            data = documents[name]
            seg = filter(lambda x: len(x) > 0, map(elt, jieba.cut(data, cut_all=False)))
            for word in seg:
                if word not in count_dict:
                    count_dict[word] = 1
                else:
                    count_dict[word] += 1
        for word in count_dict:
            if count_dict[word] < minimum or count_dict[word] > maximum:
                self.token_once[word] = count_dict[word]
        text = [word for word in seg if word not in self.token_once]
        self.texts.append(text)
        self.dictionary.add_documents([text])
        corpu = self.dictionary.doc2bow(text)
        self.corpus.append(corpu)
        tfidf = models.TfidfModel([corpu])
        corpu_tfidf = tfidf[[corpu]]
        self.lsi.add_documents(corpu_tfidf)
        self.index = similarities.MatrixSimilarity(self.lsi[self.corpus])

    def set_dictionary(self):
        self.dictionary = corpora.Dictionary(self.texts)
        
    def set_corpus(self):
        for text in self.texts:
            self.corpus.append(self.dictionary.doc2bow(text))

    def set_tfidf(self):
        self.tfidf = models.TfidfModel(self.corpus)
        self.corpus_tfidf = self.tfidf[self.corpus]

    def set_lsimodel(self, topics=100):
        self.lsi = models.LsiModel(self.corpus_tfidf, id2word=self.dictionary,
                                    num_topics=topics)
        self.index = similarities.MatrixSimilarity(self.lsi[self.corpus])

    def silencer(self, minimum=2, maximum=100):
        count_dict = {}
        for text in self.texts:
            for word in text:
                if word not in count_dict:
                    count_dict[word] = 1
                else:
                    count_dict[word] += 1

        for word in count_dict:
            if count_dict[word] < minimum or count_dict[word] > maximum:
                self.token_once[word] = count_dict[word]
        self.texts = [[word for word in text if word not in self.token_once]
                        for text in self.texts]

    def probability(self, doc):
        vec_bow = self.dictionary.doc2bow(jieba.cut(doc, cut_all=False))
        vec_lsi = self.lsi[vec_bow]
        sims = sorted(enumerate(self.index[vec_lsi]), key=lambda item: -item[1])
        return sims

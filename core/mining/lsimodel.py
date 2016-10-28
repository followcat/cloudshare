# -*- coding: utf-8 -*-

import os
import math
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
        if len(names) > 5:
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
        u"""
            >>> from tests.multi_models import *
            >>> from tests.test_index import *
            >>> jds = [_jd for _jd, _cvs in datas.items() if len(_cvs) > 4]
            >>> models = build_models(jds)
            >>> model = models['80ce049a320711e6ac1f4ccc6a30cd76']
            >>> topics = model.lsi.show_topics(formatted=False, num_words=15)
            >>> m_topics = [
            ...     [u'显控', u'监控', u'监测'],
            ...     [u'物理', u'电表', u'相变'],
            ...     [u'成像', u'分析仪', u'控制器'],
            ...     [u'货运', u'铁路', u'机械'],
            ... ]
            >>> assert match_topics(m_topics, topics, 2)
            >>> model = models['7cadbda40b5d11e699956c3be51cefca']
            >>> topics = model.lsi.show_topics(formatted=False, num_words=15)
            >>> m_topics = [
            ...     [u'医药', u'区域', u'销售', u'客户'],
            ...     [u'医用', u'ct', u'机房'],
            ...     [u'核反应堆', u'辐射', u'防护', u'监测'],
            ... ]
            >>> assert match_topics(m_topics, topics, 2)

            >>> model = models['e9f415f653e811e6945a4ccc6a30cd76']
            >>> topics = model.lsi.show_topics(formatted=False, num_words=15)
            >>> m_topics = [
            ...     [u'加速器', u'射频'],
            ...     [u'放疗', u'束流'],
            ...     [u'digital', u'electrical', u'electronic'],
            ... ]
            >>> assert match_topics(m_topics, topics, 1)
            >>> model = models['86119050313711e69b804ccc6a30cd76']
            >>> topics = model.lsi.show_topics(formatted=False, num_words=15)
            >>> m_topics = [
            ...     [u'质子', u'治疗'],
            ...     [u'船舶', u'轮机', u'管轮'],
            ... ]
            >>> words, weights = topic_words_list(topics)
            >>> assert match_topics(m_topics, topics, 2)

        test on merge 2 group of similar cvs:
            >>> jds = ['86119050313711e69b804ccc6a30cd76', 'e9f415f653e811e6945a4ccc6a30cd76']
            >>> model = build_model(jds, name='sim')
            >>> topics = model.lsi.show_topics(formatted=False, num_words=15)
            >>> m_topics = [
            ...     [u'加速器', u'质子', u'束流'],
            ...     [u'船舶', u'轮机', u'管轮'],
            ... ]
            >>> assert match_topics(m_topics, topics, 2)

        test on merge 2 group of different cvs:
            >>> model = models['07ea1a8018be11e684026c3be51cefca']
            >>> topics = model.lsi.show_topics(formatted=False, num_words=15)
            >>> m_topics = [
            ...     [u'sap', u'运维', u'搜索'],
            ...     [u'microsoft', u'visual', u'it'],
            ... ]
            >>> assert match_topics(m_topics, topics, 2)
            >>> jds = ['86119050313711e69b804ccc6a30cd76', '07ea1a8018be11e684026c3be51cefca']
            >>> topics = build_model(jds, name='diff').lsi.show_topics(formatted=False, num_words=15)
            >>> m_topics = [
            ...     [u'质子', u'治疗'],
            ...     [u'船舶', u'轮机', u'管轮'],
            ...     [u'sap', u'运维', u'搜索'],
            ...     [u'microsoft', u'visual', u'it'],
            ... ]
            >>> assert match_topics(m_topics, topics, 3)
            >>> jds = ['86119050313711e69b804ccc6a30cd76', 'e9f415f653e811e6945a4ccc6a30cd76', '07ea1a8018be11e684026c3be51cefca']
            >>> topics = build_model(jds, name='mixed').lsi.show_topics(formatted=False, num_words=15)
            >>> m_topics = [
            ...     [u'加速器', u'质子', u'束流'],
            ...     [u'船舶', u'轮机', u'管轮'],
            ...     [u'dr', u'放射', u'放疗'],
            ...     [u'microsoft', u'visual', u'it'],
            ... ]
            >>> assert match_topics(m_topics, topics, 2)

        test on uav classify model
            >>> cvs = datas['UAV']
            >>> jds = ['UAV']
            >>> model = build_model(jds, name='mixed', path='tests/lsimodel_words')
            >>> topics = model.lsi.show_topics(formatted=False, num_words=15)
            >>> uav_topic1 = [u'飞行', u'频段', u'航拍']
            >>> uav_topic2 = [u'解算', u'航姿']
            >>> uav_topic1_index = match_topic_index(uav_topic1, topics)
            >>> uav_topic2_index = match_topic_index(uav_topic2, topics)
            >>> match_cvs = ['2471572', '6gja28pi', '1587957595', '10978947', '1565799600', '2471572', '4782048', '5223250', '5346432', '6730128', '6gja28pi', 'c16q7ylp', 'ryzvspix']
            >>> for cv in cvs:
            ...     cv_doc = get_cv_md(cv)
            ...     vec_cv = model.probability(cv_doc)
            ...     cv_mapping_vec = sorted(vec_cv, key=lambda item: abs(item[1]), reverse=True)
            ...     cv_match_topics = [item[0] for item in cv_mapping_vec]
            ...     if cv_match_topics.index(0) == 0:
            ...         if (uav_topic1_index != -1 and cv_match_topics.index(uav_topic1_index) < 2):
            ...             (cv, cv in match_cvs)
        """
        self.tfidf = models.TfidfModel(self.corpus, wlocal=tf_cal)
        self.corpus_tfidf = self.tfidf[self.corpus]

    def set_lsimodel(self):
        self.lsi = models.LsiModel(self.corpus_tfidf, id2word=self.dictionary,
                                   num_topics=self.topics, power_iters=6, extra_samples=0)

    def probability(self, doc):
        u"""
            >>> from tests.test_index import *
            >>> from webapp.settings import *
            >>> import compiler.ast
            >>> model = SVC_MIN.lsi_model['medical']
            >>> topics = model.lsi.show_topics(formatted=False)
            >>> words, weights = topic_words_list(topics)
            >>> fatten_words = compiler.ast.flatten(words)

        Some words happen to appear in the most significant topics from time
        to time, that will be considered as defective.
            >>> assert not fatten_words.count(u'湖南') < 15 #FIXME
            >>> assert not fatten_words.count(u'飞利浦') < 15 #FIXME
            >>> assert not fatten_words.count(u'通用电气') < 15 #FIXME
            >>> assert not fatten_words.count(u'常州') < 15 #FIXME
            >>> assert not fatten_words.count(u'东莞') < 15 #FIXME
            >>> assert not fatten_words.count(u'税前') < 15 #FIXME
            >>> assert not fatten_words.count(u'理邦') < 15 #FIXME
            >>> assert not fatten_words.count(u'ge') < 15 #FIXME
            >>> assert not fatten_words.count(u'软件测试') < 14 #FIXME
            >>> assert not fatten_words.count(u'大专') < 14 #FIXME

        On the other hand, some words do not appear in any of the topics
        at all.
            >>> topics = model.lsi.show_topics(num_topics=100, num_words=10, formatted=False)
            >>> words = topic_words_list(topics)
            >>> fatten_words = compiler.ast.flatten(words)
            >>> assert u'飞机' in model.dictionary.values()
            >>> assert u'航天' in model.dictionary.values()
            >>> assert u'航空' in model.dictionary.values()
            >>> assert not u'飞机' in fatten_words #FIXME
            >>> assert not u'航天' in fatten_words #FIXME
            >>> assert u'航空' in fatten_words
            >>> assert u'物流' in model.dictionary.values()
            >>> assert u'物流' in fatten_words
            >>> assert u'律师' in model.dictionary.values()
            >>> assert not u'律师' in fatten_words #FIXME
            >>> assert u'法律' in model.dictionary.values()
            >>> assert not u'法律' in fatten_words #FIXME
            >>> assert u'行销' in model.dictionary.values()
            >>> assert not u'行销' in fatten_words #FIXME
            >>> assert u'产业化' in model.dictionary.values()
            >>> assert not u'产业化' in fatten_words #FIXME
            >>> assert not u'销售' in model.dictionary.values() #FIXME
            >>> assert not u'销售' in fatten_words #FIXME
            >>> assert not u'售后' in model.dictionary.values() #FIXME
            >>> assert not u'售后' in fatten_words #FIXME
            >>> assert u'商务' in model.dictionary.values()
            >>> assert not u'商务' in fatten_words #FIXME

        Show mapping topics words of input doc.
            >>> jd = {'text' : u"岗位职责："
            ...     u"\\n1.协助部门经理实施公司质子医疗装置产业化的市场业务推广与沟通；"
            ...     u"\\n2.负责参与各种市场行销展会的工作；"
            ...     u"\\n3.配合装置售前，售后技术推广与沟通工作；"
            ...     u"\\n4.相关的英文沟通及翻译工作。"
            ...     u"\\n"
            ...     u"\\n岗位要求："
            ...     u"\\n1.放疗、肿瘤、医学物理、医学影像、临床等医学相关专业本科，硕士以上学历者优先；"
            ...     u"\\n2.从事相关工作1-3年以上，熟悉放射医疗器械，具有大型医院放疗科、肿瘤科、影像设备科等相关科室工作经验者优先考虑；"
            ...     u"\\n3.有良好的团队精神、协调沟通能力及表达能力；"
            ...     u"\\n4.具有良好的英文写作及口头表达能力。"}
            >>> assert  u'英文' in model.dictionary.values()
            >>> assert u'推广' in model.dictionary.values()
            >>> assert u'产业化' in model.dictionary.values()
            >>> assert u'放射' in model.dictionary.values()
            >>> assert u'放疗' in mapping_topic_words(jd['text'], model, num_topics=5, num_words=10)
            >>> assert not u'市场' in model.dictionary.values() #FIXME
            >>> assert not u'行销' in mapping_topic_words(jd['text'], model) #FIXME
            >>> assert not u'市场' in mapping_topic_words(jd['text'], model) #FIXME
            >>> assert not u'医学影像' in mapping_topic_words(jd['text'], model) #FIXME
            >>> assert not u'英文' in mapping_topic_words(jd['text'], model) #FIXME

        After removing sentences containing '放疗' and '物理' from jd,
        mapping topic change to more torward '销售' related.
            >>> jd = {'text' : u"岗位职责："
            ...     u"\\n1.协助部门经理实施公司医疗装置产业化的市场业务推广与沟通；"
            ...     u"\\n2.负责参与各种市场行销展会的工作；"
            ...     u"\\n3.配合装置售前，售后技术推广与沟通工作；"
            ...     u"\\n4.相关的英文沟通及翻译工作。"
            ...     u"\\n"
            ...     u"\\n岗位要求："
            ...     u"\\n3.有良好的团队精神、协调沟通能力及表达能力；"
            ...     u"\\n4.具有良好的英文写作及口头表达能力。"}
            >>> assert not u'市场' in model.dictionary.values() #FIXME
            >>> assert not u'市场' in mapping_topic_words(jd['text'], model) #FIXME
            >>> assert not u'行销' in mapping_topic_words(jd['text'], model) #FIXME
            >>> assert not u'产业化' in mapping_topic_words(jd['text'], model) #FIXME
            >>> assert not u'推广' in mapping_topic_words(jd['text'], model) #FIXME
            >>> assert not u'英文' in mapping_topic_words(jd['text'], model) #FIXME
        """
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


def tf_cal(term_freq):
    """
        >>> from core.mining.lsimodel import *
        >>> '%.3f'%(tf_cal(30) - tf_cal(10))
        '0.239'
        >>> '%.3f'%(tf_cal(10) - tf_cal(1))
        '0.500'
    """
    return math.log(1.01*math.sqrt(term_freq), 10)

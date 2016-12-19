# -*- coding: utf-8 -*-

import os
import math
import ujson

from gensim import corpora, models


class LSImodel(object):

    names_save_name = 'lsi.names'
    model_save_name = 'lsi.model'
    corpu_dict_save_name = 'lsi.dict'
    corpus_save_name = 'lsi.corpus'
    texts_save_name = 'lsi.texts'
    most_save_name = 'lsi.most'

    def __init__(self, savepath, no_above=1./8, topics=100, extra_samples=300,
                 tfidf_local=None, slicer=None, config=None):
        if config is None:
            config = {}
        self.path = savepath
        self.topics = topics
        self.no_above = no_above
        self.config = {
            'topics': topics,
            'no_above': no_above,
            'extra_samples': extra_samples,
        }
        self.config.update(config)
        if slicer:
            self.slicer = slicer
        else:
            self.slicer = lambda x:x.split('\n')
        self.extra_samples = extra_samples
        self.tfidf_local = tfidf_local
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
        texts = []
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
        self.set_dictionary()
        self.set_corpus()
        self.set_tfidf()
        self.set_lsimodel()

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
                            num_topics=self.topics, power_iters=6, extra_samples=self.extra_samples)
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
            >>> models = build_models(jds, path='tests/lsimodel')
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
            >>> path = 'tests/lsimodel_words'
            >>> model = build_model(jds, name='uav', path='tests/lsimodel_words')
            >>> topics = model.lsi.show_topics(formatted=False, num_words=15)
            >>> uav_topic1 = [u'飞行', u'频段', u'航拍']
            >>> uav_topic1_index = match_topic_index(uav_topic1, topics)
            >>> assert uav_topic1_index != -1
            >>> assert doc_match_topic(get_cv_md('1587957595'), model, uav_topic1_index, match_range=3)

        test on engineer classify' model, to separate embedded engineer
        and application engineer
            >>> cvs = datas['SW']
            >>> jds = ['SW']
            >>> model = build_model(jds, name='sw', path='tests/lsimodel_words')
            >>> topics = model.lsi.show_topics(formatted=False, num_words=15)
            >>> sw_topic1 = [u'电气', u'plc', u'调试']
            >>> sw_topic1_index = match_topic_index(sw_topic1, topics)
            >>> assert sw_topic1_index != -1
            >>> assert doc_match_topic(get_cv_md('a4lg46d6'), model, sw_topic1_index, match_range=3)
            >>> assert doc_match_topic(get_cv_md('dojbde7n'), model, sw_topic1_index, match_range=3)
            >>> assert doc_match_topic(get_cv_md('kzd4qoft'), model, sw_topic1_index, match_range=3)
            >>> assert doc_match_topic(get_cv_md('itftwn1d'), model, sw_topic1_index, match_range=3)
            >>> sw_topic2 = [u'运维', u'tomcat', u'nginx']
            >>> sw_topic2_index = match_topic_index(sw_topic2, topics)
            >>> assert sw_topic2_index != -1
            >>> assert doc_match_topic(get_cv_md('tn8cdk92'), model, sw_topic2_index, match_range=3)
        """
        if self.tfidf_local is None:
            self.tfidf = models.TfidfModel(self.corpus)
        else:
            self.tfidf = models.TfidfModel(self.corpus, wlocal=self.tfidf_local)
        self.corpus_tfidf = self.tfidf[self.corpus]

    def set_lsimodel(self):
        self.lsi = models.LsiModel(self.corpus_tfidf, id2word=self.dictionary,
                                   num_topics=self.topics, power_iters=6, extra_samples=self.extra_samples)

    def probability(self, doc):
        u"""
            >>> from tests.test_index import *
            >>> from tests.multi_models import *
            >>> from webapp.settings import *
            >>> import compiler.ast
            >>> model = SVC_MIN.lsi_model['medical']
            >>> names = [n for n in SVC_CV_REPO.names()]
            >>> texts = [SVC_CV_REPO.getmd(n) for n in names]
            >>> path = 'tests/lsimodel/medical'
            >>> model = build_lsimodel(path, model.slicer, names, texts, no_above=1./8, extra_samples=300, tfidf_local=core.mining.lsimodel.tf_cal)
            >>> topics = model.lsi.show_topics(formatted=False)
            >>> words, weights = topic_words_list(topics)
            >>> fatten_words = compiler.ast.flatten(words)

        Some words happen to appear in the most significant topics from time
        to time, that will be considered as defective.
            >>> assert not fatten_words.count(u'湖南') < 15 #FIXME
            >>> assert not fatten_words.count(u'渠道') < 13 #FIXME
            >>> assert not fatten_words.count(u'通用电气') < 13 #FIXME
            >>> assert not fatten_words.count(u'常州') < 14 #FIXME
            >>> assert not fatten_words.count(u'加速器') < 13 #FIXME
            >>> assert not fatten_words.count(u'ge') < 13 #FIXME
            >>> assert not fatten_words.count(u'大专') < 13 #FIXME
            >>> assert not fatten_words.count(u'南京') < 13 #FIXME

        On the other hand, some words do not appear in any of the topics
        at all.
            >>> topics = model.lsi.show_topics(num_topics=100, num_words=10, formatted=False)
            >>> words, weights = topic_words_list(topics)
            >>> fatten_words = compiler.ast.flatten(words)
            >>> assert u'飞机' in model.dictionary.values()
            >>> assert u'航天' in model.dictionary.values()
            >>> assert not u'航空' in model.dictionary.values() #FIXME
            >>> assert not u'飞机' in fatten_words #FIXME
            >>> assert not u'航天' in fatten_words #FIXME
            >>> assert not u'航空' in fatten_words #FIXME
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

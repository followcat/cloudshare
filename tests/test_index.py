# -*- coding: utf-8 -*-

import compiler.ast


def mapping_topic_words(doc, model, num_topics=10, num_words=10):
    u"""
        >>> from tests.test_index import *
        >>> from webapp.settings import *
        >>> model = SVC_MIN.lsi_model['medical']
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

    after removing sentences containing '放疗' and '物理' from jd,
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
    vec = model.probability(doc)
    mapping_vec = sorted(vec, key=lambda item: abs(item[1]), reverse=True)
    topics = model.lsi.show_topics(num_words=num_words)
    words = topic_words_list(topics, mapping_vec[:num_topics])
    return compiler.ast.flatten(words)

def topic_words_list(topics, mapping_vec=None):
    u"""
        >>> from tests.test_index import *
        >>> from webapp.settings import *
        >>> import compiler.ast
        >>> model = SVC_MIN.lsi_model['medical']
        >>> topics = model.lsi.show_topics()
        >>> words = topic_words_list(topics)
        >>> fatten_words = compiler.ast.flatten(words)

    Some words happen to appear in the most significant topics from time
    to time, that will be considered as defective.
        >>> assert not fatten_words.count(u'品质') < 15 #FIXME
        >>> assert not fatten_words.count(u'飞利浦') < 15 #FIXME
        >>> assert not fatten_words.count(u'通用电气') < 15 #FIXME
        >>> assert not fatten_words.count(u'机器人') < 15 #FIXME
        >>> assert not fatten_words.count(u'南京') < 15 #FIXME
        >>> assert not fatten_words.count(u'天津') < 15 #FIXME
        >>> assert not fatten_words.count(u'可靠性') < 15 #FIXME
        >>> assert not fatten_words.count(u'加速器') < 15 #FIXME
        >>> assert not fatten_words.count(u'ge') < 15 #FIXME
        >>> assert not fatten_words.count(u'图像') < 14 #FIXME

    On the other hand, some words do not appear in any of the topics
    at all.
        >>> topics = model.lsi.show_topics(num_topics=100, num_words=10)
        >>> words = topic_words_list(topics)
        >>> fatten_words = compiler.ast.flatten(words)
        >>> assert u'飞机' in model.dictionary.values()
        >>> assert u'航天' in model.dictionary.values()
        >>> assert u'航空' in model.dictionary.values()
        >>> assert not u'飞机' in fatten_words #FIXME
        >>> assert not u'航天' in fatten_words #FIXME
        >>> assert not u'航空' in fatten_words #FIXME
        >>> assert u'物流' in model.dictionary.values()
        >>> assert not u'物流' in fatten_words #FIXME
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

    """
    words = []
    if mapping_vec is None:
        m_topics = topics
    else:
        m_topics = mapping_topics(mapping_vec, topics)
    for topic in m_topics:
        words.append(split_topic(topic))
    return words

def mapping_topics(mapping_vec, topics):
    ret_topics = []
    for id, score in mapping_vec:
        ret_topics.append(topics[id])        
    return ret_topics

def split_topic(topic):
    raw_words = topic[1].split(' + ')
    words = []
    for _word in raw_words:
        _word = _word[_word.index('"')+1: _word.rindex('"')]
        words.append(_word)
    return words
    

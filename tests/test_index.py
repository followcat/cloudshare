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
        >>> assert u'放疗' in mapping_topic_words(jd['text'], model, num_topics=5, num_words=10)
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
        >>> assert not fatten_words.count(u'品质') < 15 #FIXME
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
    

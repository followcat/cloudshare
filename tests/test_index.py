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
        >>> assert u'放疗' in mapping_topic_words(jd['text'], model, num_topics=5, num_words=10)
    """
    vec = model.probability(doc)
    mapping_vec = sorted(vec, key=lambda item: abs(item[1]), reverse=True)
    topics = model.lsi.show_topics(num_words=num_words, formatted=False)
    words, weights = topic_words_list(topics, mapping_vec[:num_topics])
    return compiler.ast.flatten(words)

def topic_words_list(topics, mapping_vec=None):
    u"""
        >>> from tests.test_index import *
        >>> from webapp.settings import *
        >>> import compiler.ast
        >>> model = SVC_MIN.lsi_model['medical']
        >>> topics = model.lsi.show_topics(formatted=False)
        >>> words, weights = topic_words_list(topics)
        >>> fatten_words = compiler.ast.flatten(words)
        >>> assert u'品质' in fatten_words
    """
    words = []
    weights = []
    if mapping_vec is None:
        m_topics = topics
    else:
        m_topics = mapping_topics(mapping_vec, topics)
    for topic in m_topics:
        _words = []
        _weights = []
        for _word, _weight in topic[1]:
            _words.append(_word)
            _weights.append(_weight)
        words.append(_words)
        weights.append(_weights)
    return words, weights

def match_topics(words_list, topics, num=1):
    t_words, t_weights = topic_words_list(topics)
    count = 0
    for words in words_list:
        for ws in t_words:
            if set(words).issubset(set(ws)):
                count += 1
                break
    return count >= num

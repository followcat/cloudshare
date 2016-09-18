# -*- coding: utf-8 -*-
import os
import re
import core.mining.lsimodel
import core.mining.lsisimilarity

from utils.builtin import jieba_cut, pos_extract


REJECT = re.compile('(('+')|('.join([
    u'中文', u'日期', u'汽车',
    #u'个人', u'未填写',
    #u'财务',
    #u'招聘', u'英才网', u'人力',
    u'互联网',
    ])+'))')

LINE = re.compile(ur'[\n\t]+')
HEAD = ur'(((http|HTTP)[sS]?|(ftp|FTP))\:\/\/)'
UID = ur'([\w\-]+@)'
DEMAIN = ur'([a-zA-Z0-9][\-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][\-a-zA-Z0-9]{0,62})*(\.(cn|us|uk|jp|hk|com|edu|gov|int|mil|net|org|biz)))'
IP = ur'((([1]?\d{1,2}|2[0-4]\d|25[0-5])\.){3}([1]?\d{1,2}|2[0-4]\d|25[0-5]))'
PORT = ur'(\:(6553[0-5]|655[0-2]\d|65[0-4]\d{2}|6[0-4]\d{3}|[1-5]\d{4}|[1-9]\d{0,3}|0))'
SERVICE = ur'((\/[^\/\s][\w\.\,\?\'\(\)\*\\\+&%\$#\=~_\-@]*)*[^\.\,\?\"\'\(\)\[\]!;<>{}\s]?)*'

WEB = re.compile(ur"\(?\s?(" + HEAD + ur'?' + UID + ur'?(' + DEMAIN + ur'|' + IP + ur')' + PORT + ur'?' + SERVICE + ur")\s?\)?")

SYMBOL = re.compile(ur'[- /]+')
SHORT = re.compile('(([a-z]\d{0,2})|([a-z]{1,4})|[\d\.]{1,11})$')

FLAGS = ['x', # spaces
         'm', # number and date
         #'a', # adverb
         'c', # conjunction
         'd', # adverb
         'e', # interjection
         'f', # noun of locality
         'g', # morpheme word
         'h', # prefix
         'i', # idiom
         #'j', # abbreviation
         'k', # suffix
         'nrt', 'nr', 'ng', #'nz', fails on myjnoee7.md
         'o', # onomatopoeia
         'p', # preposition
         'q', # quantifier
         'r', # pronoun
         'tg', # time root word
         'u', # unclassified (eg. etc)
         'vg', # verb morpheme word
         #'v', # verb
         'y', # statement label designator
         'z', # State word
         #'ns', # city and country
        ]

def re_sub(reg, sub, text):
    """
        >>> from services.mining import *
        >>> s = "[测试计量技术及仪器]( http://www.test.com )[测试计量技术及仪器]\\n"
        >>> s += "[测试计量技术及仪器] (http://www.test.com) [测试计量技术及仪器]"
        >>> print(s)
        [测试计量技术及仪器]( http://www.test.com )[测试计量技术及仪器]
        [测试计量技术及仪器] (http://www.test.com) [测试计量技术及仪器]
        >>> print(re_sub(LINE, ' ', s))
        [测试计量技术及仪器]( http://www.test.com )[测试计量技术及仪器] [测试计量技术及仪器] (http://www.test.com) [测试计量技术及仪器]
        >>> print(re_sub(WEB, ' ', s))
        [测试计量技术及仪器] [测试计量技术及仪器]
        [测试计量技术及仪器]   [测试计量技术及仪器]
        >>> s = "[测试计量技术及仪器] (www.test.com) [测试计量技术及仪器]"
        >>> print(re_sub(WEB, ' ', s))
        [测试计量技术及仪器]   [测试计量技术及仪器]
        >>> s = "[测试计量技术及仪器] (test123@test.com) [测试计量技术及仪器]"
        >>> print(re_sub(WEB, ' ', s))
        [测试计量技术及仪器]   [测试计量技术及仪器]
        >>> s = "--------------------\\n"
        >>> s += "英语(CET4)、普通话\\n"
        >>> s += "--------------------\\n"
        >>> print(re_sub(LINE, '', re_sub(SYMBOL, '', s)))
        英语(CET4)、普通话
        >>> assert 'http://search.51job.com/job/52405118,c.html' in WEB.match('http://search.51job.com/job/52405118,c.html').group(0)
        >>> assert 'https://h.liepin.com/soResume/?company=ASI+CONVEYORS(Shanghai)+CO.,LTD' in WEB.match(
        ...             "https://h.liepin.com/soResume/?company=ASI+CONVEYORS(Shanghai)+CO.,LTD").group(0)
        >>> assert '2014.06' in WEB.match("https://h.liepin.com/cvsearch/soResume/?company=%AC%E5%8F%B8)2014.06").group(0) #FIXME
        >>> assert 'bertwalker2005@yahoo.co.uk' in WEB.match('bertwalker2005@yahoo.co.uk').group(0)
        >>> assert 'http://h.highpin.cn/ResumeManage/26566491@qq.com' in WEB.match('http://h.highpin.cn/ResumeManage/26566491@qq.com').group(0)
        >>> assert 'http://www.dajie.com/profile/W39a7xmS5fk*' in WEB.match('http://www.dajie.com/profile/W39a7xmS5fk*').group(0)
        >>> assert 'http://www.linkedin.com/search?search=&goback=%2Enmp_*1_*1&trk=prof-exp-company-name' in WEB.match('http://www.linkedin.com/search?search=&goback=%2Enmp_*1_*1&trk=prof-exp-company-name').group(0)
        >>> assert 'https://h.liepin.com/message/showmessage/#c:1' in WEB.match('https://h.liepin.com/message/showmessage/#c:1').group(0)
        >>> assert '2007' not in WEB.match('http://www.hindawi.com/journals/tswj/2014/465702/ 2007').group(0)
        >>> assert 'team.Desig' in WEB.match('team.Desig').group(0) # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        AttributeError: 'NoneType' object has no attribute 'group'
    """
    return reg.sub(sub, text)

def silencer(document):
    if isinstance(document, list):
        texts = document
    else:
        texts = [document]
    selected_texts = []
    for text in texts:
        text = re_sub(LINE, ' ', text)
        text = re_sub(WEB, '\n', text)
        text = re_sub(SYMBOL, ' ', text)
        words = jieba_cut(text, pos=True)
        words = pos_extract(words, FLAGS)
        out = []
        for word in words:
            if REJECT.match(word):
                continue
            if word.istitle():
                # Can make it match SHORT later for skip (eg 'Ltd' ...)
                word = word.lower()
            if not SHORT.match(word):
                # Even out tools and brands (eg 'CLEARCASE' vs 'clearcase')
                word = word.lower()
                out.append(word)
        selected_texts.append(out)
    if isinstance(document, list):
        return selected_texts
    else:
        return selected_texts[0]


class Mining(object):

    def __init__(self, path, cvsvc, slicer=None):
        self.sim = {}
        self.path = path
        self.lsi_model = dict()
        self.additionals = cvsvc.additionals
        self.services = {
                'default': {cvsvc.default.name: cvsvc.default},
                'all': dict([tuple([each.name, each])
                            for each in self.additionals+[cvsvc.default]])
            }
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        if slicer is None:
            self.slicer = silencer
        else:
            self.slicer = slicer
        self.make_lsi(self.services['default'])

    def setup(self, name):
        assert name in self.services
        self.add(self.services[name], name)

    def make_lsi(self, services):
        self.lsi_model = dict()
        for name in services:
            service = services[name]
            lsi_path = os.path.join(self.path, name, 'model')
            lsi = core.mining.lsimodel.LSImodel(lsi_path, slicer=self.slicer)
            try:
                lsi.load()
            except IOError:
                if lsi.build([service]):
                    lsi.save()
            self.lsi_model[name] = lsi

    def add(self, services, name):
        assert self.lsi_model
        for modelname in self.lsi_model:
            if not self.lsi_model[modelname].names:
                continue
            model = self.lsi_model[modelname]
            save_path = os.path.join(self.path, modelname, name)
            self.sim[modelname] = dict()
            for svc_name in services:
                svc = services[svc_name]
                index = core.mining.lsisimilarity.LSIsimilarity(os.path.join(save_path,
                                                                svc_name), model)
                try:
                    index.load()
                except IOError:
                    if index.build([svc]):
                        index.save()
                self.sim[modelname][svc_name] = index

    def update_model(self):
        for modelname in self.lsi_model:
            updated = self.lsi_model[modelname].update([self.services['default'][modelname]])
            if updated:
                self.update_sims()

    def update_sims(self):
        for modelname in self.sim:
            for simname in self.sim[modelname]:
                svc = self.services['all'][simname]
                self.sim[modelname][simname].update([svc])
                self.sim[modelname][simname].save()

    def probability(self, basemodel, doc, uses=None):
        if uses is None:
            uses = self.sim[basemodel].keys()
        result = []
        for name in uses:
            sim = self.sim[basemodel][name]
            result.extend(sim.probability(doc))
        return sorted(result, key=lambda x:float(x[1]), reverse=True)

    def probability_by_id(self, basemodel, doc, id, uses=None):
        if uses is None:
            uses = self.sim[basemodel].keys()
        result = tuple()
        for dbname in uses:
            sim = self.sim[basemodel][dbname]
            probability = sim.probability_by_id(doc, id)
            if probability is not None:
                result = probability
                break
        return result

    def lenght(self, basemodel, uses=None):
        if uses is None:
            uses = self.sim[basemodel].keys()
        result = 0
        for name in uses:
            sim = self.sim[basemodel][name]
            result += len(sim.names)
        return result

    def minetop(self, doc, basemodel, top=None, uses=None):
        results = self.probability(basemodel, doc, uses=uses)
        if top is None:
            top = len(results)
        return results[:top]

    def minelist(self, doc, lists, basemodel, uses=None):
        return map(lambda x: self.probability_by_id(basemodel, doc, x, uses=uses), lists)

    def minelistrank(self, doc, lists, basemodel, uses=None):
        probalist = set(self.probability(basemodel, doc, uses=uses))
        probalist.update(set(lists))
        ranklist = sorted(probalist, key=lambda x:float(x[1]), reverse=True)
        return map(lambda x: (x[0], ranklist.index(x)), lists)

    def default_names(self):
        return [name for name in self.services['default']]

    def addition_names(self):
        return [additional.name for additional in self.additionals]

    @property
    def SIMS(self):
        results = list()
        for modelname in self.lsi_model:
            for simname in self.sim[modelname]:
                results.append(self.sim[modelname][simname])
        return results

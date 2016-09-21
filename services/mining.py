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
DEMAIN = ur'([a-zA-Z0-9][\-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][\-a-zA-Z0-9]{0,62})*(\.(cn|CN|us|US|uk|jp|hk|com|COM|edu|gov|int|mil|net|org|biz)))'
IP = ur'((([1]?\d{1,2}|2[0-4]\d|25[0-5])\.){3}([1]?\d{1,2}|2[0-4]\d|25[0-5]))'
PORT = ur'(\:(6553[0-5]|655[0-2]\d|65[0-4]\d{2}|6[0-4]\d{3}|[1-5]\d{4}|[1-9]\d{0,3}|0))'
SERVICE = ur'((\/[^\/\s> 】）\)\]][\w\.\,\?\'\*\\\+&%\$#\=~_\-@]*)*([\(（【<\[][^\s \(\)（）\[\]<>【】]+[\)）】>\]])*[^\s \(\)<> （）【】\[\]]*)*'

WEB = re.compile(ur"(" + HEAD + ur'?' + UID + ur'?(' + DEMAIN + ur'|' + IP + ur')' + PORT + ur'?' + SERVICE + ur")")

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
        [测试计量技术及仪器](   )[测试计量技术及仪器]
        [测试计量技术及仪器] ( ) [测试计量技术及仪器]
        >>> s = "[测试计量技术及仪器] (www.test.com) [测试计量技术及仪器]"
        >>> print(re_sub(WEB, ' ', s))
        [测试计量技术及仪器] ( ) [测试计量技术及仪器]
        >>> s = "[测试计量技术及仪器] (test123@test.com) [测试计量技术及仪器]"
        >>> print(re_sub(WEB, ' ', s))
        [测试计量技术及仪器] ( ) [测试计量技术及仪器]
        >>> s = "--------------------\\n"
        >>> s += "英语(CET4)、普通话\\n"
        >>> s += "--------------------\\n"
        >>> print(re_sub(LINE, '', re_sub(SYMBOL, '', s)))
        英语(CET4)、普通话
        >>> assert u'http://search.51job.com/job/52405118,c.html' in WEB.search(u'http://search.51job.com/job/52405118,c.html').group(0)
        >>> assert u'https://h.liepin.com/soResume/?company=ASI+CONVEYORS(Shanghai)+CO.,LTD' in WEB.search(
        ...             u"https://h.liepin.com/soResume/?company=ASI+CONVEYORS(Shanghai)+CO.,LTD").group(0)
        >>> assert u'2014.06' not in WEB.search(u"https://h.liepin.com/cvsearch/soResume/?company=%AC%E5%8F%B8)2014.06").group(0)
        >>> assert u'bertwalker2005@yahoo.co.uk' in WEB.search(u'bertwalker2005@yahoo.co.uk').group(0)
        >>> assert u'http://h.highpin.cn/ResumeManage/26566491@qq.com' in WEB.search(u'http://h.highpin.cn/ResumeManage/26566491@qq.com').group(0)
        >>> assert u'http://www.dajie.com/profile/W39a7xmS5fk*' in WEB.search(u'http://www.dajie.com/profile/W39a7xmS5fk*').group(0)
        >>> assert u'http://www.linkedin.com/search?search=&goback=%2Enmp_*1_*1&trk=prof-exp-company-name' in WEB.search(u'http://www.linkedin.com/search?search=&goback=%2Enmp_*1_*1&trk=prof-exp-company-name').group(0)
        >>> assert u'https://h.liepin.com/message/showmessage/#c:1' in WEB.search(u'https://h.liepin.com/message/showmessage/#c:1').group(0)
        >>> assert u'2007' not in WEB.search(u'http://www.hindawi.com/journals/tswj/2014/465702/ 2007').group(0)
        >>> assert u'team.Desig' in WEB.search(u'team.Desig').group(0) # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        AttributeError: 'NoneType' object has no attribute 'group'
        >>> assert u'www.chineseanytime.com' in WEB.search(u'负责创业公司官方网站建设（已上线，网址www.chineseanytime.com）').group(0)
        >>> assert u'IP.COM' in WEB.search(u'IP.COM').group(0)
        >>> assert u'123456789@QQ.COM' in WEB.search(u'123456789@QQ.COM').group(0)
        >>> assert u'http://www.linkedin.com/vsearch/p?f_G=cn:8905&goback=.pyk_eml*4inv' in WEB.search(u'http://www.linkedin.com/vsearch/p?f_G=cn:8905&goback=.pyk_eml*4inv').group(0)
        >>> assert u'www.chineseanytime.com' == WEB.search(u'负责创业公司官方网站建设[已上线，网址www.chineseanytime.com]').group(0)
        >>> assert u'http://search.51job.com/job/18,c.html' == WEB.search('http://search.51job.com/job/18,c.html 广州乐电子科技有限公司是一家专业的超声公司'.decode('utf-8')).group(0)
        >>> assert 'http://www.test.com/company=贝恩医疗设备（广州）有限公司'.decode('utf-8') == WEB.search('http://www.test.com/company=贝恩医疗设备（广州）有限公司)由香港集团有限公司投资'.decode('utf-8')).group(0)
        >>> assert u'http://www.test.com/' == WEB.search('http://www.test.com/)由香某基集团有限公司投资'.decode('utf-8')).group(0)
        >>> assert u'http://www.test.com/' == WEB.search('http://www.test.com/】由某基集团有限公司投资'.decode('utf-8')).group(0)
        >>> assert u'http://www.test.com/' == WEB.search('http://www.test.com/>由香某基集团有限公司投资'.decode('utf-8')).group(0)
        >>> assert u'http://www.test.com/' == WEB.search('http://www.test.com/）由某基集团有限公司投资'.decode('utf-8')).group(0)
        >>> assert 'http://h.test.com/cv/soResume/?c=某医备(广州)有限公司'.decode('utf-8') == WEB.search('http://h.test.com/cv/soResume/?c=某医备(广州)有限公司'.decode('utf-8')).group(0)
        >>> assert 'http://h.test.com/cv/soResume/?c=某医备（广州）有限公司'.decode('utf-8') == WEB.search('http://h.test.com/cv/soResume/?c=某医备（广州）有限公司'.decode('utf-8')).group(0)
        >>> assert 'http://h.test.com/cv/soResume/?c=%AC%E5%8F%B8'.decode('utf-8') == WEB.search('http://h.test.com/cv/soResume/?c=%AC%E5%8F%B8)2014.06'.decode('utf-8')).group(0)
        >>> assert 'http://h.test.com/cv/soResume/?c=中国集团（央企）业——长沙有限公司'.decode('utf-8') == WEB.search('http://h.test.com/cv/soResume/?c=中国集团（央企）业——长沙有限公司)2010.07'.decode('utf-8')).group(0)
        >>> assert 'http://h.test.com/cv/soResume/?c=浙江院附属第一医院(浙江省第一医院)'.decode('utf-8') == WEB.search('http://h.test.com/cv/soResume/?c=浙江院附属第一医院(浙江省第一医院)'.decode('utf-8')).group(0)
        >>> assert 'http://h.test.com/cv/soResume/?c=深圳生物医疗电子有限公司（www.mindray.com）'.decode('utf-8') == WEB.search('http://h.test.com/cv/soResume/?c=深圳生物医疗电子有限公司（www.mindray.com）'.decode('utf-8')).group(0)
        >>> assert 'http://h.test.com/cv/soResume/?c=天津XX集团有限公司[电话15900376608]'.decode('utf-8') == WEB.search('http://h.test.com/cv/soResume/?c=天津XX集团有限公司[电话15900376608]'.decode('utf-8')).group(0)
        >>> assert 'http://h.test.com/cv/soResume/?c=天津XX集团有限公司(电话15900376608)'.decode('utf-8') == WEB.search('http://h.test.com/cv/soResume/?c=天津XX集团有限公司(电话15900376608)'.decode('utf-8')).group(0)
        >>> assert 'http://h.test.com/cv/soResume/?c=(天津)+XX+(集团)有限公司(电话15900376608)'.decode('utf-8') == WEB.search('http://h.test.com/cv/soResume/?c=(天津)+XX+(集团)有限公司(电话15900376608)'.decode('utf-8')).group(0)
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
        self.lsi_model = None
        self.services = {
                'default': [cvsvc.default],
                'all': cvsvc.svcls
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

    def make_lsi(self, service):
        self.lsi_model = None
        lsi_path = os.path.join(self.path, 'model')
        lsi = core.mining.lsimodel.LSImodel(lsi_path, slicer=self.slicer)
        try:
            lsi.load()
        except IOError:
            if lsi.build(service):
                lsi.save()
        self.lsi_model = lsi

    def add(self, svc_list, name):
        assert self.lsi_model
        save_path = os.path.join(self.path, name)
        for svc in svc_list:
            assert svc.name
            index = core.mining.lsisimilarity.LSIsimilarity(os.path.join(save_path, svc.name), self.lsi_model)
            try:
                index.load()
            except IOError:
                if index.build([svc]):
                    index.save()
            self.sim[svc.name] = index

    def update_model(self):
        updated = self.lsi_model.update(self.services['default'])
        if updated:
            self.update_sims()

    def update_sims(self):
        for name in self.services:
            for svc in self.services[name]:
                self.sim[svc.name].update([svc])
                self.sim[svc.name].save()

    def probability(self, doc, uses=None):
        if uses is None:
            uses = self.sim.keys()
        result = []
        for name in uses:
            sim = self.sim[name]
            result.extend(sim.probability(doc))
        return sorted(result, key=lambda x:float(x[1]), reverse=True)

    def probability_by_id(self, doc, id, uses=None):
        if uses is None:
            uses = self.sim.keys()
        result = tuple()
        for dbname in uses:
            sim = self.sim[dbname]
            probability = sim.probability_by_id(doc, id)
            if probability is not None:
                result = probability
                break
        return result

    def lenght(self, uses=None):
        if uses is None:
            uses = self.sim.keys()
        result = 0
        for name in uses:
            sim = self.sim[name]
            result += len(sim.names)
        return result

    def minetop(self, doc, top=None, uses=None):
        results = self.probability(doc, uses=uses)
        if top is None:
            top = len(results)
        return results[:top]

    def minelist(self, doc, lists, uses=None):
        return map(lambda x: self.probability_by_id(doc, x, uses=uses), lists)

    def minelistrank(self, doc, lists, uses=None):
        probalist = set(self.probability(doc, uses=uses))
        probalist.update(set(lists))
        ranklist = sorted(probalist, key=lambda x:float(x[1]), reverse=True)
        return map(lambda x: (x[0], ranklist.index(x)), lists)

    def default_names(self):
        return [n.name for n in self.services['default'] if n.name in self.sim.keys()]

    def addition_names(self):
        names = self.sim.keys()
        for n in self.default_names():
            names.remove(n)
        return names

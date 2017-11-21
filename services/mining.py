# -*- coding: utf-8 -*-
import os
import re
import math

import core.basedata
import core.mining.lsimodel
import core.mining.lsisimilarity

from utils.builtin import jieba_cut, pos_extract, industrytopath


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
SERVICE = ur'(\/(([\(（【<\[][^\s \(\)（）\[\]<>【】]+[\)）】>\]])*[^\s ，\(\)<> （）【】\[\]]*)*)*'

WEB = re.compile(ur"(" + HEAD + ur'?' + UID + ur'?(' + DEMAIN + ur'|' + IP + ur')' + PORT + ur'?' + SERVICE + ur")")

DOT_NET = re.compile(ur'((vs|VS|C#|c#|asp|ASP|Asp|ADO|ado)\.(Net|net|NET))')

SYMBOL = re.compile(ur'[- /]+')
SHORT = re.compile('(([a-z]\d{0,2})|([a-z]{1,4})|[\d\.]{1,11})$')


FLAGS = ['x', # spaces
         'm', # number and date
         #'a', # adverb
         'ad', 'an',
         'c', # conjunction
         'd', 'df', # adverb
         'e', # interjection
         'f', # noun of locality
         'g', # morpheme word
         'h', # prefix
         'i', # idiom
         #'j', # abbreviation
         'k', # suffix
         'm', 'mq',
         'nrt', 'nr', 'ng', 'nrfg', 'ngrf', #'nz', fails on myjnoee7.md
         'o', # onomatopoeia
         'p', # preposition
         'q', # quantifier
         'r', 'rg', 'rr', # pronoun
         's', #space
         't', 'tg', # time root word
         'u', 'ug', # unclassified (eg. etc)
         'vi', 'vd', 'vg', 'vq',  # verb morpheme word
         #'v', # verb
         'y', # statement label designator
         'z', 'zg', # State word
         #'ns', # city and country
        ]

def re_sub(reg, repl, text):
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
        >>> assert u'asp.net' in re_sub(WEB, repl_web, '使用asp.net，ado.net进行业务开发'.decode('utf-8'))
        >>> assert u'C#.Net' in re_sub(WEB, repl_web, '使用C#.Net进行业务开发'.decode('utf-8'))
        >>> assert u'yu_yinghui@yeah.net' not in re_sub(WEB, repl_web, 'emailto: yu_yinghui@yeah.net'.decode('utf-8'))
        >>> assert u'EHS.CN' == WEB.search('EHS.CN于2011年12月前成功上线'.decode('utf-8')).group(0)
    """
    return reg.sub(repl, text)

def repl_web(m):
    if DOT_NET.search(m.group(0)) is not None:
        return m.group(0)
    else:
        return '\n'

def silencer(document, cutservice=None, id=None):
    if isinstance(id, unicode):
        id = id.encode('utf-8')
    if (cutservice and id) and cutservice.exists(id):
        return cutservice.getyaml(id)['words']
    if isinstance(document, list):
        texts = document
    else:
        texts = [document]
    selected_texts = []
    for text in texts:
        text = re_sub(LINE, ' ', text)
        text = re_sub(WEB, repl_web, text)
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
            if SHORT.match(word):
                continue
                # Even out tools and brands (eg 'CLEARCASE' vs 'clearcase')
            if len(word) == 1:
                continue
            word = word.lower()
            out.append(word)
        selected_texts.append(out)
    if isinstance(document, list):
        result = selected_texts
    else:
        result = selected_texts[0]
    if cutservice and id:
        cutobj = core.basedata.DataObject(metadata={'id': id, 'words': result},
                                          data=None)
        cutservice.add(cutobj)
    return result


class Mining(object):

    SIMS_PATH = 'all'

    def __init__(self, path, slicer=None):
        self.sim = dict()
        self.path = path
        self.lsi_model = dict()
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        if slicer is None:
            self.slicer = silencer
        else:
            self.slicer = slicer

    def setup(self, modelname, simnames):
        result = True
        if modelname not in self.lsi_model:
            result = self.init_lsi(modelname)
        if result is True:
            model = self.lsi_model[modelname]
            if model.names:
                if modelname not in self.sim:
                    self.sim[modelname] = dict()
                for simname in simnames:
                    if simname in self.sim[modelname]:
                        continue
                    self.init_sim(modelname, simname)
        return result

    def init_sim(self, modelname, svc_name, gen=None):
        model = self.lsi_model[modelname]
        save_path = os.path.join(self.path, modelname, self.SIMS_PATH)
        industrypath = industrytopath(svc_name)
        index = core.mining.lsisimilarity.LSIsimilarity(svc_name,
                                                        os.path.join(save_path,
                                                        industrypath), model)
        try:
            index.load()
        except IOError:
            if gen is None:
                gen = list()
            index.build(gen)
            index.save()
        self.sim[modelname][svc_name] = index

    def getsims(self, basemodel, uses=None):
        sims = []
        if uses is None:
            try:
                uses = self.sim[basemodel].keys()
            except KeyError:
                return sims
        for each in uses:
            try:
                sim = self.sim[basemodel][each]
            except KeyError:
                continue
            sims.append(sim)
        return sims

    def init_lsi(self, modelname, gen=None, config=None):
        result = False
        if modelname not in self.lsi_model:
            lsi_path = os.path.join(self.path, modelname, 'model')
            lsi = core.mining.lsimodel.LSImodel(modelname, lsi_path,
                                                slicer=self.slicer,
                                                no_above=1./3, config=config)
            try:
                lsi.load()
                result = True
            except IOError:
                if gen is not None and lsi.getconfig('autosetup') is True:
                    result = lsi.build(gen)
                    if result is True:
                        lsi.load_config()
                        lsi.save()
            self.lsi_model[modelname] = lsi
        return result

    def probability(self, basemodel, doc, uses=None, top=None, minimum=None):
        result = []
        sims = self.getsims(basemodel, uses=uses)
        for sim in sims:
            result.extend(sim.probability(doc, top=top, minimum=minimum))
        results_set = set(result)
        return sorted(results_set, key=lambda x:float(x[1]), reverse=True)

    def probability_by_id(self, basemodel, doc, id, uses=None):
        result = tuple()
        sims = self.getsims(basemodel, uses=uses)
        for sim in sims:
            probability = sim.probability_by_id(doc, id)
            if probability is not None:
                result = probability
                break
        return result

    def idsims(self, modelname, ids):
        results = list()
        for id in ids:
            for sim in self.sim[modelname].values():
                if id in sim.names:
                    results.append(sim.name)
                    break
        return results

    def minetop(self, doc, basemodel, top=None, uses=None):
        results = self.probability(basemodel, doc, top=top, uses=uses)
        return results

    def minelist(self, doc, lists, basemodel, uses=None):
        result = list()
        for name in lists:
            uses = list()
            for sim in self.sim[basemodel].values():
                if sim.exists(name):
                    uses.append(sim.name)
                    break
            result.append(self.probability_by_id(basemodel, doc, name, uses=uses))
        return result

    def minelistrank(self, doc, lists, basemodel, uses=None, top=None, minimum=None):
        if uses is None:
            uses = list()
            for name, value in lists:
                for sim in self.sim[basemodel].values():
                    if sim.exists(name):
                        uses.append(sim.name)
        probalist = set(self.probability(basemodel, doc, uses=uses,
                                         top=top, minimum=minimum))
        probalist.update(set(lists))
        ranklist = sorted(probalist, key=lambda x:float(x[1]), reverse=True)
        return len(ranklist), map(lambda x: (x[0], ranklist.index(x)), lists)

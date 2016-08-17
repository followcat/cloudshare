# -*- coding: utf-8 -*-
import os
import re
import core.mining.lsimodel
import core.mining.lsisimilarity

import jieba.posseg


REJECT = re.compile('(('+')|('.join([
    u'中文', u'日期', u'汽车',
    #u'个人', u'未填写',
    #u'财务',
    #u'招聘', u'英才网', u'人力',
    u'互联网',
    ])+'))')

def silencer(document):
        FLAGS = ['x', # spaces
                 'm', # number and date
                 'a', # adverb
                 'i', 'j',
                 'nrt', 'nr', 'ns', #'nz', fails on myjnoee7.md
                 'u', # unclassified (eg. etc)
                 'f', # time and place
                 'q', # quantifier
                 'p', # preposition
                 'v', # vernicular expression
                 'ns', # city and country
                ]
        LINE = re.compile(ur'[\n- /]+')
        SBHTTP = re.compile(ur'\(https?:.*\)(?=\s)')
        BHTTP = re.compile(ur'\(https?:.*?\)')
        HTTP = re.compile(ur'https?:\S*(?=\s)')
        WWW = re.compile('www\.[\.\w]+')
        EMAIL = re.compile('\w+@[\.\w]+')
        SHORT = re.compile('(([a-z]\d{0,2})|([a-z]{1,4})|[\d\.]{1,11})$')
        if isinstance(document, list):
            texts = document
        else:
            texts = [document]
        selected_texts = []
        for text in texts:
            text = HTTP.sub('\n', BHTTP.sub('\n', SBHTTP.sub('\n', LINE.sub(' ', text))))
            text = WWW.sub('', EMAIL.sub('', text))
            doc = [word.word for word in jieba.posseg.cut(text) if word.flag not in FLAGS]
            out = []
            for d in doc:
                if REJECT.match(d):
                    continue
                if d.istitle():
                    # Can make it match SHORT later for skip (eg 'Ltd' ...)
                    d = d.lower()
                if not SHORT.match(d):
                    # Even out tools and brands (eg 'CLEARCASE' vs 'clearcase')
                    d = d.lower()
                    out.append(d)
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
        self.services = {
                'default': cvsvc.dbcenter,
                'additionals': cvsvc.additionals,
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

    def make_lsi(self, services):
        self.lsi_model = dict()
        for service in services:
            lsi_path = os.path.join(self.path, service.name, 'model')
            lsi = core.mining.lsimodel.LSImodel(lsi_path, slicer=self.slicer)
            try:
                lsi.load()
            except IOError:
                if lsi.build([service]):
                    lsi.save()
            self.lsi_model[service.name] = lsi

    def add(self, svc_list, name):
        assert self.lsi_model
        for modelname in self.lsi_model:
            if not self.lsi_model[modelname].names:
                continue
            model = self.lsi_model[modelname]
            save_path = os.path.join(self.path, modelname, name)
            self.sim[modelname] = dict()
            for svc in svc_list:
                assert svc.name
                index = core.mining.lsisimilarity.LSIsimilarity(os.path.join(save_path,
                                                                svc.name), model)
                try:
                    index.load()
                except IOError:
                    if index.build([svc]):
                        index.save()
                self.sim[modelname][svc.name] = index

    def update_model(self):
        for modelname in self.lsi_model:
            updated = self.lsi_model[modelname].update(self.services['default'][modelname])
            if updated:
                self.update_sims()

    def update_sims(self):
        for modelname in self.lsimodel:
            for name in self.services:
                for svc in self.services[name]:
                    self.sim[modelname][svc.name].update([svc])
                    self.sim[modelname][svc.name].save()

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
        return [n.name for n in self.services['default']]

    def addition_names(self):
        return [n.name for n in self.services['additionals']]

    @property
    def SIMS(self):
        results = list()
        for modelname in self.lsimodel:
            for sim in self.sim[modelname]:
                results.append(sim)
        return results

# -*- coding: utf-8 -*-
import os
import re
import core.mining.lsimodel
import core.mining.lsisimilarity

import jieba.posseg


REJECT = re.compile('(('+')|('.join([
    u'中文', u'日期', u'汽车',
    #u'个人', u'未填写',
    u'财务',
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

    def __init__(self, path, svc_list, default_svc, slicer=None):
        self.sim = {}
        self.path = path
        self.lsi_model = None
        self.services = {
                'default': [default_svc],
                'all': svc_list
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
        return self.sim[name]

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
        index = core.mining.lsisimilarity.LSIsimilarity(save_path, self.lsi_model)
        try:
            index.load()
        except IOError:
            if index.build(svc_list):
                index.save()
        self.sim[name] = index

    def update(self):
        self.lsi_model.update(self.services['default'])
        for name in self.sim:
            self.sim[name].update(self.services[name])

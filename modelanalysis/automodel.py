# -*- coding: utf-8 -*-
import os
import re
import glob
import collections

import services.mining
import core.mining.lsimodel
from utils.builtin import jieba_cut, pos_extract

import modelanalysis.judge


def gen_models(sources, path, maxmodels=None, flags=None, regression=False, autosave=False):
    """
        >>> from modelanalysis.automodel import *
        >>> from baseapp.projects import *
        >>> sources = dict(map(lambda x: (x['id'], x['description']),
        ...                SVC_PRJ_MED.jobdescription.lists()))
        >>> am = gen_models(sources, '/tmp/genmodel', maxmodels=10)
    """
    g = Automodels(sources, path, maxmodels, flags)
    results = list()
    for k in g.model_generate(autosave, regression=regression):
        results.append(k)
    return g

class Automodels(object):

    FLAGS = ['s', 'x']

    def __init__(self, sources, path, maxmodels=None, flags=None):
        """
            >>> from modelanalysis.automodel import *
            >>> from baseapp.projects import *
            >>> sources = dict(map(lambda x: (x['id'], x['description']),
            ...                SVC_PRJ_MED.jobdescription.lists()))
            >>> am = Automodels(sources, '/tmp/automodel')
            >>> gen = am.model_generate(autosave=False)
            >>> model = gen.next()
        """
        if flags is not None:
            self.FLAGS = flags
        self.path = path
        self.models = []
        self.sources = sources
        self.maxmodels = maxmodels

    def load(self):
        models_dump = glob.glob(os.path.join(self.path, '*'))
        models_num = len(models_dump)
        self.models = [None]*models_num
        for f in models_dump:
            index = int(os.path.split(f)[-1])
            self.models[index] = core.mining.lsimodel.LSImodel(f)
            self.models[index].load()

    def unit_gen(self, sources):
        for id in sources:
            for unit in sources[id]:
                yield id, unit

    def source_reloaded(self):
        d = collections.defaultdict(dict) 
        for id in self.sources:
            d[id] = collections.defaultdict(dict)
            for unit in re.split(u'[\n,.。，;]', self.sources[id]):
                d[id][unit] = {'used': set(),
                               'todo': set(pos_extract(jieba_cut(unit, pos=True),
                                           self.FLAGS))}
        return d

    def model_generate(self, autosave=False, path=None, regression=False):
        if path is None:
            path = self.path
        sources = self.source_reloaded()
        for id in sources:
            for requirement in sources[id]:
                model = self.train_model(id, requirement, regression)
                if model is None:
                    continue
                yield model

    def pick_model(self, id, requirement, effectline=1.5):
        candidates = dict()
        for model in self.models:
            candidates[model] = modelanalysis.judge.probably(requirement, model)
        results = sorted(candidates.items(), key=lambda d:d[1], reverse=True)
        if results and results[0][1] > effectline:
            model = results[0][0]
        else:
            if self.maxmodels is None or len(self.models) < self.maxmodels:
                model = self.new_model(id, requirement)
            else:
                try:
                    model = results[0][0]
                except IndexError:
                    model = None
        return model

    def new_model(self, id, unit):
        model = core.mining.lsimodel.LSImodel(self.path)
        model.slicer = services.mining.silencer
        return model

    def upgrade_model(self, model, id, requirement):
        result = True
        try:
            model.setup(model.names+[id], model.texts+[model.slicer(requirement)])
        except ValueError:
            result = False
        return result

    def regression_model(self, resources, model):
        def judge_model(self, resource, model, skyline=2):
            result = False
            if model.slicer(resource) not in model.texts:
                try:
                    sumgood = modelanalysis.judge.linalg(resource, model)
                    result = sumgood > skyline
                except TypeError:
                    pass
            return result
        while(resources):
            for reid, resource in self.unit_gen(resources):
                if judge_model(resource, model):
                    try:
                        model.setup(model.names+[reid], model.texts+[model.slicer(resource)])
                    except ValueError:
                        continue
                    resources.pop(reid)
                    break
            else:
                break

    def train_model(self, id, requirement, regression=False):
        model = self.pick_model(id, requirement)
        result = self.upgrade_model(model, id, requirement)
        if result:
            if regression:
                resources = self.source_reloaded()
                resources.pop(id)
                self.regression_model(resources, model)
            if model not in self.models:
                self.models.append(model)
        else:
            model = None
        return model

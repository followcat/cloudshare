# -*- coding: utf-8 -*-
import os
import re
import glob
import collections

import services.mining
import core.mining.lsimodel
from utils.builtin import jieba_cut, pos_extract

import modelanalysis.judge


def gen_models(sources, path, flags=None):
    """
        >>> from modelanalysis.automodel import *
        >>> from baseapp.projects import *
        >>> sources = dict(map(lambda x: (x['id'], x['description']),
        ...                SVC_PRJ_MED.jobdescription.lists()[:10]))
        >>> gen_models(sources, '/tmp/genmodel')
    """
    g = Automodels(sources, path, flags)
    results = list()
    for k in g.model_generate():
        results.append(k)
    return results

class Automodels(object):

    FLAGS = ['s', 'x']

    def __init__(self, sources, path, flags=None):
        """
            >>> from modelanalysis.automodel import *
            >>> from baseapp.projects import *
            >>> sources = dict(map(lambda x: (x['id'], x['description']),
            ...                SVC_PRJ_MED.jobdescription.lists()[:10]))
            >>> am = Automodels(sources, '/tmp/automodel')
            >>> gen = am.model_generate(autosave=False)
        """
        if flags is not None:
            self.FLAGS = flags
        self.path = path
        self.models = []
        self.sources = sources

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

    def model_generate(self, autosave=False, path=None):
        if path is None:
            path = self.path
        sources = self.source_reloaded()
        for id in sources:
            for requirement in sources[id]:
                indexs = self.train_by_model(id, requirement)
                if not indexs:
                    continue
                yield self.models[indexs[0]]

    def origin_model(self, id, unit):
        model = core.mining.lsimodel.LSImodel(self.path)
        model.slicer = services.mining.silencer
        try:
            model.setup([id], [model.slicer(unit)])
        except ValueError:
            model.names.append(id)
            model.texts.append(model.slicer(unit))
        return model

    def judge_model(self, resource, model, skyline=1.5):
        result = False
        try:
            sumgood = modelanalysis.judge.linalg(resource, model)
            result = sumgood > skyline
        except TypeError:
            pass
        return result

    def train_by_model(self, id, requirement):
        indexs = []
        model = self.origin_model(id, requirement)
        resources = self.source_reloaded()
        resources.pop(id)
        while(resources):
            for reid, resource in self.unit_gen(resources):
                if self.judge_model(requirement, model):
                    try:
                        model.setup(model.names+[reid], model.texts+[model.slicer(resource)])
                    except ValueError:
                        continue
                    resources.pop(reid)
                    break
            else:
                break
        if model not in self.models:
            self.models.append(model)
        indexs.append(self.models.index(model))
        return indexs
# -*- coding: utf-8 -*-

import re
import collections

import services.mining
import core.mining.lsimodel
from utils.builtin import jieba_cut, pos_extract

import modelanalysis.judge


class Automodels(object):

    FLAGS = ['s', 'x']

    def __init__(self, sources, flags=None):
        """
            >>> from modelanalysis.automodel import *
            >>> from baseapp.projects import *
            >>> sources = dict(map(lambda x: (x['id'], x['description']),
            ...                 SVC_PRJ_MED.jobdescription.lists()))
            >>> am = Automodels(sources)
            >>> models = am.gen_models()
        """
        if flags is not None:
            self.FLAGS = flags
        self.sources = sources

    def unit_gen(self, sources):
        for id in sources:
            for unit in sources[id]:
                yield id, unit

    def source_list(self):
        d = dict()
        for id in self.sources:
            d[id] = self.sources[id].keys()
        return d

    def source_reloaded(self):
        d = collections.defaultdict(dict) 
        for id in self.sources:
            d[id] = collections.defaultdict(dict)
            for unit in re.split(u'[\n,.。，;]', self.sources[id]):
                d[id][unit] = {'used': set(),
                                   'todo': set(pos_extract(jieba_cut(unit, pos=True),
                                                           self.FLAGS))}
        return d

    def origin_unit(self, sources, used_units, todos):
        for id in sources:
            for inputunit in sources[id]:
                if inputunit not in used_units:
                    for todo in todos:
                        if todo in inputunit:
                            return inputunit

    def gen_models(self):
        models = []
        sources = self.source_reloaded()
        for id in sources:
            for unit in sources[id]:
                used_units = list()
                while(sources[id][unit]['todo']):
                    inputunit = self.origin_unit(sources, used_units, sources[id][unit]['todo'])
                    if inputunit is None:
                        break
                    used_units.append(inputunit)
                    indexs = self.train_by_model(id, inputunit, sources, models) # train_by_source
                    if not indexs:
                        continue
                    for index in indexs:
                        finished = set(models[index].dictionary.values()).intersection(
                                       sources[id][unit]['todo'])
                        for finish in finished:
                            sources[id][unit]['todo'].remove(finish)
                            sources[id][unit]['used'].add(finish)
        return models

    def origin_model(self, id, unit):
        model = core.mining.lsimodel.LSImodel('')
        model.slicer = services.mining.silencer
        try:
            model.setup([id], [model.slicer(unit)])
        except ValueError:
            model.names.append(id)
            model.texts.append(model.slicer(unit))
        return model


    def train_by_source(self, id, requirement, sources, models, skyline=1.5):
        des = self.source_reloaded()
        indexs = []
        while(des):
            index = None
            for i in range(len(models)):
                sumgood = modelanalysis.judge.linalg(requirement, models[i])
                if sumgood > skyline:
                    index = i
                    model = models[i]
            else:
                try:
                    model = origin_model(id, requirement)
                except ValueError:
                    continue
            for id, unit in unit_gen(des):
                sumgood = modelanalysis.judge.linalg(unit, model)
                if sumgood > skyline:
                    model = core.mining.lsimodel.LSImodel('/tmp/lsimodel')
                    model.slicer = services.mining.silencer
                    try:
                        model.setup(model.names+[id], model.texts+[model.slicer(unit)])
                    except ValueError:
                        continue
                    if index is None:
                        models.append(model)
                        index = models.index(model)
                    else:
                        models[index] = model
                    des.pop(id)
                    indexs.append(index)
                    break
            else:
                break
        return indexs


    def train_by_model(self, id, requirement, sources, models, skyline=1.5):
        indexs = []
        index = None
        model = self.origin_model(id, requirement)
        resources = self.source_reloaded()
        resources.pop(id)
        while(resources):
            for reid, resource in self.unit_gen(resources):
                sumgood = modelanalysis.judge.linalg(resource, model)
                if sumgood > skyline:
                    try:
                        model.setup(model.names+[reid], model.texts+[model.slicer(resource)])
                    except ValueError:
                        continue
                    resources.pop(reid)
                    break
            else:
                break
        if model.names:
            models.append(model)
            indexs.append(models.index(model))
        return indexs

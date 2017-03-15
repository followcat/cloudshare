# -*- coding: utf-8 -*-
import os
import re
import glob
import collections

import services.mining
import core.mining.lsimodel
from utils.builtin import jieba_cut, pos_extract

import modelanalysis.judge


class Automodels(object):

    FLAGS = ['s', 'x']

    def __init__(self, sources, path, flags=None):
        """
            >>> from modelanalysis.automodel import *
            >>> from baseapp.projects import *
            >>> sources = dict(map(lambda x: (x['id'], x['description']),
            ...                SVC_PRJ_MED.jobdescription.lists()))
            >>> am = Automodels(sources, '/tmp/automodel')
            >>> models = am.gen_models(autosave=False)
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

    def origin_unit(self, sources, used_units, todos):
        for id in sources:
            for inputunit in sources[id]:
                if inputunit not in used_units:
                    for todo in todos:
                        if todo in inputunit:
                            return inputunit

    def gen_models(self, autosave=False, path=None):
        if path is None:
            path = self.path
        sources = self.source_reloaded()
        for id in sources:
            for unit in sources[id]:
                used_units = list()
                while(sources[id][unit]['todo']):
                    inputunit = self.origin_unit(sources, used_units, sources[id][unit]['todo'])
                    if inputunit is None:
                        break
                    used_units.append(inputunit)
                    indexs = self.train_by_model(id, inputunit, sources)
                    if not indexs:
                        continue
                    for index in indexs:
                        if autosave is True:
                            self.models[index].save(os.path.join(path, str(index)))
                        finished = set(self.models[index].dictionary.values()).intersection(
                                       sources[id][unit]['todo'])
                        for finish in finished:
                            sources[id][unit]['todo'].remove(finish)
                            sources[id][unit]['used'].add(finish)

    def origin_model(self, id, unit):
        model = core.mining.lsimodel.LSImodel(self.path)
        model.slicer = services.mining.silencer
        try:
            model.setup([id], [model.slicer(unit)])
        except ValueError:
            model.names.append(id)
            model.texts.append(model.slicer(unit))
        return model

    def train_by_model(self, id, requirement, sources, skyline=1.5):
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
            self.models.append(model)
            indexs.append(self.models.index(model))
        return indexs

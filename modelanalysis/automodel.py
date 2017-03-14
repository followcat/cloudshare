# -*- coding: utf-8 -*-

import re
import collections

import services.mining
import core.mining.lsimodel
from utils.builtin import jieba_cut, pos_extract

import modelanalysis.judge


def unit_gen(sources):
    for source in sources:
        for unit in sources[source]:
            yield source, unit


def source_list(sources):
    d = dict()
    for source in sources:
        d[source] = sources[source].keys()
    return d


def source_reloaded(sources):
    d = collections.defaultdict(dict) 
    for source in sources:
        d[source] = collections.defaultdict(dict)
        for unit in re.split(u'[\n,.。，;]', sources[source]):
            d[source][unit] = {'used': set(),
                               'todo': set(pos_extract(jieba_cut(unit, pos=True),
                                                       ['s', 'x']))}
    return d


def origin_unit(sources, used_units, todos):
    for source in sources:
        for inputunit in sources[source]:
            if inputunit not in used_units:
                for todo in todos:
                    if todo in inputunit:
                        return inputunit


def gen_models(sources):
    """
        >>> from modelanalysis.automodel import *
        >>> from baseapp.projects import *
        >>> sources = dict(map(lambda x: (x['id'], x['description']),
        ...                 SVC_PRJ_MED.jobdescription.lists()))
        >>> loaded_sources = source_reloaded(sources)
        >>> models = gen_models(loaded_sources)
    """
    models = []
    for source in sources:
        for unit in sources[source]:
            used_units = list()
            while(sources[source][unit]['todo']):
                inputunit = origin_unit(sources, used_units, sources[source][unit]['todo'])
                if inputunit is None:
                    break
                used_units.append(inputunit)
                indexs = train_by_source(source, inputunit, sources, models)
                if not indexs:
                    continue
                for index in indexs:
                    finished = set(models[index].dictionary.values()).intersection(
                                   sources[source][unit]['todo'])
                    for finish in finished:
                        sources[source][unit]['todo'].remove(finish)
                        sources[source][unit]['used'].add(finish)
        break
    return models

def origin_model(source, unit):
    model = core.mining.lsimodel.LSImodel('')
    model.slicer = services.mining.silencer
    model.setup([source], [model.slicer(unit)])
    return model

def train_by_source(source, requirement, sources, models, skyline=1.5):
    des = source_list(sources)
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
                model = origin_model(source, requirement)
            except ValueError:
                continue
        for source, unit in unit_gen(des):
            sumgood = modelanalysis.judge.linalg(unit, model)
            if sumgood > skyline:
                names = model.names
                texts = model.texts
                model = core.mining.lsimodel.LSImodel('/tmp/lsimodel')
                model.slicer = services.mining.silencer
                names.append(requirement)
                texts.append(model.slicer(unit))
                try:
                    model.setup(names, texts)
                except ValueError:
                    continue
                if index is None:
                    models.append(model)
                    index = models.index(model)
                else:
                    models[index] = model
                des.pop(source)
                indexs.append(index)
                break
        else:
            break
    return indexs

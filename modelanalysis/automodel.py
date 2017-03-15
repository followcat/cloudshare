# -*- coding: utf-8 -*-

import re
import collections

import services.mining
import core.mining.lsimodel
from utils.builtin import jieba_cut, pos_extract

import modelanalysis.judge


def unit_gen(sources):
    for id in sources:
        for unit in sources[id]:
            yield id, unit


def source_list(sources):
    d = dict()
    for id in sources:
        d[id] = sources[id].keys()
    return d


def source_reloaded(sources):
    d = collections.defaultdict(dict) 
    for id in sources:
        d[id] = collections.defaultdict(dict)
        for unit in re.split(u'[\n,.。，;]', sources[id]):
            d[id][unit] = {'used': set(),
                               'todo': set(pos_extract(jieba_cut(unit, pos=True),
                                                       ['s', 'x']))}
    return d


def origin_unit(sources, used_units, todos):
    for id in sources:
        for inputunit in sources[id]:
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
    for id in sources:
        for unit in sources[id]:
            used_units = list()
            while(sources[id][unit]['todo']):
                inputunit = origin_unit(sources, used_units, sources[id][unit]['todo'])
                if inputunit is None:
                    break
                used_units.append(inputunit)
                indexs = train_by_source(id, inputunit, sources, models)
                if not indexs:
                    continue
                for index in indexs:
                    finished = set(models[index].dictionary.values()).intersection(
                                   sources[id][unit]['todo'])
                    for finish in finished:
                        sources[id][unit]['todo'].remove(finish)
                        sources[id][unit]['used'].add(finish)
        break
    return models


def origin_model(id, unit):
    model = core.mining.lsimodel.LSImodel('')
    model.slicer = services.mining.silencer
    try:
        model.setup([id], [model.slicer(unit)])
    except ValueError:
        model.names.append(id)
        model.texts.append(model.slicer(unit))
    return model


def train_by_source(id, requirement, sources, models, skyline=1.5):
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
                model = origin_model(id, requirement)
            except ValueError:
                continue
        for id, unit in unit_gen(des):
            sumgood = modelanalysis.judge.linalg(unit, model)
            if sumgood > skyline:
                model = core.mining.lsimodel.LSImodel('/tmp/lsimodel')
                model.slicer = services.mining.silencer
                try:
                    model.setup(model.names+[requirement], model.texts+[model.slicer(unit)])
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

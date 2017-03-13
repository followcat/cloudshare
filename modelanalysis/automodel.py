# -*- coding: utf-8 -*-

import re
import collections

import services.mining
import core.mining.lsimodel
from utils.builtin import jieba_cut, pos_extract

import modelanalysis.judge


def add_one_source(source, unit, des, models, skyline=1.5):
    result = False
    index = None
    for i in range(len(models)):
        sumgood = modelanalysis.judge.linalg(unit, models[i])
        if sumgood > skyline:
            index = i
            model = models[i]
    else:
        try:
            model = origin_model(source, unit)
        except ValueError:
            return result, unit, index
    model.slicer = services.mining.silencer
    for requirement in des:
        for unit in des[requirement]:
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
                result = True
                break
        if result:
            break
    if result:
        if index is None:
            models.append(model)
            index = models.index(model)
        else:
            models[index] = model
    return result, requirement, index

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
                indexs = train(source, inputunit, sources, models)
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

def train(source, unit, sources, models):
    des = source_list(sources)
    indexs = []
    while(des):
        result, requirement, index = add_one_source(source, unit, des, models)
        if result:
            des.pop(requirement)
            indexs.append(index)
        else:
            break
    return indexs

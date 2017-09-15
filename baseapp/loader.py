import os
import yaml
import functools

import services.index
import services.mining
import services.multiclsify
import services.analysis.cutword


SUPPORT_DOCPROCESSOR = {}
try:
    import utils.docprocessor.pandoc
    SUPPORT_DOCPROCESSOR['pandoc'] = utils.docprocessor.pandoc.PandocProcessor
except ImportError:
    pass

try:
    import utils.docprocessor.libreoffice
    SUPPORT_DOCPROCESSOR['libreoffice'] = utils.docprocessor.libreoffice.LibreOfficeProcessor
except ImportError:
    pass


LSI_PATH = 'lsimodel'
CONFIG_PATH = 'config'
CUTWORD_PATH = 'cutwords'


def load_mult_classify(svc_storages):
    SVC_MULT_CLSIFY = services.multiclsify.MultiClassify(svc_storages)
    SVC_CLS_CV = SVC_MULT_CLSIFY.classifies
    return SVC_MULT_CLSIFY, SVC_CLS_CV


def load_mining(SVC_MEMBERS, SVC_CLS_CV, silencer, lsipath=None, cutwordpath=None):
    global LSI_PATH, CUTWORD_PATH
    if lsipath is None:
        lsipath = LSI_PATH
    if cutwordpath is None:
        cutwordpath = CUTWORD_PATH
    SVC_CUTWORD = services.analysis.cutword.Cutword(cutwordpath)
    slicer = functools.partial(silencer, cutservice=SVC_CUTWORD)
    SVC_MIN = services.mining.Mining(lsipath, SVC_MEMBERS.allprojects(), SVC_CLS_CV, slicer=slicer)
    SVC_MIN.setup()
    return SVC_CUTWORD, SVC_MIN


def load_doc_processor(name):
    global SUPPORT_DOCPROCESSOR
    return SUPPORT_DOCPROCESSOR[name]


def load_index(SVC_MEMBERS, SVC_CLS_CV):
    svc_cvs = list()
    for name, project in SVC_MEMBERS.allprojects().items():
        svc_cvs.append(project.curriculumvitae)
    svc_cvs.extend(SVC_CLS_CV.values())
    SVC_INDEX = services.index.ReverseIndexing('Index', svc_cvs)
    SVC_INDEX.setup()
    return SVC_INDEX


def load_esindex(es_conn, cv_storages):
    import services.esindex
    from elasticsearch import Elasticsearch
    SVC_INDEX = services.esindex.ElasticsearchIndexing(cv_storages)
    SVC_INDEX.setup(es_conn)
    return SVC_INDEX


def load_es_searchengine():
    from elasticsearch import Elasticsearch
    global CONFIG_PATH
    config = dict()
    try:
        stream = open(os.path.join(CONFIG_PATH, 'es.yaml')).read()
        config = yaml.load(stream)
    except IOError:
        pass
    ES = Elasticsearch(**config)
    return ES

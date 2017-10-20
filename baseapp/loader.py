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


class Config(object):

    es_config_file = 'es.yaml'
    storage_config_file = 'storage.yaml'

    default_storage_path = 'datas'
    storage_template = (
        ("LSI",             "model/lsimodel"),
        ("CUTWORD",         "cache/cutwords"),
        ("REINDEX",         "cache/Index"),
        ("ACCOUNT",         "account/account"),
        ("PASSWORD",        "account/password"),
        ("MESSAGE",         "account/message"),
        ("JD_REPO",         "JD/repo"),
        ("CO_REPO",         "CO/repo"),
        ("CV_REPO",         "CV/repo"),
        ("CV_INDIV",        "CV/indiv"),
        ("CV_STO",          "CV/storage"),
        ("PEO_REPO",        "PEO/repo"),
        ("PEO_INDIV",       "PEO/indiv"),
        ("PEO_STO",         "PEO/storage"),
        ("MULT_CLSIFY",     "CV/classify"),
        ("MEMBERS",         "members"),
        ("UPLOAD_TEMP",     "output"),
        ("RAW",             "raw")
    )

    es_template = (
        ("CV_INDEXNAME",    "cloudshare.index"),
        ("JD_INDEXNAME",    "jobdescription.index"),
        ("CO_INDEXNAME",    "company.index"),
    )

    def __init__(self, path):
        self.path = path

    def generate_storage_template(self, base_dir):
        storage_config = {}
        for each in self.storage_template:
            storage_config[each[0]] = os.path.join(base_dir, each[1])
        return storage_config

    def generate_es_template(self):
        es_config = {}
        for each in self.es_template:
            es_config[each[0]] = each[1]
        return es_config

    @property
    def storage_config(self):
        config = dict()
        base_dir = self.default_storage_path
        try:
            stream = open(os.path.join(self.path, self.storage_config_file)).read()
            config = yaml.load(stream)
        except IOError:
            pass
        if 'path' in config:
            base_dir = config['path']
        storage_config = self.generate_storage_template(base_dir)
        storage_config.update(config)
        return storage_config

    @property
    def es_config(self):
        config = dict()
        try:
            stream = open(os.path.join(self.path, self.es_config_file)).read()
            config = yaml.load(stream)
        except IOError:
            pass
        es_config = self.generate_es_template()
        es_config.update(config)
        return es_config

CONFIG_PATH = 'config'
config = Config(CONFIG_PATH)

def load_mult_classify(svc_storages):
    global config
    MULT_CLSIFY_PATH = config.storage_config['MULT_CLSIFY']
    SVC_MULT_CLSIFY = services.multiclsify.MultiClassify(MULT_CLSIFY_PATH, svc_storages)
    SVC_CLS_CV = SVC_MULT_CLSIFY.classifies
    return SVC_MULT_CLSIFY, SVC_CLS_CV


def load_mining(SVC_MEMBERS, SVC_CLS_CV, silencer):
    global config
    LSI_PATH = config.storage_config['LSI']
    CUTWORD_PATH = config.storage_config['CUTWORD']
    SVC_CUTWORD = services.analysis.cutword.Cutword(CUTWORD_PATH)
    slicer = functools.partial(silencer, cutservice=SVC_CUTWORD)
    SVC_MIN = services.mining.Mining(LSI_PATH, SVC_MEMBERS, SVC_CLS_CV, slicer=slicer)
    SVC_MIN.setup()
    SVC_MIN.update_project_sims()
    return SVC_CUTWORD, SVC_MIN


def load_doc_processor(name):
    global SUPPORT_DOCPROCESSOR
    return SUPPORT_DOCPROCESSOR[name]


def load_index(SVC_MEMBERS, SVC_CLS_CV):
    global config
    REINDEX_PATH = config.storage_config['REINDEX']
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
    global config
    SVC_INDEX = services.esindex.ElasticsearchIndexing(cv_storages)
    SVC_INDEX.setup(es_conn, config.es_config['CV_INDEXNAME'])
    return SVC_INDEX


def load_es_searchengine():
    global config
    from elasticsearch import Elasticsearch
    ES = Elasticsearch(**config.es_config)
    return ES

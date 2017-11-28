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

    storage_config_file = 'storage.yaml'

    default_storage_path = {'1.1': '.',
        '1.2': '.',
        '1.5': 'datas',
        }
    storage_template = {'1.1': (
        ("RAW",             "raw"),
        ("UPLOAD_TEMP",     "output"),
        ("CUTWORD",         "cutwords"),
        ("LSI",             "lsimodel"),
        ("PROJECT",         "projects"),
        ("ACCOUNT",         "account"),
        ("JD_REPO",         "repo/JD"),
        ("CO_REPO",         "repo/CO"),
        ("CV_REPO",         "repo/CV"),
        ("PEO_REPO",        "repo/PEO"),
        ("CV_STO",          "storage/CV"),
        ("PEO_STO",         "storage/PEO"),
        ("MULT_CLSIFY",     "classify"),
    ),
    '1.2': (
        ("RAW",             "raw"),
        ("UPLOAD_TEMP",     "output"),
        ("REINDEX",         "Index"),
        ("CUTWORD",         "cutwords"),
        ("LSI",             "lsimodel"),
        ("MEMBERS",         "members"),
        ("ACCOUNT",         "account"),
        ("PASSWORD",        "password"),
        ("MESSAGE",         "message"),
        ("CV_REPO",         "repo/CV"),
        ("PEO_REPO",        "repo/PEO"),
        ("PEO_LIMIT",       "repo/LIMITPEO"),
        ("CV_INDIV",        "indiv/CV"),
        ("PEO_INDIV",       "indiv/PEO"),
        ("CV_STO",          "storage/CV"),
        ("PEO_STO",         "storage/PEO"),
        ("MULT_CLSIFY",     "classify"),
    ),
    '1.5': (
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
        ("PEO_LIMIT",       "PEO/limit"),
        ("MULT_CLSIFY",     "CV/classify"),
        ("MEMBERS",         "members"),
        ("UPLOAD_TEMP",     "output"),
        ("RAW",             "raw")
    ),
    }

    def __init__(self, path, version):
        self.path = path
        self.version = version

    def generate_storage_template(self, base_dir):
        storage_config = {}
        for each in self.storage_template[self.version]:
            storage_config[each[0]] = os.path.join(base_dir, each[1])
        return storage_config

    @property
    def storage_config(self):
        config = dict()
        try:
            base_dir = self.default_storage_path[self.version]
        except KeyError:
            base_dir = '.'
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
 
CONFIG_PATH = 'config'
config = Config(CONFIG_PATH, version='1.2')

LSI_PATH = config.storage_config['LSI']
CUTWORD_PATH = config.storage_config['CUTWORD']


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
    SVC_MIN = services.mining.Mining(lsipath, SVC_MEMBERS, SVC_CLS_CV, slicer=slicer)
    SVC_MIN.setup()
    SVC_MIN.update_project_sims()
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

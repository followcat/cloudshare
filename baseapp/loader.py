import os
import yaml
import functools

from elasticsearch import Elasticsearch

import tools.updater
import services.mining
import services.esindex
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
    min_config_file = 'min.yaml'
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
        ("PEO_LIMIT",       "PEO/limit"),
        ("MULT_CLSIFY",     "CV/classify"),
        ("MEMBERS",         "members"),
        ("UPLOAD_TEMP",     "output"),
        ("RAW",             "raw")
    )

    es_template = (
        ("cvstorage",          "cvstorage"),    # SVC_CV_STO
        ("cvmembers",          "cvmembers"),    # SVC_CO_MEMBERS
        ("jdmembers",          "jdmembers"),    # SVC_JD_MEMBERS
        ("comembers",          "cormembers"),   # SVC_CO_MEMBERS
    )

    min_template = (
        ("JD_MIN",        "jdmatch"),
        ("CO_MIN",        "comatch"),
        ("PRJ_MIN",       "prjmatch"),
        ("POS_MIN",       "posmatch"),
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

    def generate_min_template(self):
        es_config = {}
        for each in self.min_template:
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

    @property
    def min_config(self):
        config = dict()
        try:
            stream = open(os.path.join(self.path, self.min_config_file)).read()
            config = yaml.load(stream)
        except IOError:
            pass
        min_config = self.generate_min_template()
        min_config.update(config)
        return min_config


CONFIG_PATH = 'config'
config = Config(CONFIG_PATH)

def load_mult_classify(svc_storages):
    global config
    MULT_CLSIFY_PATH = config.storage_config['MULT_CLSIFY']
    SVC_MULT_CLSIFY = services.multiclsify.MultiClassify(MULT_CLSIFY_PATH, svc_storages)
    SVC_CLS_CV = SVC_MULT_CLSIFY.classifies
    return SVC_MULT_CLSIFY, SVC_CLS_CV


def load_mining(silencer):
    global config
    LSI_PATH = config.storage_config['LSI']
    CUTWORD_PATH = config.storage_config['CUTWORD']
    SVC_CUTWORD = services.analysis.cutword.Cutword(CUTWORD_PATH)
    slicer = functools.partial(silencer, cutservice=SVC_CUTWORD)
    SVC_MIN = services.mining.Mining(LSI_PATH, slicer=slicer)
    return SVC_MIN


def load_cv_mining(SVC_MIN, SVC_MEMBERS):
    for member in SVC_MEMBERS.members.values():
        for project in member.projects.values():
            modelname = project.modelname
            simnames = [prj.id for prj in member.projects.values()] + project.getclassify()
            SVC_MIN.setup(modelname, simnames)
    tools.updater.update_cv_sims(SVC_MIN, SVC_MEMBERS)


def load_jd_mining(SVC_MIN, SVC_JDS):
    SVC_MIN.setup('jdmatch', [JD.name for JD in SVC_JDS])
    tools.updater.update_jd_sims('jdmatch', SVC_MIN, SVC_JDS)


def load_co_mining(SVC_MIN, SVC_CVS):
    SVC_MIN.setup('comatch', [CV.name for CV in SVC_CVS])
    SVC_MIN.setup('prjmatch', [CV.name for CV in SVC_CVS])
    SVC_MIN.setup('posmatch', [CV.name for CV in SVC_CVS])
    #tools.updater.update_co_sims('comatch', SVC_MIN, SVC_CVS)
    #tools.updater.update_pos_sims('posmatch', SVC_MIN, SVC_CVS)
    #tools.updater.update_prj_sims('prjmatch', SVC_MIN, SVC_CVS)


def load_doc_processor(name):
    global SUPPORT_DOCPROCESSOR
    return SUPPORT_DOCPROCESSOR[name]


def load_esindex(es_conn):
    global config
    SVC_INDEX = services.esindex.ElasticsearchIndexing()
    for each in config.es_config:
        SVC_INDEX.setup(es_conn, config.es_config[each])
    return SVC_INDEX


def load_es_searchengine():
    global config
    ES = Elasticsearch(**config.es_config)
    return ES

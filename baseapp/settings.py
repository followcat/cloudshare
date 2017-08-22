import baseapp.loader
from baseapp.datadbs import *
from baseapp.index import *
from baseapp.mining import *
from baseapp.customer import *
from baseapp.searchengine import *
from baseapp.docprocessor import *

def sync_reload():
    class ReloadObj(object):
        def __init__(self, SVC_MULT_CLSIFY, SVC_CLS_CV,
                     SVC_CUTWORD, SVC_MIN, SVC_INDEX):
            self.SVC_MULT_CLSIFY = SVC_MULT_CLSIFY
            self.SVC_CLS_CV = SVC_CLS_CV
            self.SVC_CUTWORD = SVC_CUTWORD
            self.SVC_MIN = SVC_MIN
            self.SVC_INDEX = SVC_INDEX
    SVC_MULT_CLSIFY, SVC_CLS_CV = baseapp.loader.load_mult_classify([SVC_CV_STO, SVC_CV_INDIV])
    SVC_CUTWORD, SVC_MIN = baseapp.loader.load_mining(SVC_CUSTOMERS, SVC_CLS_CV,
                                                      services.mining.silencer)
    SVC_INDEX = baseapp.loader.load_esindex(ES, [SVC_CV_REPO, SVC_CV_STO, SVC_CV_INDIV])
    reloadobj = ReloadObj(SVC_MULT_CLSIFY, SVC_CLS_CV,
                          SVC_CUTWORD, SVC_MIN, SVC_INDEX)
    return reloadobj

SYNC_METHOD_RELOAD = sync_reload

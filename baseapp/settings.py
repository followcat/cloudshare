import baseapp.loader
from baseapp.datadbs import *
from baseapp.index import *
from baseapp.mining import *
from baseapp.member import *
from baseapp.searchengine import *
from baseapp.docprocessor import *

def sync_reload():
    class ReloadObj(object):
        def __init__(self, SVC_MIN, SVC_INDEX):
            self.SVC_MIN = SVC_MIN
            self.SVC_INDEX = SVC_INDEX
    SVC_MIN = baseapp.mining.load_mining(services.mining.silencer)
    baseapp.loader.load_cv_mining(SVC_MIN, SVC_MEMBERS)
    SVC_INDEX = baseapp.loader.load_esindex(ES, [SVC_CV_REPO, SVC_CV_STO, SVC_CV_INDIV])
    reloadobj = ReloadObj(SVC_MIN, SVC_INDEX)
    return reloadobj

SYNC_METHOD_RELOAD = sync_reload

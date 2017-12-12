# -*- coding: utf-8 -*-
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
    SVC_MIN = baseapp.loader.load_mining(services.mining.silencer)
    baseapp.loader.load_cv_mining(SVC_MIN, SVC_MEMBERS)
    baseapp.loader.load_addedcv_mining(SVC_MIN, SVC_MEMBERS, {'*': [u'综合']})
    baseapp.loader.load_jd_mining(SVC_MIN, [SVC_JD_REPO])
    baseapp.loader.load_co_mining(SVC_MIN, [SVC_CV_REPO])
    SVC_INDEX = baseapp.loader.load_esindex(ES)
    reloadobj = ReloadObj(SVC_MIN, SVC_INDEX)
    return reloadobj

SYNC_METHOD_RELOAD = sync_reload

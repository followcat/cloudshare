from baseapp.index import *
from baseapp.mining import *
from baseapp.datadbs import *
from baseapp.sync import *


SVC_ADD_SYNC.update(filterfunc=update_bydate)
SVC_MULT_CLSIFY.updatenewids()
SVC_MIN.update_sims()
SVC_INDEX.update(ES_CONFIG['CV_INDEXNAME'], [SVC_CV_REPO, SVC_CV_STO, SVC_CV_INDIV])
ids = [each[2]['id'] for each in SVC_ADD_SYNC.yamls_gen(filterfunc=update_bydate)]
SVC_INDEX.upgrade(ES_CONFIG['CV_INDEXNAME'], [SVC_CV_REPO, SVC_CV_STO, SVC_CV_INDIV], ['date'], ids=ids)

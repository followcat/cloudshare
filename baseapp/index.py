import baseapp.loader


#from baseapp.datadbs import SVC_CLS_CV
#from baseapp.member import SVC_MEMBERS
#SVC_INDEX = baseapp.loader.load_index(SVC_MEMBERS, SVC_CLS_CV)

import baseapp.searchengine
from baseapp.datadbs import SVC_CV_REPO, SVC_CV_STO, SVC_CV_INDIV
ES_CONFIG = baseapp.loader.config.es_config
SVC_INDEX = baseapp.loader.load_esindex(baseapp.searchengine.ES)

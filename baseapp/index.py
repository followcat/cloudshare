import baseapp.loader


#from baseapp.multicv import SVC_MULT_CV
#SVC_INDEX = baseapp.loader.load_index(SVC_MULT_CV)

import searchengine
from baseapp.datadbs import SVC_CV_REPO, SVC_CV_STO
SVC_INDEX = baseapp.loader.load_esindex(searchengine.ES, [SVC_CV_REPO, SVC_CV_STO])

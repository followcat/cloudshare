import baseapp.loader


#from baseapp.datadbs import SVC_CLS_CV
#from baseapp.customer import SVC_CUSTOMERS
#SVC_INDEX = baseapp.loader.load_index(SVC_CUSTOMERS, SVC_CLS_CV)

import baseapp.searchengine
from baseapp.datadbs import SVC_CV_REPO, SVC_CV_STO
SVC_INDEX = baseapp.loader.load_esindex(baseapp.searchengine.ES, [SVC_CV_REPO, SVC_CV_STO])

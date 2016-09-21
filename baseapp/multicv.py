from baseapp.datadbs import SVC_CLS_CV, DEF_SVC_CV
from baseapp.projects import *

import services.multicv


SVC_CV = services.multicv.MultiCV([SVC_PRJ_MED], DEF_SVC_CV, SVC_CLS_CV)

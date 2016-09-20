from baseapp.datadbs import SVC_CLS_CV
from baseapp.projects import *

import services.multicv


SVC_CV = services.multicv.MultiCV([SVC_PRJ_MED], SVC_CLS_CV)

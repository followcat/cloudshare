from baseapp.datadbs import SVC_CLS_CV, SVC_CV_REPO
from baseapp.projects import *

import services.multicv


SVC_MULT_CV = services.multicv.MultiCV([SVC_PRJ_MED, SVC_PRJ_AI], SVC_CV_REPO, SVC_CLS_CV)

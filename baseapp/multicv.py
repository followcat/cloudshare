from baseapp.datadbs import SVC_CLS_CV, SVC_CV_REPO
from baseapp.projects import *

import services.multicv


SVC_MULT_CV = services.multicv.MultiCV(PRJ_LIST, SVC_CV_REPO, SVC_CLS_CV)

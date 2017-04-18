from baseapp.datadbs import SVC_CLS_CV, SVC_CV_REPO
from baseapp.projects import *

import services.multicv


def load_mult_cv(SVC_CLS_CV):
    SVC_MULT_CV = services.multicv.MultiCV(PRJ_LIST, SVC_CV_REPO, SVC_CLS_CV)
    return SVC_MULT_CV


SVC_MULT_CV = load_mult_cv(SVC_CLS_CV)

from baseapp.datadbs import SVC_CLS_CV, SVC_CV_REPO
from baseapp.projects import *

import services.multicv


def load_mult_cv(SVC_CLS_CV):
    SVC_MULT_CV = services.multicv.MultiCV([SVC_PRJ_MED, SVC_PRJ_AI, SVC_PRJ_BT,
                                            SVC_PRJ_IA, SVC_PRJ_NE],
                                            SVC_CV_REPO, SVC_CLS_CV)
    return SVC_MULT_CV


SVC_MULT_CV = load_mult_cv(SVC_CLS_CV)

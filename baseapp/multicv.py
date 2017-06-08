import baseapp.loader

from baseapp.projects import PRJ_LIST
from baseapp.datadbs import SVC_CLS_CV, SVC_CV_REPO


SVC_MULT_CV = baseapp.loader.load_mult_cv(PRJ_LIST, SVC_CV_REPO , SVC_CLS_CV)

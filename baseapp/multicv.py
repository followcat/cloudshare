from baseapp.datadbs import SVC_CLS_CV, DATA_DB
from baseapp.projects import *

import services.multicv


SVC_CV = services.multicv.MultiCV([SVC_PRJ_MED], SVC_CLS_CV)

SVC_JD = services.jobdescription.JobDescription(DATA_DB, SVC_CV.default.company)

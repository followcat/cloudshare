#encoding: utf-8
import os

import services.projectcv
import sources.industry_id
from baseapp.datadbs import *


PRJ_PATH = 'projects'
if not os.path.exists(PRJ_PATH):
    os.makedirs(PRJ_PATH)

MED_needed = sources.industry_id.needed_medical
UAV_needed = sources.industry_id.needed_uav


MED_DB = interface.gitinterface.GitInterface(os.path.join(PRJ_PATH, 'medical'))
SVC_PRJ_MED = services.projectcv.ProjectCV(MED_DB, SVC_CV_REPO, 'medical')
SVC_PRJ_MED.setup(MED_needed)

UAV_DB = interface.gitinterface.GitInterface(os.path.join(PRJ_PATH, 'UAV'))
SVC_PRJ_UAV = services.projectcv.ProjectCV(UAV_DB, SVC_CV_REPO, 'UAV')
SVC_PRJ_UAV.setup(UAV_needed)

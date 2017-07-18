#encoding: utf-8
import os

import services.project
import sources.industry_id
from baseapp.datadbs import *


PRJ_PATH = 'projects'
if not os.path.exists(PRJ_PATH):
    os.makedirs(PRJ_PATH)

MED_needed = sources.industry_id.needed_medical
AI_needed = sources.industry_id.needed_ai


SVC_PRJ_MED = services.project.Project(os.path.join(PRJ_PATH, 'medical'),
                                       SVC_CO_REPO, SVC_CV_REPO, SVC_MULT_PEO,
                                       'medical')
SVC_PRJ_MED.setup()

SVC_PRJ_AI = services.project.Project(os.path.join(PRJ_PATH, 'ArtificialIntelligence'),
                                      SVC_CO_REPO, SVC_CV_REPO, SVC_MULT_PEO,
                                      'ArtificialIntelligence')
SVC_PRJ_AI.setup()

SVC_PRJ_BT = services.project.Project(os.path.join(PRJ_PATH, 'BioTechnology'),
                                      SVC_CO_REPO, SVC_CV_REPO, SVC_MULT_PEO,
                                      'BioTechnology')
SVC_PRJ_BT.setup()

SVC_PRJ_IA = services.project.Project(os.path.join(PRJ_PATH, 'IndustrialAccelerator'),
                                      SVC_CO_REPO, SVC_CV_REPO, SVC_MULT_PEO,
                                      'IndustrialAccelerator')
SVC_PRJ_IA.setup()

SVC_PRJ_NE = services.project.Project(os.path.join(PRJ_PATH, 'NewEnergy'),
                                      SVC_CO_REPO, SVC_CV_REPO, SVC_MULT_PEO,
                                      'NewEnergy')
SVC_PRJ_NE.setup()

PRJ_LIST = [SVC_PRJ_MED, SVC_PRJ_AI, SVC_PRJ_BT, SVC_PRJ_IA, SVC_PRJ_NE]

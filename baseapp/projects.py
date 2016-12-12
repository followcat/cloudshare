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
                                       SVC_CO_REPO, SVC_CV_REPO, 'medical')
SVC_PRJ_MED.setup(MED_needed)

SVC_PRJ_AI = services.project.Project(os.path.join(PRJ_PATH, 'ArtificialIntelligence'),
                                       SVC_CO_REPO, SVC_CV_REPO, 'ArtificialIntelligence')
SVC_PRJ_AI.setup(AI_needed, config={'autoupdate': False})

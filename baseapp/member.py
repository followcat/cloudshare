import os

import services.members
import sources.industry_id
from baseapp.datadbs import *
from baseapp.loader import config


MED_needed = sources.industry_id.needed_medical
AI_needed = sources.industry_id.needed_ai

SVC_MEMBERS = services.members.Members(config.storage_config['MEMBERS'], [SVC_ACCOUNT],
                                       [SVC_CV_REPO, SVC_CV_STO, SVC_CV_INDIV],
                                       [SVC_JD_REPO], [SVC_MULT_PEO])

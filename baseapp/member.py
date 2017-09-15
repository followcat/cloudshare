import os

import services.members
import sources.industry_id
from baseapp.datadbs import *


MED_needed = sources.industry_id.needed_medical
AI_needed = sources.industry_id.needed_ai

MEMBERS_PATH = 'members'
SVC_MEMBERS = services.members.Members(MEMBERS_PATH, [SVC_ACCOUNT],
                                       [SVC_CV_REPO, SVC_CV_STO, SVC_CV_INDIV],
                                       [SVC_MULT_PEO])

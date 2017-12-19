import os

import services.members
import sources.industry_id
from baseapp.datadbs import *
from baseapp.loader import config


MED_needed = sources.industry_id.needed_medical
AI_needed = sources.industry_id.needed_ai

SVC_MEMBERS = services.members.Members(config.storage_config['MEMBERS'], [SVC_ACCOUNT],
                                       [SVC_BD_REPO],
                                       [SVC_CO_STO],
                                       [SVC_CV_REPO, SVC_CV_STO, SVC_CV_INDIV],
                                       [SVC_JD_REPO],
                                       [SVC_PEO_REPO, SVC_PEO_STO, SVC_PEO_INDIV, SVC_PEO_LIMIT]
                                    )

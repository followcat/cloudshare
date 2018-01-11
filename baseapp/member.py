# -*- coding: utf-8 -*-
import os

import services.members
import sources.industry_id
import baseapp.loader
from baseapp.mining import *
from baseapp.datadbs import *
from baseapp.loader import config
from baseapp.searchengine import ES


MED_needed = sources.industry_id.needed_medical
AI_needed = sources.industry_id.needed_ai

SVC_MEMBERS = services.members.Members(config.storage_config['MEMBERS'],
                                       SVC_MIN,
                                       [SVC_BD_REPO],
                                       [SVC_CO_STO],
                                       [SVC_CV_REPO, SVC_CV_STO, SVC_CV_INDIV],
                                       [SVC_JD_REPO],
                                       [SVC_PEO_REPO, SVC_PEO_STO, SVC_PEO_INDIV, SVC_PEO_LIMIT],
                                       ES, config.generate_es_template(),
                                    )

MIN_ADDITIONALS = { u'综合': SVC_CV_STO }
baseapp.loader.load_cv_mining(SVC_MIN, SVC_MEMBERS)
baseapp.loader.load_addedcv_mining(SVC_MIN, SVC_MEMBERS, {'*': MIN_ADDITIONALS.keys()})
baseapp.loader.load_jd_mining(SVC_MIN, [SVC_JD_REPO])
baseapp.loader.load_co_mining(SVC_MIN, [SVC_CV_REPO])

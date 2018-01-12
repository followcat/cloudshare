# -*- coding: utf-8 -*-
import tools.updater

from baseapp.sync import *
from baseapp.index import *
from baseapp.member import *
from baseapp.mining import *
from baseapp.datadbs import *


SVC_ADD_SYNC.update(filterfunc=update_bydate)
tools.updater.update_cv_models(SVC_MIN, SVC_MEMBERS)
tools.updater.update_cv_sims(SVC_MIN, SVC_MEMBERS)
tools.updater.update_cv_sims(SVC_MIN, SVC_MEMBERS, additionals=MIN_ADDITIONALS)
tools.updater.update_jd_sims('jdmatch', SVC_MIN, [SVC_JD_REPO])
tools.updater.update_co_sims('comatch', SVC_MIN, [SVC_CV_REPO])
tools.updater.update_pos_sims('posmatch', SVC_MIN, [SVC_CV_REPO])
tools.updater.update_prj_sims('prjmatch', SVC_MIN, [SVC_CV_REPO])
SVC_MEMBERS.idx_updatesvc()
ids = [each[2]['id'] for each in SVC_ADD_SYNC.yamls_gen(filterfunc=update_bydate)]
SVC_MEMBERS.idx_upgradesvc(ids=ids)

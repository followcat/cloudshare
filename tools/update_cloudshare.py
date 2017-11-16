import tools.updater

from baseapp.index import *
from baseapp.mining import *
from baseapp.datadbs import *
from baseapp.member import *
from baseapp.sync import *


SVC_ADD_SYNC.update(filterfunc=update_bydate)
tools.updater.update_cv_models(SVC_MIN, SVC_MEMBERS)
tools.updater.update_cv_sims(SVC_MIN, SVC_MEMBERS)
tools.updater.update_jd_sims('jdmatch', SVC_MIN, [SVC_JD_REPO])
tools.updater.update_co_sims('comatch', SVC_MIN, [SVC_CV_REPO])
tools.updater.update_pos_sims('posmatch', SVC_MIN, [SVC_CV_REPO])
tools.updater.update_prj_sims('prjmatch', SVC_MIN, [SVC_CV_REPO])
SVC_INDEX.updatesvc(SVC_INDEX.config['CV_STO'], SVC_CV_STO.id,
                    SVC_CV_STO, content=False, numbers=5000)
ids = [each[2]['id'] for each in SVC_ADD_SYNC.yamls_gen(filterfunc=update_bydate)]
SVC_INDEX.upgradesvc(SVC_INDEX.config['CV_STO'], SVC_CV_STO.id, SVC_CV_STO,
                     ids=ids, numbers=5000)

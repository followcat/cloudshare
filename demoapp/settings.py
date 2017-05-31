import os

import webapp.jsonencoder

import baseapp.loader
import services.mining
import services.project
import sources.industry_id
import services.curriculumvitae


PRJ_PATH = 'projects'
MED_needed = sources.industry_id.needed_medical

SVC_CV_REPO = services.curriculumvitae.CurriculumVitae('repo/CV', 'repostorage')
SVC_CV_STO = services.curriculumvitae.CurriculumVitae('storage/CV', 'cvstorage')
SVC_PRJ_TMP = services.project.Project(os.path.join(PRJ_PATH, 'temporary'),
                                       None, SVC_CV_REPO, None, 'temporary')
SVC_PRJ_TMP.setup(MED_needed, config={'autoupdate': False, 'autosetup': False})

SVC_MULT_CLSIFY, SVC_CLS_CV = baseapp.loader.load_mult_classify(SVC_CV_STO)
SVC_MULT_CV = baseapp.loader.load_mult_cv([SVC_PRJ_TMP], SVC_CV_REPO , SVC_CLS_CV)
SVC_CUTWORD, SVC_MIN = baseapp.loader.load_mining(SVC_MULT_CV, services.mining.silencer)

CAESAR_CIPHER_NUM = 3
RESTFUL_JSON = {'cls': webapp.jsonencoder.CustomJSONEncoder}

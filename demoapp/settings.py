from baseapp.mining import *

import services.project
import sources.industry_id
import services.curriculumvitae

import webapp.jsonencoder

PRJ_PATH = 'projects'
MED_needed = sources.industry_id.needed_medical

SVC_CV_REPO = services.curriculumvitae.CurriculumVitae('repo/CV', 'repostorage')
SVC_CV_STO = services.curriculumvitae.CurriculumVitae('storage/CV', 'cvstorage')
SVC_PRJ_MED = services.project.Project(os.path.join(PRJ_PATH, 'medical'),
                                       None, SVC_CV_REPO, None, 'medical')
SVC_PRJ_MED.setup(MED_needed, config={'autoupdate': True, 'autosetup': True})
SVC_MULT_CV = services.multicv.MultiCV([SVC_PRJ_MED], SVC_CV_STO)

CAESAR_CIPHER_NUM = 3
RESTFUL_JSON = {'cls': webapp.jsonencoder.CustomJSONEncoder}

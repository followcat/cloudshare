import os

import webapp.jsonencoder
import services.index
import services.mining
import services.account
import services.company
import services.multicv
import services.classifycv
import services.cvstoragesync
import services.curriculumvitae
import services.jobdescription
import interface.basefs
import interface.predator
import interface.gitinterface

import sources.industry_id


RESTFUL_JSON = {'cls': webapp.jsonencoder.CustomJSONEncoder}

UPLOAD_TEMP = 'output'
SECRET_KEY = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'

USER_HOME = os.path.expanduser("~")
BACKUP_FOLDER = 'cloudshare_repodb'
BACKUP_DIRS = [os.path.join(USER_HOME, BACKUP_FOLDER),
               os.path.join('/data_center/backup', BACKUP_FOLDER)]

ACCOUNT_DB_NAME = 'account'
ACCOUNT_DB = interface.gitinterface.GitInterface(ACCOUNT_DB_NAME)
SVC_ACCOUNT = services.account.Account(ACCOUNT_DB)

DATA_DB_NAME = 'repo'
DATA_DB = interface.gitinterface.GitInterface(DATA_DB_NAME)

SVC_CO = services.company.Company(DATA_DB)
SVC_JD = services.jobdescription.JobDescription(DATA_DB, SVC_CO)

DEF_SVC_CV = services.curriculumvitae.CurriculumVitae(DATA_DB, 'cloudshare')

RAW_DIR = 'raw'
RAW_DB = dict()
if os.path.exists(RAW_DIR):
    for name in os.listdir(RAW_DIR):
        namepath = os.path.join(RAW_DIR, name)
        RAW_DB[name] = interface.predator.PredatorInterface(namepath)

CV_STORAGE_DIR = 'cvstorage'
CV_STORAGE_DB = interface.basefs.BaseFSInterface(CV_STORAGE_DIR)
SVC_CV_STO = services.curriculumvitae.CurriculumVitaeStorage(CV_STORAGE_DB, 'cvstorage')

SVC_ADD_SYNC = services.cvstoragesync.CVStorageSync(SVC_CV_STO, RAW_DB)

CLASSIFY_DIR = 'classify'
SVC_CLS_CV = dict()
for name in sources.industry_id.industryID.keys():
     cls_cv = services.classifycv.ClassifyCV(name, CLASSIFY_DIR, SVC_CV_STO, RAW_DB)
     if cls_cv.NUMS == 0:
        continue
     SVC_CLS_CV[name] = cls_cv
SVC_CV = services.multicv.MultiCV(DEF_SVC_CV, SVC_CLS_CV.values())

SVC_INDEX = services.index.ReverseIndexing('Index', SVC_CV)
SVC_INDEX.setup()

LSI_PATH = 'lsimodel'
SVC_MIN = services.mining.Mining(LSI_PATH, SVC_CV)
SVC_MIN.setup('all')

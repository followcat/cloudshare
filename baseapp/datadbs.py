import os

import services.account
import services.classifycv
import services.cvstoragesync
import services.curriculumvitae
import interface.basefs
import interface.predator
import interface.gitinterface

import sources.industry_id


ACCOUNT_DB_NAME = 'account'
ACCOUNT_DB = interface.gitinterface.GitInterface(ACCOUNT_DB_NAME)
SVC_ACCOUNT = services.account.Account(ACCOUNT_DB)

REPO_DB_NAME = 'repo'
REPO_DB = interface.gitinterface.GitInterface(REPO_DB_NAME)
SVC_CV_REPO = services.curriculumvitae.CurriculumVitae(REPO_DB, 'cloudshare')


CV_STORAGE_DIR = 'cvstorage'
CV_STORAGE_DB = interface.basefs.BaseFSInterface(CV_STORAGE_DIR)
SVC_CV_STO = services.curriculumvitae.CurriculumVitaeStorage(CV_STORAGE_DB, 'cvstorage')

RAW_DIR = 'raw'
RAW_DB = dict()
if os.path.exists(RAW_DIR):
    for name in os.listdir(RAW_DIR):
        namepath = os.path.join(RAW_DIR, name)
        RAW_DB[name] = interface.predator.PredatorInterface(namepath)
SVC_ADD_SYNC = services.cvstoragesync.CVStorageSync(SVC_CV_STO, RAW_DB)

CLASSIFY_DIR = 'classify'
SVC_CLS_CV = dict()
for name in sources.industry_id.industryID.keys():
    cls_cv = services.classifycv.ClassifyCV(name, CLASSIFY_DIR, SVC_CV_STO, RAW_DB)
    if cls_cv.NUMS == 0:
        continue
    SVC_CLS_CV[name] = cls_cv

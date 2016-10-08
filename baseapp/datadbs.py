import os

import services.account
import services.multiclsify
import services.cvstoragesync
import services.curriculumvitae
import interface.basefs
import interface.predator
import interface.gitinterface


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

SVC_MULT_CLSIFY = services.multiclsify.MultiClassify(SVC_CV_STO)
SVC_CLS_CV = SVC_MULT_CLSIFY.classifies

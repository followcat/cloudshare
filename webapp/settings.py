import os

import services.index
import services.mining
import services.account
import services.company
import services.multicv
import services.additionalsync
import services.curriculumvitae
import services.jobdescription
import interface.predator
import interface.gitinterface


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
ADDITIONAL_DIR = 'additional'

ADD_DB = dict()
ADD_SVC_CV = dict()
for name in os.listdir(ADDITIONAL_DIR):
    namepath = os.path.join(ADDITIONAL_DIR, name)
    ADD_DB[name] = interface.predator.PredatorInterface(namepath)
    add_svc_cv = services.curriculumvitae.CurriculumVitae(ADD_DB[name], name)
    if add_svc_cv.NUMS > 0:
        ADD_SVC_CV[name] = add_svc_cv

RAW_DB = dict()
for name in os.listdir(RAW_DIR):
    namepath = os.path.join(RAW_DIR, name)
    RAW_DB[name] = interface.predator.PredatorInterface(namepath)

SVC_CV = services.multicv.MultiCV(DEF_SVC_CV, ADD_SVC_CV.values())
SVC_ADD_SYNC = services.additionalsync.AdditionalSync(ADD_SVC_CV, ADDITIONAL_DIR, RAW_DB)

SVC_INDEX = services.index.ReverseIndexing('Index', SVC_CV)
SVC_INDEX.setup()

LSI_PATH = 'lsimodel'
SVC_MIN = services.mining.Mining(LSI_PATH, SVC_CV)
SVC_MIN.setup('all')

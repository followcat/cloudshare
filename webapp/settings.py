import os

import services.mining
import services.account
import services.company
import services.multicv
import services.curriculumvitae
import services.jobdescription
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

DEF_SVC_CV = services.curriculumvitae.CurriculumVitae(DATA_DB)
SVC_CV = services.multicv.MultiCV(DEF_SVC_CV, [])

LSI_PATH = 'lsimodel'
SVC_MIN = services.mining.Mining(LSI_PATH, [DEF_SVC_CV], DEF_SVC_CV)
LSI_MODEL = SVC_MIN.lsi['default']

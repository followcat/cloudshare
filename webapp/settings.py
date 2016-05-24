import os

import services.account
import services.company
import services.curriculumvitae
import services.jobdescription
import core.mining.lsimodel
import interface.gitinterface


UPLOAD_TEMP = 'output'
SECRET_KEY = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'

USER_HOME = os.path.expanduser("~")
BACKUP_FOLDER = 'cloudshare_repodb'
BACKUP_DIRS = [os.path.join(USER_HOME, BACKUP_FOLDER),
               os.path.join('/data_center/backup', BACKUP_FOLDER)]

DATA_DB_NAME = 'repo'
DATA_DB = interface.gitinterface.GitInterface(DATA_DB_NAME)
SVC_CV = services.curriculumvitae.CurriculumVitae(DATA_DB)

SVC_CO = services.company.Company(DATA_DB)
SVC_JD = services.jobdescription.JobDescription(DATA_DB, SVC_CO)

ACCOUNT_DB_NAME = 'account'
ACCOUNT_DB = interface.gitinterface.GitInterface(ACCOUNT_DB_NAME)
SVC_ACCOUNT = services.account.Account(ACCOUNT_DB)

def init_lsimodel(lsi, svc_cv):
    try:
        lsi.load()
    except IOError:
        if lsi.build(svc_cv):
            lsi.save()

LSI_SAVE_PATH = 'lsimodel'
LSI_MODEL = core.mining.lsimodel.LSImodel(LSI_SAVE_PATH)
init_lsimodel(LSI_MODEL, SVC_CV)

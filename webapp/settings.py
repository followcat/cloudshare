import os
import re
import glob

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

def init_lsimodel(lsi, lsipath, svc_cv):
    try:
        lsi.load(lsipath)
    except IOError:
        lsi.build(svc_cv)
        lsi.save(lsipath)

LSI_SAVE_PATH = 'lsimodel'
LSI_MODEL = core.mining.lsimodel.LSImodel()
init_lsimodel(LSI_MODEL, LSI_SAVE_PATH, SVC_CV)

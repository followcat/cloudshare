import os.path

import webapp.core.account
import repointerface.gitinterface


UPLOAD_TEMP = 'output'
SECRET_KEY = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'

USER_HOME = os.path.expanduser("~")
BACKUP_FOLDER = 'cloudshare_repodb'
BACKUP_DIRS = [os.path.join(USER_HOME, BACKUP_FOLDER),
               os.path.join('/data_center/backup', BACKUP_FOLDER)]

DATA_DB_NAME = 'repo'
DATA_DB = repointerface.gitinterface.GitInterface(DATA_DB_NAME)

ACCOUNT_DB_NAME = 'account'
ACCOUNT_DB = repointerface.gitinterface.GitInterface(ACCOUNT_DB_NAME)
REPO_ACCOUNT = webapp.core.account.RepoAccount(ACCOUNT_DB)

LSI_MODEL = None

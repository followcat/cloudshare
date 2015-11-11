import os.path

import webapp.core.account
import repointerface.gitinterface


UPLOAD_TEMP = 'output'
SECRET_KEY = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'
REPO_DB_NAME = 'repo'

USER_HOME = os.path.expanduser("~")
BACKUP_FOLDER = 'repodb_backup'
BACKUP_DIR = os.path.join(USER_HOME, BACKUP_FOLDER)

REPO_DB = repointerface.gitinterface.GitInterface(REPO_DB_NAME)
REPO_ACCOUNT = webapp.core.account.RepoAccount(REPO_DB)

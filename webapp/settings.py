import repointerface.gitinterface


UPLOAD_TEMP = '/tmp'
SECRET_KEY = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'
REPO_DB_NAME = 'repo'

REPO_DB = repointerface.gitinterface.GitInterface(REPO_DB_NAME)

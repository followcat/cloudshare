import os
import re
import glob

import jieba

import webapp.views.account
import core.mining.lsimodel
import repointerface.gitinterface


UPLOAD_TEMP = 'output'
SECRET_KEY = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'

USER_HOME = os.path.expanduser("~")
BACKUP_FOLDER = 'cloudshare_repodb'
BACKUP_DIRS = [os.path.join(USER_HOME, BACKUP_FOLDER),
               os.path.join('/data_center/backup', BACKUP_FOLDER)]

DATA_DB_NAME = 'repo'
DATA_DB = repointerface.gitinterface.GitInterface(DATA_DB_NAME)

CO_DB_NAME = 'co_repo'
CO_DB = repointerface.gitinterface.GitInterface(CO_DB_NAME)
REPO_CO = webapp.core.company.RepoCompany(CO_DB)

JD_DB_NAME = 'jd_repo'
JD_DB = repointerface.gitinterface.GitInterface(JD_DB_NAME)

ACCOUNT_DB_NAME = 'account'
ACCOUNT_DB = repointerface.gitinterface.GitInterface(ACCOUNT_DB_NAME)
REPO_ACCOUNT = webapp.views.account.RepoAccount(ACCOUNT_DB)

def build_lsimodel(lsimodel, lsipath):
    global DATA_DB_NAME
    names = []
    texts = []
    def elt(s):
        return s
    count = 0
    for pathfile in glob.glob(os.path.join(DATA_DB_NAME, '*.yaml')):
        mdfile = pathfile.replace('.yaml', '.md')
        if os.path.isfile(mdfile):
            data = open(mdfile, 'rb').read()
            data = re.sub(ur'[\n- /]+' ,' ' , data)
            path, name = mdfile.split('/')
            names.append(name)
            seg = filter(lambda x: len(x) > 0, map(elt, jieba.cut(data, cut_all=False)))
            texts.append(seg)
            count += 1
    if count > 0:
        lsimodel.setup(names, texts)
        lsimodel.save(lsipath)

def init_lsimodel(lsi, lsipath):
    try:
        lsi.load(lsipath)
    except IOError:
        build_lsimodel(lsi, lsipath)

LSI_SAVE_PATH = 'lsimodel'
LSI_MODEL = core.mining.lsimodel.LSImodel()
init_lsimodel(LSI_MODEL, LSI_SAVE_PATH)

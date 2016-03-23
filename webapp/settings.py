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

ACCOUNT_DB_NAME = 'account'
ACCOUNT_DB = repointerface.gitinterface.GitInterface(ACCOUNT_DB_NAME)
REPO_ACCOUNT = webapp.views.account.RepoAccount(ACCOUNT_DB)

def init_lsimodel():
    global DATA_DB_NAME
    names = []
    texts = []
    def elt(s):
        return s
    for pathfile in glob.glob(os.path.join(DATA_DB_NAME, '*.yaml')):
        mdfile = pathfile.replace('.yaml', '.md')
        if os.path.isfile(mdfile):
            data = open(mdfile, 'rb').read()
            data = re.sub(ur'[\n- /]+' ,' ' , data)
            path, name = mdfile.split('/')
            names.append(name)
            seg = filter(lambda x: len(x) > 0, map(elt, jieba.cut(data, cut_all=False)))
            texts.append(seg)
    lsi = core.mining.lsimodel.LSImodel()
    lsi.setup(names, texts)
    return lsi

LSI_MODEL = init_lsimodel()

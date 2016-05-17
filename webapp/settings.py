import os
import re
import glob

import jieba.posseg

import webapp.views.cv
import webapp.views.account
import webapp.views.company
import webapp.views.jobdescription
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
REPO_CV = webapp.views.cv.RepoCurriculumVitae(DATA_DB)

REPO_CO = webapp.views.company.RepoCompany(DATA_DB)
REPO_JD = webapp.views.jobdescription.RepoJobDescription(DATA_DB, REPO_CO)

ACCOUNT_DB_NAME = 'account'
ACCOUNT_DB = interface.gitinterface.GitInterface(ACCOUNT_DB_NAME)
REPO_ACCOUNT = webapp.views.account.RepoAccount(ACCOUNT_DB)

def build_lsimodel(lsimodel, lsipath):
    names = []
    texts = []
    for data in REPO_CV.datas():
        name, doc = data
        names.append(name.md)
        text = [word.word for word in jieba.posseg.cut(doc) if word.flag != 'x']
        texts.append(text)
    if len(names) > 0:
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

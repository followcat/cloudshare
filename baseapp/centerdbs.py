import os
import interface.gitinterface
import services.curriculumvitae

DBCENTER_NAME = 'dbcenter'
DBCENTER_NAMES = {'medical', 'flying'}

DBCENTER = dict()
DBCENTER_SVC_CV = dict()
for name in DBCENTER_NAMES:
    namepath = os.path.join(DBCENTER_NAME, name)
    DBCENTER[name] = interface.gitinterface.GitInterface(namepath)
    DBCENTER_SVC_CV[name] = services.curriculumvitae.CurriculumVitae(DBCENTER[name], name)

DATA_DB_NAME = 'repo'
DATA_DB = interface.gitinterface.GitInterface(DATA_DB_NAME)
DEF_SVC_CV = services.curriculumvitae.CurriculumVitae(DATA_DB, 'cloudshare')

import os

import services.account
import services.multiclsify
import services.cvstoragesync
import services.people
import services.company
import services.curriculumvitae
import interface.basefs
import interface.predator
import interface.gitinterface


SVC_ACCOUNT = services.account.Account('account')

SVC_CO_REPO = services.company.Company('repo/CO', 'corepo')
SVC_CV_REPO = services.curriculumvitae.CurriculumVitae('repo/CV', 'cloudshare')

SVC_CV_STO = services.curriculumvitae.CurriculumVitae('storage/CV', 'cvstorage')
SVC_PEO_STO = services.people.People('storage/PEO', [SVC_CV_REPO, SVC_CV_STO])

RAW_DIR = 'raw'
RAW_DB = dict()
if os.path.exists(RAW_DIR):
    for name in os.listdir(RAW_DIR):
        namepath = os.path.join(RAW_DIR, name)
        RAW_DB[name] = interface.predator.PredatorInterface(namepath)
SVC_ADD_SYNC = services.cvstoragesync.CVStorageSync(SVC_CV_STO, RAW_DB)

SVC_MULT_CLSIFY = services.multiclsify.MultiClassify(SVC_CV_STO)
SVC_CLS_CV = SVC_MULT_CLSIFY.classifies

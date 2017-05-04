import os

import services.account
import services.multiclsify
import services.multipeople
import services.people
import services.company
import services.curriculumvitae
import interface.basefs
import interface.gitinterface


SVC_ACCOUNT = services.account.Account('account')

SVC_CO_REPO = services.company.Company('repo/CO', 'corepo')
SVC_CV_REPO = services.curriculumvitae.CurriculumVitae('repo/CV', 'cloudshare')
SVC_PEO_REPO = services.people.People('repo/PEO', SVC_CV_REPO, iotype='base')

SVC_CV_STO = services.curriculumvitae.CurriculumVitae('storage/CV', 'cvstorage')
SVC_PEO_STO = services.people.People('storage/PEO', SVC_CV_STO, iotype='base')
SVC_MULT_PEO = services.multipeople.MultiPeople([SVC_PEO_REPO, SVC_PEO_STO])

def load_mult_classify():
    SVC_MULT_CLSIFY = services.multiclsify.MultiClassify(SVC_CV_STO)
    SVC_CLS_CV = SVC_MULT_CLSIFY.classifies
    return SVC_MULT_CLSIFY, SVC_CLS_CV

SVC_MULT_CLSIFY, SVC_CLS_CV = load_mult_classify()

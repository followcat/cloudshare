import os

import baseapp.loader
import services.account
import services.people
import services.company
import services.multipeople
import baseapp.searchengine
import services.curriculumvitae


SVC_MSG = services.account.Message('message', 'msgrepo')
SVC_PWD = services.account.Password('password', 'pwdrepo')
SVC_ACCOUNT = services.account.Account(SVC_PWD, 'account', 'accrepo')

SVC_CO_REPO = services.company.Company('repo/CO', 'corepo')
SVC_CV_REPO = services.curriculumvitae.CurriculumVitae('repo/CV', 'cloudshare',
                                                       searchengine=baseapp.searchengine.ES)
SVC_PEO_REPO = services.people.People(SVC_CV_REPO, 'repo/PEO', 'peorepo', iotype='base')

SVC_CV_STO = services.curriculumvitae.CurriculumVitae('storage/CV', 'cvstorage')
SVC_PEO_STO = services.people.People(SVC_CV_STO, 'storage/PEO', 'peostorage', iotype='base')
SVC_MULT_PEO = services.multipeople.MultiPeople([SVC_PEO_REPO, SVC_PEO_STO])

SVC_MULT_CLSIFY, SVC_CLS_CV = baseapp.loader.load_mult_classify([SVC_CV_STO])

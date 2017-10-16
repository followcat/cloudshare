import os

import baseapp.loader
import services.account
import services.people
import services.multipeople
import services.jobdescription
import services.curriculumvitae
import baseapp.searchengine

from baseapp.loader import config


PATHS = config.storage_config

SVC_PWD = services.account.Password(PATHS['PASSWORD'], 'pwdrepo')
SVC_ACCOUNT = services.account.Account(SVC_PWD, PATHS['ACCOUNT'], 'accrepo')
SVC_MSG = services.account.Message(SVC_ACCOUNT, PATHS['MESSAGE'], 'msgrepo')

SVC_JD_REPO = services.jobdescription.JobDescription(PATHS['JD_REPO'], 'jdrepo')

SVC_CV_REPO = services.curriculumvitae.CurriculumVitae(PATHS['CV_REPO'], 'cloudshare',
                                                       searchengine=baseapp.searchengine.ES)
SVC_PEO_REPO = services.people.People(SVC_CV_REPO, PATHS['PEO_REPO'], 'peorepo', iotype='base')

SVC_CV_STO = services.curriculumvitae.CurriculumVitae(PATHS['CV_STO'], 'cvstorage')
SVC_PEO_STO = services.people.People(SVC_CV_STO, PATHS['PEO_STO'], 'peostorage', iotype='base')
SVC_CV_INDIV = services.curriculumvitae.CurriculumVitae(PATHS['CV_INDIV'], 'cvindividual',
                                                        searchengine=baseapp.searchengine.ES,
                                                        iotype='base')
SVC_PEO_INDIV = services.people.People(SVC_CV_INDIV, PATHS['PEO_INDIV'],
                                       'peoindividual', iotype='base')
SVC_MULT_PEO = services.multipeople.MultiPeople([SVC_PEO_REPO, SVC_PEO_STO, SVC_PEO_INDIV])

SVC_MULT_CLSIFY, SVC_CLS_CV = baseapp.loader.load_mult_classify([SVC_CV_STO, SVC_CV_INDIV])

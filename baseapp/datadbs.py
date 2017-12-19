import os

import baseapp.loader
import services.people
import services.bidding
import services.company
import services.account
import services.message
import services.multipeople
import services.jobdescription
import services.curriculumvitae

from baseapp.loader import config


PATHS = config.storage_config

SVC_PWD = services.account.Password(PATHS['PASSWORD'], 'pwdrepo')
SVC_ACCOUNT = services.account.Account(SVC_PWD, PATHS['ACCOUNT'], 'accrepo')
SVC_MSG = services.message.Message(SVC_ACCOUNT, PATHS['MESSAGE'], 'msgrepo')

SVC_BD_REPO = services.bidding.Bidding(PATHS['BD_REPO'], 'corepo')
SVC_JD_REPO = services.jobdescription.JobDescription(PATHS['JD_REPO'], 'jdrepo')

SVC_CV_REPO = services.curriculumvitae.CurriculumVitae(PATHS['CV_REPO'], 'cloudshare')

SVC_PEO_REPO = services.people.People(PATHS['PEO_REPO'], 'peorepo')
SVC_PEO_LIMIT = services.people.People(PATHS['PEO_LIMIT'], 'peolimit')

SVC_CO_STO = services.company.Company(PATHS['CO_STO'], 'costorage')
SVC_CV_STO = services.curriculumvitae.CurriculumVitae(PATHS['CV_STO'], 'cvstorage')
SVC_PEO_STO = services.people.People(PATHS['PEO_STO'], 'peostorage')
SVC_CV_INDIV = services.curriculumvitae.CurriculumVitae(PATHS['CV_INDIV'], 'cvindividual')

SVC_PEO_INDIV = services.people.People(PATHS['PEO_INDIV'], 'peoindividual')
SVC_MULT_PEO = services.multipeople.MultiPeople([SVC_PEO_REPO, SVC_PEO_STO,
                                                 SVC_PEO_INDIV, SVC_PEO_LIMIT])
SVC_PEO_CV = services.people.CVSelector(
                operator_service=services.people.People(PATHS['PEO_REPO'], 'peorepo'),
                data_service=SVC_MULT_PEO
                )

import services.account
import services.company
import services.multicv
import services.additionalsync
import services.jobdescription
import interface.gitinterface

from baseapp.additionals import *
from baseapp.centerdbs import DBCENTER_SVC_CV


ACCOUNT_DB_NAME = 'account'
ACCOUNT_DB = interface.gitinterface.GitInterface(ACCOUNT_DB_NAME)
SVC_ACCOUNT = services.account.Account(ACCOUNT_DB)

DATA_DB_NAME = 'repo'
DATA_DB = interface.gitinterface.GitInterface(DATA_DB_NAME)

SVC_CO = services.company.Company(DATA_DB)
SVC_JD = services.jobdescription.JobDescription(DATA_DB, SVC_CO)
SVC_CV = services.multicv.MultiCV(DBCENTER_SVC_CV,
                                  [PRE_SVC_CV, JGYG_SVC_CV, ZILN_SVC_CV, YICA_SVC_CV])

SVC_ADD_SYNC = services.additionalsync.AdditionalSync(SVC_CV)

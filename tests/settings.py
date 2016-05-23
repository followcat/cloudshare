import os
import shutil

import services.account
import services.company
import services.curriculumvitae
import services.jobdescription
import core.mining.lsimodel
import interface.gitinterface

class Config(object):

    TESTING = True
    SECRET_KEY = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'
    UPLOAD_TEMP = 'tests/testcase_output'
    DATA_DB_NAME = 'tests/testcase_data'
    ACCOUNT_DB_NAME = 'tests/testcase_account'
    LSI_SAVE_PATH = 'tests/lsimodel'

    def __init__(self):
        self.rebuild()
        self.REBUILD = self.rebuild
        self.DESTORY = self.destory

    def rebuild(self):
        if not os.path.exists(self.UPLOAD_TEMP):
            os.mkdir(self.UPLOAD_TEMP)

        self.DATA_DB = interface.gitinterface.GitInterface(self.DATA_DB_NAME)
        self.SVC_CV = services.curriculumvitae.CurriculumVitae(self.DATA_DB)

        self.SVC_CO = services.company.Company(self.DATA_DB)
        self.SVC_JD = services.jobdescription.JobDescription(self.DATA_DB, self.SVC_CO)

        self.ACCOUNT_DB = interface.gitinterface.GitInterface(self.ACCOUNT_DB_NAME)
        self.SVC_ACCOUNT = services.account.Account(self.ACCOUNT_DB)

        self.LSI_MODEL = core.mining.lsimodel.LSImodel()

    def destory(self):
        if os.path.exists(self.UPLOAD_TEMP):
            shutil.rmtree(self.UPLOAD_TEMP)
        if os.path.exists(self.DATA_DB_NAME):
            shutil.rmtree(self.DATA_DB_NAME)
        if os.path.exists(self.ACCOUNT_DB_NAME):
            shutil.rmtree(self.ACCOUNT_DB_NAME)
        if os.path.exists(self.LSI_SAVE_PATH):
            shutil.rmtree(self.LSI_SAVE_PATH)

config = Config()

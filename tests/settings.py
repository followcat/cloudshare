import os
import shutil

import services.mining
import services.account
import services.multicv
import services.curriculumvitae
import interface.gitinterface

class Config(object):

    TESTING = True
    SECRET_KEY = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'
    UPLOAD_TEMP = 'tests/testcase_output'
    REPO_DB_NAME = 'tests/testcase_data'
    ACCOUNT_DB_NAME = 'tests/testcase_account'
    LSI_PATH = 'tests/lsimodel'

    def __init__(self):
        self.build()
        self.REBUILD = self.rebuild
        self.DESTORY = self.destory

    def build(self):
        if not os.path.exists(self.UPLOAD_TEMP):
            os.mkdir(self.UPLOAD_TEMP)

        self.ACCOUNT_DB = interface.gitinterface.GitInterface(self.ACCOUNT_DB_NAME)
        self.SVC_ACCOUNT = services.account.Account(self.ACCOUNT_DB)

        self.REPO_DB = interface.gitinterface.GitInterface(self.REPO_DB_NAME)

        self.SVC_REPO_CV = services.curriculumvitae.CurriculumVitae(self.REPO_DB, 'cloudshare')
        self.SVC_CV = services.multicv.MultiCV(self.SVC_REPO_CV, [])

        self.SVC_MIN = services.mining.Mining(self.LSI_PATH, self.SVC_CV)
        self.SVC_MIN.lsi_model.no_above = 1
        self.SVC_MIN.lsi_model.setup('first.md', ['here is a text for testing.'])
        self.SVC_MIN.setup('default')

    def rebuild(self):
        self.destory()
        self.build()

    def destory(self):
        if os.path.exists(self.UPLOAD_TEMP):
            shutil.rmtree(self.UPLOAD_TEMP)
        if os.path.exists(self.REPO_DB_NAME):
            shutil.rmtree(self.REPO_DB_NAME)
        if os.path.exists(self.ACCOUNT_DB_NAME):
            shutil.rmtree(self.ACCOUNT_DB_NAME)
        if os.path.exists(self.LSI_PATH):
            shutil.rmtree(self.LSI_PATH)

config = Config()

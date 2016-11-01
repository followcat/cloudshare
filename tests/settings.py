import os
import shutil

import services.mining
import services.account
import services.multicv
import services.project
import services.curriculumvitae
import core.converterutils
import interface.gitinterface

class Config(object):

    TESTING = True
    SECRET_KEY = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'
    UPLOAD_TEMP = 'tests/testcase_output'
    REPO_DB_NAME = 'tests/testcase_data'
    ACCOUNT_DB_NAME = 'tests/testcase_account'
    LSI_PATH = 'tests/lsimodel'
    PRJ_PATH = 'tests/projects'

    def __init__(self):
        self.build()
        self.REBUILD = self.rebuild
        self.DESTORY = self.destory

    def build(self):
        if not os.path.exists(self.UPLOAD_TEMP):
            os.mkdir(self.UPLOAD_TEMP)
        if not os.path.exists(self.PRJ_PATH):
            os.mkdir(self.PRJ_PATH)

        self.ACCOUNT_DB = interface.gitinterface.GitInterface(self.ACCOUNT_DB_NAME)
        self.SVC_ACCOUNT = services.account.Account(self.ACCOUNT_DB)

        self.REPO_DB = interface.gitinterface.GitInterface(self.REPO_DB_NAME)
        self.SVC_CV_REPO = services.curriculumvitae.CurriculumVitae(self.REPO_DB, 'cloudshare')

        self.PRJ_DB = interface.gitinterface.GitInterface(os.path.join(self.PRJ_PATH,
                                                          'project_test'))
        self.SVC_PRJ_MED = services.project.Project(self.PRJ_DB,
                                                    self.SVC_CV_REPO,
                                                    'project_test')
        self.SVC_PRJ_MED.setup([])

        self.SVC_MULT_CV = services.multicv.MultiCV([self.SVC_PRJ_MED],
                                                    self.SVC_CV_REPO)

        self.SVC_MIN = services.mining.Mining(self.LSI_PATH, self.SVC_MULT_CV)
        self.SVC_MIN.lsi_model[self.SVC_PRJ_MED.name].no_above = 1
        self.SVC_MIN.lsi_model[self.SVC_PRJ_MED.name].setup('first.md',
            ['here is a text for testing.'])
        self.SVC_MIN.setup()

    def init_samplecv(self):
        filename = 'cv_1.doc'
        f = open(os.path.join('core/test', filename))
        filepro = core.converterutils.FileProcesser(f, filename,
                                                    self.UPLOAD_TEMP)
        cvobj = services.curriculumvitae.CurriculumVitaeObject(filepro.name,
                                                               filepro.markdown_stream,
                                                               filepro.yamlinfo)
        self.SVC_MULT_CV.add(cvobj, projectname='project_test')

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
        if os.path.exists(self.PRJ_PATH):
            shutil.rmtree(self.PRJ_PATH)

config = Config()

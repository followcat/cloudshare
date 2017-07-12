import os
import shutil

import core.basedata
import services.mining
import services.people
import services.account
import services.multicv
import services.project
import services.company
import services.curriculumvitae
import interface.gitinterface
import utils.docprocessor.libreoffice
import extractor.information_explorer

class Config(object):

    TESTING = True
    SECRET_KEY = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'
    TESTDATA_PATH = 'tests/testcase_data'
    UPLOAD_TEMP = os.path.join(TESTDATA_PATH, 'output')
    REPO_DB_NAME = os.path.join(TESTDATA_PATH, 'repo')
    ACCOUNT_DB_NAME = os.path.join(TESTDATA_PATH, 'account')
    LSI_PATH = os.path.join(TESTDATA_PATH, 'lsimodel')
    PRJ_PATH = os.path.join(TESTDATA_PATH, 'projects')

    def __init__(self):
        self.build()
        self.REBUILD = self.rebuild
        self.DESTORY = self.destory

    def build(self):
        if not os.path.exists(self.TESTDATA_PATH):
            os.mkdir(self.TESTDATA_PATH)
        if not os.path.exists(self.UPLOAD_TEMP):
            os.mkdir(self.UPLOAD_TEMP)
        if not os.path.exists(self.PRJ_PATH):
            os.mkdir(self.PRJ_PATH)

        self.SVC_ACCOUNT = services.account.Account(self.ACCOUNT_DB_NAME)
        self.SVC_CV_REPO = services.curriculumvitae.CurriculumVitae(self.REPO_DB_NAME,
                                                                    'cloudshare')
        self.SVC_CO_REPO = services.company.Company(self.REPO_DB_NAME, 'corepo')
        self.SVC_PEO_REPO = services.people.People(self.SVC_CV_REPO,
                                                   os.path.join(self.REPO_DB_NAME, 'PEO'),
                                                   name='peorepo', iotype='base')
        self.SVC_PRJ_TEST = services.project.Project(os.path.join(self.PRJ_PATH,
                                                                 'project_test'),
                                                    self.SVC_CO_REPO, self.SVC_CV_REPO,
                                                    self.SVC_PEO_REPO, 'project_test')
        self.SVC_PRJ_TEST.setup([])

        self.SVC_MULT_CV = services.multicv.MultiCV([self.SVC_PRJ_TEST],
                                                    self.SVC_CV_REPO)

        self.SVC_MIN = services.mining.Mining(self.LSI_PATH, self.SVC_MULT_CV)
        self.SVC_MIN.lsi_model[self.SVC_PRJ_TEST.name].no_above = 1
        self.SVC_MIN.lsi_model[self.SVC_PRJ_TEST.name].setup(['first.md'],
            ['here is a text for testing.'])
        self.SVC_MIN.setup()

    def init_samplecv(self):
        filename = 'cv_1.doc'
        f = open(os.path.join('core/test', filename))
        filepro = utils.docprocessor.libreoffice.LibreOfficeProcessor(f, filename,
                                                                      self.UPLOAD_TEMP)
        yamlinfo = extractor.information_explorer.catch_cvinfo(
                                    stream=filepro.markdown_stream.decode('utf8'),
                                    filename=filename)
        dataobj = core.basedata.DataObject(data=filepro.markdown_stream,
                                           metadata=yamlinfo)
        peopmeta = extractor.information_explorer.catch_peopinfo(yamlinfo)
        peopobj = core.basedata.DataObject(data='', metadata=peopmeta)
        project = self.SVC_MULT_CV.getproject('project_test')
        self.SVC_MULT_CV.repodb.add(dataobj, 'tester', unique=True)
        project.cv_add(dataobj)
        self.SVC_PEO_REPO.add(peopobj)
        self.SVC_PRJ_TEST.peo_add(peopobj)

    def rebuild(self):
        self.destory()
        self.build()

    def destory(self):
        if os.path.exists(self.TESTDATA_PATH):
            shutil.rmtree(self.TESTDATA_PATH)

import os
import shutil

import core.basedata
import services.mining
import services.people
import services.account
import services.project
import services.customers
import services.multipeople
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
    PWD_DB_NAME = os.path.join(TESTDATA_PATH, 'password')
    ACCOUNT_DB_NAME = os.path.join(TESTDATA_PATH, 'account')
    LSI_PATH = os.path.join(TESTDATA_PATH, 'lsimodel')
    CUSTOMERS_PATH = os.path.join(TESTDATA_PATH, 'customers')

    def __init__(self):
        self.build()
        self.REBUILD = self.rebuild
        self.DESTORY = self.destory

    def build(self):
        if not os.path.exists(self.TESTDATA_PATH):
            os.mkdir(self.TESTDATA_PATH)
        if not os.path.exists(self.UPLOAD_TEMP):
            os.mkdir(self.UPLOAD_TEMP)

        self.SVC_PWD = services.account.Password(self.PWD_DB_NAME, 'pwdrepo')
        self.SVC_ACCOUNT = services.account.Account(self.SVC_PWD, self.ACCOUNT_DB_NAME,
                                                    'accrepo')
        self.SVC_CV_REPO = services.curriculumvitae.CurriculumVitae(self.REPO_DB_NAME,
                                                                    'cloudshare')
        self.SVC_PEO_REPO = services.people.People(self.SVC_CV_REPO,
                                                   os.path.join(self.REPO_DB_NAME, 'PEO'),
                                                   name='peorepo', iotype='base')

        self.SVC_MULT_PEO = services.multipeople.MultiPeople([self.SVC_PEO_REPO])
        self.SVC_CUSTOMERS = services.customers.Customers(self.CUSTOMERS_PATH,
                                                          [self.SVC_ACCOUNT],
                                                          [self.SVC_CV_REPO], [self.SVC_MULT_PEO])
        self.SVC_CUSTOMERS.create('test_customer')
        self.SVC_CUSTOMER = self.SVC_CUSTOMERS.get('test_customer')
        self.SVC_CUSTOMER.add_project('project_test', {})
        self.SVC_PRJ_TEST = self.SVC_CUSTOMER.projects['project_test']

        self.SVC_MIN = services.mining.Mining(self.LSI_PATH, self.SVC_CUSTOMERS.allprojects(),
                                              {'repoclassify': self.SVC_CV_REPO})
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
        project = self.SVC_CUSTOMER.getproject('project_test')
        self.SVC_CV_REPO.add(dataobj, 'tester', unique=True)
        project.cv_add(dataobj)
        self.SVC_PEO_REPO.add(peopobj)
        self.SVC_PRJ_TEST.peo_add(peopobj)

    def rebuild(self):
        self.destory()
        self.build()

    def destory(self):
        if os.path.exists(self.TESTDATA_PATH):
            shutil.rmtree(self.TESTDATA_PATH)

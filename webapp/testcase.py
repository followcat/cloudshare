import os
import json
import shutil
import tempfile

import flask
import jinja2.ext
import flask.ext.testing

import ext.views
import services.account
import webapp.views.cv
import webapp.views.company
import webapp.views.jobdescription
import interface.gitinterface


class Test(flask.ext.testing.TestCase):

    def tearDown(self):
        shutil.rmtree(self.data_db.repo.path)
        shutil.rmtree(self.account_db.repo.path)
        shutil.rmtree(self.upload_tmp)

    def create_app(self):

        self.app = flask.Flask(__name__)
        self.app.config.from_object('webapp.settings')
        self.app.jinja_env.add_extension(jinja2.ext.loopcontrols)

        self.data_db = interface.gitinterface.GitInterface('testcase_data')
        self.account_db = interface.gitinterface.GitInterface('testcase_account')
        self.upload_tmp = 'testcase_output'
        os.mkdir(self.upload_tmp)

        self.app.config['SECRET_KEY'] = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'
        self.app.config['TESTING'] = True
        self.app.config['DATA_DB'] = self.data_db
        self.app.config['REPO_CV'] = webapp.views.cv.RepoCurriculumVitae(self.data_db)
        self.app.config['REPO_ACCOUNT'] = services.account.Account(self.account_db)
        REPO_CO = webapp.views.company.RepoCompany(self.data_db)
        self.app.config['REPO_CO'] = REPO_CO
        REPO_JD = webapp.views.jobdescription.RepoJobDescription(self.data_db, REPO_CO)
        self.app.config['REPO_JD'] = REPO_JD
        self.app.config['UPLOAD_TEMP'] = self.upload_tmp

        ext.views.configure(self.app)
        return self.app

    def login(self, username, password):
        return self.client.post('/login/check', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def adduser(self, username, password):
        return self.client.post('/adduser', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def deleteuser(self, username):
        return self.client.post('/deleteuser', data=dict(
            name=username
        ), follow_redirects=True)

    def changepassword(self, oldpassword, newpassword):
        return self.client.post('/changepassword', data=dict(
            oldpassword=oldpassword,
            newpassword=newpassword
        ), follow_redirects=True)

    def upload(self, filepath):
        with open(filepath) as f:
            stream = f.read()
        temp = tempfile.NamedTemporaryFile()
        temp.write(stream)
        temp.flush()
        temp.seek(0)
        temp.name = 'x-y-z.doc'
        return self.client.post('/upload', data=dict(
            file=temp,
        ), follow_redirects=True)

    def uppreview(self):
        return self.client.get('/uppreview', follow_redirects=True)

    def confirm(self, name, origin, id):
        return self.client.post('/confirm', data=dict(
            name=name,
            origin=origin,
            id=id,
        ), follow_redirects=True)

    def search(self, keyword):
        return self.client.get('/search?search_text=%s' % keyword,
                               follow_redirects=True)


class LoginoutSuperAdminTest(Test):

    def test_superadmin_login_logout(self):
        rv = self.login('root', 'password')
        assert('Management System' in rv.data)
        rv = self.logout()
        assert('Login In' in rv.data)

    def test_superadmin_add_delete_user(self):
        self.login('root', 'password')
        self.adduser('addname', 'addpassword')
        assert('addname' in self.app.config['REPO_ACCOUNT'].USERS)
        self.deleteuser('addname')
        assert('addname' not in self.app.config['REPO_ACCOUNT'].USERS)
        self.logout()


class User(Test):

    user_name = 'username'
    user_password = 'userpassword'

    def init_user(self):
        self.login('root', 'password')
        self.adduser(self.user_name, self.user_password)
        self.logout()


class LoginoutUser(User):

    def test_login_user(self):
        self.init_user()
        rv = self.login(self.user_name, self.user_password)
        assert(self.user_name in rv.data)
        rv = self.logout()
        assert('Login In' in rv.data)

    def test_user_add_delete_user(self):
        self.init_user()
        self.login(self.user_name, self.user_password)
        self.adduser('addname', 'addpassword')
        assert('addname' not in self.app.config['REPO_ACCOUNT'].USERS)
        self.deleteuser(self.user_name)
        assert(self.user_name in self.app.config['REPO_ACCOUNT'].USERS)
        self.logout()

    def test_user_modify_password(self):
        self.init_user()
        self.login(self.user_name, self.user_password)
        rv = self.changepassword(self.user_password, 'newpassword')
        assert('true' in rv.data)
        rv = self.login(self.user_name, 'newpassword')
        assert(self.user_name in rv.data)


class UploadFile(User):

    def test_upload(self):
        self.init_user()
        self.login(self.user_name, self.user_password)
        rv = self.upload('core/test/cv_1.doc')
        assert(rv.data == 'True')
        rv = self.uppreview()
        assert('13888888888' in rv.data)
        rv = self.confirm('name', 'origin', 'id')
        assert(json.loads(rv.data)['result'] is True)
        commit = self.data_db.repo.get_object(self.data_db.repo.head())
        assert('Add file' in commit.message)
        assert('username' == commit.author)


class Search(User):

    def init_search(self):
        self.init_user()
        self.login(self.user_name, self.user_password)
        rv = self.upload('core/test/cv_1.doc')
        assert(rv.data == 'True')
        rv = self.uppreview()
        assert('13888888888' in rv.data)
        rv = self.confirm('name', 'origin', 'id')
        assert(json.loads(rv.data)['result'] is True)

    def test_searchresult(self):
        self.init_search()
        keyword = '2005.9'
        rv = self.search(keyword)
        assert('position' in rv.data)

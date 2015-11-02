import os
import shutil
import tempfile

import flask
import flask.ext.testing

import ext.views
import webapp.core.account
import repointerface.gitinterface


class Test(flask.ext.testing.TestCase):

    def tearDown(self):
        shutil.rmtree(self.repo_db.repo.path)
        shutil.rmtree(self.upload_tmp)

    def create_app(self):

        self.app = flask.Flask(__name__)
        self.app.config.from_object('webapp.settings')

        self.repo_db = repointerface.gitinterface.GitInterface('testcase_repo')
        self.upload_tmp = 'testcase_output'
        os.mkdir(self.upload_tmp)

        self.app.config['SECRET_KEY'] = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'
        self.app.config['TESTING'] = True
        self.app.config['REPO_DB'] = self.repo_db
        self.app.config['UPLOAD_TEMP'] = self.upload_tmp

        webapp.core.account.init_login(self.app)
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

    def upload(self, filepath):
        with open(filepath) as f:
            stream = f.read()
        temp = tempfile.NamedTemporaryFile()
        temp.name = 'x-y-z.doc'
        temp.write(stream)
        return self.client.post('/upload', data=dict(
            Filedata=temp
        ), follow_redirects=True)

    def uppreview(self):
        return self.client.get('/uppreview', follow_redirects=True)

    def confirm(self):
        return self.client.get('/confirm', follow_redirects=True)


class LoginoutSuperAdminTest(Test):

    def test_superadmin_login_logout(self):
        rv = self.login('root', 'password')
        assert('Management System' in rv.data)
        rv = self.logout()
        assert('Login In' in rv.data)

    def test_superadmin_add_delete_user(self):
        self.login('root', 'password')
        self.adduser('addname', 'addpassword')
        assert('addname' in webapp.core.account.RepoAccount.USERS)
        self.deleteuser('addname')
        assert('addname' not in webapp.core.account.RepoAccount.USERS)
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
        assert('addname' not in webapp.core.account.RepoAccount.USERS)
        self.deleteuser(self.user_name)
        assert(self.user_name in webapp.core.account.RepoAccount.USERS)
        self.logout()


class UploadFile(User):

    def test_upload(self):
        self.init_user()
        self.login(self.user_name, self.user_password)
        rv = self.upload('core/test/cv_1.doc')
        assert(rv.data == 'True')
        rv = self.uppreview()
        assert('CV Templates' in rv.data)
        rv = self.confirm()
        assert(rv.data == 'True')
        commit = self.repo_db.repo.get_object(self.repo_db.repo.head())
        assert('Add file' in commit.message)
        assert('username' == commit.author)

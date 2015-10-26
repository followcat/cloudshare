import shutil

import flask
import flask.ext.testing

import ext.views
import webapp.core
import webapp.core.account
import repointerface.gitinterface


class Test(flask.ext.testing.TestCase):

    def tearDown(self):
        shutil.rmtree(self.repo_db.repo.path)

    def create_app(self):

        self.app = flask.Flask(__name__)
        self.app.config.from_object('webapp.settings')

        self.app.config['SECRET_KEY'] = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'
        self.repo_db = repointerface.gitinterface.GitInterface('testcase_repo')
        self.app.config['REPO_DB'] = self.repo_db
        self.app.config['TESTING'] = True

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


class LoginoutSuperAdminTest(Test):

    def test_superadmin_login_logout(self):
        rv = self.login('root', 'password')
        assert('Management System' in rv.data)
        rv = self.logout()
        assert('Login In' in rv.data)

    def test_superadmin_add_user(self):
        self.login('root', 'password')
        self.adduser('addname', 'addpassword')
        assert('addname' in webapp.core.account.RepoAccount.USERS)
        self.logout()


class LoginoutUser(Test):

    def init_user(self):
        self.login('root', 'password')
        self.adduser('addname', 'addpassword')
        self.logout()

    def test_login_user(self):
        self.init_user()
        login_name = 'addname'
        rv = self.login(login_name, 'addpassword')
        assert(login_name in rv.data)
        rv = self.logout()
        assert('Login In' in rv.data)

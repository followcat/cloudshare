import flask
import flask.ext.testing

import ext.views
import webapp.core
import webapp.core.account


class Test(flask.ext.testing.TestCase):

    def create_app(self):

        app = flask.Flask(__name__)
        app.config.from_object('webapp.settings')

        app.config['SECRET_KEY'] = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'
        app.config['REPO_DB'] = webapp.core.repo
        app.config['TESTING'] = True

        webapp.core.account.init_login(app)
        ext.views.configure(app)
        return app


class LoginoutTest(Test):

    def login(self, username, password):
        return self.client.post('/login/check', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('root', 'root')
        assert 'Hello root' in rv.data
        rv = self.logout()
        assert 'Hello Guest' in rv.data

import json
import yaml
import tempfile

import flask
import jinja2.ext
import flask.ext.testing

import ext.views


class Test(flask.ext.testing.TestCase):

    def setUp(self):
        self.config['REBUILD']()

    def tearDown(self):
        self.config['DESTORY']()

    def create_app(self):
        self.app = flask.Flask(__name__)
        self.app.config.from_object('tests.settings.config')
        self.config = self.app.config
        self.data_db = self.app.config['DATA_DB']
        self.account_db = self.app.config['ACCOUNT_DB']
        self.upload_tmp = self.app.config['UPLOAD_TEMP']
        self.svc_cv = self.app.config['SVC_CV']
        self.app.jinja_env.add_extension(jinja2.ext.loopcontrols)
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

    def confirmenglish(self, name):
        return self.client.post('/confirmenglish', data=dict(
            name=name))

    def search(self, keyword):
        return self.client.get('/search?search_text=%s' % keyword,
                               follow_redirects=True)

    def show(self, filename):
        return self.client.get('/show/%s' % filename,
                               follow_redirects=True)

    def updateinfo(self, filename, info):
        return self.client.post('/updateinfo', data=json.dumps(dict(
            filename=filename,
            yamlinfo=info,
        )), follow_redirects=True, content_type = 'application/json')

    def addcompany(self, name, introduction):
        return self.client.post('/addcompany', data=dict(
            name=name,
            introduction=introduction
        ))


class TestLoginoutSuperAdminTest(Test):

    def test_superadmin_login_logout(self):
        rv = self.login('root', 'password')
        assert('Management System' in rv.data)
        rv = self.logout()
        assert('Login In' in rv.data)

    def test_superadmin_add_delete_user(self):
        self.login('root', 'password')
        self.adduser('addname', 'addpassword')
        assert('addname' in self.app.config['SVC_ACCOUNT'].USERS)
        self.deleteuser('addname')
        assert('addname' not in self.app.config['SVC_ACCOUNT'].USERS)
        self.logout()


class User(Test):

    user_name = 'username'
    user_password = 'userpassword'

    def init_user(self):
        self.login('root', 'password')
        self.adduser(self.user_name, self.user_password)
        self.logout()


class TestLoginoutUser(User):

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
        assert('addname' not in self.app.config['SVC_ACCOUNT'].USERS)
        self.deleteuser(self.user_name)
        assert(self.user_name in self.app.config['SVC_ACCOUNT'].USERS)
        self.logout()

    def test_user_modify_password(self):
        self.init_user()
        self.login(self.user_name, self.user_password)
        rv = self.changepassword(self.user_password, 'newpassword')
        assert('true' in rv.data)
        rv = self.login(self.user_name, 'newpassword')
        assert(self.user_name in rv.data)


class UploadFile(User):

    def init_upload(self):
        self.init_user()
        self.login(self.user_name, self.user_password)
        rv = self.upload('core/test/cv_1.doc')
        assert(rv.data == 'True')
        rv = self.uppreview()
        assert('13888888888' in rv.data)
        rv = self.confirm('name', 'origin', 'id')
        assert(json.loads(rv.data)['result'] is True)


class TestUploadFile(UploadFile):

    def test_upload(self):
        self.init_upload()
        commit = self.data_db.repo.get_object(self.data_db.repo.head())
        assert('Add file' in commit.message)
        assert('username' == commit.author)
        yamlname = list(self.svc_cv.yamls())[0]
        yaml_obj = self.svc_cv.getyaml(yamlname)
        assert(yaml_obj['originid'] == '')
        assert(yaml_obj['id'] in yamlname)


class TestSearch(UploadFile):

    def test_searchresult(self):
        self.init_upload()
        keyword = '2005.9'
        rv = self.search(keyword)
        assert('position' in rv.data)


class ShowCV(UploadFile):

    def init_showcv(self):
        self.init_upload()
        self.yamlname = [yaml for yaml in self.app.config['SVC_CV'].yamls()][0]
        self.name = self.yamlname.replace('yaml', 'md')


class TestShowCV(ShowCV):

    def test_showcv(self):
        self.init_showcv()
        rv = self.show(self.name)
        assert('160 cm' in rv.data)

    def test_addtag(self):
        self.init_showcv()
        tag_text = 'AddedTAG'
        info = {'tag': tag_text}
        self.updateinfo(self.name, info)
        search_keyword = '2005.9'
        rv = self.search(search_keyword)
        assert (tag_text in rv.data)
        rv = self.show(self.name)
        assert (tag_text in rv.data)

    def test_addtracking(self):
        self.init_showcv()
        tracking_text = 'AddedTRACK'
        info = {'tracking': {
            "data": "2009-12-31",
            "text": tracking_text
            }
        }
        self.updateinfo(self.name, info)
        search_keyword = '2005.9'
        rv = self.search(search_keyword)
        assert (self.user_name in rv.data)
        rv = self.show(self.name)
        assert (tracking_text in rv.data)

    def test_addcomment(self):
        self.init_showcv()
        comment_text = 'AddedCOMMENT'
        info = {'comment': comment_text}
        self.updateinfo(self.name, info)
        search_keyword = '2005.9'
        rv = self.search(search_keyword)
        assert (comment_text in rv.data)
        rv = self.show(self.name)
        assert (comment_text in rv.data)

    def test_addenglish(self):
        self.init_showcv()
        rv = self.upload('core/test/cv_2.doc')
        assert (rv.data == 'True')
        rv = self.uppreview()
        assert ('13777777777' in rv.data)
        self.confirmenglish(self.name)
        yamldata = self.app.config['SVC_CV'].getyaml(self.yamlname)
        assert ('enversion' in yamldata)

class SVCCompany(User):

    def init_svccompany(self):
        self.name = 'AddedCompany'
        self.introduction = 'Company Introduce'
        self.init_user()
        self.login(self.user_name, self.user_password)

class TestSVCCompany(SVCCompany):

    def test_addcompany(self):
        self.init_svccompany()
        rv = self.addcompany(self.name, self.introduction)
        assert (json.loads(rv.data)['result'] is True)
        SVC_CO = self.app.config['SVC_CO']
        assert ('Company Introduce' in SVC_CO.company(self.name)['introduction'])

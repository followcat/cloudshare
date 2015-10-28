import os
import glob
import pickle
import codecs
import hashlib
import os.path

import yaml
import flask
import pypandoc
import flask.views
import flask.ext.login

import webapp.core
import webapp.core.upload
import core.outputstorage
import core.converterutils
import webapp.core.account
import webapp.core.exception


class Search(flask.views.MethodView):
    repo = webapp.core.repo

    def get(self):
        return flask.render_template('search.html')

    def post(self):
        repo = self.repo
        search_text = flask.request.form['search_text']
        result = repo.grep(search_text)
        datas = []
        for each in result:
            base, suffix = os.path.splitext(each)
            name = core.outputstorage.ConvertName(base)
            with open(os.path.join(repo.repo.path, name.yaml), 'r') as yf:
                stream = yf.read()
            yaml_data = yaml.load(stream)
            datas.append([os.path.join(repo.repo.path, name), yaml_data])
            print(search_text)
            print(flask.jsonify(datas))
        return flask.render_template('search_result.html',
                                     search_key=search_text,
                                     result=datas)


class Listdata(flask.views.MethodView):
    repo = webapp.core.repo

    def get(self):
        datas = []
        repo = self.repo
        for position in glob.glob(os.path.join(repo.repo.path, '*.yaml')):
            with open(position, 'r') as yf:
                stream = yf.read()
            yaml_data = yaml.load(stream)
            datas.append([os.path.splitext(position)[0],
                          yaml_data])
        return flask.render_template('listdata.html', datas=datas)


class Upload(flask.views.MethodView):
    upload_tmp_path = 'output'
    upload_repo = webapp.core.repo

    @classmethod
    def setup_upload_tmp(cls, path, repo):
        cls.upload_repo = repo
        cls.upload_tmp_path = path

    def judge(self, filename):
        return len(filename.split('-')) is 3

    def get(self):
        return flask.render_template('upload.html')

    def post(self):
        network_file = flask.request.files['Filedata']
        if self.judge(network_file.filename) is False:
            return str('Not support file name format.')
        upobj = webapp.core.upload.UploadObject(network_file.filename,
                                                network_file,
                                                self.upload_tmp_path)
        flask.session['upload'] = pickle.dumps(upobj)
        flask.session.modified = True
        return str(upobj.result)


class UploadPreview(flask.views.MethodView):
    def get(self):
        upobj = pickle.loads(flask.session['upload'])
        preview_path = os.path.join(upobj.storage.markdown_path,
                                    upobj.storage.name.md)
        return flask.redirect(os.path.join('showtest', preview_path))


class Confirm(flask.views.MethodView):
    def get(self):
        user = flask.ext.login.current_user
        upobj = pickle.loads(flask.session['upload'])
        result = upobj.confirm(Upload.upload_repo, user.id)
        return str(result)


class Showtest(flask.views.MethodView):
    def get(self, filename):
        with codecs.open(filename, 'r', encoding='utf-8') as file:
            data = file.read()
        output = pypandoc.convert(data, 'html', format='markdown')
        return flask.render_template('cv.html', markdown=output)


class Index(flask.views.MethodView):

    def get(self):
        return flask.render_template('index.html')


class Login(flask.views.MethodView):

    def get(self):
        return '''
            <form action="/login/check" method="post">
                <p>Username: <input name="username" type="text"></p>
                <p>Password: <input name="password" type="password"></p>
                <input type="submit">
            </form>
        '''


class LoginCheck(flask.views.MethodView):

    def post(self):
        user = webapp.core.account.User.get(flask.request.form['username'])
        password = flask.request.form['password']
        upassword = webapp.core.account.RepoAccount.unicodemd5(password)
        error = None
        if (user and user.password == upassword):
            flask.ext.login.login_user(user)
            if(user.id == "root"):
                return flask.redirect(flask.url_for("urm"))
            else:
                return flask.redirect(flask.url_for("search"))
        else:
            # flask.flash('Username or Password Incorrect.')
            error = 'Username or Password Incorrect.'
        return flask.render_template('index.html', error=error)
        # return flask.redirect(flask.url_for('index'),error=error)


class Logout(flask.views.MethodView):

    def get(self):
        flask.ext.login.logout_user()
        return flask.redirect(flask.url_for('index'))


class AddUser(flask.views.MethodView):

    def post(self):
        result = False
        id = flask.request.form['username']
        password = flask.request.form['password']
        user = flask.ext.login.current_user
        try:
            result = webapp.core.account.RepoAccount.add(user.id, id, password)
        except webapp.core.exception.ExistsUser:
            pass
        return flask.jsonify(result=result)


class ChangePassword(flask.views.MethodView):

    def post(self): 
        result = False
        oldpassword = flask.request.form['oldpassword']
        newpassword = flask.request.form['newpassword']
        md5newpwd = webapp.core.account.RepoAccount.unicodemd5(oldpassword)
        user = flask.ext.login.current_user
        # user.id
        # user.password
        try:
            if( user.password == md5newpwd ):
                user.changepassword(newpassword)
                result = True
            else:
                result = False
        except webapp.core.exception.ExistsUser:
            pass
        return flask.jsonify(result=result)


class Urm(flask.views.MethodView):

    def get(self):
        userlist = webapp.core.account.RepoAccount.get_user_list()
        return flask.render_template('urm.html', userlist=userlist)


class UrmSetting(flask.views.MethodView):

    def get(self):
        return flask.render_template('urmsetting.html')


class DeleteUser(flask.views.MethodView):

    def post(self):
        name = flask.request.form['name']
        user = flask.ext.login.current_user
        result = webapp.core.account.RepoAccount.delete(user.id, name)
        return flask.jsonify(result=result)

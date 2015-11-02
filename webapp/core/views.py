import pickle
import codecs
import os.path

import yaml
import flask
import pypandoc
import flask.views
import flask.ext.login

import utils.builtin
import webapp.core.upload
import core.outputstorage
import webapp.core.account
import webapp.core.exception


class Search(flask.views.MethodView):

    def get(self):
        return flask.render_template('search.html')

    def post(self):
        repo = flask.current_app.config['REPO_DB']
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
        return flask.render_template('search_result.html',
                                     search_key=search_text,
                                     result=datas)


class Upload(flask.views.MethodView):

    def judge(self, filename):
        return len(filename.split('-')) is 3

    def post(self):
        network_file = flask.request.files['Filedata']
        if self.judge(network_file.filename) is False:
            return str('Not support file name format.')
        upobj = webapp.core.upload.UploadObject(network_file.filename,
                                                network_file,
                                                flask.current_app.config['UPLOAD_TEMP'])
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
        result = upobj.confirm(flask.current_app.config['REPO_DB'], user.id)
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
        username = flask.request.form['username']
        password = flask.request.form['password']
        repoaccount = flask.current_app.config['REPO_ACCOUNT']
        user = webapp.core.account.User.get(username, repoaccount)
        upassword = utils.builtin.md5(password)
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
            repoaccount = flask.current_app.config['REPO_ACCOUNT']
            result = repoaccount.add(user.id, id, password)
        except webapp.core.exception.ExistsUser:
            pass
        return flask.jsonify(result=result)


class ChangePassword(flask.views.MethodView):

    def post(self): 
        result = False
        oldpassword = flask.request.form['oldpassword']
        newpassword = flask.request.form['newpassword']
        md5newpwd = utils.builtin.md5(oldpassword)
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
        repoaccount = flask.current_app.config['REPO_ACCOUNT']
        userlist = repoaccount.get_user_list()
        return flask.render_template('urm.html', userlist=userlist)


class UrmSetting(flask.views.MethodView):

    def get(self):
        return flask.render_template('urmsetting.html')


class DeleteUser(flask.views.MethodView):

    def post(self):
        name = flask.request.form['name']
        user = flask.ext.login.current_user
        repoaccount = flask.current_app.config['REPO_ACCOUNT']
        result = repoaccount.delete(user.id, name)
        return flask.jsonify(result=result)

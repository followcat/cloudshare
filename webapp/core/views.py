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


class LoginRedirect(flask.views.MethodView):

    def get(self):
        return flask.render_template('gotologin.html')


class Search(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        return flask.render_template('search.html')

    def post(self):
        repo = flask.current_app.config['DATA_DB']
        search_text = flask.request.form['search_text']
        result = repo.grep(search_text)
        datas = []
        for each in result:
            base, suffix = os.path.splitext(each)
            name = core.outputstorage.ConvertName(base)
            yaml_data = utils.builtin.load_yaml(repo.repo.path, name.yaml)
            info = repo.get_file_create_info(name.md)
            datas.append([name, yaml_data, info])
        return flask.render_template('search_result.html',
                                     search_key=search_text,
                                     result=datas)


class Upload(flask.views.MethodView):

    def post(self):
        network_file = flask.request.files['file']
        upobj = webapp.core.upload.UploadObject(network_file.filename,
                                                network_file,
                                                flask.current_app.config['UPLOAD_TEMP'])
        flask.session['upload'] = pickle.dumps(upobj)
        flask.session.modified = True
        return str(upobj.result)


class UploadPreview(flask.views.MethodView):

    def get(self):
        upobj = pickle.loads(flask.session['upload'])
        output = upobj.preview_markdown()
        info = {
            "name": upobj.storage.yamlinfo['name'],
            "origin": upobj.storage.yamlinfo['origin'],
            "id": upobj.storage.yamlinfo['id']
        }
        return flask.render_template('cv.html', markdown=output, info=info)


class Confirm(flask.views.MethodView):

    def post(self):
        info = {
            'name': flask.request.form['name'],
            'origin': flask.request.form['origin'],
            'id': flask.request.form['id']
        }
        user = flask.ext.login.current_user
        upobj = pickle.loads(flask.session['upload'])
        upobj.storage.yamlinfo.update(info)
        result = upobj.confirm(flask.current_app.config['DATA_DB'], user.id)
        return str(result)


class Show(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self, filename):
        repo = flask.current_app.config['DATA_DB']
        name = core.outputstorage.ConvertName(filename)
        with codecs.open(os.path.join(repo.repo.path, name.md),
                         'r', encoding='utf-8') as file:
            md_data = file.read()
        md = pypandoc.convert(md_data, 'html', format='markdown')
        yaml_info = utils.builtin.load_yaml(repo.repo.path, name.yaml)
        return flask.render_template('cv.html', markdown=md, yaml=yaml_info)


class UpdateInfo(flask.views.MethodView):

    @flask.ext.login.login_required
    def post(self):
        result = True
        user = flask.ext.login.current_user
        repo = flask.current_app.config['DATA_DB']
        filename = flask.request.json['filename']
        updateinfo = flask.request.json['yamlinfo']
        key, value = updateinfo.popitem()
        name = core.outputstorage.ConvertName(filename)
        yaml_info = utils.builtin.load_yaml(repo.repo.path, name.yaml)
        if key in yaml_info:
            yaml_info[key].insert(0, {'author': user.id, 'content': value})
            repo.modify_file(bytes(name.yaml), yaml.dump(yaml_info),
                             "Add %s in %s." % (key, name.yaml), user.id)
        else:
            result = False
        return flask.jsonify(result=result)


class Index(flask.views.MethodView):

    def get(self):
        with codecs.open('webapp/features.md', 'r', encoding='utf-8') as fp:
            data = fp.read()
        return flask.render_template('index.html', features=data)


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
        try:
            if(user.password == md5newpwd):
                user.changepassword(newpassword)
                result = True
            else:
                result = False
        except webapp.core.exception.ExistsUser:
            pass
        return flask.jsonify(result=result)


class Urm(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        repoaccount = flask.current_app.config['REPO_ACCOUNT']
        userlist = repoaccount.get_user_list()
        return flask.render_template('urm.html', userlist=userlist)


class UrmSetting(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        return flask.render_template('urmsetting.html')


class DeleteUser(flask.views.MethodView):

    def post(self):
        name = flask.request.form['name']
        user = flask.ext.login.current_user
        repoaccount = flask.current_app.config['REPO_ACCOUNT']
        result = repoaccount.delete(user.id, name)
        return flask.jsonify(result=result)

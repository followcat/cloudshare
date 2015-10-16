import os
import glob
import codecs
import hashlib
import os.path

import yaml
import flask
import pypandoc
import flask.views
import flask.ext.login

import webapp.core
import core.outputstorage
import core.converterutils
import webapp.core.account


class Search(flask.views.MethodView):
    def get(self):
        return flask.render_template('search.html')

    def post(self):
        repo = webapp.core.repo
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


class Listdata(flask.views.MethodView):
    def get(self):
        datas = []
        repo = webapp.core.repo
        for position in glob.glob(os.path.join(repo.repo.path, '*.yaml')):
            with open(position, 'r') as yf:
                stream = yf.read()
            yaml_data = yaml.load(stream)
            datas.append([os.path.splitext(position)[0],
                          yaml_data])
        return flask.render_template('listdata.html', datas=datas)


class Upload(flask.views.MethodView):
    upload_tmp_path = '/tmp'

    @classmethod
    def setup_upload_tmp(cls, path):
        cls.upload_tmp_path = path

    def get(self):
        return flask.render_template('upload.html')

    def post(self):
        network_file = flask.request.files['file']
        convertname = core.outputstorage.ConvertName(
            network_file.filename.encode('utf-8'))
        path = self.upload_tmp_path
        core.outputstorage.save_stream(path, convertname, network_file.read())
        storage_file = core.converterutils.FileProcesser(path, convertname)
        try:
            result = storage_file.convert()
            if result is False:
                return flask.render_template('upload.html', result='Can not Convert')
        except:
            return flask.render_template('upload.html', result='Exist File')
        md_html = showtest(os.path.join(core.outputstorage.OutputPath.markdown,
                                        storage_file.name.md))
        storage_file.deleteconvert()
        return md_html


class Showtest(flask.views.MethodView):
    def get(self, filename):
        with codecs.open(filename, 'r', encoding='utf-8') as file:
            data = file.read()
        output = pypandoc.convert(data, 'html', format='markdown')
        return flask.render_template('cv.html', markdown=output)


class Index(flask.views.MethodView):

    def get(self):
        return (
            '''
                <h1>Hello {1}</h1>
                <p style="color: #f00;">{0}</p>
                <p>{2}</p>
            '''.format(
                # flash message
                ', '.join([str(m) for m in flask.get_flashed_messages()]),
                flask.ext.login.current_user.get_id() or 'Guest',
                ('<a href="/logout">Logout</a>' if flask.ext.login.current_user.is_authenticated
                    else '<a href="/login">Login</a>')
            )
        )


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
        m = hashlib.md5()
        m.update(password)
        upassword = unicode(m.hexdigest())
        if (user and user.password == upassword):
            flask.ext.login.login_user(user)
        else:
            flask.flash('Username or password incorrect.')

        return flask.redirect(flask.url_for('index'))


class Logout(flask.views.MethodView):

    def get(self):
        flask.ext.login.logout_user()
        return flask.redirect(flask.url_for('index'))

import time
import pickle
import codecs
import os.path

import yaml
import flask
import flask.views
import flask.ext.login

import utils.builtin
import utils.chsname
import services.curriculumvitae
import core.outputstorage
import webapp.views.account
import services.exception

import json


class LoginRedirect(flask.views.MethodView):

    def get(self):
        return flask.render_template('gotologin.html')

class Upload(flask.views.MethodView):

    @flask.ext.login.login_required
    def post(self):
        user = flask.ext.login.current_user
        network_file = flask.request.files['file']
        upobj = services.curriculumvitae.CurriculumVitaeObject(network_file.filename,
                                                network_file,
                                                flask.current_app.config['UPLOAD_TEMP'])
        flask.session[user.id]['upload'] = pickle.dumps(upobj)
        flask.session.modified = True
        return str(upobj.result)


class UploadPreview(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        user = flask.ext.login.current_user
        upobj = pickle.loads(flask.session[user.id]['upload'])
        output = upobj.preview_markdown()
        yaml_info = upobj.filepro.yamlinfo
        return flask.render_template('upload_preview.html', markdown=output, yaml=yaml_info)


class ConfirmEnglish(flask.views.MethodView):

    @flask.ext.login.login_required
    def post(self):
        user = flask.ext.login.current_user
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        name = core.outputstorage.ConvertName(flask.request.form['name'])
        yaml_data = svc_mult_cv.getyaml(name)
        upobj = pickle.loads(flask.session[user.id]['upload'])
        result = svc_mult_cv.add_md(upobj, user.id)
        yaml_data['enversion'] = upobj.filepro.name.md
        svc_mult_cv.modify(name.yaml, yaml.safe_dump(yaml_data, allow_unicode=True),
                           committer=user.id)
        return flask.jsonify(result=result, filename=yaml_data['id']+'.md')


class Show(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self, filename):
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        md = svc_mult_cv.gethtml(filename)
        yaml_info = svc_mult_cv.getyaml(filename)
        yaml_info['date'] = utils.builtin.strftime(yaml_info['date'], '%Y-%m-%d %H:%M')
        user = flask.ext.login.current_user
        result = user.getbookmark()
        if yaml_info['id'] in result:
            yaml_info['collected'] = True
        else:
            yaml_info['collected'] = False
        return flask.render_template('cv_refactor.html', markdown=md, yaml=yaml_info)


class Edit(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self, filename):
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        md = svc_mult_cv.gethtml(filename)
        return flask.render_template('edit.html', markdown=md)


class ShowEnglish(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self, project, id):
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        md = svc_mult_cv.getproject(project).getmd_en(id)
        return flask.render_template('edit.html', markdown=md)


class Modify(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self, filename):
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        md_data = svc_mult_cv.getmd(filename)
        yaml_info = svc_mult_cv.getyaml(filename)
        return flask.render_template('modify.html', markdown=md_data, yaml=yaml_info)

    def post(self, filename):
        user = flask.ext.login.current_user
        md_data = flask.request.form['mddata']
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        name = core.outputstorage.ConvertName(filename)
        svc_mult_cv.modify(name.md, md_data.encode('utf-8'), committer=user.id)
        return "True"


class Preview(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        user = flask.ext.login.current_user
        upobj = pickle.loads(flask.session[user.id]['upload'])
        output = upobj.preview_markdown()
        _id = upobj.filepro.yamlinfo['id']
        return flask.render_template('upload_preview.html', markdown=output, id=_id)

    @flask.ext.login.login_required
    def post(self):
        md_data = flask.request.form['mddata']
        md = core.converterutils.md_to_html(md_data)
        return flask.render_template('preview.html', markdown=md)

class Index(flask.views.MethodView):

    def get(self):
        with codecs.open('webapp/features.md', 'r', encoding='utf-8') as fp:
            data = fp.read()
        return flask.render_template('index.html', features=data)


class GetBookmark(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        user = flask.ext.login.current_user
        result = user.getbookmark()
        return flask.jsonify(result=list(result))


class AddBookmark(flask.views.MethodView):

    @flask.ext.login.login_required
    def post(self):
        user = flask.ext.login.current_user
        bookid = flask.request.form['id']
        result = user.addbookmark(bookid)
        return flask.jsonify(result=result)


class DelBookmark(flask.views.MethodView):

    @flask.ext.login.login_required
    def post(self):
        user = flask.ext.login.current_user
        bookid = flask.request.form['id']
        result = user.delbookmark(bookid)
        return flask.jsonify(result=result)


#Render mange page of RESTful
class Manage(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        return flask.render_template('manage.html')


#Render uploader page of RESTful
class Uploader(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        return flask.render_template('upload.html')

#Render userinfo page of RESTful
class UserInfo(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        return flask.render_template('userinfo.html')

#Render listjd page of RESTful
class ListJD(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        return flask.render_template('listjd.html')

#Render fastmatching page of RESTful
class FastMatching(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        return flask.render_template('fastmatching.html')

#Render search page of RESTful
class Search(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        return flask.render_template('search.html')

#Render search page of RESTful
class SearchResult(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        return flask.render_template('result.html')
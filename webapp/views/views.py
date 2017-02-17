import time
import codecs
import os.path

import yaml
import flask
import flask.views
import flask.ext.login

import utils.builtin
import core.basedata
import core.outputstorage
import core.docprocessor
import extractor.information_explorer

import json


class LoginRedirect(flask.views.MethodView):

    def get(self):
        return flask.render_template('gotologin.html')

class Index(flask.views.MethodView):

    def get(self):
        with codecs.open('webapp/features.md', 'r', encoding='utf-8') as fp:
            data = fp.read()
        return flask.render_template('index.html', features=data)

#Render mange page of RESTful
class Manage(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        return flask.render_template('manage.html')

#Render uploader page of RESTful
class Uploader(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        return flask.render_template('uploader.html')

#Render userinfo page of RESTful
class UserInfo(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        return flask.render_template('userinfo.html')

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

#Render resume page of RESTful
class Resume(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self, id):
        return flask.render_template('resume.html')

#Render upload preview page of RESTful
class UploadPreview(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        return flask.render_template('uploadpreview.html')

#Render Project Management page of RESTful
class ProjectManagement(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        return flask.render_template('projectmanagement.html')
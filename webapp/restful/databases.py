import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import sources.industry_id


class ProjectNamesAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def get(self):
        user = flask.ext.login.current_user
        member = user.getmember()
        try:
            return { 'code': 200, 'data': member.projects.keys() }
        except AttributeError:
            return { 'code': 200, 'data': [member.default_model] }


class DBNumbersAPI(flask.views.MethodView):

    decorators = [flask.ext.login.login_required]

    def get(self):
        user = flask.ext.login.current_user
        member = user.getmember()
        return { 'code': 200, 'data': member.getnums() }

    def post(self):
        user = flask.ext.login.current_user
        member = user.getmember()
        return { 'code': 200, 'data': member.getnums() }


class AllSIMSAPI(flask.views.MethodView):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(AllSIMSAPI, self).__init__()
        self.svc_min = flask.current_app.config['SVC_MIN']
        self.min_additionals = flask.current_app.config['MIN_ADDITIONALS']

    def post(self):
        user = flask.ext.login.current_user
        member = user.getmember()
        return { 'code': 200, 'projects': [member.name],
                 'classify': self.min_additionals.keys() }


class ClassifyAPI(flask.views.MethodView):

    def get(self):
        return { 'code': 200, 'data': sources.industry_id.industryID.keys() }


class IndustryAPI(flask.views.MethodView):

    def get(self):
        result = dict()
        for each in sources.industry_id.industryID:
            result.update({each: sources.industry_id.sources[each]})
        return { 'code': 200, 'data': result }

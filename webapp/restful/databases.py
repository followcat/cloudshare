import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import sources.industry_id


class ProjectNamesAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        super(ProjectNamesAPI, self).__init__()

    def get(self):
        user = flask.ext.login.current_user
        member = user.getmember(self.svc_members)
        return { 'code': 200, 'data': member.projects.keys() }


class DBNumbersAPI(flask.views.MethodView):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        super(DBNumbersAPI, self).__init__()

    def get(self):
        user = flask.ext.login.current_user
        member = user.getmember(self.svc_members)
        return { 'code': 200, 'data': member.getnums() }

    def post(self):
        user = flask.ext.login.current_user
        member = user.getmember(self.svc_members)
        return { 'code': 200, 'data': member.getnums() }


class AllSIMSAPI(flask.views.MethodView):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_min = flask.current_app.config['SVC_MIN']
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.min_additionals = flask.current_app.config['MIN_ADDITIONALS']
        super(AllSIMSAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        projectname = args['project']
        user = flask.ext.login.current_user
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        return { 'code': 200, 'projects': member.projects.keys(),
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

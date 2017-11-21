import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource


class ProjectNamesAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        super(ProjectNamesAPI, self).__init__()

    def get(self):
        user = flask.ext.login.current_user
        member = user.getmember(self.svc_members)
        return { 'code': 200, 'data': member.projects.keys() }


class AdditionNamesAPI(Resource):

    def __init__(self):
        self.svc_cls_cv = flask.current_app.config['SVC_CLS_CV']
        super(AdditionNamesAPI, self).__init__()

    def get(self):
        return { 'code': 200, 'data': self.svc_cls_cv.keys() }


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
        super(AllSIMSAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        projectname = args['project']
        user = flask.ext.login.current_user
        member = user.getmember(self.svc_members)
        return { 'code': 200, 'projects': member.projects.keys(),
                 'classify': member.getproject(projectname).getclassify() }


class ClassifyAPI(flask.views.MethodView):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        super(ClassifyAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        projectname = args['project']
        user = flask.ext.login.current_user
        member = user.getmember(self.svc_members)
        return { 'code': 200, 'data': member.getproject(projectname).getclassify() }


class IndustryAPI(flask.views.MethodView):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        super(IndustryAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        projectname = args['project']
        user = flask.ext.login.current_user
        member = user.getmember(self.svc_members)
        return { 'code': 200, 'data': member.getproject(projectname).getindustry() }

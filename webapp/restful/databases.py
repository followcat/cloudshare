import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource


class ProjectNamesAPI(Resource):
    
    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        super(ProjectNamesAPI, self).__init__()

    def get(self):
        return { 'code': 200, 'data': self.svc_mult_cv.projects.keys() }


class AdditionNamesAPI(Resource):

    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        super(AdditionNamesAPI, self).__init__()

    def get(self):
        return { 'code': 200, 'data': self.svc_mult_cv.additionals.keys() }


class DBNumberAPI(Resource):

    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        super(DBNumberAPI, self).__init__()

    def get(self, name):
        numbs = self.svc_mult_cv.getnums()
        return { 'result': numbs[name] }


class DBNumbersAPI(flask.views.MethodView):

    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        super(DBNumbersAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', type = str, location = 'json')

    def get(self):
        return { 'code': 200, 'data': self.svc_mult_cv.getnums() }

    def post(self):
        args = self.reqparse.parse_args()
        project = args['project']
        return { 'code': 200, 'data': self.svc_mult_cv.getprjnums(project) }


class AllSIMSAPI(flask.views.MethodView):

    def __init__(self):
        self.svc_min = flask.current_app.config['SVC_MIN']
        super(AllSIMSAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', type = str, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        project = args['project']
        return { 'code': 200, 'data': self.svc_min.sim[project].keys() }


class ClassifyAPI(flask.views.MethodView):

    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        super(ClassifyAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', type = str, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        project = args['project']
        return { 'code': 200, 'data': self.svc_mult_cv.getproject(project).getclassify() }


class IndustryAPI(flask.views.MethodView):

    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        super(IndustryAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', type = str, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        project = args['project']
        return { 'code': 200, 'data': self.svc_mult_cv.getproject(project).getindustry() }

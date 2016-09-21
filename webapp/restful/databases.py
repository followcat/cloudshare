import flask
import flask.ext.login
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

    def get(self):
        return { 'result': self.svc_mult_cv.getnums() }

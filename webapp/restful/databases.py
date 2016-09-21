import flask
import flask.ext.login
from flask.ext.restful import Resource


class DatabasesAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        super(DatabasesAPI, self).__init__()

    def get(self):
        return { 'code': 200, 'data': [a.name for a in self.svc_mult_cv.additionals] }


class DBNumbersAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        super(DatabasesAPI, self).__init__()

    def get(self, name):
        numbs = self.svc_mult_cv.getnums()
        return { 'result': numbs[name] }

import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource


class CompanyAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('introduction', type = str, location = 'json')
        super(CompanyAPI, self).__init__()

    def get(self, name):
        result = self.svc_mult_cv.default.company_get(name)
        return { 'result': result }

    def post(self, name):
        args = self.reqparse.parse_args()
        introduction = args['introduction']
        user = flask.ext.login.current_user
        result = self.svc_mult_cv.default.company_add(name, introduction, user.id)
        return { 'result': result }


class CompanyListAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        super(CompanyListAPI, self).__init__()

    def get(self):
        result = self.svc_mult_cv.default.company_names()
        return { 'result': result }

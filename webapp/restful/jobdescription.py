import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource


class JobDescriptionAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('coname', type = str, location = 'json')
        self.reqparse.add_argument('status', type = str, location = 'json')
        self.reqparse.add_argument('description', type = str, location = 'json')
        super(JobDescriptionAPI, self).__init__()

    def get(self, id):
        result = self.svc_mult_cv.default.jd_get(id)
        return { 'result': result }

    def put(self, id):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        status = args['status']
        co_name = args['coname']
        description = args['description']
        result = self.svc_mult_cv.default.jd_modify(id, description, status, user.id)
        return { 'result': result }


class JobDescriptionByNameAPI(JobDescriptionAPI):

    def post(self, jdname):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        status = args['status']
        co_name = args['coname']
        description = args['description']
        result = self.svc_mult_cv.default.jd_add(co_name, jd_name, description, user.id, status)
        return { 'result': result }


class JobDescriptionListAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        super(JobDescriptionListAPI, self).__init__()

    def get(self):
        result = self.svc_mult_cv.default.jd_lists()
        return { 'result': result }


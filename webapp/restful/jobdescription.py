import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource


class JobDescriptionAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('coname', location = 'json')
        self.reqparse.add_argument('status', location = 'json')
        self.reqparse.add_argument('description', location = 'json')
        self.reqparse.add_argument('project', location = 'json')
        super(JobDescriptionAPI, self).__init__()

    def get(self, id):
        project = args['project']
        result = self.svc_mult_cv.getproject(project).jd_get(id + '.yaml')
        return { 'code': 200, 'data': result }

    def put(self, id):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        project = args['project']
        status = args['status']
        co_name = args['coname']
        description = args['description']
        result = self.svc_mult_cv.getproject(project).jd_modify(id, description, status, user.id)
        return { 'code': 200, 'data': result, 'message': 'Update job description successed.' }


class JobDescriptionUploadAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('jd_name', location = 'json')
        self.reqparse.add_argument('co_name', location = 'json')
        self.reqparse.add_argument('jd_description', location = 'json')
        self.reqparse.add_argument('project', location = 'json')
        super(JobDescriptionUploadAPI, self).__init__()

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        project = args['project']
        co_name = args['co_name']
        jd_name = args['jd_name']
        description = args['jd_description']
        result = self.svc_mult_cv.getproject(project).jd_add(co_name, jd_name, description, user.id)
        return { 'code': 200, 'data': result, 'message': 'Create job description successed.' }


class JobDescriptionListAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        super(JobDescriptionListAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        project = args['project']
        result = self.svc_mult_cv.getproject(project).jd_lists()
        return { 'code': 200, 'data': result }


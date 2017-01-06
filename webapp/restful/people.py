import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource


class PeopleByUniqueIDAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(PeopleByUniqueIDAPI, self).__init__()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('date', type = str, location = 'json')
        self.reqparse.add_argument('project', type = str, location = 'json')
        self.reqparse.add_argument('uniqueid', type = str, location = 'json')

    def post(self):
        uniqueid = args['uniqueid']
        projectname = args['project']
        project = self.svc_mult_cv.getproject(projectname)
        peopleinfo = project.peo_getyaml(uniqueid)
        return { 'code': 200, 'data': peopleinfo }

    def put(self):
        args = self.reqparse.parse_args()
        user = flask.ext.login.current_user
        id = args['id']
        projectname = args['project']
        update_info = args['update_info']
        project = self.svc_mult_cv.getproject(projectname)
        for key, value in update_info.iteritems():
            data = project.peo_updateyaml(id, key, value, user.id)
            if data is not None:
                response = { 'code': 200, 'data': data, 'message': 'Update information success.' }
            else:
                response = { 'code': 400, 'message': 'Update information error.'}
                break
        return response

    def delete(self):
        args = self.reqparse.parse_args()
        user = flask.ext.login.current_user
        id = args['id']
        date = args['date']
        projectname = args['project']
        update_info = args['update_info']
        project = self.svc_mult_cv.getproject(projectname)
        for key, value in update_info.iteritems():
            data = project.peo_deleteyaml(id, key, value, user.id, date)
            if data is not None:
                response = { 'code': 200, 'data': data, 'message': 'Delete information success.' }
            else:
                response = { 'code': 400, 'message': 'Delete information error.'}
                break
        return response


class PeopleByIDAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(PeopleByIDAPI, self).__init__()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('project', type = str, location = 'json')

    def post(self):
        id = args['id']
        projectname = args['project']
        project = self.svc_mult_cv.getproject(projectname)
        yamlinfo = project.cv_getyaml(id)
        uniqueid = yamlinfo['unique_id']
        peopleinfo = project.peo_getyaml(uniqueid)
        return { 'code': 200, 'data': peopleinfo }

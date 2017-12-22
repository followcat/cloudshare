import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource


class PeopleAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(PeopleAPI, self).__init__()
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('date', type = str, location = 'json')
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('unique_id', type = str, location = 'json')
        self.reqparse.add_argument('update_info', type = dict, location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        unique_id = args['unique_id']
        member = user.getmember(self.svc_members)
        peopleinfo = member.peo_getyaml(unique_id)
        return { 'code': 200, 'data': peopleinfo }

    def put(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        unique_id = args['unique_id']
        update_info = args['update_info']
        member = user.getmember(self.svc_members)
        for key, value in update_info.iteritems():
            data = member.peo_updateyaml(unique_id, key, value, user.name)
            if data is not None:
                response = { 'code': 200, 'data': data, 'message': 'Update information success.' }
            else:
                response = { 'code': 400, 'message': 'Update information error.'}
                break
        return response

    def delete(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        unique_id = args['unique_id']
        date = args['date']
        update_info = args['update_info']
        member = user.getmember(self.svc_members)
        for key, value in update_info.iteritems():
            data = member.peo_deleteyaml(unique_id, key, value, user.name, date)
            if data is not None:
                response = { 'code': 200, 'data': data, 'message': 'Delete information success.' }
            else:
                response = { 'code': 400, 'message': 'Delete information error.'}
                break
        return response


class PeopleByCVAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(PeopleByCVAPI, self).__init__()
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('cv_id', type = str, location = 'json')
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        cv_id = args['cv_id']
        member = user.getmember(self.svc_members)
        yamlinfo = member.cv_getyaml(cv_id)
        try:
            unique_id = yamlinfo['unique_id']
        except KeyError:
            unique_id = yamlinfo['id']
        peopleinfo = member.peo_getyaml(unique_id)
        if not peopleinfo:
            peopleinfo = {'id': unique_id, 'cv': [cv_id]}
        return { 'code': 200, 'data': peopleinfo }

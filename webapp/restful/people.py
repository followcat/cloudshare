import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource


class PeopleByUniqueIDAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(PeopleByUniqueIDAPI, self).__init__()
        self.svc_peo = flask.current_app.config['SVC_PEO_STO']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('uniqueid', type = str, location = 'json')

    def get(self, uniqueid):
        try:
            peopleinfo = self.svc_peo.getyaml(uniqueid)
        except IOError:
            peopleinfo = {'id': '', 'cv': [uniqueid]}
        except KeyError:
            peopleinfo = {'id': '', 'cv': [uniqueid]}
        return { 'code': 200, 'data': peopleinfo }


class PeopleByIDAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(PeopleByIDAPI, self).__init__()
        self.svc_peo = flask.current_app.config['SVC_PEO_STO']
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = str, location = 'json')

    def get(self, id):
        yamlinfo = self.svc_mult_cv.getyaml(id)
        try:
            peopleinfo = self.svc_peo.getyaml(yamlinfo['unique_id'])
        except IOError:
            peopleinfo = {'id': '', 'cv': [yamlinfo['unique_id']]}
        except KeyError:
            peopleinfo = {'id': '', 'cv': [yamlinfo['id']]}
        return { 'code': 200, 'data': peopleinfo }

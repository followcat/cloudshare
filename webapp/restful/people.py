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
        peopleinfo = self.svc_peo.getyaml(uniqueid)
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
        peopleinfo = self.svc_peo.getyaml(yamlinfo['unique_id'])
        return { 'code': 200, 'data': peopleinfo }

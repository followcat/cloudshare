import flask

from flask.ext.restful import reqparse
from flask.ext.restful import Resource

class IndustryAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        super(IndustryAPI, self).__init__()

    def get(self):
        miner = flask.current_app.config['SVC_MIN']
        sim_names = miner.addition_names()
        return { 'code': 200, 'data': sim_names }

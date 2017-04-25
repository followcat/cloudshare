import flask.ext.restful

from demoapp.restful.docmining import *

def initialize(app):
    api = flask.ext.restful.Api(app)

    api.add_resource(DocMiningAPI, '/api/mining/analysisdoc', endpoint = 'docmining')

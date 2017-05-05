import flask.ext.restful

from demoapp.restful.docmining import *

def initialize(app):
    api = flask.ext.restful.Api(app)

    api.add_resource(DocMiningAPI, '/api/mining/analysisdoc', endpoint = 'docmining')
    api.add_resource(DocValuableAPI, '/api/mining/valuable', endpoint = 'valuable')
    api.add_resource(CurrivulumvitaeAPI, '/api/mining/cv', endpoint = 'currivulumvitae')

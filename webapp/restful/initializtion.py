import flask
import flask.ext.restful

from webapp.restful.account import *


def initialize(app):
    api = flask.ext.restful.Api(app)
    api.add_resource(AccountAPI, '/api/account/<string:id>', endpoint = 'account')
    api.add_resource(AccountListAPI, '/api/accountlist', endpoint = 'accountlist')

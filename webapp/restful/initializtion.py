import flask
import flask.ext.restful

from webapp.restful.account import *
from webapp.restful.company import *


def initialize(app):
    api = flask.ext.restful.Api(app)
    api.add_resource(AccountAPI, '/api/account/<string:id>', endpoint = 'account')
    api.add_resource(AccountListAPI, '/api/accountlist', endpoint = 'accountlist')
    api.add_resource(AccountHistoryAPI, '/api/accounthistory', endpoint = 'accounthistory')

    api.add_resource(CompanyAPI, '/api/company/<string:name>', endpoint = 'company')
    api.add_resource(CompanyListAPI, '/api/companylist', endpoint = 'companylist')

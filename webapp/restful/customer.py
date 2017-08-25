import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import utils.builtin


class CustomerAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(CustomerAPI, self).__init__()
        self.svc_customers = flask.current_app.config['SVC_CUSTOMERS']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('customername', type = str, location = 'json')
# get customer's projectname
    def get(self):
        user = flask.ext.login.current_user
        customer = user.getcustomer(self.svc_customers)
        return { 'code': 200, 'result': customer.name }
# user become customer
    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        customername = args['customername']
        result = user.createcustomer(customername, self.svc_customers)
        return { 'code': 200, 'result': result }

    def delete(self):
        user = flask.ext.login.current_user
        result = user.awaycustomer(user.id, self.svc_customers)
        return { 'code': 200, 'result': result }


class ListCustomerAccountsAPI(CustomerAPI):

    def get(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        customer = user.getcustomer(self.svc_customers)
        result = list()
        for id in customer.accounts.ids:
            info = customer.accounts.getinfo(id)
            info['date'] = utils.builtin.strftime(info['date'])
            result.append(info)
        return { 'code': 200, 'result': result }


class CustomerAccountAPI(CustomerAPI):

    def __init__(self):
        super(CustomerAccountAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.svc_msg = flask.current_app.config['SVC_MSG']
        self.reqparse.add_argument('msgid', type = str, location = 'json')
        self.reqparse.add_argument('userid', type = str, location = 'json')

    def post(self, name):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        msgid = args['msgid']
        result = self.svc_msg.process_invite(user.id, msgid, user.name)
        if result is True:
            result = user.joincustomer(user.id, name, self.svc_customers)
        return { 'code': 200, 'result': result }

    def delete(self, name):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        userid = args['userid']
        result = user.awaycustomer(userid, self.svc_customers)
        return { 'code': 200, 'result': result }


class CustomerProjectAPI(CustomerAPI):

    def __init__(self):
        super(CustomerProjectAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('classify', type = list, location = 'json')

    def post(self, projectname):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        classify = args['classify']
        customer = user.getcustomer(self.svc_customers)
        result = customer.add_project(projectname, classify)
        return result

import flask
import flask.ext.login
import services.customer
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


class IsCustomerAPI(CustomerAPI):

    def get(self):
        user = flask.ext.login.current_user
        customer = user.getcustomer(self.svc_customers)
        result = not isinstance(customer, services.customer.DefaultCustomer)
        return { 'code': 200, 'result': result }


class IsCustomerAdminAPI(CustomerAPI):

    def get(self):
        user = flask.ext.login.current_user
        customer = user.getcustomer(self.svc_customers)
        result = customer.check_admin(user.id)
        return { 'code': 200, 'result': result }


class ListCustomerAccountsAPI(CustomerAPI):

    def __init__(self):
        super(ListCustomerAccountsAPI, self).__init__()
        self.svc_account = flask.current_app.config['SVC_ACCOUNT']

    def get(self):
        user = flask.ext.login.current_user
        customer = user.getcustomer(self.svc_customers)
        result = list()
        for id in customer.accounts.ids:
            info = self.svc_account.getinfo(id)
            customer_info = customer.accounts.getinfo(id)
            customer_info['date'] = utils.builtin.strftime(customer_info['date'])
            customer_info['name'] = info['name']
            customer_info['id'] = id
            result.append(customer_info)
        return { 'code': 200, 'result': result }


class CustomerAccountAPI(CustomerAPI):

    def delete(self, userid):
        result = user.awaycustomer(userid, self.svc_customers)
        return { 'code': 200, 'result': result }

class CustomerAdminAPI(CustomerAPI):

    def __init__(self):
        super(CustomerAdminAPI, self).__init__()
        self.reqparse.add_argument('userid', type = str, location = 'json')

    def get(self):
        user = flask.ext.login.current_user
        customer = user.getcustomer(self.svc_customers)
        result = set()
        if customer.check_admin(user.id):
            result = customer.get_admins()
        return { 'code': 200, 'result': result }

    def post(self):
        user = flask.ext.login.current_user
        customer = user.getcustomer(self.svc_customers)
        args = self.reqparse.parse_args()
        userid = args['userid']
        result = customer.add_admin(user.id, userid)
        return { 'code': 200, 'result': result }

    def delete(self):
        user = flask.ext.login.current_user
        customer = user.getcustomer(self.svc_customers)
        args = self.reqparse.parse_args()
        userid = args['userid']
        result = customer.delete_admin(user.id, userid)
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
        result = customer.add_project(projectname, classify, user.id)
        return { 'code': 200, 'result': result }

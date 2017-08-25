import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import services.exception

class UserAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type = str, required = True,
                                   help = 'No email provided', location = 'json')
        self.reqparse.add_argument('phone', type = str, required = True,
                                   help = 'No phone provided', location = 'json')


        super(UserAPI, self).__init__()


    def get(self):
        user = flask.ext.login.current_user
        return { 'code': 200, 'result': user.info }

    def put(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        phone = args['phone']
        email = args['email']
        result = user.updateinfo({'phone': phone, 'email': email})
        return { 'code': 200, 'result': result }


class AccountAPI(Resource):

    def __init__(self):
        self.svc_msg = flask.current_app.config['SVC_MSG']
        self.svc_account = flask.current_app.config['SVC_ACCOUNT']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('password', type = str,
                                   help = 'No password provided', location = 'json')
        self.reqparse.add_argument('email', type = str, required = True,
                                   help = 'No email provided', location = 'json')
        self.reqparse.add_argument('phone', type = str, required = True,
                                   help = 'No phone provided', location = 'json')
        super(AccountAPI, self).__init__()

    def get(self, name):
        result = name in self.svc_account.USERS
        return { 'code': 200, 'result': result}

    def post(self, name):
        args = self.reqparse.parse_args()
        phone = args['phone']
        email = args['email']
        password = args['password']
        bsobj = self.svc_account.baseobj({'name': name, 'phone': phone, 'email': email})
        addresult = self.svc_account.add(bsobj, password)
        if addresult is True:
            msgobj = self.svc_msg.baseobj({'id': bsobj.ID.base})
            msgresult = self.svc_msg.add(msgobj, committer=name)
            result = { 'code': 200, 'message': 'Create user successed.','redirect_url': '/'}
        else:
            result = { 'code': 400, 'message': 'This username is existed.'}
        return result


class PasswordAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_account = flask.current_app.config['SVC_ACCOUNT']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('oldpassword', type = str, location = 'json')
        self.reqparse.add_argument('newpassword', type = str, location = 'json')
        super(PasswordAPI, self).__init__()

    def put(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        result = { 'code': 400, 'message': 'Change password failed.',
                   'error': 'Request arguments error.' }
        if 'oldpassword' in args and 'newpassword' in args:
            oldpassword = args['oldpassword']
            newpassword = args['newpassword']
            changeresult = user.changepassword(oldpassword, newpassword)
            if changeresult is True:
                result = { 'code': 200, 'message': 'Change password successed.' }
            else:
                result = { 'code': 400, 'message': 'Old password validation errors.' }
        return  result


class AccountListAPI(Resource):
    """
        AccoutList RESTful API

        GET    Get Account List.
    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.svc_account = flask.current_app.config['SVC_ACCOUNT']
        super(AccountListAPI, self).__init__()
        self.reqparse.add_argument('name', type = unicode, required = True,
                                   help = 'No name provided', location = 'json')
        self.reqparse.add_argument('password', type = str, required = True,
                                   help = 'No password provided', location = 'json')

    @flask.ext.login.login_required
    def get(self):
        userlist = self.svc_account.get_user_list()
        return { 'code': 200, 'data': userlist }


class AccountHistoryAPI(Resource):
    """
        AccountHistory RESTful API
        GET     Get Accout commit history.
    """

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_customers = flask.current_app.config['SVC_CUSTOMERS']
        super(AccountHistoryAPI, self).__init__()

    def get(self, project):
        user = flask.ext.login.current_user
        customer = user.getcustomer(self.svc_customers)
        info_list = customer.getproject(project).cv_history(user.name, entries=10)
        for info in info_list:
            for md5 in info['filenames']:
                try:
                    info['information'] = customer.getproject(project).cv_getyaml(id)
                except IOError:
                    info['information'] = md5
                info['name'] = md5
            info['message'] = info['message'].decode('utf-8')
        return { 'data': info_list }

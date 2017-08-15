import json

import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import services.exception

class AccountAPI(Resource):
    """
        Accout RESTful API

        PUT     str id
                {'oldpassword': str, 'newpassword': str}
                Modify password.
        POST    str id
                {'password': str}
                Add new account, need root.
        DELETE  str id
                Delete account.
    """

    def __init__(self):
        self.svc_account = flask.current_app.config['SVC_ACCOUNT']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = unicode, required = True,
                                   help = 'No name provided', location = 'json')
        self.reqparse.add_argument('email', type = str, required = True,
                                   help = 'No email provided', location = 'json')
        self.reqparse.add_argument('phone', type = str, required = True,
                                   help = 'No phone provided', location = 'json')
        self.reqparse.add_argument('password', type = str, required = True,
                                   help = 'No password provided', location = 'json')
        self.reqparse.add_argument('oldpassword', type = str, location = 'json')
        self.reqparse.add_argument('newpassword', type = str, location = 'json')
        super(AccountAPI, self).__init__()

    @flask.ext.login.login_required
    def put(self, id):
        result = False
        info = ''
        args = self.reqparse.parse_args()
        if 'oldpassword' not in args or 'newpassword' not in args:
            result = { 'code': 400, 'message': 'Change password failed.', 'error': 'Request arguments error.' }
        else:
            oldpassword = args['oldpassword']
            newpassword = args['newpassword']
        user = flask.ext.login.current_user
        changeresult = user.changepassword(oldpassword, newpassword)
        if changeresult is True:
            result = { 'code': 200, 'message': 'Change password successed.' }
        else:
            result = { 'code': 400, 'message': 'Old password validation errors.' }
        return  result

    def post(self, name):
        args = self.reqparse.parse_args()
        phone = args['phone']
        email = args['email']
        password = args['password']
        bsobj = self.svc_account.baseobj({'name': name, 'phone': phone, 'email': email})
        addresult = self.svc_account.add(bsobj, password)
        if addresult is True:
            result = { 'code': 200, 'message': 'Create user successed.','redirect_url': '/'}
        else:
            result = { 'code': 400, 'message': 'This username is existed.'}
        return result

"""
    def delete(self, name):
        root_user = flask.ext.login.current_user
        if self.svc_account.delete(root_user.name, name):
            result = { 'code': 200, 'message': 'Delete ' + id + ' successed.' }
        else:
            result = { 'code': 400, 'message': 'Deleted ' + id + ' failed.' }
        return result
"""


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
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        super(AccountHistoryAPI, self).__init__()

    def get(self, project):
        user = flask.ext.login.current_user
        info_list = self.svc_mult_cv.getproject(project).cv_history(user.name, entries=10)
        for info in info_list:
            for md5 in info['filenames']:
                try:
                    info['information'] = self.svc_mult_cv.getyaml(md5)
                except IOError:
                    info['information'] = md5
                info['name'] = md5
            info['message'] = info['message'].decode('utf-8')
        return { 'data': info_list }

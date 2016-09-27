import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource
import services
import json
import utils.builtin

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

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_account = flask.current_app.config['SVC_ACCOUNT']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('oldpassword', type = str, location = 'json')
        self.reqparse.add_argument('newpassword', type = str, location = 'json')
        super(AccountAPI, self).__init__()

    def put(self, id):
        result = False
        info = ''
        args = self.reqparse.parse_args()
        if 'oldpassword' not in args or 'newpassword' not in args:
            result = { 'code': 400, 'message': 'Change password failed.', 'error': 'Request arguments error.' }
        else:
            oldpassword = args['oldpassword']
            newpassword = args['newpassword']
        md5newpwd = utils.builtin.md5(oldpassword)
        user = flask.ext.login.current_user
        try:
            if(user.password == md5newpwd):
                user.changepassword(newpassword)
                result = { 'code': 200, 'message': 'Change password successed.' }
            else:
                result = { 'code': 400, 'message': 'Old password validation errors.' }
        except services.exception.ExistsUser:
            pass
        return  result

    def post(self, id):
        result = False
        args = self.reqparse.parse_args()
        password = args['password']
        user = flask.ext.login.current_user
        try:
            result = self.svc_account.add(user.id, id, password)
        except services.exception.ExistsUser:
            pass
        return { 'data': result }

    def delete(self, id):
        root_user = flask.ext.login.current_user
        if self.svc_account.delete(root_user.id, id):
            result = { 'code': 200, 'message': 'Delete ' + id + ' successed.' }
        else:
            result = { 'code': 400, 'message': 'Deleted ' + id + ' failed.' }
        return result


class AccountListAPI(Resource):
    """
        AccoutList RESTful API

        GET    Get Account List.
    """

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.svc_account = flask.current_app.config['SVC_ACCOUNT']
        super(AccountListAPI, self).__init__()
        self.reqparse.add_argument('name', type = str, required = True,
                                   help = 'No name provided', location = 'json')
        self.reqparse.add_argument('password', type = str, required = True,
                                   help = 'No password provided', location = 'json')

    def get(self):
        userlist = self.svc_account.get_user_list()
        return { 'code': 200, 'data': userlist }

    def post(self):
        args = self.reqparse.parse_args()
        name = args['name']
        password = args['password']
        root_user = flask.ext.login.current_user
        try:
            if self.svc_account.add(root_user.id, name, password):
                result = { 'code': 200, 'message': 'Create user successed.'}
            else:
                result = { 'code': 400, 'message': 'The currently logged in user does not have permissions.'}
        except services.exception.ExistsUser:
            result = { 'code': 400, 'message': 'This username is existed.'}
        return result


class AccountHistoryAPI(Resource):
    """
        AccountHistory RESTful API
        GET     Get Accout commit history.
    """

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        super(AccountHistoryAPI, self).__init__()

    def get(self):
        user = flask.ext.login.current_user
        info_list = self.svc_mult_cv.getproject().interface.history(user.id, max_commits=10)
        for info in info_list:
            for md5 in info['filenames']:
                try:
                    info['information'] = self.svc_mult_cv.getyaml(md5)
                except IOError:
                    info['information'] = md5
                info['name'] = md5
            info['message'] = info['message'].decode('utf-8')
        return { 'data': info_list }

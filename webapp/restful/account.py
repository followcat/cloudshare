import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

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
        self.reqparse.add_argument('password', type = str, required = True,
                                   help = 'No password provided', location = 'json')
        self.reqparse.add_argument('oldpassword', type = str, location = 'json')
        self.reqparse.add_argument('newpassword', type = str, location = 'json')
        super(AccountAPI, self).__init__()

    def put(self, id):
        result = False
        info = ''
        args = self.reqparse.parse_args()
        if 'oldpassword' not in args or 'newpassword' not in args:
            result = False 
        else:
            oldpassword = args['oldpassword']
            newpassword = args['newpassword']
        md5newpwd = utils.builtin.md5(oldpassword)
        user = flask.ext.login.current_user
        try:
            if(user.password == md5newpwd):
                user.changepassword(newpassword)
                result = True
            else:
                result = False
        except services.exception.ExistsUser:
            pass
        return  { 'result': result }

    def post(self, id):
        result = False
        args = self.reqparse.parse_args()
        password = args['password']
        user = flask.ext.login.current_user
        try:
            result = self.svc_account.add(user.id, id, password)
        except services.exception.ExistsUser:
            pass
        return { 'result': result }

    def delete(self, id):
        user = flask.ext.login.current_user
        result = self.svc_account.delete(user.id, id)
        return { 'result': result }


class AccountListAPI(Resource):
    """
        AccoutList RESTful API

        GET    Get Account List.
    """

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        self.svc_account = flask.current_app.config['SVC_ACCOUNT']
        super(AccountListAPI, self).__init__()

    def get(self):
        userlist = self.svc_account.get_user_list()
        return { 'result': userlist }


class AccountHistoryAPI(Resource):
    """
        AccountHistory RESTful API
        GET     Get Accout commit history.
    """

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.repo = flask.current_app.config['DATA_DB']
        self.svc_cv = flask.current_app.config['SVC_CV']
        super(AccountHistoryAPI, self).__init__()

    def get(self):
        user = flask.ext.login.current_user
        info_list = self.repo.history(user.id, max_commits=10)
        for info in info_list:
            for md5 in info['filenames']:
                try:
                    info['filenames'] = self.svc_cv.getyaml(md5)
                except IOError:
                    info['filenames'] = md5
                info['name'] = md5
            info['message'] = info['message'].decode('utf-8')
        return { 'result': info_list }

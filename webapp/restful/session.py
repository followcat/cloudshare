import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import webapp.views.account

class SessionAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.svc_account = flask.current_app.config['SVC_ACCOUNT']
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        super(SessionAPI, self).__init__()
        self.reqparse.add_argument('username', type = str, required = True,
                                   help = 'No name provided', location = 'json')
        self.reqparse.add_argument('password', type = str, required = True,
                                   help = 'No password provided', location = 'json')

    def post(self):
        result = dict()
        args = self.reqparse.parse_args()
        username = args['username']
        password = args['password']
        user = webapp.views.account.User.get_fromname(username, self.svc_account,
                                                      members=self.svc_members)
        error = None
        if (user and user.checkpassword(password)):
            flask.ext.login.login_user(user, remember=True)
            token = flask.ext.login.current_user.get_auth_token()
            result = { 'code': 200, 'token': token, 'user': user.name,
                       'id': user.id, 'redirect_url': '/search' }
        else:
            result =  { 'code': 400 , 'message': 'Username or Password Incorrect.' }
        return result

    def delete(self):
        result = dict()
        try:
            flask.ext.login.logout_user()
            result = { 'code': 200, 'massage': 'Sign out successed.', 'redirect_url': '/' }
        except Exception:
            result = { 'code': 200, 'massage': 'Sign out successed.', 'redirect_url': '/' }
        return result

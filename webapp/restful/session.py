import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import webapp.views.account

class SessionAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.svc_account = flask.current_app.config['SVC_ACCOUNT']
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
        user = webapp.views.account.User.get(username, self.svc_account)
        error = None
        if (user and user.checkpassword(password)):
            flask.ext.login.login_user(user, remember=True)
            token = flask.ext.login.current_user.get_auth_token()
            if(user.id == "root"):
                result = { 'code': 200, 'token': token, 'user': user.id, 'redirect_url': '/manage' }
            else:
                flask.session[user.id] = dict()
                result =  { 'code': 200, 'token': token, 'user': user.id, 'redirect_url': '/search' }
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

import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import webapp.views.account
import utils.builtin

class SessionAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.svc_account = flask.current_app.config['SVC_ACCOUNT']
        super(SessionAPI, self).__init__()
        self.reqparse.add_argument('name', type = str, required = True,
                                   help = 'No name provided', location = 'json')
        self.reqparse.add_argument('password', type = str, required = True,
                                   help = 'No password provided', location = 'json')

    def post(self):
        result = dict()
        args = self.reqparse.parse_args()
        name = args['name']
        password = args['password']
        user = webapp.views.account.User.get(name, self.svc_account)
        upassword = utils.builtin.md5(password)
        error = None
        if (user and user.password == upassword):
            flask.ext.login.login_user(user,remember=True)
            token = flask.ext.login.current_user.get_auth_token()
            if(user.id == "root"):
                result = { 'code': 200, 'token': token, 'user': user.id, 'redirect_url': '/manage.html' }
            else:
                flask.session[user.id] = dict()
                result =  { 'code': 200, 'token': token, 'user': user.id, 'redirect_url': '' }
        else:
            result =  { 'code': 400 , 'message': 'Username or Password Incorrect.' }
        return result
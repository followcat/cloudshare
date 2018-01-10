import flask
import flask.ext.login
from itsdangerous import BadSignature

import webapp.views.account

def init_login(app):
    login_manager = flask.ext.login.LoginManager()
    login_manager.login_view = "/"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        svc_account = app.config['SVC_ACCOUNT']
        svc_members = app.config['SVC_MEMBERS']
        return webapp.views.account.User.get(id, svc_account, members=svc_members)

    @login_manager.request_loader
    def load_user_from_request(request):
        token = request.headers.get('Authorization')
        svc_account = app.config['SVC_ACCOUNT']
        svc_members = app.config['SVC_MEMBERS']
        try:
            user = webapp.views.account.User.get_by_authorization(token, svc_account,
                                                                  members=svc_members)
        except BadSignature:
            flask.abort(401)
        return user

def configure(app):

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return flask.render_template('index.html')

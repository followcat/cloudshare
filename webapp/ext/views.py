import flask
import flask.ext.login
import utils.builtin

import webapp.views.mining
import webapp.views.account
import webapp.views.jobdescription

def init_login(app):
    login_manager = flask.ext.login.LoginManager()
    login_manager.login_view = "/gotologin"
    login_manager.setup_app(app)

    @login_manager.user_loader
    def load_user(id):
        return webapp.views.account.User.get(id, app.config['SVC_ACCOUNT'])

    @login_manager.request_loader
    def load_user_from_request(request):
        token = request.headers.get('Authorization')
        svcaccount = flask.current_app.config['SVC_ACCOUNT']
        return webapp.views.account.User.get_by_authorization(token, svcaccount)


def configure(app):

    init_login(app)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return flask.render_template('index.html')

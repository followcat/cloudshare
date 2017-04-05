import flask
import flask.ext.login
import utils.builtin

import webapp.views.views
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

    #RESTful Index page entrance
    @app.route('/')
    def rootindex():
        return flask.redirect(flask.url_for('index'))

    app.add_url_rule(
        '/index',
        view_func=webapp.views.views.Index.as_view('index'),
    )

    #RESTful Uploader page entrance
    app.add_url_rule(
        '/uploader',
        view_func=webapp.views.views.Uploader.as_view('uploader'),
    )

    #RESTful Sync Reload request entrance
    app.add_url_rule(
        '/syncreload',
        view_func=webapp.views.views.SyncReload.as_view('syncreload'),
    )

    #RESTful Manage page entrance
    app.add_url_rule(
        '/manage',
        view_func=webapp.views.views.Manage.as_view('manage'),
    )

    #RESTful UserInfo page entrance
    app.add_url_rule(
        '/userinfo',
        view_func=webapp.views.views.UserInfo.as_view('userinfo'),
    )

    #RESTful FastMatching page entrance
    app.add_url_rule(
        '/fastmatching',
        view_func=webapp.views.views.FastMatching.as_view('fastmatching')
    )

    #RESTful Search page entrance
    app.add_url_rule(
        '/search',
        view_func=webapp.views.views.Search.as_view('search')
    )

    #RESTful SearchResult page entrance
    app.add_url_rule(
        '/search/result',
        view_func=webapp.views.views.SearchResult.as_view('searchresult')
    )

    #RESTful Resume page entrance
    app.add_url_rule(
        '/resume/<path:id>',
        view_func=webapp.views.views.Resume.as_view('resume')
    )

    #RESTful Upload Preview page entrance
    app.add_url_rule(
        '/uploadpreview',
        view_func=webapp.views.views.UploadPreview.as_view('uploadpreview'),
    )

    #RESTful Project Management page entrance
    app.add_url_rule(
        '/pm',
        view_func=webapp.views.views.ProjectManagement.as_view('ProjectManagement'),
    )

    app.add_url_rule(
        '/gotologin',
        view_func=webapp.views.views.LoginRedirect.as_view('gotologin'),
    )


import flask.ext.login

import webapp.core.views
import webapp.core.account


def init_login(app):
    login_manager = flask.ext.login.LoginManager()
    login_manager.login_view = "/gotologin"
    login_manager.setup_app(app)

    @login_manager.user_loader
    def load_user(id):
        return webapp.core.account.User.get(id, app.config['REPO_ACCOUNT'])


def configure(app):

    init_login(app)

    app.add_url_rule(
        '/gotologin',
        view_func=webapp.core.views.LoginRedirect.as_view('gotologin'),
        )

    app.add_url_rule(
        '/search',
        view_func=webapp.core.views.Search.as_view('search'),
        )

    app.add_url_rule(
        '/upload',
        view_func=webapp.core.views.Upload.as_view('upload'),
        )

    app.add_url_rule(
        '/uppreview',
        view_func=webapp.core.views.UploadPreview.as_view('uppreview'),
        )

    app.add_url_rule(
        '/confirm',
        view_func=webapp.core.views.Confirm.as_view('confirm'),
        )

    app.add_url_rule(
        '/show/<path:filename>',
        view_func=webapp.core.views.Show.as_view('show'),
        )

    app.add_url_rule(
        '/edit/<path:filename>',
        view_func=webapp.core.views.Edit.as_view('edit'),
        )

    app.add_url_rule(
        '/modify/<path:filename>',
        view_func=webapp.core.views.Modify.as_view('modify'),
        )

    app.add_url_rule(
        '/preview',
        view_func=webapp.core.views.Preview.as_view('preview'),
        )

    app.add_url_rule(
        '/updateinfo',
        view_func=webapp.core.views.UpdateInfo.as_view('updateinfo'),
        )

    app.add_url_rule(
        '/',
        view_func=webapp.core.views.Index.as_view('index'),
        )

    app.add_url_rule(
        '/login',
        view_func=webapp.core.views.Login.as_view('login'),
        )

    app.add_url_rule(
        '/login/check',
        view_func=webapp.core.views.LoginCheck.as_view('logincheck'),
        )

    app.add_url_rule(
        '/logout',
        view_func=webapp.core.views.Logout.as_view('logout'),
        )

    app.add_url_rule(
        '/userinfo',
        view_func=webapp.core.views.UserInfo.as_view('userinfo'),
        )

    app.add_url_rule(
        '/adduser',
        view_func=webapp.core.views.AddUser.as_view('adduser'),
        )

    app.add_url_rule(
        '/changepassword',
        view_func=webapp.core.views.ChangePassword.as_view('changepassword'),
        )

    app.add_url_rule(
        '/urm',
        view_func=webapp.core.views.Urm.as_view('urm'),
        )

    app.add_url_rule(
        '/urmsetting',
        view_func=webapp.core.views.UrmSetting.as_view('urmsetting'),
        )

    app.add_url_rule(
        '/deleteuser',
        view_func=webapp.core.views.DeleteUser.as_view('deleteuser'),
        )

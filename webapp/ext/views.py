import webapp.core.views
import webapp.core.account


def configure(app):
    webapp.core.views.Search.repo = app.config['REPO_DB']
    app.add_url_rule(
        '/',
        view_func=webapp.core.views.Search.as_view('search'),
        )

    webapp.core.views.Listdata.repo = app.config['REPO_DB']
    app.add_url_rule(
        '/listdata',
        view_func=webapp.core.views.Listdata.as_view('listdata'),
        )

    webapp.core.views.Upload.setup_upload_tmp(app.config['UPLOAD_TEMP'],
                                              app.config['REPO_DB'])
    app.add_url_rule(
        '/upload',
        view_func=webapp.core.views.Upload.as_view('upload'),
        )

    app.add_url_rule(
        '/uppreview',
        view_func=webapp.core.views.UploadPreview.as_view('uppreview'),
        )

    app.add_url_rule(
        '/showtest/<path:filename>',
        view_func=webapp.core.views.Showtest.as_view('showtest'),
        )

    webapp.core.account.RepoAccount.repo = app.config['REPO_DB']
    app.add_url_rule(
        '/index',
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

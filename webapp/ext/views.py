import webapp.core.views


def configure(app):
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
        '/showtest/<path:filename>',
        view_func=webapp.core.views.Showtest.as_view('showtest'),
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

import webapp.core.views


def configure(app):
    app.add_url_rule(
        '/',
        view_func=webapp.core.views.Search.as_view('search'),
        )

    app.add_url_rule(
        '/listdata',
        view_func=webapp.core.views.Listdata.as_view('listdata'),
        )

    webapp.core.views.Upload.setup_upload_tmp(app.config['UPLOAD_TEMP'])
    app.add_url_rule(
        '/upload',
        view_func=webapp.core.views.Upload.as_view('upload'),
        )

    app.add_url_rule(
        '/showtest/<path:filename>',
        view_func=webapp.core.views.Showtest.as_view('showtest'),
        )

import flask.ext.login
import utils.builtin

import webapp.views.views
import webapp.views.mining
import webapp.views.company
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

    #RESTful Uploader page entrance
    app.add_url_rule(
        '/uploader',
        view_func=webapp.views.views.Uploader.as_view('uploader'),
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

    #RESTful ListJD page entrance
    app.add_url_rule(
        '/listjd',
        view_func=webapp.views.views.ListJD.as_view('listjd')
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

    app.add_url_rule(
        '/gotologin',
        view_func=webapp.views.views.LoginRedirect.as_view('gotologin'),
        )

    app.add_url_rule(
        '/upload',
        view_func=webapp.views.views.Upload.as_view('upload'),
        )

    app.add_url_rule(
        '/uppreview',
        view_func=webapp.views.views.UploadPreview.as_view('uppreview'),
        )

    app.add_url_rule(
        '/confirmenglish',
        view_func=webapp.views.views.ConfirmEnglish.as_view('confirmenglish'),
        )

    app.add_url_rule(
        '/show/<path:filename>',
        view_func=webapp.views.views.Show.as_view('show'),
        )

    app.add_url_rule(
        '/mining/position',
        view_func=webapp.views.mining.Position.as_view('miningposition'),
        )

    app.add_url_rule(
        '/mining/region',
        view_func=webapp.views.mining.Region.as_view('miningregion'),
        )

    app.add_url_rule(
        '/mining/capacity',
        view_func=webapp.views.mining.Capacity.as_view('miningcapacity'),
        )

    app.add_url_rule(
        '/analysis/lsi',
        view_func=webapp.views.mining.LSI.as_view('lsi'),
        )

    app.add_url_rule(
        '/analysis/similar',
        view_func=webapp.views.mining.Similar.as_view('mining_similar'),
        )

    app.add_url_rule(
        '/analysis/valuable',
        view_func=webapp.views.mining.Valuable.as_view('valuable'),
        )

    app.add_url_rule(
        '/edit/<path:filename>',
        view_func=webapp.views.views.Edit.as_view('edit'),
        )

    app.add_url_rule(
        '/modify/<path:filename>',
        view_func=webapp.views.views.Modify.as_view('modify'),
        )

    app.add_url_rule(
        '/showeng/<path:id>',
        view_func=webapp.views.views.ShowEnglish.as_view('showenglish'),
        )

    app.add_url_rule(
        '/preview',
        view_func=webapp.views.views.Preview.as_view('preview'),
        )

    app.add_url_rule(
        '/updateinfo',
        view_func=webapp.views.views.UpdateInfo.as_view('updateinfo'),
        )

    app.add_url_rule(
        '/',
        view_func=webapp.views.views.Index.as_view('index'),
        )

    app.add_url_rule(
        '/getbookmark',
        view_func=webapp.views.views.GetBookmark.as_view('getbookmark'),
        )

    app.add_url_rule(
        '/addbookmark',
        view_func=webapp.views.views.AddBookmark.as_view('addbookmark'),
        )

    app.add_url_rule(
        '/delbookmark',
        view_func=webapp.views.views.DelBookmark.as_view('delbookmark'),
        )

    app.add_url_rule(
        '/lsipage',
        view_func=webapp.views.mining.LSI.as_view('lsipage'),
        )

    app.add_url_rule(
        '/addcompany',
        view_func=webapp.views.company.AddCompany.as_view('addcompany'),
        )

    app.add_url_rule(
        '/listcompany',
        view_func=webapp.views.company.ListCompany.as_view('listcompany'),
        )

    app.add_url_rule(
        '/companybyname',
        view_func=webapp.views.company.CompanyByName.as_view('companybyname'),
        )

    app.add_url_rule(
        '/addjd',
        view_func=webapp.views.jobdescription.AddJobDescription.as_view('addjd'),
        )

    app.add_url_rule(
        '/modifyjd',
        view_func=webapp.views.jobdescription.ModifyJobDescription.as_view('modifyjd'),
        )

    app.add_url_rule(
        '/searchjd',
        view_func=webapp.views.jobdescription.SearchJobDescription.as_view('searchjd'),
        )

    # app.add_url_rule(
    #     '/listjd',
    #     view_func=webapp.views.jobdescription.ListJobDescription.as_view('listjd'),
    #     )

    app.add_url_rule(
        '/resumetojd/<path:filename>/<status>',
        view_func=webapp.views.jobdescription.ResumeToJobDescription.as_view('resumetojd'),
        )

    app.add_url_rule(
        '/modellist',
        view_func=webapp.views.mining.ModelList.as_view('modellist'),
        )
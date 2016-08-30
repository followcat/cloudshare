import flask.ext.login
import utils.builtin

import webapp.views.views
import webapp.views.mining
import webapp.views.company
import webapp.views.account
import webapp.views.jobdescription
from itsdangerous import JSONWebSignatureSerializer

def init_login(app):
    login_manager = flask.ext.login.LoginManager()
    login_manager.login_view = "/gotologin"
    login_manager.setup_app(app)

    @login_manager.user_loader
    def load_user(id):
        return webapp.views.account.User.get(id, app.config['SVC_ACCOUNT'])

    @login_manager.token_loader
    def load_token(token):
        s = JSONWebSignatureSerializer(flask.current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception:
            return None
        svcaccount = flask.current_app.config['SVC_ACCOUNT']
        user = webapp.views.account.User.get(data.id, svcaccount)
        if user is not None:
            return user
        return None

    @login_manager.request_loader
    def load_user_from_request(request):
        token = request.headers.get('Authorization')
        if token:
            token = token.replace('Basic ', '', 1)
            try:
                token = base64.b64decode(token)
                s = JSONWebSignatureSerializer(flask.current_app.config['SECRET_KEY'])
                data = s.loads(token)
                svcaccount = flask.current_app.config['SVC_ACCOUNT']
                user = webapp.views.account.User.get(data.id, svcaccount)
                if user is not None:
                    return user
            except Exception:
                return None
        return None

def configure(app):

    init_login(app)

    app.add_url_rule(
        '/gotologin',
        view_func=webapp.views.views.LoginRedirect.as_view('gotologin'),
        )

    app.add_url_rule(
        '/cvnumbers',
        view_func=webapp.views.views.CVnumbers.as_view('cvnumbers'),
        )

    app.add_url_rule(
        '/search',
        view_func=webapp.views.views.Search.as_view('search'),
        )

    app.add_url_rule(
        '/batchupload',
        view_func=webapp.views.views.BatchUpload.as_view('batchupload'),
        )

    app.add_url_rule(
        '/batchconfirm',
        view_func=webapp.views.views.BatchConfirm.as_view('batchconfirm'),
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
        '/confirm',
        view_func=webapp.views.views.Confirm.as_view('confirm'),
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
        view_func=webapp.views.mining.Similar.as_view('similar'),
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
        '/login',
        view_func=webapp.views.views.Login.as_view('login'),
        )

    app.add_url_rule(
        '/login/check',
        view_func=webapp.views.views.LoginCheck.as_view('logincheck'),
        )

    app.add_url_rule(
        '/logout',
        view_func=webapp.views.views.Logout.as_view('logout'),
        )

    app.add_url_rule(
        '/userinfo',
        view_func=webapp.views.views.UserInfo.as_view('userinfo'),
        )

    app.add_url_rule(
        '/adduser',
        view_func=webapp.views.views.AddUser.as_view('adduser'),
        )

    app.add_url_rule(
        '/changepassword',
        view_func=webapp.views.views.ChangePassword.as_view('changepassword'),
        )

    app.add_url_rule(
        '/urm',
        view_func=webapp.views.views.Urm.as_view('urm'),
        )

    app.add_url_rule(
        '/urmsetting',
        view_func=webapp.views.views.UrmSetting.as_view('urmsetting'),
        )

    app.add_url_rule(
        '/deleteuser',
        view_func=webapp.views.views.DeleteUser.as_view('deleteuser'),
        )

    app.add_url_rule(
        '/lsipage',
        view_func=webapp.views.mining.LSI.as_view('lsipage'),
        )

    app.add_url_rule(
        '/makechart',
        view_func=webapp.views.views.MakeChart.as_view('makechart'),
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

    app.add_url_rule(
        '/listjd',
        view_func=webapp.views.jobdescription.ListJobDescription.as_view('listjd'),
        )

    app.add_url_rule(
        '/resumetojd/<path:filename>/<status>',
        view_func=webapp.views.jobdescription.ResumeToJobDescription.as_view('resumetojd'),
        )

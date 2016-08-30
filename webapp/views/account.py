import flask
import flask.ext.login

import services.exception
from itsdangerous import JSONWebSignatureSerializer

class User(flask.ext.login.UserMixin):

    def __init__(self, id, svc_account):
        self.id = id
        self.svc_account = svc_account
        if id not in svc_account.USERS:
            raise services.exception.UserNotFoundError()
        self.password = svc_account.USERS[unicode(id)]

    def get_auth_token(self):
        s = JSONWebSignatureSerializer(flask.current_app.config['SECRET_KEY'])
        return s.dumps({ 'id': self.id })

    def changepassword(self, password):
        self.svc_account.modify(self.id, password)

    @classmethod
    def get(self_class, id, svc_account):
        """
            >>> import shutil
            >>> import services.account
            >>> import webapp.views.account
            >>> import interface.gitinterface
            >>> repo_name = 'webapp/views/test_repo'
            >>> interface = interface.gitinterface.GitInterface(repo_name)
            >>> svc_account = services.account.Account(interface)
            >>> user = webapp.views.account.User.get('root', svc_account)
            >>> user.id
            'root'
            >>> user.password
            u'5f4dcc3b5aa765d61d8327deb882cf99'
            >>> type(webapp.views.account.User.get('None', svc_account))
            <type 'NoneType'>
            >>> shutil.rmtree(repo_name)
        """
        try:
            return self_class(id, svc_account)
        except services.exception.UserNotFoundError:
            return None

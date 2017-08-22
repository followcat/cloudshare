import flask
import flask.ext.login

import services.exception
from itsdangerous import JSONWebSignatureSerializer

class User(flask.ext.login.UserMixin):

    def __init__(self, id, svc_account):
        if not svc_account.exists(id):
            raise services.exception.UserNotFoundError()
        self.id = id
        self.svc_account = svc_account

    def get_auth_token(self):
        s = JSONWebSignatureSerializer(flask.current_app.config['SECRET_KEY'])
        return s.dumps({ 'id': self.id, 'name': self.name })

    def updateinfo(self, info):
        origininfo = self.svc_account.getinfo(self.id)
        origininfo.update(info)
        return self.svc_account.saveinfo(self.id, origininfo,
                                         'User %s update info.'%(self.id),
                                         self.name)

    def checkpassword(self, password):
        return self.svc_account.checkpwd(self.id, password)

    def changepassword(self, oldpassword, newpassword):
        return self.svc_account.updatepwd(self.id, oldpassword, newpassword)

    def getbookmark(self):
        return self.svc_account.getbookmark(self.id)

    def addbookmark(self, id):
        return self.svc_account.addbookmark(self.id, id)

    def delbookmark(self, id):
        return self.svc_account.delbookmark(self.id, id)

    @property
    def info(self):
        return self.svc_account.getinfo(self.id)

    @property
    def name(self):
        return self.info['name']

    @classmethod
    def get(self_class, id, svc_account):
        try:
            return self_class(id, svc_account)
        except services.exception.UserNotFoundError:
            return None

    @classmethod
    def get_fromname(self_class, name, svc_account):
        """
            >>> import shutil
            >>> import services.account
            >>> import webapp.views.account
            >>> pwd_path = 'webapp/views/test_pwd'
            >>> acc_path = 'webapp/views/test_acc'
            >>> svc_password = services.account.Password(pwd_path)
            >>> svc_account = services.account.Account(svc_password, acc_path)
            >>> accobj = svc_account.baseobj({'name': u'admin'})
            >>> svc_account.add(accobj, 'password')
            True
            >>> user = webapp.views.account.User.get_fromname('admin', svc_account)
            >>> user.name
            'admin'
            >>> user.checkpassword('password')
            True
            >>> type(webapp.views.account.User.get_fromname('None', svc_account))
            <type 'NoneType'>
            >>> shutil.rmtree(pwd_path)
            >>> shutil.rmtree(acc_path)
        """
        info = svc_account.getinfo_byname(name)
        return self_class.get(info['id'], svc_account)

    @classmethod
    def get_by_authorization(self_class, token, svc_account):
        if token:
            token = token.replace('Basic ', '', 1)
            s = JSONWebSignatureSerializer(flask.current_app.config['SECRET_KEY'])
            data = s.loads(token)
            return User.get_fromname(data['name'], svc_account)
        return None

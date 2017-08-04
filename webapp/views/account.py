import flask
import flask.ext.login

import services.exception
from itsdangerous import JSONWebSignatureSerializer

class User(flask.ext.login.UserMixin):

    def __init__(self, id, svc_account, svc_customer=None):
        if not svc_account.exists(id):
            raise services.exception.UserNotFoundError()
        self.svc_account = svc_account
        self.svc_customer = svc_customer
        self.info = svc_account.getinfo(id)
        self.customer = None
        if svc_customer is not None:
            self.customer = svc_customer.use(self.info['customer'], id)

    def get_auth_token(self):
        s = JSONWebSignatureSerializer(flask.current_app.config['SECRET_KEY'])
        return s.dumps({ 'id': self.id, 'name': self.name })

    def createcustomer(self, name):
        result = False
        if not self.info['customer']:
            customer = self.svc_customer.create(name)
            customer.add_account(self.name, self.name, creator=True)
            self.customer = svc_customer.use(self.info['customer'], self.id)
            self.svc_account.updateinfo(self.id, 'customer', name, self.id)
            self.info = self.svc_account.getinfo(self.id)
            result = True
        return result

    def awaycustomer(self):
        result = False
        result = self.svc_account.updateinfo(self.id, 'customer', name, self.id)
        if result is True:
            result = self.customer.rm_account(self.id, self.id)
            if result is True:
                self.info = self.svc_account.getinfo(self.id)
        return result

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
    def id(self):
        return self.info['id']

    @property
    def name(self):
        return self.info['name']

    @classmethod
    def get(self_class, id, svc_account, svc_customer):
        try:
            return self_class(id, svc_account, svc_customer)
        except services.exception.UserNotFoundError:
            return None

    @classmethod
    def get_fromname(self_class, name, svc_account, svc_customer):
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
        return self_class.get(info['id'], svc_account, svc_customer)

    @classmethod
    def get_by_authorization(self_class, token, svc_account, svc_customer):
        if token:
            token = token.replace('Basic ', '', 1)
            s = JSONWebSignatureSerializer(flask.current_app.config['SECRET_KEY'])
            data = s.loads(token)
            return User.get_fromname(data['name'], svc_account, svc_customer)
        return None

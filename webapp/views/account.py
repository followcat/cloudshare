import flask
import flask.ext.login

import services.exception
from itsdangerous import JSONWebSignatureSerializer

class User(flask.ext.login.UserMixin):

    def __init__(self, id, svc_account):
        if not svc_account.exists(id):
            raise services.exception.UserNotFoundError()
        self.id = id
        self._name = None
        self.svc_account = svc_account

    def get_auth_token(self):
        s = JSONWebSignatureSerializer(flask.current_app.config['SECRET_KEY'])
        return s.dumps({ 'id': self.id, 'name': self.name })

    def createmember(self, name, svc_members):
        result = self.svc_account.createmember(self.id, name, svc_members)
        return result

    def quitmember(self, awayid, svc_members):
        result = self.svc_account.quitmember(self.id, awayid, svc_members)
        return result

    def joinmember(self, inviter_id, name, svc_members):
        result = self.svc_account.joinmember(inviter_id, self.id, name, svc_members)
        return result

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

    def getmember(self, svc_members):
        return svc_members.use(self.member, self.id)

    def getmessage(self, msgid, svc_message):
        return svc_message.getcontent(self.id, msgid)

    def getinvitedmessage(self, msgid, svc_message):
        return svc_message.getinvitedcontent(self.id, msgid)

    def getreadmessages(self, svc_message):
        return svc_message.getinfo(self.id)['read_chat']

    def getsentmessages(self, svc_message):
        return svc_message.getinfo(self.id)['sent_chat']

    def getunreadmessages(self, svc_message):
        return svc_message.getinfo(self.id)['unread_chat']

    def getinvitedmessages(self, svc_message):
        return svc_message.getinfo(self.id)['invited_member']

    def getinvitermessages(self, svc_message):
        return svc_message.getinfo(self.id)['inviter_member']

    def sentmessage(self, des_name, content, svc_message):
        des_info = self.svc_account.getinfo_byname(des_name)
        des_id = des_info['id']
        result = svc_message.send_chat(self.id, des_id, content, self.name)
        return result

    def readmessage(self, msgid, svc_message):
        result = svc_message.read(self.id, msgid, self.name)
        return result

    def invitemember(self, des_name, svc_message):
        result = False
        if self.member:
            des_info = self.svc_account.getinfo_byname(des_name)
            des_id = des_info['id']
            result = svc_message.send_invitation(self.id, des_id,
                                                 self.member, self.name)
        return result

    @property
    def member(self):
        result = ''
        if 'member' in self.info:
            result = self.info['member']
        return result

    @property
    def defaultmember(self):
        return not self.member

    @property
    def info(self):
        return self.svc_account.getinfo(self.id)

    @property
    def name(self):
        if self._name is None:
            self._name = self.info['name']
        return self._name

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
        try:
            info = svc_account.getinfo_byname(name)
        except KeyError:
            return None
        return self_class.get(info['id'], svc_account)

    @classmethod
    def get_by_authorization(self_class, token, svc_account):
        if token:
            token = token.replace('Basic ', '', 1)
            s = JSONWebSignatureSerializer(flask.current_app.config['SECRET_KEY'])
            data = s.loads(token)
            return User.get_fromname(data['name'], svc_account)
        return None

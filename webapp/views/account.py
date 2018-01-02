import flask
import flask.ext.login

import services.exception
from itsdangerous import JSONWebSignatureSerializer

import core.basedata


class User(flask.ext.login.UserMixin):

    def __init__(self, id, svc_account, svc_members=None):
        if not svc_account.exists(id):
            raise services.exception.UserNotFoundError()
        self.id = id
        self._name = None
        self._member = None
        self.svc_account = svc_account
        self.svc_members = svc_members
        self.svc_projects = None

    def get_auth_token(self):
        s = JSONWebSignatureSerializer(flask.current_app.config['SECRET_KEY'])
        return s.dumps({ 'id': self.id, 'name': self.name })

    def getmember(self):
        return self.member

    def createmember(self, name):
        result = False
        info = self.svc_account.getyaml(self.id)
        if not info['member']:
            self.svc_members.create(name)
            member = self.svc_members.get(name)
            member.join(info['id'], info['id'], info['name'], creator=True)
            metadata = {'id': self.id, 'member': name}
            bsobj = core.basedata.DataObject(metadata=metadata, data=None)
            result = self.svc_account.modify(bsobj, info['name'])
        return result

    def quitmember(self, invited_id):
        result = False
        info = self.svc_account.getyaml(self.id)
        if self.member:
            result = self.member.quit(self.id, invited_id, info['name'])
            if result is True:
                metadata = {'id': invited_id, 'member': ''}
                bsobj = core.basedata.DataObject(metadata=metadata, data=None)
                result = self.svc_account.modify(bsobj, info['name'])
        self._member = None
        return result

    def joinmember(self, inviter_id, name):
        assert not self.member
        assert self.svc_members.exists(name)
        result = False
        inviter_info = self.svc_account.getyaml(inviter_id)
        invited_info = self.svc_account.getyaml(self.id)
        if inviter_info['member'] == name and not invited_info['member']:
            member = self.svc_members.use(name, inviter_id)
            result = member.join(inviter_id, self.id, inviter_info['name'])
            if result is True:
                metadata = {'id': self.id, 'member': name}
                bsobj = core.basedata.DataObject(metadata=metadata, data=None)
                result = self.svc_account.save(bsobj, committer=invited_info['name'])
                assert self.member is member
        return result

    def updateinfo(self, info):
        origininfo = self.svc_account.getyaml(self.id)
        origininfo.update(info)
        bsobj = core.basedata.DataObject(metadata=origininfo, data=None)
        return self.svc_account.modify(bsobj, committer=self.name)

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

    def getmessage(self, msgid, svc_message):
        return svc_message.getcontent(self.id, msgid)

    def deletemessage(self, msgid, svc_message):
        return svc_message.deleteinfo(self.id, msgid, committer=self.name)

    def getinvitedmessage(self, msgid, svc_message):
        return svc_message.getinvitedcontent(self.id, msgid)

    def getreadmessages(self, svc_message):
        return svc_message.getyaml(self.id)['read_chat']

    def getsentmessages(self, svc_message):
        return svc_message.getyaml(self.id)['sent_chat']

    def getunreadmessages(self, svc_message):
        return svc_message.getyaml(self.id)['unread_chat']

    def getinvitedmessages(self, svc_message):
        return svc_message.getyaml(self.id)['invited_member']

    def getinvitermessages(self, svc_message):
        return svc_message.getyaml(self.id)['inviter_member']

    def getprocessedmessages(self, svc_message):
        return svc_message.getyaml(self.id)['processed_member']

    def sentmessage(self, des_name, content, svc_message):
        des_info = self.svc_account.getinfo_byname(des_name)
        des_id = des_info['id']
        result = svc_message.send_chat(self.id, des_id, content, des_name, self.name)
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
                                                 self.member.name, des_name, self.name)
        return result

    @property
    def peopleID(self):
        result = ''
        if 'people' in self.info:
            result = self.info['people']
        return result

    @peopleID.setter
    def peopleID(self, peoID):
        self.svc_account.setpeople(self.id, peoID, self.name)

    @property
    def member(self):
        if not self._member:
            try:
                name = self.info['member']
                self._member = self.svc_members.use(name, self.id)
            except KeyError:
                pass
        return self._member

    @property
    def defaultmember(self):
        return not self.member

    @property
    def info(self):
        return self.svc_account.getyaml(self.id)

    @property
    def name(self):
        if self._name is None:
            self._name = self.info['name']
        return self._name

    @classmethod
    def get(self_class, id, svc_account, members=None):
        try:
            return self_class(id, svc_account, svc_members=members)
        except services.exception.UserNotFoundError:
            return None

    @classmethod
    def get_fromname(self_class, name, svc_account, members=None):
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
        return self_class.get(info['id'], svc_account, members=members)

    @classmethod
    def get_by_authorization(self_class, token, svc_account, members=None):
        if token:
            token = token.replace('Basic ', '', 1)
            s = JSONWebSignatureSerializer(flask.current_app.config['SECRET_KEY'])
            data = s.loads(token)
            return User.get_fromname(data['name'], svc_account, members=members)
        return None

import os.path

import core.basedata
import utils.builtin
import services.exception
import core.outputstorage
import services.base.kv_storage


class Password(services.base.kv_storage.KeyValueStorage):
    """
        >>> import shutil
        >>> import services.account
        >>> repo_path = 'services/test_pwd'
        >>> svc_password = services.account.Password(repo_path)
        >>> bsobj = svc_password.baseobj({'id': 'admin', 'password': 'pwd'})
        >>> svc_password.add(bsobj)
        True
        >>> svc_password.add(bsobj)
        False
        >>> svc_password.updatepwd('admin', 'pwd', 'npwd')
        True
        >>> shutil.rmtree(repo_path)
    """

    YAML_TEMPLATE = (
        ("id",                  str),
        ("password",            str),
    )

    MUST_KEY = ['id', 'password']

    def updatepwd(self, id, oldpassword, newpassword):
        assert self.exists(id)
        result = False
        info = self.getinfo(id)
        if self.check(id, oldpassword):
            metadata = {'id': id, 'password': newpassword}
            bsobj = core.basedata.DataObject(metadata=metadata, data=None)
            result = self.modify(bsobj, committer=id)
        return result

    def check(self, id, password):
        info = self.getinfo(id)
        return info['password'] == password


class Account(services.base.kv_storage.KeyValueStorage):
    """
        >>> import shutil
        >>> import services.account
        >>> acc_path = 'services/test_acc'
        >>> pwd_path = 'services/test_pwd'
        >>> svc_password = services.account.Password(pwd_path)
        >>> svc_account = services.account.Account(svc_password, acc_path)
        >>> accobj = svc_account.baseobj({'name': u'admin'})
        >>> svc_account.add(accobj, 'password')
        True
        >>> svc_account.USERS.keys()
        ['admin']
        >>> svc_account.USERS['admin']['id']
        '21232f297a57a5a743894a0e4a801fc3'
        >>> svc_account.get_user_list()
        ['admin']
        >>> svc_account.add(accobj, 'password')
        False
        >>> shutil.rmtree(acc_path)
        >>> shutil.rmtree(pwd_path)
    """

    MUST_KEY = ['name']
    YAML_TEMPLATE = (
        ("id",                  str),
        ("name",                unicode),
        ("bookmark",            set),
        ("phone",               str),
        ("email",               str),
        ("member",              str),
        ("people",              str),
    )

    def __init__(self, svc_password, path, name=None, iotype=None):
        self.svc_password = svc_password
        super(Account, self).__init__(path, name=name, iotype=iotype)

    def unique(self, bsobj):
        email = bsobj.metadata['email']
        phone = bsobj.metadata['phone']
        return super(Account, self).unique(bsobj) and email not in self.EMAILS and phone not in self.PHONES

    def getinfo_byname(self, name):
        return self.USERS[name]

    def add(self, bsobj, password, committer=None, unique=True,
            yamlfile=True, mdfile=False, do_commit=True):
        pwd_result = False
        result = super(Account, self).add(bsobj, committer, unique,
                                          yamlfile, mdfile, do_commit=do_commit)
        if result:
            metadata = {'id': str(bsobj.ID), 'password': utils.builtin.hash(password)}
            pwdobj = core.basedata.DataObject(metadata=metadata, data=None)
            pwd_result = self.svc_password.add(pwdobj)
        return result and pwd_result

    def checkpwd(self, id, password):
        return self.svc_password.check(id, utils.builtin.hash(password))

    def updatepwd(self, id, oldpassword, newpassword):
        result = False
        if self.exists(id):
            result = self.svc_password.updatepwd(id, utils.builtin.hash(oldpassword), utils.builtin.hash(newpassword))
        return result

    def setpeople(self, id, people, committer):
        metadata = {'id': id, 'people': people}
        bsobj = core.basedata.DataObject(metadata=metadata, data=None)
        return self.modify(bsobj, committer)

    def createmember(self, id, name, svc_members):
        """
            >>> from tests.settings import *
            >>> config = Config()
            >>> svc_account = config.SVC_ACCOUNT
            >>> svc_members = config.SVC_MEMBERS
            >>> accobj = svc_account.baseobj({'name': u'user'})
            >>> svc_account.add(accobj, 'password')
            True
            >>> info = svc_account.getinfo_byname(u'user')
            >>> svc_account.createmember(info['id'], 'added_member', svc_members)
            True
            >>> svc_account.createmember(info['id'], 'added_member', svc_members)
            False
            >>> config.destory()
        """
        result = False
        info = self.getinfo(id)
        if not info['member']:
            svc_members.create(name)
            member = svc_members.get(name)
            member.add_account(info['id'], info['id'], info['name'], creator=True)
            metadata = {'id': id, 'member': name}
            bsobj = core.basedata.DataObject(metadata=metadata, data=None)
            result = self.modify(bsobj, info['name'])
        return result

    def quitmember(self, inviter_id, invited_id, svc_members):
        """
            >>> from tests.settings import *
            >>> config = Config()
            >>> svc_account = config.SVC_ACCOUNT
            >>> svc_members = config.SVC_MEMBERS
            >>> accobj = svc_account.baseobj({'name': u'user'})
            >>> svc_account.add(accobj, 'password')
            True
            >>> accobj2 = svc_account.baseobj({'name': u'user2'})
            >>> svc_account.add(accobj2, 'password2')
            True
            >>> info1 = svc_account.getinfo_byname(u'user')
            >>> info2 = svc_account.getinfo_byname(u'user2')
            >>> svc_account.createmember(info1['id'], 'added_member', svc_members)
            True
            >>> svc_account.quitmember(info1['id'], info1['id'], svc_members)
            False
            >>> svc_account.joinmember(info1['id'], info2['id'], 'added_member', svc_members)
            True
            >>> svc_account.quitmember(info2['id'], info2['id'], svc_members)
            True
            >>> info = svc_account.getinfo_byname(u'user2')
            >>> info['member']
            ''
            >>> config.destory()
        """
        result = False
        info = self.getinfo(inviter_id)
        member = svc_members.use(info['member'], inviter_id)
        if member:
            result = member.rm_account(inviter_id, invited_id, info['name'])
            if result is True:
                if member.check_admin(invited_id) is True:
                    result = member.delete_admin(inviter_id, invited_id)
                metadata = {'id': invited_id, 'member': ''}
                bsobj = core.basedata.DataObject(metadata=metadata, data=None)
                self.modify(bsobj, info['name'])
        return result

    def joinmember(self, inviter_id, invited_id, name, svc_members):
        """
            >>> from tests.settings import *
            >>> config = Config()
            >>> svc_account = config.SVC_ACCOUNT
            >>> svc_members = config.SVC_MEMBERS
            >>> accobj = svc_account.baseobj({'name': u'user'})
            >>> svc_account.add(accobj, 'password')
            True
            >>> invited_accobj = svc_account.baseobj({'name': u'invited'})
            >>> svc_account.add(invited_accobj, 'password')
            True
            >>> info = svc_account.getinfo_byname(u'user')
            >>> invited_info = svc_account.getinfo_byname(u'invited')
            >>> svc_account.createmember(info['id'], 'added_member', svc_members)
            True
            >>> svc_account.joinmember(info['id'], invited_info['id'],
            ...                          'added_member', svc_members)
            True
            >>> member = svc_members.get('added_member')
            >>> member.accounts.exists(invited_info['id'])
            True
            >>> validateinfo = member.accounts.getinfo(invited_info['id'])
            >>> validateinfo['inviter'] == 'user'
            True
            >>> config.destory()
        """
        assert svc_members.exists(name)
        result = False
        inviter_info = self.getinfo(inviter_id)
        invited_info = self.getinfo(invited_id)
        if inviter_info['member'] == name and not invited_info['member']:
            member = svc_members.use(name, inviter_id)
            result = member.add_account(inviter_id, invited_id, inviter_info['name'])
            if result is True:
                metadata = {'id': invited_id, 'member': name}
                bsobj = core.basedata.DataObject(metadata=metadata, data=None)
                self.modify(bsobj, invited_info['name'])
        return result

    @property
    def USERS(self):
        result = dict()
        for id in self.ids:
            info = self.getinfo(id)
            result[info['name']] = info
        return result

    @property
    def PHONES(self):
        result = dict()
        for id in self.ids:
            info = self.getinfo(id)
            result[info['phone']] = info
        return result

    @property
    def EMAILS(self):
        result = dict()
        for id in self.ids:
            info = self.getinfo(id)
            result[info['email']] = info
        return result

    def get_user_list(self):
        result = list()
        for id in self.ids:
            info = self.getinfo(id)
            result.append(info['name'])
        return result

    def getbookmark(self, id):
        info = self.getinfo(id)
        return info['bookmark']

    def addbookmark(self, id, book):
        info = self.getinfo(id)
        name = info['name']
        bookmark = info['bookmark']
        if id in bookmark:
            return False
        bookmark.add(book)
        self.saveinfo(id, info, "Add %s bookmark." % id, name)
        return True

    def delbookmark(self, id, book):
        info = self.getinfo(id)
        name = info['name']
        bookmark = info['bookmark']
        if book not in bookmark:
            return False
        bookmark.remove(book)
        self.saveinfo(id, info, "Delete %s bookmark." % id, name)
        return True

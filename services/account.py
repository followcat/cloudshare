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

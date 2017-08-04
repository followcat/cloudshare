import os.path

import yaml

import core.basedata
import utils.builtin
import services.exception
import core.outputstorage
import services.base.storage


class Password(services.base.storage.BaseStorage):
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

    def __init__(self, path, name=None, searchengine=None, iotype='git'):
        super(Password, self).__init__(path, name=name,
                                       searchengine=searchengine, iotype=iotype)

    def baseobj(self, info):
        metadata = self._metadata(info)
        bsobj = core.basedata.DataObject(metadata=metadata, data=None)
        return bsobj

    def _metadata(self, info):
        assert set(self.MUST_KEY).issubset(set(info.keys()))
        origin = self.generate_info_template()
        for key, datatype in self.YAML_TEMPLATE:
            if key in info and isinstance(info[key], datatype):
                origin[key] = info[key]
        origin['password'] = utils.builtin.hash(origin['password'])
        return origin

    def add(self, bsobj, committer=None, unique=True, yamlfile=True, mdfile=False, do_commit=True):
        return super(Password, self).add(bsobj, committer, unique,
                                         yamlfile, mdfile, do_commit=do_commit)

    def updatepwd(self, id, oldpassword, newpassword):
        assert self.exists(id)
        result = False
        info = self.getinfo(id)
        md5_opwd = utils.builtin.hash(oldpassword)
        if info['password'] == md5_opwd:
            md5_npwd = utils.builtin.hash(newpassword)
            self.updateinfo(id, 'password', md5_npwd, id)
            result = True
        return result

    def get(self, id):
        info = self.getinfo(id)
        return info['password']


class Account(services.base.storage.BaseStorage):
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
        ("customer",            str),
    )

    def __init__(self, svc_password, path, name=None, searchengine=None, iotype='git'):
        self.svc_password = svc_password
        super(Account, self).__init__(path, name=name,
                                      searchengine=searchengine, iotype=iotype)

    def getinfo_byname(self, name):
        return self.USERS[name]

    def baseobj(self, info):
        metadata = self._metadata(info)
        bsobj = core.basedata.DataObject(metadata=metadata, data=None)
        return bsobj

    def _metadata(self, info):
        assert set(self.MUST_KEY).issubset(set(info.keys()))
        origin = self.generate_info_template()
        for key, datatype in self.YAML_TEMPLATE:
            if key in info and isinstance(info[key], datatype):
                origin[key] = info[key]
        origin['id'] = utils.builtin.hash(info['name'])
        return origin

    def add(self, bsobj, password, committer=None, unique=True,
            yamlfile=True, mdfile=False, do_commit=True):
        result = False
        pwd_result = False
        result = super(Account, self).add(bsobj, committer, unique,
                                          yamlfile, mdfile, do_commit=do_commit)
        if result is True:
            pwdobj = self.svc_password.baseobj({'id': str(bsobj.ID), 'password': password})
            pwd_result = self.svc_password.add(pwdobj)
        return result and pwd_result

    def checkpwd(self, id, password):
        return self.svc_password.get(id) == utils.builtin.hash(password)

    def updatepwd(self, id, oldpassword, newpassword):
        result = False
        if self.exists(id):
            result = self.svc_password.updatepwd(id, oldpassword, newpassword)
        return result

    @property
    def USERS(self):
        result = dict()
        for id in self.ids:
            info = self.getinfo(id)
            result[info['name']] = info
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
        bookmark = info['bookmark']
        if id in bookmark:
            return False
        bookmark.add(book)
        self.saveinfo(id, info, "Add %s bookmark." % id, id)
        return True

    def delbookmark(self, id, book):
        info = self.getinfo(id)
        bookmark = info['bookmark']
        if book not in bookmark:
            return False
        bookmark.remove(book)
        self.saveinfo(id, info, "Delete %s bookmark." % id, id)
        return True

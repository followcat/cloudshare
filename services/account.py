import os.path

import yaml

import utils.builtin
import services.base.service
import services.exception
import core.outputstorage


class Account(services.base.service.Service):
    """
        >>> import shutil
        >>> import services.account
        >>> import interface.gitinterface
        >>> repo_name = 'services/test_repo'
        >>> interface = interface.gitinterface.GitInterface(repo_name)
        >>> svc_account = services.account.Account(interface.path)
        >>> svc_account.USERS
        {u'root': u'5f4dcc3b5aa765d61d8327deb882cf99'}
        >>> svc_account.add('root', 'admin', 'password')
        True
        >>> svc_account.USERS['admin']
        u'5f4dcc3b5aa765d61d8327deb882cf99'
        >>> svc_account.get_user_list()
        [u'admin']
        >>> svc_account.add('root', 'admin', 'password') # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        ExistsUser: admin
        >>> svc_account.delete('root', 'admin')
        True
        >>> svc_account.USERS
        {u'root': u'5f4dcc3b5aa765d61d8327deb882cf99'}
        >>> shutil.rmtree(repo_name)
    """
    default_root_name = u'root'
    default_root_password = 'password'
    account_filename = 'account.yaml'

    def __init__(self, interface, name=None):
        super(Account, self).__init__(interface, name)

    def create(self):
        upassword = utils.builtin.md5(self.default_root_password)
        empty_dict = {self.default_root_name: upassword}
        self.interface.add(self.account_filename, yaml.dump(empty_dict),
                           "Add account file.")

    def add(self, mender, id, password):
        if mender != u'root':
            return False
        data = self.USERS
        uid = unicode(id)
        upw = utils.builtin.md5(password)
        if uid in data:
            raise services.exception.ExistsUser(uid)
        data[uid] = upw
        dump_data = yaml.dump(data)
        self.interface.modify(self.account_filename, dump_data,
                              self.default_root_name)
        self.initaccount(uid)
        return True

    def modify(self, id, password):
        data = self.USERS
        uid = unicode(id)
        upw = utils.builtin.md5(password)
        data[uid] = upw
        dump_data = yaml.dump(data)
        self.interface.modify(self.account_filename, dump_data,
                              "Modify %s password." % id, self.default_root_name)

    def delete(self, mender, id):
        if mender != u'root':
            return False
        data = self.USERS
        data.pop(unicode(id))
        dump_data = yaml.dump(data)
        self.interface.modify(self.account_filename, dump_data,
                              "Delete %s user." % id, self.default_root_name)
        return True

    @property
    def USERS(self):
        account_file = self.interface.repo.get_named_file(
            os.path.join('..', self.account_filename))
        if account_file is None:
            self.create()
            account_file = self.interface.repo.get_named_file(
                os.path.join('..', self.account_filename))
        data = yaml.load(account_file.read())
        account_file.close()
        return data

    def get_user_list(self):
        account_list = self.USERS.keys()
        account_list.remove(self.default_root_name)
        user_list = account_list
        return user_list

    def getinfo(self, id):
        filename = core.outputstorage.ConvertName(id).yaml
        account_file = self.interface.repo.get_named_file(
            os.path.join('..', filename))
        if account_file is None:
            self.initaccount(id)
            account_file = self.interface.repo.get_named_file(
            os.path.join('..', filename))
        data = yaml.load(account_file.read())
        account_file.close()
        return data

    def saveinfo(self, id, data, message=None):
        if message is None:
            message = "Modify %s data." % id
        filename = core.outputstorage.ConvertName(id).yaml
        dump_data = yaml.dump(data)
        self.interface.modify(filename, dump_data, message)
        return True

    def initaccount(self, id):
        empty_dict = {'id': id, 'bookmark': set()}
        filename = core.outputstorage.ConvertName(id).yaml
        self.interface.add(filename, yaml.dump(empty_dict),
                           "Add %s account setting." % id)
        return True

    def getbookmark(self, id):
        info = self.getinfo(id)
        return info['bookmark']

    def addbookmark(self, id, book):
        info = self.getinfo(id)
        bookmark = info['bookmark']
        if id in bookmark:
            return False
        bookmark.add(book)
        self.saveinfo(id, info, "Add %s bookmark." % id)
        return True

    def delbookmark(self, id, book):
        info = self.getinfo(id)
        bookmark = info['bookmark']
        if book not in bookmark:
            return False
        bookmark.remove(book)
        self.saveinfo(id, info, "Delete %s bookmark." % id)
        return True

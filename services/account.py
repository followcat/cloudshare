import time
import os.path

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


class Message(services.base.storage.BaseStorage):
    """
        >>> import shutil
        >>> import services.account
        >>> repo_path = 'services/test_msg'
        >>> svc_message = services.account.Message(repo_path)
        >>> svc_message.add(svc_message.baseobj({'id': 'id1'}))
        True
        >>> svc_message.add(svc_message.baseobj({'id': 'id2'}))
        True
        >>> send, receive = svc_message.send_chat('id1', 'id2', 'hello world', 'name1')
        >>> send['relation'] == 'id2'
        True
        >>> receive['relation'] == 'id1'
        True
        >>> info1 = svc_message.getinfo('id1')
        >>> info2 = svc_message.getinfo('id2')
        >>> info1['send_chat'][0] == send
        True
        >>> info2['unread_chat'][0] == receive
        True
        >>> svc_message.read('id2', receive['id'], 'name2')
        True
        >>> info2 = svc_message.getinfo('id2')
        >>> len(info2['unread_chat']) == 0
        True
        >>> info2['read_chat'][0] == receive
        True
        >>> invitation = svc_message.send_invitation('id1', 'id2', 'mock_customer', 'name1')
        >>> info2 = svc_message.getinfo('id2')
        >>> info2['invited_customer'][0] == invitation
        True
        >>> shutil.rmtree(repo_path)
    """
    YAML_TEMPLATE = (
        ("id",                  str),
        ("invited_customer",    list),
        ("send_chat",           list),
        ("read_chat",           list),
        ("unread_chat",         list),
    )

    MUST_KEY = ['id']
    list_item = {"invited_customer", "send_chat", "read_chat", "unread_chat"}
    fix_item  = {"id"}

    def __init__(self, path, name=None, searchengine=None, iotype='git'):
        super(Message, self).__init__(path, name=name,
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
        return origin

    def add(self, bsobj, committer=None, unique=True, yamlfile=True,
        mdfile=False, do_commit=True):
        return super(Message, self).add(bsobj, committer, unique,
                                        yamlfile, mdfile, do_commit=do_commit)

    def _listframe(self, value, username, date=None):
        if date is None:
            date = time.strftime('%Y-%m-%d %H:%M:%S')
        data = {'id': utils.builtin.hash(' '.join([str(time.time()), value, username])),
                'relation': username,
                'content': value,
                'date': date}
        return data

    def _addinfo(self, id, key, value, relation, committer, do_commit=True):
        projectinfo = self.getinfo(id)
        data = self._listframe(value, relation)
        projectinfo[key].insert(0, data)
        self.saveinfo(id, projectinfo,
                      'Add %s key %s.' % (id, key), committer, do_commit=do_commit)
        return data

    def _move(self, id, msgid, origin_key, des_key, committer, do_commit=True):
        result = False
        projectinfo = self.getinfo(id)
        for msg in projectinfo[origin_key]:
            if msg['id'] == msgid:
                projectinfo[origin_key].remove(msg)
                projectinfo[des_key].insert(0, msg)
                self.saveinfo(id, projectinfo, 'Move %s message id %s from %s to %s.' %
                              (id, msgid, origin_key, des_key),
                              committer, do_commit=do_commit)
                result =True
                break
        return result

    def _deleteinfo(self, id, key, msgid, committer, do_commit=True):
        result = None
        projectinfo = self.getinfo(id)
        for msg in projectinfo[key]:
            if msg['id'] == msgid:
                projectinfo[key].remove(msg)
                self.saveinfo(id, projectinfo, 'Delete %s key %s %s.' % (id, key, msgid),
                              committer, do_commit=do_commit)
                result = msg
                break
        return result

    def updateinfo(self, id, key, value, relation, committer, do_commit=True):
        assert key not in self.fix_item
        assert self.exists(id)
        projectinfo = self.getinfo(id)
        result = None
        if key in projectinfo:
            if key in self.list_item:
                result = self._addinfo(id, key, value, relation,
                                       committer, do_commit=do_commit)
            else:
                result = self._modifyinfo(id, key, value, committer, do_commit=do_commit)
        return result

    def deleteinfo(self, id, key, value, committer, date, do_commit=True):
        assert key not in self.fix_item
        assert key in self.list_item
        assert self.exists(id)
        projectinfo = self.getinfo(id)
        result = None
        if key not in projectinfo:
            return result
        result = self._deleteinfo(id, key, msgid, committer, do_commit=do_commit)
        return result

    def read(self, id, msgid, committer):
        return self._move(id, msgid, 'unread_chat', 'read_chat', committer)

    def send_chat(self, ori_id, des_id, content, committer):
        send = self.updateinfo(ori_id, 'send_chat', content, des_id, committer)
        receive = self.updateinfo(des_id, 'unread_chat', content, ori_id, committer)
        return send, receive

    def send_invitation(self, ori_id, des_id, customer, committer):
        return self.updateinfo(des_id, 'invited_customer', customer, ori_id, committer)


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

    def createcustomer(self, id, name, svc_customers):
        """
            >>> from tests.settings import *
            >>> config = Config()
            >>> svc_account = config.SVC_ACCOUNT
            >>> svc_customers = config.SVC_CUSTOMERS
            >>> accobj = svc_account.baseobj({'name': u'user'})
            >>> svc_account.add(accobj, 'password')
            True
            >>> info = svc_account.getinfo_byname(u'user')
            >>> svc_account.createcustomer(info['id'], 'added_customer', svc_customers)
            True
            >>> svc_account.createcustomer(info['id'], 'added_customer', svc_customers)
            False
            >>> config.destory()
        """
        result = False
        info = self.getinfo(id)
        if not info['customer']:
            svc_customers.create(name)
            customer = svc_customers.get(name)
            customer.add_account(info['id'], info['id'], info['name'], creator=True)
            self.updateinfo(id, 'customer', name, info['name'])
            result = True
        return result

    def awaycustomer(self, id, svc_customers):
        """
            >>> from tests.settings import *
            >>> config = Config()
            >>> svc_account = config.SVC_ACCOUNT
            >>> svc_customers = config.SVC_CUSTOMERS
            >>> accobj = svc_account.baseobj({'name': u'user'})
            >>> svc_account.add(accobj, 'password')
            True
            >>> info = svc_account.getinfo_byname(u'user')
            >>> svc_account.createcustomer(info['id'], 'added_customer', svc_customers)
            True
            >>> svc_account.awaycustomer(info['id'], svc_customers)
            True
            >>> info = svc_account.getinfo_byname(u'user')
            >>> info['customer']
            ''
            >>> config.destory()
        """
        result = False
        info = self.getinfo(id)
        customer = svc_customers.use(info['customer'], id)
        if customer:
            result = customer.rm_account(id, id, info['name'])
            if result is True:
                self.updateinfo(id, 'customer', '', info['name'])
        return result

    def joincustomer(self, inviter_id, invited_id, name, svc_customers):
        """
            >>> from tests.settings import *
            >>> config = Config()
            >>> svc_account = config.SVC_ACCOUNT
            >>> svc_customers = config.SVC_CUSTOMERS
            >>> accobj = svc_account.baseobj({'name': u'user'})
            >>> svc_account.add(accobj, 'password')
            True
            >>> invited_accobj = svc_account.baseobj({'name': u'invited'})
            >>> svc_account.add(invited_accobj, 'password')
            True
            >>> info = svc_account.getinfo_byname(u'user')
            >>> invited_info = svc_account.getinfo_byname(u'invited')
            >>> svc_account.createcustomer(info['id'], 'added_customer', svc_customers)
            True
            >>> svc_account.joincustomer(info['id'], invited_info['id'],
            ...                          'added_customer', svc_customers)
            True
            >>> customer = svc_customers.get('added_customer')
            >>> customer.accounts.exists(invited_info['id'])
            True
            >>> validateinfo = customer.accounts.getinfo(invited_info['id'])
            >>> validateinfo['inviter'] == 'user'
            True
            >>> config.destory()
        """
        assert svc_customers.exists(name)
        result = False
        inviter_info = self.getinfo(inviter_id)
        invited_info = self.getinfo(invited_id)
        if inviter_info['customer'] == name and not invited_info['customer']:
            customer = svc_customers.use(name, inviter_id)
            result = customer.add_account(inviter_id, invited_id, inviter_info['name'])
            if result is True:
                self.updateinfo(invited_id, 'customer', name, invited_info['name'])
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

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

    def __init__(self, path, name=None, iotype='git'):
        super(Password, self).__init__(path, name=name, iotype=iotype)

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
        >>> pwd_path = 'services/test_pwd'
        >>> acc_path = 'services/test_acc'
        >>> msg_path = 'services/test_msg'
        >>> svc_password = services.account.Password(pwd_path)
        >>> svc_account = services.account.Account(svc_password, acc_path)
        >>> svc_message = services.account.Message(svc_account, msg_path)
        >>> acc1_info = svc_account.baseobj({'name': 'name1'})
        >>> acc2_info = svc_account.baseobj({'name': 'name2'})
        >>> ID1, ID2 = acc1_info.ID.base, acc2_info.ID.base
        >>> svc_account.add(acc1_info, 'pwd1')
        True
        >>> svc_account.add(acc2_info, 'pwd2')
        True
        >>> svc_message.add(svc_message.baseobj({'id': ID1}))
        True
        >>> svc_message.add(svc_message.baseobj({'id': ID2}))
        True
        >>> sent, receive = svc_message.send_chat(ID1, ID2, 'hello world', 'name1')
        >>> sent['relation'] == ID2
        True
        >>> receive['relation'] == ID1
        True
        >>> info1 = svc_message.getinfo(ID1)
        >>> info2 = svc_message.getinfo(ID2)
        >>> info1['sent_chat'][0] == sent
        True
        >>> info2['unread_chat'][0] == receive
        True
        >>> svc_message.read(ID2, receive['id'], 'name2')
        True
        >>> info2 = svc_message.getinfo(ID2)
        >>> len(info2['unread_chat']) == 0
        True
        >>> info2['read_chat'][0] == receive
        True
        >>> invitation = svc_message.send_invitation(ID1, ID2, 'mock_member', 'name1')
        >>> info1 = svc_message.getinfo(ID1)
        >>> info1['inviter_member'][0]['relation'] == ID2
        True
        >>> info2 = svc_message.getinfo(ID2)
        >>> info2['invited_member'][0] == invitation
        True
        >>> result = svc_message.process_invite(ID2, invitation['id'], ID2)
        >>> result['content'], result['relation'] == ID1
        ('mock_member', True)
        >>> svc_message.getcontent(ID2, invitation['id'])['relation'] == ID1
        True
        >>> len(svc_message.getinfo(ID1)['inviter_member'])
        0
        >>> shutil.rmtree(pwd_path)
        >>> shutil.rmtree(acc_path)
        >>> shutil.rmtree(msg_path)
    """
    YAML_TEMPLATE = (
        ("id",                  str),
        ("invited_member",      list),
        ("inviter_member",      list),
        ("processed_member",    list),
        ("sent_chat",           list),
        ("read_chat",           list),
        ("unread_chat",         list),
    )

    MUST_KEY = ['id']
    list_item = {"invited_member", "inviter_member", "processed_member",
                 "sent_chat", "read_chat", "unread_chat"}
    fix_item  = {"id"}

    def __init__(self, svc_account, path, name=None, iotype='git'):
        super(Message, self).__init__(path, name=name, iotype=iotype)
        self.svc_account = svc_account

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

    def _listframe(self, value, userid, date=None):
        if date is None:
            date = time.strftime('%Y-%m-%d %H:%M:%S')
        relation_info = self.svc_account.getinfo(userid)
        name = relation_info['name']
        data = {'id': utils.builtin.hash(' '.join([str(time.time()), userid])),
                'relation': userid,
                'name': name,
                'content': value,
                'date': date}
        return data

    def _addinfo(self, id, key, value, relation, committer, do_commit=True):
        projectinfo = self.getinfo(id)
        if key not in projectinfo:
            projectinfo[key] = list()
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

    def _deleteinfo(self, id, msgid, committer, do_commit=True):
        result = None
        found = False
        messageinfo = self.getinfo(id)
        for key in messageinfo:
            for msg in messageinfo[key]:
                if msg['id'] == msgid:
                    messageinfo[key].remove(msg)
                    self.saveinfo(id, messageinfo, 'Delete %s key %s %s.' % (id, key, msgid),
                                  committer, do_commit=do_commit)
                    result = msg
                    found = True
                    break
            if found:
                 break
        return result

    def updateinfo(self, id, key, value, relation, committer, do_commit=True):
        assert key not in self.fix_item
        result = None
        if key in [each[0] for each in self.YAML_TEMPLATE]:
            if key in self.list_item:
                result = self._addinfo(id, key, value, relation,
                                       committer, do_commit=do_commit)
            else:
                result = self._modifyinfo(id, key, value, committer, do_commit=do_commit)
        return result

    def deleteinfo(self, id, msgid, committer, do_commit=True):
        result = self._deleteinfo(id, msgid, committer, do_commit=do_commit)
        return result

    def getinfo(self, id):
        assert self.svc_account.exists(id)
        if not self.exists(id):
            tmpobj = self.baseobj({'id': str(id)})
            assert self.add(tmpobj)
        return super(Message, self).getinfo(id)

    def getcontent(self, id, msgid):
        result = None
        msginfo = self.getinfo(id)
        for each in msginfo:
            if each in ['unread_chat', 'read_chat', 'sent_chat']:
                for msg in msginfo[each]:
                    if msg['id'] == msgid:
                        result = msg
                        return result

    def getinvitedcontent(self, id, msgid):
        result = None
        msginfo = self.getinfo(id)
        for each in msginfo:
            if each in ['invited_member']:
                for msg in msginfo[each]:
                    if msg['id'] == msgid:
                        result = msg
                        return result

    def getinvitercontent(self, id, msgid):
        result = None
        msginfo = self.getinfo(id)
        for each in msginfo:
            if each in ['inviter_member']:
                for msg in msginfo[each]:
                    if msg['id'] == msgid:
                        result = msg
                        return result

    def process_invite(self, invited_id, msgid, committer):
        result = None
        sent_info = None
        receive_info = self.getinvitedcontent(invited_id, msgid)
        inviter_id = receive_info['relation']
        for each in self.getinfo(inviter_id)['inviter_member']:
            if receive_info['content'] == each['content'] and invited_id == each['relation']:
                sent_info = each
                break
        if sent_info and receive_info:
            sent_result = self._move(inviter_id, sent_info['id'], 'inviter_member',
                                     'processed_member', committer)
            receive_result = self._move(invited_id, receive_info['id'], 'invited_member',
                                     'processed_member', committer)
            if sent_result and receive_result:
                result = receive_info
        return result

    def read(self, id, msgid, committer):
        return self._move(id, msgid, 'unread_chat', 'read_chat', committer)

    def send_chat(self, ori_id, des_id, content, committer):
        sent = self.updateinfo(ori_id, 'sent_chat', content, des_id, committer)
        receive = self.updateinfo(des_id, 'unread_chat', content, ori_id, committer)
        return sent, receive

    def send_invitation(self, ori_id, des_id, member, committer):
        sent_result = self.updateinfo(ori_id, 'inviter_member', member, des_id, committer)
        receive_result = self.updateinfo(des_id, 'invited_member', member, ori_id, committer)
        return sent_result and receive_result


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
        ("member",              str),
        ("people",              str),
    )

    def __init__(self, svc_password, path, name=None, iotype='git'):
        self.svc_password = svc_password
        super(Account, self).__init__(path, name=name, iotype=iotype)

    def unique(self, bsobj):
        id = bsobj.ID
        email = bsobj.metadata['email']
        phone = bsobj.metadata['phone']
        return id not in self.ids and email not in self.EMAILS and phone not in self.PHONES

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

    def setpeople(self, id, people, committer):
        return self.updateinfo(id, 'people', committer)

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
            self.updateinfo(id, 'member', name, info['name'])
            result = True
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
                self.updateinfo(invited_id, 'member', '', info['name'])
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
                self.updateinfo(invited_id, 'member', name, invited_info['name'])
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

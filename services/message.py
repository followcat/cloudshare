import time

import core.basedata
import utils.builtin
import services.base.frame_storage


class Message(services.base.frame_storage.ListFrameStorage):
    """
        >>> import shutil
        >>> import services.account
        >>> import services.message
        >>> pwd_path = 'services/test_pwd'
        >>> acc_path = 'services/test_acc'
        >>> msg_path = 'services/test_msg'
        >>> svc_password = services.account.Password(pwd_path)
        >>> svc_account = services.account.Account(acc_path)
        >>> svc_message = services.message.Message(msg_path)
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
        >>> sent, receive = svc_message.send_chat(ID1, ID2, 'hello world', acc2_info.name, 'name1')
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
        >>> invitation = svc_message.send_invitation(ID1, ID2, 'mock_member', acc2_info.name, 'name1')
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

    list_frame = {
        'id':           str,
        'relation':     str,
        'name':         str,
        'content':      str,
        'date':         str,
        }

    MUST_KEY = ['id']
    fix_item  = {"id"}

    def moveinfo(self, id, msgid, origin_key, des_key, committer, do_commit=True):
        result = False
        projectinfo = self.getinfo(id)
        info = {}
        for msg in projectinfo[origin_key]:
            if msg['id'] == msgid:
                projectinfo[origin_key].remove(msg)
                projectinfo[des_key].insert(0, msg)
                info[origin_key] = projectinfo[origin_key]
                info[des_key] = projectinfo[des_key]
                break
        if info:
            info['id'] = id
            bsobj = core.basedata.DataObject(metadata=info, data=None)
            result = self.save(bsobj, committer, do_commit=do_commit) 
        return result

    def deleteinfo(self, id, msgid, committer, do_commit=True):
        result = None
        found = False
        messageinfo = self.getinfo(id)
        info = {}
        for key in messageinfo:
            for msg in messageinfo[key]:
                if msg['id'] == msgid:
                    messageinfo[key].remove(msg)
                    found = True
                    break
            if found:
                info[key] = messageinfo[key]
                break
        if info:
            info['id'] = id
            bsobj = core.basedata.DataObject(metadata=info, data=None)
            result = self.save(bsobj, committer, do_commit=do_commit) 
        return result

    def getinfo(self, id):
        if not self.exists(id):
            info = self.generate_info_template()
            info.update({'id': str(id)})
            assert self.add(core.basedata.DataObject(metadata=info, data=None))
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
            sent_result = self.moveinfo(inviter_id, sent_info['id'], 'inviter_member',
                                     'processed_member', committer)
            receive_result = self.moveinfo(invited_id, receive_info['id'], 'invited_member',
                                     'processed_member', committer)
            if sent_result and receive_result:
                result = receive_info
        return result

    def read(self, id, msgid, committer):
        return self.moveinfo(id, msgid, 'unread_chat', 'read_chat', committer)

    def send_chat(self, ori_id, des_id, content, name, committer):
        sent_info = {
            'id': ori_id,
            'sent_chat': {
                    'id': utils.builtin.hash(' '.join([str(time.time()), ori_id])),
                    'content': content,
                    'relation': des_id,
                    'name': name,
                }
        }
        received_info = {
            'id': des_id,
            'unread_chat': {
                    'id': utils.builtin.hash(' '.join([str(time.time()), des_id])),
                    'content': content,
                    'relation': ori_id,
                    'name': name,
            }
        }
        sent = self.modify(core.basedata.DataObject(metadata=sent_info, data=None), committer)
        received = self.modify(core.basedata.DataObject(metadata=sent_info, data=None), committer)
        return sent, received

    def send_invitation(self, ori_id, des_id, member, name, committer):
        inviter_info = {
            'id': ori_id,
            'inviter_member': {
                    'id': utils.builtin.hash(' '.join([str(time.time()), ori_id])),
                    'content': member,
                    'relation': des_id,
                    'name': name,
            }
        }
        invited_info = {
            'id': des_id,
            'invited_member': {
                    'id': utils.builtin.hash(' '.join([str(time.time()), des_id])),
                    'content': member,
                    'relation': ori_id,
                    'name': name,
            }
        }
        sent_result = self.modify(core.basedata.DataObject(metadata=inviter_info, data=None), committer)
        receive_result = self.modify(core.basedata.DataObject(metadata=invited_info, data=None), committer)
        return sent_result and receive_result


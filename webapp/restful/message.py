import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource


class ListUnreadMessagesAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def get(self):
        user = flask.ext.login.current_user
        svc_msg = flask.current_app.config['SVC_MSG']
        return { 'code': 200, 'result': user.getunreadmessages(svc_msg) }


class ListSentMessagesAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def get(self):
        user = flask.ext.login.current_user
        svc_msg = flask.current_app.config['SVC_MSG']
        return { 'code': 200, 'result': user.getsentmessages(svc_msg) }


class ListReadMessagesAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def get(self):
        user = flask.ext.login.current_user
        svc_msg = flask.current_app.config['SVC_MSG']
        return { 'code': 200, 'result': user.getreadmessages(svc_msg) }


class ListInvitedMessagesAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def get(self):
        user = flask.ext.login.current_user
        svc_msg = flask.current_app.config['SVC_MSG']
        return { 'code': 200, 'result': user.getinvitedmessages(svc_msg) }


class ListInviterMessagesAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def get(self):
        user = flask.ext.login.current_user
        svc_msg = flask.current_app.config['SVC_MSG']
        return { 'code': 200, 'result': user.getinvitermessages(svc_msg) }


class MessagesNotifyAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def get(self):
        user = flask.ext.login.current_user
        svc_msg = flask.current_app.config['SVC_MSG']
        msginfo = svc_msg.getinfo(user.id)
        return { 'code': 200, 'result': {'unread_chat': len(msginfo['unread_chat']),
                                         'invited_member': len(msginfo['invited_member'])} }


class MessageAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(MessageAPI, self).__init__()
        self.svc_msg = flask.current_app.config['SVC_MSG']

    # Get message
    def get(self, msgid):
        user = flask.ext.login.current_user
        return { 'code': 200, 'result': user.getmessage(msgid, self.svc_msg) }

    # Read message
    def put(self, msgid):
        user = flask.ext.login.current_user
        result = user.readmessage(msgid, self.svc_msg)
        return { 'code': 200, 'result': result }


class SendMessageAPI(MessageAPI):

    def __init__(self):
        super(SendMessageAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('msgcontent', type = str, location = 'json')

    # Send message
    def post(self, desname):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        msgcontent = args['msgcontent']
        result = user.sentmessage(desname, msgcontent, self.svc_msg)
        return { 'code': 200, 'result': result }


class InvitedMessageAPI(MessageAPI):

    def __init__(self):
        super(InvitedMessageAPI, self).__init__()
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('reply', type = bool, location = 'json')

    def get(self, msgid):
        user = flask.ext.login.current_user
        return { 'code': 200, 'result': user.getinvitedmessage(msgid, self.svc_msg) }

    def post(self, msgid):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        reply = args['reply']
        message = self.svc_msg.process_invite(user.id, msgid, user.name)
        result = False
        if message is not None and reply is True:
            result = user.joinmember(message['relation'], message['content'], self.svc_members)
        return { 'code': 200, 'result': result }


class SendInviteMessageAPI(MessageAPI):
        
    def post(self, desname):
        user = flask.ext.login.current_user
        result = user.invitemember(desname, self.svc_msg)
        return { 'code': 200, 'result': result }

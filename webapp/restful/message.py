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

    def get(self, msgid):
        user = flask.ext.login.current_user
        return { 'code': 200, 'result': user.getinvitedmessage(msgid, self.svc_msg) }


class SendInviteMessageAPI(MessageAPI):
        
    def post(self, desname):
        user = flask.ext.login.current_user
        result = user.invitecustomer(desname, self.svc_msg)
        return { 'code': 200, 'result': result }

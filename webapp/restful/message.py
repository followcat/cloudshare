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
        self.svc_msg = flask.current_app.config['SVC_MSG']
        super(MessageAPI, self).__init__()

    # Get message
    def get(self, msgid):
        user = flask.ext.login.current_user
        return { 'code': 200, 'result': user.getmessage(msgid, self.svc_msg) }

    # Read message
    def put(self, msgid):
        user = flask.ext.login.current_user
        result = user.readmessage(msgid, self.svc_msg)
        return { 'code': 200, 'result': result }


class SendMessageAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_msg = flask.current_app.config['SVC_MSG']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('msgcontent', type = str, location = 'json')
        super(SendMessageAPI, self).__init__()

    # Send message
    def post(self, desname):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        msgcontent = args['msgcontent']
        result = user.sentmessage(desname, msgcontent, self.svc_msg)
        return { 'code': 200, 'result': result }


class CustomerMessageAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.svc_msg = flask.current_app.config['SVC_MSG']
        self.svc_customers = flask.current_app.config['SVC_CUSTOMERS']
        super(CustomerMessageAPI, self).__init__()
        self.reqparse.add_argument('msgid', type = str, location = 'json')
        self.reqparse.add_argument('desname', type = str, location = 'json')
        self.reqparse.add_argument('msgcontent', type = str, location = 'json')

    def get(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        msgid = args['msgid']
        return { 'code': 200, 'result': user.getinvitedmessage(msgid, self.svc_msg) }
        
    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        desname = args['desname']
        result = user.invitecustomer(desname, self.svc_msg)
        return { 'code': 200, 'result': result }

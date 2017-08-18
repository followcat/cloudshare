import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource


class ListUnreadMessagesAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def get(self):
        user = flask.ext.login.current_user
        svc_msg = flask.current_app.config['SVC_MSG']
        return { 'code': 200, 'result': user.getunreadmessage(svc_msg) }


class ListReadMessagesAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def get(self):
        user = flask.ext.login.current_user
        svc_msg = flask.current_app.config['SVC_MSG']
        return { 'code': 200, 'result': user.getreadmessage(svc_msg) }


class ListInvitedMessagesAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def get(self):
        user = flask.ext.login.current_user
        svc_msg = flask.current_app.config['SVC_MSG']
        return { 'code': 200, 'result': user.getinvitedmessages(svc_msg) }


class MessageAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.svc_msg = flask.current_app.config['SVC_MSG']
        super(MessageAPI, self).__init__()
        self.reqparse.add_argument('msgid', type = str, location = 'json')
        self.reqparse.add_argument('desname', type = str, location = 'json')
        self.reqparse.add_argument('msgcontent', type = str, location = 'json')

    def get(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        msgid = args['msgid']
        return { 'code': 200, 'result': user.getmessage(msgid, self.svc_msg) }
        
    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        desname = args['desname']
        msgcontent = args['msgcontent']
        result = user.sentmessage(desname, msgcontent, self.svc_msg)
        return { 'code': 200, 'result': result }

    def put(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        msgid = args['msgid']
        result = user.readmessage(msgid, self.svc_msg)
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

    def put(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        msgid = args['msgid']
        invitemsg = user.getinvitedmessage(msgid, self.svc_msg)
        name = invitemsg['content']
        inviter_id = invitemsg['relation']
        result = user.joincustomer(inviter_id, name, svc_customers)
        return { 'code': 200, 'result': result }

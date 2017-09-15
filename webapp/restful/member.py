import flask
import flask.ext.login
import services.member
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import utils.builtin


class MemberAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(MemberAPI, self).__init__()
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('membername', type = str, location = 'json')
# get member's projectname
    def get(self):
        user = flask.ext.login.current_user
        member = user.getmember(self.svc_members)
        return { 'code': 200, 'result': member.name }
# user become member
    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        membername = args['membername']
        result = user.createmember(membername, self.svc_members)
        return { 'code': 200, 'result': result }

    def delete(self):
        user = flask.ext.login.current_user
        result = user.quitmember(user.id, self.svc_members)
        return { 'code': 200, 'result': result }


class IsMemberAPI(MemberAPI):

    def get(self):
        user = flask.ext.login.current_user
        member = user.getmember(self.svc_members)
        result = not isinstance(member, services.member.DefaultMember)
        return { 'code': 200, 'result': result }


class IsMemberAdminAPI(MemberAPI):

    def get(self):
        user = flask.ext.login.current_user
        member = user.getmember(self.svc_members)
        result = member.check_admin(user.id)
        return { 'code': 200, 'result': result }


class ListMemberAccountsAPI(MemberAPI):

    def __init__(self):
        super(ListMemberAccountsAPI, self).__init__()
        self.svc_account = flask.current_app.config['SVC_ACCOUNT']

    def get(self):
        user = flask.ext.login.current_user
        member = user.getmember(self.svc_members)
        result = list()
        for id in member.accounts.ids:
            info = self.svc_account.getinfo(id)
            member_info = member.accounts.getinfo(id)
            member_info['date'] = utils.builtin.strftime(member_info['date'])
            member_info['name'] = info['name']
            member_info['admin'] = member.check_admin(id)
            member_info['id'] = id
            result.append(member_info)
        return { 'code': 200, 'result': result }


class MemberAccountAPI(MemberAPI):

    def delete(self, userid):
        user = flask.ext.login.current_user
        result = user.quitmember(userid, self.svc_members)
        return { 'code': 200, 'result': result }

class MemberAdminAPI(MemberAPI):

    def __init__(self):
        super(MemberAdminAPI, self).__init__()
        self.reqparse.add_argument('userid', type = str, location = 'json')

    def get(self):
        user = flask.ext.login.current_user
        member = user.getmember(self.svc_members)
        result = set()
        if member.check_admin(user.id):
            result = member.get_admins()
        return { 'code': 200, 'result': result }

    def post(self):
        user = flask.ext.login.current_user
        member = user.getmember(self.svc_members)
        args = self.reqparse.parse_args()
        userid = args['userid']
        result = member.add_admin(user.id, userid)
        return { 'code': 200, 'result': result }

    def delete(self):
        user = flask.ext.login.current_user
        member = user.getmember(self.svc_members)
        args = self.reqparse.parse_args()
        userid = args['userid']
        result = member.delete_admin(user.id, userid)
        return { 'code': 200, 'result': result }


class MemberProjectAPI(MemberAPI):

    def __init__(self):
        super(MemberProjectAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('classify', type = list, location = 'json')

    def post(self, projectname):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        classify = args['classify']
        member = user.getmember(self.svc_members)
        result = member.add_project(projectname, classify, user.id)
        return { 'code': 200, 'result': result }

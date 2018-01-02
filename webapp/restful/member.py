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
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('membername', location = 'json')

# get member's projectname
    def get(self):
        user = flask.ext.login.current_user
        member = user.getmember()
        return { 'code': 200, 'result': member.name }

# user become member
    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        membername = args['membername']
        result = user.createmember(membername)
        return { 'code': 200, 'result': result }

    def delete(self):
        user = flask.ext.login.current_user
        result = user.quitmember(user.id)
        return { 'code': 200, 'result': result }


class IsMemberAPI(MemberAPI):

    def get(self):
        user = flask.ext.login.current_user
        member = user.getmember()
        result = type(member) is not services.member.DefaultMember
        return { 'code': 200, 'result': result }


class IsMemberAdminAPI(MemberAPI):

    def get(self):
        user = flask.ext.login.current_user
        member = user.getmember()
        result = member.check_admin(user.id)
        return { 'code': 200, 'result': result }


class ListMemberAccountsAPI(MemberAPI):

    def __init__(self):
        super(ListMemberAccountsAPI, self).__init__()
        self.svc_account = flask.current_app.config['SVC_ACCOUNT']

    def get(self):
        user = flask.ext.login.current_user
        member = user.getmember()
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
        result = user.quitmember(userid)
        return { 'code': 200, 'result': result }

class MemberAdminAPI(MemberAPI):

    def __init__(self):
        super(MemberAdminAPI, self).__init__()
        self.reqparse.add_argument('userid', type = str, location = 'json')

    def get(self):
        user = flask.ext.login.current_user
        member = user.getmember()
        result = set()
        if member.check_admin(user.id):
            result = member.get_admins()
        return { 'code': 200, 'result': result }

    def post(self):
        user = flask.ext.login.current_user
        member = user.getmember()
        args = self.reqparse.parse_args()
        userid = args['userid']
        result = member.add_admin(user.id, userid)
        return { 'code': 200, 'result': result }

    def delete(self):
        user = flask.ext.login.current_user
        member = user.getmember()
        args = self.reqparse.parse_args()
        userid = args['userid']
        result = member.delete_admin(user.id, userid)
        return { 'code': 200, 'result': result }


class MemberProjectAPI(MemberAPI):

    def __init__(self):
        super(MemberProjectAPI, self).__init__()

    def post(self, projectname):
        user = flask.ext.login.current_user
        member = user.getmember()
        result = member.add_project(projectname, user.id)
        return { 'code': 200, 'result': result }

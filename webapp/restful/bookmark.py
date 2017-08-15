import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import webapp.views.account

class BookmarkAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.svc_customers = flask.current_app.config['SVC_CUSTOMERS']
        super(BookmarkAPI, self).__init__()
        self.reqparse.add_argument('bookmark_id', type = str, required = True,
                                   help = 'No bookmark id provided', location = 'json')

    def get(self, name):
        user = flask.ext.login.current_user
        data = []
        customer = user.getcustomer(self.svc_customers)
        project = customer.getproject()
        bookmark_list = list(user.getbookmark())
        for bookmark_item in bookmark_list:
            yaml_info = project.cv_getyaml(bookmark_item)
            data.append(yaml_info)
        if name == user.name:
            result = { 'code': 200, 'data': data }
        else:
            result = { 'code': 400, 'message': 'Illegal user.' }
        return result

    def post(self, name):
        args = self.reqparse.parse_args()
        user = flask.ext.login.current_user
        if name == user.name:
            bookmark_id = args['bookmark_id']
            r = user.addbookmark(bookmark_id)
            if r:
                result = { 'code': 200, 'message': 'Add bookmark successed.' }
            else:
                result = { 'code': 400, 'message': 'Add bookmark failed.' }
        else:
            result = { 'code': 400, 'message': 'Illegal user.' }
        return result

    def delete(self, name):
        args = self.reqparse.parse_args()
        user = flask.ext.login.current_user
        if name == user.name:
            bookmark_id = args['bookmark_id']
            r = user.delbookmark(bookmark_id)
            if r:
                result = { 'code': 200, 'message': 'Delete successed.' }
            else:
                result = { 'code': 400, 'message': 'Delete failed.' }
        else:
            result = { 'code': 400, 'message': 'Illegal user.' }
        return result
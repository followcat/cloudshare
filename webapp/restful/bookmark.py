import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import webapp.views.account

class BookmarkAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.svc_account = flask.current_app.config['SVC_ACCOUNT']
        super(BookmarkAPI, self).__init__()
        self.reqparse.add_argument('bookmark_id', type = str, required = True,
                                   help = 'No bookmark id provided', location = 'json')

    def get(self, id):
        data = []
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        user = flask.ext.login.current_user
        bookmark_list = list(user.getbookmark())
        for bookmark_item in bookmark_list:
            yaml_info = svc_mult_cv.getyaml(bookmark_item)
            data.append(yaml_info)
        if id == user.id:
            result = { 'code': 200, 'data': data }
        else:
            result = { 'code': 400, 'message': 'Illegal user.' }
        return result

    def post(self, id):
        args = self.reqparse.parse_args()
        user = flask.ext.login.current_user
        if id == user.id:
            bookmark_id = args['bookmark_id']
            r = user.addbookmark(bookmark_id)
            if r:
                result = { 'code': 200, 'message': 'Add bookmark successed.' }
            else:
                result = { 'code': 400, 'message': 'Add bookmark failed.' }
        else:
            result = { 'code': 400, 'message': 'Illegal user.' }
        return result

    def delete(self, id):
        args = self.reqparse.parse_args()
        user = flask.ext.login.current_user
        if id == user.id:
            bookmark_id = args['bookmark_id']
            r = user.delbookmark(bookmark_id)
            if r:
                result = { 'code': 200, 'message': 'Delete successed.' }
            else:
                result = { 'code': 400, 'message': 'Delete failed.' }
        else:
            result = { 'code': 400, 'message': 'Illegal user.' }
        return result
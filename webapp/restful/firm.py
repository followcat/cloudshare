import math

import flask
import flask.ext.login
from flask import request
from flask.ext.restful import Resource, reqparse

import core.basedata
import extractor.information_explorer


class FirmAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        super(FirmAPI, self).__init__()

    def get(self, id):
        user = flask.ext.login.current_user
        member = user.getmember()
        result = member.co_getyaml(id)
        code = 200
        if not result:
            code = 404
        return {'data': result}, code


class FirmSearchAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        super(FirmSearchAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('q', type=unicode, location='args')
        self.reqparse.add_argument('page', type=int, default=1, location = 'args')
        self.reqparse.add_argument('size', type=int, default=20, location = 'args')

    def get(self):
        args = self.reqparse.parse_args()
        query = args['q']
        page = args['page']
        size = args['size']
        user = flask.ext.login.current_user
        member = user.getmember()
        total, searches = member.co_search(filterdict={'name': query},
                                           start=(page-1)*size,
                                           size=size)
        pages = int(math.ceil(float(total)/size))
        datas = list()
        for item in searches:
            info = member.co_getyaml(item['_id'])
            if info:
                datas.append(info)
            else:
                total -= 1
        code = 200
        return {'data': datas, 'total': total}, code


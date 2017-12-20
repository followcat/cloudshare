import os
import math
import datetime

import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import utils.builtin


class CurrivulumvitaeAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(CurrivulumvitaeAPI, self).__init__()
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        member = user.getmember(self.svc_members)
        result = user.getbookmark()
        yaml = member.cv_getyaml(id)
        if yaml['id'] in result:
            yaml['collected'] = True
        else:
            yaml['collected'] = False
        yaml['date'] = utils.builtin.strftime(yaml['date'])
        cv_projects = member.cv_projects(id)
        en_html = ''
        html = member.cv_gethtml(id)
        if 'enversion' in yaml:
            en_html = member.cv_getmd_en(id)
        return { 'code': 200, 'data': { 'html': html, 'en_html': en_html,
                                        'yaml_info': yaml, 'projects': cv_projects } }


class UpdateCurrivulumvitaeInformation(Resource):
    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(UpdateCurrivulumvitaeInformation, self).__init__()
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('update_info', type = dict, location = 'json')

    def put(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        member = user.getmember(self.svc_members)
        update_info = args['update_info']

        for key, value in update_info.iteritems():
            data = member.cv_updateyaml(id, key,
                                                                      value, user.name)
            if data is not None:
                response = { 'code': 200, 'data': data, 'message': 'Update information success.' }
            else:
                response = { 'code': 400, 'message': 'Update information error.'}
                break
        return response


class SearchCVbyTextAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(SearchCVbyTextAPI, self).__init__()
        self.svc_index = flask.current_app.config['SVC_INDEX']
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('search_text', location = 'json')
        self.reqparse.add_argument('page', type = int, location = 'json')
        self.reqparse.add_argument('filterdict', type=dict, location = 'json')

    def post(self):
        count = 20
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        text = args['search_text']
        cur_page = args['page'] if args['page'] else 1
        filterdict = args['filterdict'] if args['filterdict'] else {}
        member = user.getmember(self.svc_members)
        index = self.svc_index.config['CV_MEM']
        filterdict['content'] = text
        total, searchs = self.svc_index.search(index=index, doctype=[member.id],
                                        filterdict=filterdict, source=False,
                                        kwargs={'_source_exclude': ['content']},
                                        start=(cur_page-1)*count, size=count)
        pages = int(math.ceil(float(total)/count))
        datas = list()
        for item in searchs:
            id = item['_id']
            yaml_info = member.cv_getyaml(id)
            info = {
                'author': yaml_info['committer'],
                'time': utils.builtin.strftime(yaml_info['date']),
            }
            datas.append({ 'cv_id': yaml_info['id'],
                           'yaml_info': yaml_info,
                           'info': info})
        return {
            'code': 200,
            'data': {
                'keyword': text,
                'datas': datas,
                'pages': pages,
                'totals': total,
            }
        }

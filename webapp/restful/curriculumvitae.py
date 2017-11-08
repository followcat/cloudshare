import os

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
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        result = user.getbookmark()
        yaml = project.cv_getyaml(id)
        if yaml['id'] in result:
            yaml['collected'] = True
        else:
            yaml['collected'] = False
        yaml['date'] = utils.builtin.strftime(yaml['date'])
        cv_projects = member.cv_projects(id)
        en_html = ''
        html = project.cv_gethtml(id)
        if 'enversion' in yaml:
            en_html = project.cv_getmd_en(id)
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
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        update_info = args['update_info']

        for key, value in update_info.iteritems():
            data = project.cv_updateyaml(id, key,
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
        self.cv_indexname = flask.current_app.config['ES_CONFIG']['CV_INDEXNAME']
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
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        searchs = member.cv_search(keywords=text, filterdict=filterdict,
                                   start=(cur_page-1)*count, size=count)
        total = member.cv_count(keywords=text, filterdict=filterdict)
        pages = total/count
        datas = self.paginate([each[0] for each in searchs], project)
        return {
            'code': 200,
            'data': {
                'keyword': text,
                'datas': datas,
                'pages': pages,
                'totals': total,
            }
        }

    def paginate(self, results, project):
        datas = list()
        for id in results:
            yaml_info = project.cv_getyaml(id)
            try:
                info = {
                    'author': yaml_info['committer'],
                    'time': utils.builtin.strftime(yaml_info['date']),
                }
            except Exception:
                continue
            datas.append({ 'cv_id': yaml_info['id'],
                           'yaml_info': yaml_info,
                           'info': info})
        return datas

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
        self.svc_customers = flask.current_app.config['SVC_CUSTOMERS']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('project', type = str, location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        projectname = args['project']
        customer = user.getcustomer(self.svc_customers)
        project = customer.getproject(projectname)
        result = user.getbookmark()
        if yaml['id'] in result:
            yaml['collected'] = True
        else:
            yaml['collected'] = False
        en_html = ''
        yaml['date'] = utils.builtin.strftime(yaml['date'])
        if 'enversion' in yaml:
            en_html = project.cv_getmd_en(id)
        return { 'code': 200, 'data': { 'html': html, 'en_html': en_html, 'yaml_info': yaml } }


class UpdateCurrivulumvitaeInformation(Resource):
    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(UpdateCurrivulumvitaeInformation, self).__init__()
        self.svc_customers = flask.current_app.config['SVC_CUSTOMERS']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('project', type = str, location = 'json')
        self.reqparse.add_argument('update_info', type = dict, location = 'json')

    def put(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        projectname = args['project']
        customer = user.getcustomer(self.svc_customers)
        project = customer.getproject(projectname)
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
        self.svc_customers = flask.current_app.config['SVC_CUSTOMERS']
        self.index = flask.current_app.config['SVC_INDEX']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', type = str, location = 'json')
        self.reqparse.add_argument('search_text', location = 'json')
        self.reqparse.add_argument('page', type = int, location = 'json')
        self.reqparse.add_argument('filterdict', type=dict, location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        text = args['search_text']
        cur_page = args['page']
        filterdict = args['filterdict'] if args['filterdict'] else {}
        projectname = args['project']
        customer = user.getcustomer(self.svc_customers)
        project = customer.getproject(projectname)
        searchs = dict(project.cv_search(text, selected=['cloudshare']))
        yaml_searchs = dict(project.cv_search_yaml(text, selected=['cloudshare']))
        for id in yaml_searchs:
            if id in searchs:
                searchs[id] += yaml_searchs[id]
            else:
                searchs[id] = yaml_searchs[id]
        results = sorted(searchs.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        ids = set([cv[0] for cv in results])
        results = self.index.filter_ids(results, filterdict, ids, uses=[projectname])
        results = [result[0] for result in results]
        count = 20
        datas, pages = self.paginate(results, cur_page, count, project)
        return {
            'code': 200,
            'data': {
                'keyword': text,
                'datas': datas,
                'pages': pages,
                'totals': len(results),
            }
        }

    def paginate(self, results, cur_page, eve_count, project):
        if not cur_page:
            cur_page = 1
        sum = len(results)
        if sum%eve_count != 0:
            pages = sum/eve_count + 1
        else:
            pages = sum/eve_count
        datas = []
        ids = []
        for id in results[(cur_page-1)*eve_count:cur_page*eve_count]:
            if id not in ids:
                ids.append(id)
            else:
                continue
            try:
                yaml_info = project.cv_getyaml(id)
            except IOError:
                ids.remove(id)
                continue
            info = {
                'author': yaml_info['committer'],
                'time': utils.builtin.strftime(yaml_info['date']),
            }
            datas.append({ 'cv_id': id, 'yaml_info': yaml_info, 'info': info})
        return datas, pages

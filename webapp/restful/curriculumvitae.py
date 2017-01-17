import os

import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import utils.builtin
import core.outputstorage


class CurrivulumvitaeAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(CurrivulumvitaeAPI, self).__init__()
        self.svc_peo = flask.current_app.config['SVC_PEO_STO']
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('project', type = str, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        id = args['id']
        project = args['project']
        html = self.svc_mult_cv.gethtml(id, projectname=project)
        yaml = self.svc_mult_cv.getyaml(id, projectname=project)
        user = flask.ext.login.current_user
        result = user.getbookmark()
        if yaml['id'] in result:
            yaml['collected'] = True
        else:
            yaml['collected'] = False
        en_html = ''
        yaml['date'] = utils.builtin.strftime(yaml['date'])
        if 'enversion' in yaml:
            en_html = self.svc_mult_cv.getproject(project).cv_getmd_en(id)
        return { 'code': 200, 'data': { 'html': html, 'en_html': en_html, 'yaml_info': yaml } }


class UpdateCurrivulumvitaeInformation(Resource):
    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(UpdateCurrivulumvitaeInformation, self).__init__()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('date', type = str, location = 'json')
        self.reqparse.add_argument('project', type = str, location = 'json')
        self.reqparse.add_argument('update_info', type = dict, location = 'json')

    def put(self):
        args = self.reqparse.parse_args()
        user = flask.ext.login.current_user
        id = args['id']
        project = args['project']
        update_info = args['update_info']

        for key, value in update_info.iteritems():
            data = self.svc_mult_cv.getproject(project).cv_updateyaml(id, key, value, user.id)
            if data is not None:
                response = { 'code': 200, 'data': data, 'message': 'Update information success.' }
            else:
                response = { 'code': 400, 'message': 'Update information error.'}
                break
        return response

    def delete(self):
        args = self.reqparse.parse_args()
        user = flask.ext.login.current_user
        id = args['id']
        date = args['date']
        project = args['project']
        update_info = args['update_info']

        for key, value in update_info.iteritems():
            data = self.svc_mult_cv.getproject(project).cv_deleteyaml(id, key, value,
                                                                      user.id, date)
            if data is not None:
                response = { 'code': 200, 'data': data, 'message': 'Delete information success.' }
            else:
                response = { 'code': 400, 'message': 'Delete information error.'}
                break
        return response


class SearchCVbyTextAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(SearchCVbyTextAPI, self).__init__()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', type = str, location = 'json')
        self.reqparse.add_argument('search_text', location = 'json')
        self.reqparse.add_argument('page', type = int, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        project = args['project']
        text = args['search_text']
        cur_page = args['page']
        results = self.svc_mult_cv.search(text, project)
        yaml_results = self.svc_mult_cv.search_yaml(text, project)
        results.update(yaml_results)
        count = 20
        datas, pages = self.paginate(list(results), cur_page, count)
        return {
            'code': 200,
            'data': {
                'keyword': text,
                'datas': datas,
                'pages': pages,
                'totals': len(results),
            }
        }

    def paginate(self, results, cur_page, eve_count):
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
                yaml_info = self.svc_mult_cv.getyaml(id)
            except IOError:
                ids.remove(id)
                continue
            info = {
                'author': yaml_info['committer'],
                'time': utils.builtin.strftime(yaml_info['date']),
            }
            datas.append({ 'cv_id': id, 'yaml_info': yaml_info, 'info': info})
        return datas, pages

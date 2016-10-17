import os

import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import utils.builtin
import core.outputstorage


class SearchbyTextAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(SearchbyTextAPI, self).__init__()
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
        names = []
        for each in results[(cur_page-1)*eve_count:cur_page*eve_count]:
            base, suffix = os.path.splitext(each)
            name = core.outputstorage.ConvertName(base)
            if name not in names:
                names.append(name)
            else:
                continue
            try:
                yaml_info = self.svc_mult_cv.getyaml(base)
            except IOError:
                names.remove(name)
                continue
            info = {
                'author': yaml_info['committer'],
                'time': utils.builtin.strftime(yaml_info['date']),
            }
            yaml_info['experience'] = self.experience_process(yaml_info['experience'])
            datas.append({ 'cv_id': name, 'yaml_info': yaml_info, 'info': info})
        return datas, pages

    def experience_process(self, experience):
        ex_company = experience['company'] if len(experience) and 'company' in experience else []
        ex_position = experience['position'] if len(experience) and 'position' in experience else []

        if len(ex_position) > 0:
            for position in ex_position:
                for company in ex_company:
                    if position['at_company'] == company['id']:
                        position['company'] = company['name']
                        if 'business' in company:
                            position['business'] = company['business']
            return ex_position
        else:
            return ex_company

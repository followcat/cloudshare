import os.path

import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import utils.builtin
import core.mining.info
import core.mining.valuable

import json

class BaseAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(BaseAPI, self).__init__()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('md_ids', type = list, location = 'json')

    def calculate_work_month(self, begin_y, begin_m, end_y, end_m):
        year = int(end_y) - int(begin_y)
        month = int(end_m) - int(begin_m)
        return year * 12 + month



class PositionAPI(BaseAPI): 

    def get(self, text):
        args = self.reqparse.parse_args()
        if args['md_ids'] and len(text) > 0:
            searches = args['md_ids']
        else:
            searches = self.svc_mult_cv.search(text)
        result = dict()
        for name in searches:
            positions = []
            try:
                yaml_data = self.svc_mult_cv.getyaml(name)
            except IOError:
                continue
            if 'position' in yaml_data['experience']:
                positions = [p['name'] for p in yaml_data['experience']['position']]
            for position in positions:
                if position not in result:
                    result[position] = []
                result[position].append(name)
        return { 'result': result }


class RegionAPI(BaseAPI):

    def get(self):
        args = self.reqparse.parse_args()
        result = []
        for id in args['md_ids']:
            stream = self.svc_mult_cv.getmd(id)
            result.append(core.mining.info.region(stream))
        return { 'result': result }


class CapacityAPI(BaseAPI):

    def get(self):
        args = self.reqparse.parse_args()
        result = []
        for id in args['md_ids']:
            stream = self.svc_mult_cv.getmd(id)
            result.append({'md':id, 'capacity': core.mining.info.capacity(stream)})
        return { 'result': result }


class AbilityAPI(BaseAPI):

    def post(self):
        args = self.reqparse.parse_args()
        result = []
        for id in args['md_ids']:
            stream = self.svc_mult_cv.getmd(id)
            capacitys = core.mining.info.capacity(stream)
            month = 0
            actpoint = 0
            doclen = 0
            for capacity in capacitys:
                if (len(capacity['begin']) and len(capacity['end'])):
                    month += self.calculate_work_month(capacity['begin'][0], capacity['begin'][1], capacity['end'][0], capacity['end'][1])
                actpoint += float(capacity['actpoint'])
                doclen += float(capacity['doclen'])
            result.append({ 'md': id, 'ability': { 'work_year': month/12, 'ability_value': (actpoint/doclen)*100 } })
        return { 'code': 200, 'data': result }


class ExperienceAPI(BaseAPI):

    def post(self):
        args = self.reqparse.parse_args()
        result = []
        for id in args['md_ids']:
            stream = self.svc_mult_cv.getmd(id)
            capacitys = core.mining.info.capacity(stream)
            month = 0
            actpoint = 0
            for capacity in capacitys:
                if (len(capacity['begin']) and len(capacity['end'])):
                    month += self.calculate_work_month(capacity['begin'][0], capacity['begin'][1], capacity['end'][0], capacity['end'][1])
                actpoint += capacity['actpoint']
            result.append({ 'md': id, 'experience': { 'work_year': month/12, 'experience_value': actpoint } })
        return { 'code': 200, 'data': result }


class LSIbaseAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(LSIbaseAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.miner = flask.current_app.config['SVC_MIN']
        self.index = flask.current_app.config['SVC_INDEX']
        self.sim_names = self.miner.addition_names()

    def _post(self, project, doc, uses, filterdict, cur_page):
        indexdict = {}
        for key in filterdict:
            if filterdict[key]:
                indexdict[key] = self.index.get_indexkeys([key], filterdict[key], uses)
        count = 20
        datas, pages, totals = self.process(project, uses, doc, cur_page, count, indexdict)
        return { 'datas': datas, 'pages': pages, 'totals': totals }

    def process(self, project, uses, doc, cur_page, eve_count, filterdict=None):
        if not cur_page:
            cur_page = 1
        datas = []
        result = self.miner.probability(project, doc, uses=uses)
        if filterdict:
            filteset = self.index.get(filterdict, uses=uses)
            result = filter(lambda x: os.path.splitext(x[0])[0] in filteset, result)
        totals = len(result)
        if totals%eve_count != 0:
            pages = totals/eve_count + 1
        else:
            pages = totals/eve_count
        for name, score in result[(cur_page-1)*eve_count:cur_page*eve_count]:
            yaml_info = self.svc_mult_cv.getyaml(name)
            info = {
                'author': yaml_info['committer'],
                'time': utils.builtin.strftime(yaml_info['date']),
                'match': score
            }
            yaml_info['experience'] = self.experience_process(yaml_info['experience'])
            datas.append({ 'cv_id': name, 'yaml_info': yaml_info, 'info': info})
        return datas, pages, totals

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


class LSIbyJDidAPI(LSIbaseAPI):

    def __init__(self):
        super(LSIbyJDidAPI, self).__init__()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse.add_argument('project', type = str, location = 'json')
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('uses', type = list, location = 'json')
        self.reqparse.add_argument('page', type = int, location = 'json')
        self.reqparse.add_argument('filterdict', type=dict, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        id = args['id']
        project = args['project']
        jd_yaml = self.svc_mult_cv.getproject(project).jd_get(id)
        doc = jd_yaml['description']
        uses = [project] + args['uses'] if args['uses'] else [project]
        filterdict = args['filterdict'] if args['filterdict'] else {}
        cur_page = args['page']
        result = self._post(project, doc, uses, filterdict, cur_page)
        return { 'code': 200, 'data': result }


class LSIbydocAPI(LSIbaseAPI):

    def __init__(self):
        super(LSIbydocAPI, self).__init__()
        self.reqparse.add_argument('project', type = str, location = 'json')
        self.reqparse.add_argument('doc', location = 'json')
        self.reqparse.add_argument('uses', type = list, location = 'json')
        self.reqparse.add_argument('page', type = int, location = 'json')
        self.reqparse.add_argument('filterdict', type=dict, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        doc = args['doc']
        project = args['project']
        uses = [project] + args['uses'] if args['uses'] else [project]
        filterdict = args['filterdict'] if args['filterdict'] else {}
        cur_page = args['page']
        result = self._post(project, doc, uses, filterdict, cur_page)
        return { 'code': 200, 'data': result }


class SimilarAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(SimilarAPI, self).__init__()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.miner = flask.current_app.config['SVC_MIN']

    def get(self, id):
        doc = self.svc_mult_cv.getmd(id)
        datas = []
        for name, score in self.miner.probability(doc)[:7]:
            yaml_info = self.svc_mult_cv.getyaml(name)
            info = {
                'author': yaml_info['committer'],
                'time': utils.builtin.strftime(yaml_info['date']),
                'match': score
            }
            datas.append([name, yaml_info, info])
        return { 'result': datas }


class ValuablebaseAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(ValuablebaseAPI, self).__init__()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.miner = flask.current_app.config['SVC_MIN']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name_list', type = list, location = 'json')
        self.reqparse.add_argument('uses', type = list, location = 'json')

    def _get(self, doc, project):
        args = self.reqparse.parse_args()
        uses = [project] + args['uses'] if args['uses'] else [project]
        name_list = args['name_list']
        if len(name_list) == 0:
            result = core.mining.valuable.rate(self.miner, self.svc_mult_cv, doc, project, uses=uses)
        else:
            result = core.mining.valuable.rate(self.miner, self.svc_mult_cv, doc, project,
                                               uses=uses, name_list=name_list)
        response = dict()
        datas = []
        for index in result:
            item = dict()
            item['description'] = index[0]
            values = []
            for match_item in index[1]:
                name = match_item[0]
                yaml_data = self.svc_mult_cv.getyaml(name+'.yaml')
                yaml_data['match'] = match_item[1]
                values.append({ 'match': match_item[1], 'id': yaml_data['id'], 'name': yaml_data['name'] })
            item['value'] = values
            datas.append(item)
        response['result'] = datas
        response['max'] = 100
        return response


class ValuablebyJDidAPI(ValuablebaseAPI):

    def __init__(self):
        super(ValuablebyJDidAPI, self).__init__()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('project', type = str, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        id = args['id']
        project = args['project']
        jd_yaml = self.svc_mult_cv.getproject(project).jd_get(id)
        doc = jd_yaml['description']
        result = self._get(doc, project)
        return { 'code': 200, 'data': result }

class ValuablebydocAPI(ValuablebaseAPI):

    def __init__(self):
        super(ValuablebydocAPI, self).__init__()
        self.reqparse.add_argument('doc', type = str, location = 'json')
        self.reqparse.add_argument('project', type = str, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        doc = args['doc']
        project = args['project']
        result = self._get(doc, project)
        return { 'result': result }


class ValuableAPI(ValuablebaseAPI):

    def __init__(self):
        super(ValuableAPI, self).__init__()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('doc', location = 'json')
        self.reqparse.add_argument('project', type = str, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        project = args['project']
        if args['id']:
            jd_yaml = self.svc_mult_cv.getproject(project).jd_get(args['id'])
            doc = jd_yaml['description']
        elif args['doc']:
            doc = args['doc']
        result = self._get(doc, project)
        return { 'code': 200, 'data': result }

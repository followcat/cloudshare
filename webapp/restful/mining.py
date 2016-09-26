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


class PositionAPI(BaseAPI): 

    def get(self, text):
        args = self.reqparse.parse_args()
        if 'md_ids' in args and len(text) > 0:
            searches = args['md_ids']
        else:
            searches = self.svc_mult_cv.search(text)
        result = dict()
        for name in searches:
            md_data = self.svc_mult_cv.getmd(name)
            positions = core.mining.info.position(md_data, text)
            try:
                yaml_data = self.svc_mult_cv.getyaml(name)
            except IOError:
                continue
            for position in positions:
                if position not in result:
                    result[position] = []
                result[position].append({ name: yaml_data })
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


class LSIbaseAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(LSIbaseAPI, self).__init__()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.miner = flask.current_app.config['SVC_MIN']
        self.index = flask.current_app.config['SVC_INDEX']
        self.sim_names = self.miner.addition_names()
        self.basemodel = self.svc_mult_cv.default.name

    def _post(self, doc, uses, filterdict, cur_page):
        basemodel = self.basemodel
        count = 20
        datas, pages, totals = self.process(basemodel, uses, doc, cur_page, count, filterdict)
        return { 'datas': datas, 'pages': pages, 'totals': totals }

    def process(self, basemodel, uses, doc, cur_page, eve_count, filterdict=None):
        if not cur_page:
            cur_page = 1
        datas = []
        result = self.miner.probability(basemodel, doc, uses=uses)
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
            ex_company = yaml_info['experience']['company']
            ex_position = yaml_info['experience']['position']
            if len(ex_position) > 0:
                for position in ex_position:
                    for company in ex_company:
                        if position['at_company'] == company['id']:
                            position['company'] = company['name']
                            if 'business' in company:
                                position['business'] = company['business']
                yaml_info['experience'] = ex_position
            else: 
                yaml_info['experience'] = ex_company
            datas.append({ 'cv_id': name, 'yaml_info': yaml_info, 'info': info})
        return datas, pages, totals


class LSIbyJDidAPI(LSIbaseAPI):

    def __init__(self):
        super(LSIbyJDidAPI, self).__init__()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.uses = self.miner.default_names()
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('uses', type = list, location = 'json')
        self.reqparse.add_argument('page', type = int, location = 'json')
        self.reqparse.add_argument('filterdict', type=dict, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        id = args['id']
        jd_yaml = self.svc_mult_cv.default.jd_get(id+'.yaml')
        doc = jd_yaml['description']
        uses = self.uses + args['uses']
        filterdict = args['filterdict']
        cur_page = args['page']
        result = self._post(doc, uses, filterdict, cur_page)
        return { 'code': 200, 'data': result }


class LSIbydocAPI(LSIbaseAPI):

    def __init__(self):
        super(LSIbydocAPI, self).__init__()
        self.reqparse.add_argument('doc', type = str, location = 'json')

    def get(self):
        args = self.reqparse.parse_args()
        doc = args['doc']
        result = self._get(doc)
        return { 'result': result }


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
        self.uses = self.miner.default_names()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name_list', type = list, location = 'json')
        self.reqparse.add_argument('page', type = int, location = 'json')

    def _get(self, doc):
        args = self.reqparse.parse_args()
        uses = self.uses + args['uses']
        name_list = args['name_list']
        if len(name_list) == 0:
            result = core.mining.valuable.rate(self.miner, self.svc_mult_cv, doc, uses=uses)
        else:
            result = core.mining.valuable.rate(self.miner, self.svc_mult_cv, doc,
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
                values.append(yaml_data)
            item['value'] = values
            datas.append(item)
        response['data'] = datas
        response['max'] = 100
        return { 'result': response }


class ValuablebyJDidAPI(ValuablebaseAPI):

    def __init__(self):
        super(ValuablebyJDidAPI, self).__init__()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']

    def get(self, id):
        jd_yaml = self.svc_mult_cv.default.jd_get(id+'.yaml')
        doc = jd_yaml['description']
        result = self._get(doc)
        return { 'result': result }

class ValuablebydocAPI(ValuablebaseAPI):

    def __init__(self):
        super(ValuablebydocAPI, self).__init__()
        self.reqparse.add_argument('doc', type = str, location = 'json')

    def get(self):
        args = self.reqparse.parse_args()
        doc = args['doc']
        result = self._get(doc)
        return { 'result': result }

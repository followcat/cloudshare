import os.path

import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import utils.builtin
import core.mining.info
import core.mining.valuable


class BaseAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(BaseAPI, self).__init__()
        self.svc_cv = flask.current_app.config['SVC_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('md_ids', type = list, location = 'json')


class PositionAPI(BaseAPI): 

    def get(self, text):
        args = self.reqparse.parse_args()
        if 'md_ids' in args and len(text) > 0:
            searches = args['md_ids']
        else:
            searches = self.svc_cv.search(text)
        result = dict()
        for name in searches:
            md_data = self.svc_cv.getmd(name)
            positions = core.mining.info.position(md_data, text)
            try:
                yaml_data = self.svc_cv.getyaml(name)
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
            stream = self.svc_cv.getmd(id)
            result.append(core.mining.info.region(stream))
        return { 'result': result }


class CapacityAPI(BaseAPI):

    def get(self):
        args = self.reqparse.parse_args()
        result = []
        for id in args['md_ids']:
            stream = self.svc_cv.getmd(id)
            result.append({'md':id, 'capacity': core.mining.info.capacity(stream)})
        return { 'result': result }


class LSIbaseAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(LSIAPI, self).__init__()
        self.svc_cv = flask.current_app.config['SVC_CV']
        self.miner = flask.current_app.config['SVC_MIN']
        self.index = flask.current_app.config['SVC_INDEX']
        self.sim_names = miner.addition_names()
        self.uses = miner.default_names()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('uses', type = list, location = 'json')
        self.reqparse.add_argument('page', type = int, location = 'json')
        self.reqparse.add_argument('filterdict', type = dict, location = 'json')

    def _get(self, doc):
        args = self.reqparse.parse_args()
        uses = self.uses + args['uses']
        count = 20
        cur_page = args['page']
        filterdict = args['filterdict']
        datas, pages, totals = self.process(uses, doc, cur_page,
                                            count, filterdict)
        return { 'datas': datas, 'pages': pages, 'totals': totals }

    def process(self, uses, doc, cur_page, eve_count, filterdict=None):
        if not cur_page:
            cur_page = 1
        datas = []
        result = self.miner.probability(doc, uses=uses)
        if filterdict:
            filteset = self.index.get(filterdict, uses=uses)
            result = filter(lambda x: os.path.splitext(x[0])[0] in filteset, result)
        totals = len(result)
        if totals%eve_count != 0:
            pages = totals/eve_count + 1
        else:
            pages = totals/eve_count
        for name, score in result[(cur_page-1)*eve_count:cur_page*eve_count]:
            yaml_info = self.svc.getyaml(name)
            info = {
                'author': yaml_info['committer'],
                'time': utils.builtin.strftime(yaml_info['date']),
                'match': score
            }
            datas.append([name, yaml_info, info])
        return datas, pages, totals


class LSIbyJDidAPI(LSIbaseAPI):

    def __init__(self):
        super(LSIbyJDidAPI, self).__init__()
        self.svc_jd = flask.current_app.config['SVC_JD']

    def get(self, id):
        jd_yaml = self.svc_jd.get(id+'.yaml')
        doc = jd_yaml['description']
        result = self._get(doc)
        return { 'result': result }


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
        self.svc_cv = flask.current_app.config['SVC_CV']
        self.miner = flask.current_app.config['SVC_MIN']

    def get(self, id):
        doc = self.svc_cv.getmd(id)
        datas = []
        for name, score in self.miner.probability(doc)[:7]:
            yaml_info = self.svc_cv.getyaml(name)
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
        self.svc_cv = flask.current_app.config['SVC_CV']
        self.miner = flask.current_app.config['SVC_MIN']
        self.uses = miner.default_names()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name_list', type = list, location = 'json')
        self.reqparse.add_argument('page', type = int, location = 'json')

    def _get(self, doc):
        args = self.reqparse.parse_args()
        uses = self.uses + args['uses']
        name_list = args['name_list']
        if len(name_list) == 0:
            result = core.mining.valuable.rate(self.miner, self.svc_cv, doc, uses=uses)
        else:
            result = core.mining.valuable.rate(self.miner, self.svc_cv, doc,
                                               uses=uses, name_list=name_list)
        response = dict()
        datas = []
        for index in result:
            item = dict()
            item['description'] = index[0]
            values = []
            for match_item in index[1]:
                name = match_item[0]
                yaml_data = self.svc_cv.getyaml(name+'.yaml')
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
        self.svc_jd = flask.current_app.config['SVC_JD']

    def get(self, id):
        jd_yaml = self.svc_jd.get(id+'.yaml')
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

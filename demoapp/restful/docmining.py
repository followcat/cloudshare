# -*- coding: utf-8 -*-
import re
import flask
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import utils.builtin
import webapp.restful.mining


class DocMiningAPI(Resource):

    def __init__(self):
        super(DocMiningAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.miner = flask.current_app.config['SVC_MIN']
        self.reqparse.add_argument('doc', location = 'json')
        self.reqparse.add_argument('page', type = int, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        doc = args['doc']
        cur_page = args['page']
        model = 'medical'
        result = self.process(model, doc, cur_page)
        return { 'code': 200, 'data': result }

    def process(self, model, doc, cur_page, eve_count=20):
        if not cur_page:
            cur_page = 1
        datas = []
        result = self.miner.probability(model, doc, top=500)
        totals = len(result)
        if totals%eve_count != 0:
            pages = totals/eve_count + 1
        else:
            pages = totals/eve_count
        for name, score in result[(cur_page-1)*eve_count:cur_page*eve_count]:
            yaml_info = self.svc_mult_cv.getyaml(name, projectname=model)
            info = {
                'author': '', # yaml_info['committer'],
                'time': utils.builtin.strftime(yaml_info['date']),
                'match': score
            }
            yaml_info['origin'] = ''
            datas.append({ 'cv_id': name, 'yaml_info': yaml_info, 'info': info})
        return { 'datas': datas, 'pages': pages, 'totals': totals }


class DocValuableAPI(webapp.restful.mining.ValuableAPI):

    decorators = []

    def __init__(self):
        super(DocValuableAPI, self).__init__()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('doc', location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        projectname = 'medical'
        project = self.svc_mult_cv.getproject(projectname)
        doc = args['doc']
        result = self._get(doc, project)
        return { 'code': 200, 'data': result }

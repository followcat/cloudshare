# -*- coding: utf-8 -*-
import re
import math
import flask
import hashlib
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import utils.builtin
import core.mining.valuable
import demoapp.tools.caesarcipher
from baseapp.mining import load_mining


class DocMiningAPI(Resource):

    def __init__(self):
        super(DocMiningAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.miner = flask.current_app.config['SVC_MIN']
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.caesar_cipher_num = flask.current_app.config['CAESAR_CIPHER_NUM']
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
                'author': yaml_info['committer'],
                'time': utils.builtin.strftime(yaml_info['date']),
                'match': score
            }
            yaml_info['id'] = demoapp.tools.caesarcipher.encrypt(
                                self.caesar_cipher_num, yaml_info['id'])
            ename = demoapp.tools.caesarcipher.encrypt(
                                self.caesar_cipher_num, name)
            datas.append({ 'cv_id': ename, 'yaml_info': yaml_info, 'info': info})
        return { 'datas': datas, 'pages': pages, 'totals': totals }


class DocValuableAPI(Resource):

    decorators = []

    def __init__(self):
        super(DocValuableAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.miner = flask.current_app.config['SVC_MIN']
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.caesar_cipher_num = flask.current_app.config['CAESAR_CIPHER_NUM']
        self.reqparse.add_argument('doc', location = 'json')
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('name_list', type = list, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        doc = args['doc']
        result = self._get(doc, 'medical')
        return { 'code': 200, 'data': result }

    def _get(self, doc, projectname):
        args = self.reqparse.parse_args()
        uses = [projectname]
        name_list = [demoapp.tools.caesarcipher.decrypt(self.caesar_cipher_num, name)
                     for name in args['name_list']]
        result = core.mining.valuable.rate(self.miner, self.svc_mult_cv,
                                           doc, projectname, uses=uses, name_list=name_list)
        response = dict()
        datas = []
        for index in result:
            item = dict()
            item['description'] = index[0]
            values = []
            for match_item in index[1]:
                name = match_item[0]
                yaml_data = self.svc_mult_cv.getyaml(name+'.yaml', projectname=projectname)
                yaml_data['match'] = match_item[1]
                values.append({ 'match': match_item[1],
                                'id': demoapp.tools.caesarcipher.encrypt(
                                      self.caesar_cipher_num, yaml_data['id']),
                                'name': yaml_data['name'] })
            item['value'] = values
            datas.append(item)
        response['result'] = datas
        response['max'] = 100
        return response


class DocCVValuableAPI(DocValuableAPI):

    tmpminer = load_mining('tmplsimodel', 'tmpcutwords')[1]

    def __init__(self):
        super(DocCVValuableAPI, self).__init__()
        self.reqparse.add_argument('cv', location = 'json')

    def temprate(self, cv, doc, projectname, top=200):
        rank = 0
        stars = 0
        name_list = []
        lsisim = self.tmpminer.getsims(projectname, [projectname])[0]
        tmpSha1 = hashlib.sha1()
        tmpSha1.update(cv.encode('utf-8'))
        tmpSha1_Digest = tmpSha1.hexdigest()
        if not tmpSha1_Digest in lsisim.names:
            lsisim.add(tmpSha1_Digest, cv)
            lsisim.set_index()
        result = core.mining.valuable.rate(self.tmpminer, self.svc_mult_cv,
                                           doc, projectname, uses=[projectname],
                                           name_list=[tmpSha1_Digest],
                                           education_req=False)
        ranklist = self.tmpminer.probability(projectname, doc, top=top)
        rate = self.tmpminer.probability_by_id(projectname, doc,
                                                tmpSha1_Digest, uses=[projectname])
        try:
            rank = int(ranklist.index(rate)/len(ranklist))+1
            stars = math.ceil(float(rate[1])/0.2)
        except ValueError:
            pass
        return result, rate[1], rank, stars

    def post(self):
        args = self.reqparse.parse_args()
        cv = args['cv']
        doc = args['doc']
        projectname = 'medical'
        uses = [projectname]
        response = dict()
        datas = []
        result, rate, rank, stars = self.temprate(cv, doc, projectname)
        for index in result:
            item = dict()
            item['description'] = index[0]
            values = []
            for match_item in index[1]:
                name = match_item[0]
                values.append({ 'match': match_item[1],
                                'id': name,
                                'name': 'My CV' })
            item['value'] = values
            datas.append(item)
        response['result'] = datas
        response['max'] = 100
        return { 'code': 200, 'data': response,
                 'rate': rate, 'rank': rank, 'stars': stars }


class CurrivulumvitaeAPI(Resource):

    decorators = []

    def __init__(self):
        super(CurrivulumvitaeAPI, self).__init__()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.caesar_cipher_num = flask.current_app.config['CAESAR_CIPHER_NUM']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = str, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        id = args['id']
        realid = demoapp.tools.caesarcipher.decrypt(self.caesar_cipher_num, id)
        yaml = self.svc_mult_cv.getyaml(realid, projectname='medical')
        return { 'code': 200, 'data': { 'yaml_info': yaml } }

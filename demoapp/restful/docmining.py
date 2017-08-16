# -*- coding: utf-8 -*-
import re
import math
import flask
import hashlib
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import utils.builtin
import core.outputstorage
import core.mining.valuable
import utils.timeout.process
import demoapp.tools.caesarcipher
import extractor.information_explorer


class UploadCVAPI(Resource):

    projectname = 'temporary'

    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.svc_min = flask.current_app.config['SVC_MIN']
        self.svc_docpro = flask.current_app.config['SVC_DOCPROCESSOR']
        super(UploadCVAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('files', type = str, location = 'json')

    def post(self):
        results = []
        network_file = flask.request.files['files']
        project = self.svc_mult_cv.getproject(self.projectname)
        id = None
        code = 401
        added = False
        result = False
        filename = network_file.filename
        filepro = self.svc_docpro(network_file, filename.encode('utf-8'),
                                  flask.current_app.config['UPLOAD_TEMP'])
        result = filepro.result
        if result is True:
            try:
                yamlinfo = utils.timeout.process.process_timeout_call(
                                     extractor.information_explorer.catch_cvinfo, 2000,
                                     kwargs={'stream': filepro.markdown_stream.decode('utf8'),
                                             'filename': filename})
            except utils.timeout.process.KilledExecTimeout as e:
                result = False
            if result is not False:
                id = yamlinfo['id']
                if project.curriculumvitae.exists(id):
                    added = True
                if not added:
                    filepro.renameconvert(id)
                    dataobj = core.basedata.DataObject(metadata=yamlinfo,
                                                       data=filepro.markdown_stream,)
                    yamlinfo = dataobj.metadata
                    if not yamlinfo['name']:
                        yamlinfo['name'] = utils.chsname.name_from_filename(filename)
                    repo_cv_result = self.svc_mult_cv.repodb.add(dataobj, 'temporary',
                                                                 unique=True,
                                                                 contacts=False)
                    project_cv_result = project.cv_add(dataobj, 'temporary')
                    result = project_cv_result and repo_cv_result
                code = 200
        results.append({ 'id': id,
                         'added': added,
                         'result': result,
                         'filename': filename })
        return { 'code': code, 'data': results }

class DocMiningAPI(Resource):

    projectname = 'temporary'

    def __init__(self):
        super(DocMiningAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.miner = flask.current_app.config['SVC_MIN']
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.caesar_cipher_num = flask.current_app.config['CAESAR_CIPHER_NUM']
        self.reqparse.add_argument('doc', location = 'json')
        self.reqparse.add_argument('page', type = int, location = 'json')
        self.reqparse.add_argument('CVlist', type = list, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        doc = args['doc']
        cur_page = args['page']
        cvlist = args['CVlist'] if args['CVlist'] else []
        model = self.projectname
        result = self.process(model, doc, cvlist, cur_page)
        return { 'code': 200, 'data': result }

    def process(self, model, doc, cvlist, cur_page, eve_count=20):
        if not cur_page:
            cur_page = 1
        datas = []
        result = []
        project = self.svc_mult_cv.getproject(self.projectname)
        if cvlist:
            names = []
            documents = []
            sim = self.miner.sim[self.projectname][self.projectname]
            for cv in cvlist:
                mdid = core.outputstorage.ConvertName(cv['id']).md
                if mdid not in sim.names:
                    names.append(mdid)
                    documents.append(project.cv_getmd(cv['id']))
            sim.add_documents(names, documents)
            for cv in cvlist:
                mdid = core.outputstorage.ConvertName(cv['id']).md
                result.append(self.miner.probability_by_id(model, doc, mdid,
                                                           uses=[project.name]))
            result = sorted(result, key=lambda x:float(x[1]), reverse=True)
        else:
            result = self.miner.probability(model, doc,
                                            uses=project.getclassify(),
                                            top=0.05, minimum=1000)
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
        self.svc_customers = flask.current_app.config['SVC_CUSTOMERS']
        self.caesar_cipher_num = flask.current_app.config['CAESAR_CIPHER_NUM']
        self.reqparse.add_argument('doc', location = 'json')
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('name_list', type = list, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        doc = args['doc']
        result = self._get(doc, 'temporary')
        return { 'code': 200, 'data': result }

    def _get(self, doc, projectname):
        args = self.reqparse.parse_args()
        customer = self.svc_customers.get(self.svc_customers.default_customer_name)
        project = customer.getproject(projectname)
        name_list = [demoapp.tools.caesarcipher.decrypt(self.caesar_cipher_num, name)
                     for name in args['name_list']]
        result = core.mining.valuable.rate(self.miner, project,
                                           doc, uses=[projectname], name_list=name_list)
        response = dict()
        datas = []
        for index in result:
            item = dict()
            item['description'] = index[0]
            values = []
            for match_item in index[1]:
                name = match_item[0]
                yaml_data = project.getyaml(name+'.yaml', projectname=projectname)
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

    def __init__(self):
        super(DocCVValuableAPI, self).__init__()
        self.reqparse.add_argument('cv', location = 'json')

    def temprate(self, cv, doc, projectname, top=0.1):
        rank = 0
        stars = 0
        name_list = []
        lsisim = self.miner.getsims(projectname, [projectname])[0]
        tmpSha1 = hashlib.sha1()
        tmpSha1.update(cv.encode('utf-8'))
        tmpSha1_Digest = tmpSha1.hexdigest()
        if not tmpSha1_Digest in lsisim.names:
            lsisim.add(tmpSha1_Digest, cv)
            lsisim.set_index()
        customer = self.svc_customers.get(self.svc_customers.default_customer_name)
        project = customer.getproject(projectname)
        result = core.mining.valuable.rate(self.miner, project,
                                           doc, uses=[projectname],
                                           name_list=[tmpSha1_Digest],
                                           education_req=False)
        ranklist = self.miner.probability(projectname, doc, top=0.05, minimum=1000)
        rate = self.miner.probability_by_id(projectname, doc,
                                                tmpSha1_Digest, uses=[projectname])
        try:
            rank = int(float(ranklist.index(rate))/len(ranklist)*100)+1
            stars = math.ceil(float(rate[1])/0.2)
        except ValueError:
            pass
        return result, rate[1], rank, stars

    def post(self):
        args = self.reqparse.parse_args()
        cv = args['cv']
        doc = args['doc']
        projectname = 'temporary'
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
                                'name': u'我的简历' })
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
        self.svc_customers = flask.current_app.config['SVC_CUSTOMERS']
        self.caesar_cipher_num = flask.current_app.config['CAESAR_CIPHER_NUM']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = str, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        customer = self.svc_customers.get(self.svc_customers.default_customer_name)
        project = customer.getproject()
        id = args['id']
        realid = demoapp.tools.caesarcipher.decrypt(self.caesar_cipher_num, id)
        yaml = project.cv_getyaml(realid)
        return { 'code': 200, 'data': { 'yaml_info': yaml } }

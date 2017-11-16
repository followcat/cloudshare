import flask
import flask.ext.login
from flask import request
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import core.mining.correlation


class MatchbaseAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.miner = flask.current_app.config['SVC_MIN']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('doc', type = unicode, location = 'json')
        self.reqparse.add_argument('page', type = int, location = 'json')
        self.reqparse.add_argument('numbers', type = int, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        self.doc = args['doc']
        self.page = args['page']
        self.numbers = args['numbers']


class JDmathAPI(MatchbaseAPI):

    def __init__(self):
        super(JDmathAPI, self).__init__()
        self.jd_repo = flask.current_app.config['SVC_JD_REPO']
        self.co_repo = flask.current_app.config['SVC_CO_REPO']
        self.peo_mult = flask.current_app.config['SVC_MULT_PEO']
        self.svc_members = flask.current_app.config['SVC_MEMBERS']

    def post(self):
        super(JDmathAPI, self).post()
        total, result = core.mining.correlation.jobdescription_correlation(self.miner,
                    [self.jd_repo], doc=self.doc, page=self.page, numbers=self.numbers)
        for each in result:
            jdinfo = each['data']
            jdinfo['companyID'] = jdinfo['company']
            jdinfo['company'] = self.co_repo.getyaml(jdinfo['company'])['name']
        return { 'code': 200, 'data': result, 'lenght': total }

    def get(self):
        args = request.args
        self.page = int(args['page'])
        self.numbers = int(args['numbers'])
        user = flask.ext.login.current_user
        total = 0
        result = list()
        code = 204
        if user.peopleID:
            code = 200
            doc = self.peo_mult.getmd(user.peopleID).next()
            total, result = core.mining.correlation.jobdescription_correlation(self.miner,
                        [self.jd_repo], doc=doc, page=self.page, numbers=self.numbers)
            for each in result:
                jdinfo = each['data']
                jdinfo['companyID'] = jdinfo['company']
                jdinfo['company'] = self.co_repo.getyaml(jdinfo['company'])['name']
        return { 'code': code, 'data': result, 'lenght': total }


class COmathAPI(MatchbaseAPI):

    def __init__(self):
        super(COmathAPI, self).__init__()
        self.cv_repo = flask.current_app.config['SVC_CV_REPO']

    def post(self):
        super(COmathAPI, self).post()
        total, result = core.mining.correlation.company_correlation(self.miner,
                    [self.cv_repo], doc=self.doc, page=self.page, numbers=self.numbers)
        return { 'code': 200, 'data': result, 'lenght': total }


class POSmathAPI(MatchbaseAPI):

    def __init__(self):
        super(POSmathAPI, self).__init__()
        self.cv_repo = flask.current_app.config['SVC_CV_REPO']

    def post(self):
        super(POSmathAPI, self).post()
        total, result = core.mining.correlation.position_correlation(self.miner,
                    [self.cv_repo], doc=self.doc, page=self.page, numbers=self.numbers)
        return { 'code': 200, 'data': result, 'lenght': total }


class PRJmathAPI(MatchbaseAPI):

    def __init__(self):
        super(PRJmathAPI, self).__init__()
        self.cv_repo = flask.current_app.config['SVC_CV_REPO']

    def post(self):
        super(PRJmathAPI, self).post()
        total, result = core.mining.correlation.project_correlation(self.miner,
                    [self.cv_repo], doc=self.doc, page=self.page, numbers=self.numbers)
        return { 'code': 200, 'data': result, 'lenght': total }


class CompanyProjectAPI(MatchbaseAPI):

    def __init__(self):
        super(CompanyProjectAPI, self).__init__()
        self.cv_repo = flask.current_app.config['SVC_CV_REPO']
        self.svc_index = flask.current_app.config['SVC_INDEX']
        self.es_config = flask.current_app.config['ES_CONFIG']

    def post(self):
        super(CompanyProjectAPI, self).post()
        result = list()
        index = [self.svc_index.config['CV_MEM'], self.svc_index.config['CV_STO']]
        total, search = self.svc_index.search(index=index,
                                       filterdict={'experience.project.company': self.doc},
                                       start=(self.page-1)*self.numbers,
                                       size=self.numbers, source=True)
        for each in search:
            for project in each['_source']['experience']['project']:
                if 'company' in project and project['company'] == self.doc:
                    result.append( {'id': each['_source']['id'],
                                    'value': 1,
                                    'data': project} )
        return { 'code': 200, 'data': result }

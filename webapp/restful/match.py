import flask
import flask.ext.login
from flask import request
from flask.ext.restful import reqparse
from flask.ext.restful import Resource


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


class JDmatchAPI(MatchbaseAPI):

    def __init__(self):
        super(JDmatchAPI, self).__init__()
        self.jd_repo = flask.current_app.config['SVC_JD_REPO']
        self.co_repo = flask.current_app.config['SVC_BD_REPO']

    def post(self):
        super(JDmatchAPI, self).post()
        total, result = self.miner.jobdescription_correlation(
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
        member = user.getmember()
        total = 0
        result = list()
        code = 204
        if user.peopleID:
            code = 200
            doc = member.peo_getmd(user.peopleID).next()
            total, result = self.miner.jobdescription_correlation(
                        [self.jd_repo], doc=doc, page=self.page, numbers=self.numbers)
            for each in result:
                jdinfo = each['data']
                jdinfo['companyID'] = jdinfo['company']
                jdinfo['company'] = self.co_repo.getyaml(jdinfo['company'])['name']
        return { 'code': code, 'data': result, 'lenght': total }


class COmatchAPI(MatchbaseAPI):

    def __init__(self):
        super(COmatchAPI, self).__init__()
        self.cv_repo = flask.current_app.config['SVC_CV_REPO']

    def post(self):
        super(COmatchAPI, self).post()
        total, result = self.miner.company_correlation(
                    [self.cv_repo], doc=self.doc, page=self.page, numbers=self.numbers)
        return { 'code': 200, 'data': result, 'lenght': total }


class POSmatchAPI(MatchbaseAPI):

    def __init__(self):
        super(POSmatchAPI, self).__init__()
        self.cv_repo = flask.current_app.config['SVC_CV_REPO']

    def post(self):
        super(POSmatchAPI, self).post()
        total, result = self.miner.position_correlation(
                    [self.cv_repo], doc=self.doc, page=self.page, numbers=self.numbers)
        return { 'code': 200, 'data': result, 'lenght': total }


class PRJmatchAPI(MatchbaseAPI):

    def __init__(self):
        super(PRJmatchAPI, self).__init__()
        self.cv_repo = flask.current_app.config['SVC_CV_REPO']

    def post(self):
        super(PRJmatchAPI, self).post()
        total, result = self.miner.project_correlation(
                    [self.cv_repo], doc=self.doc, page=self.page, numbers=self.numbers)
        return { 'code': 200, 'data': result, 'lenght': total }


class CompanyProjectAPI(MatchbaseAPI):

    def __init__(self):
        super(CompanyProjectAPI, self).__init__()
        self.cv_repo = flask.current_app.config['SVC_CV_REPO']

    def post(self):
        super(CompanyProjectAPI, self).post()
        user = flask.ext.login.current_user
        member = user.getmember()
        result = list()
        total, search = member.cv_search(filterdict={'experience.project.company': self.doc},
                                         start=(self.page-1)*self.numbers,
                                         size=self.numbers, source=True)
        for each in search:
            for project in each['_source']['experience']['project']:
                if 'company' in project and project['company'] == self.doc:
                    result.append( {'id': each['_source']['id'],
                                    'value': 1,
                                    'data': project} )
        return { 'code': 200, 'data': result }

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
        user = flask.ext.login.current_user
        member = user.getmember()
        total, result = member.jd_correlation(doc=self.doc, basemodel='jdmatch',
                    uses=[self.jd_repo.name], page=self.page, numbers=self.numbers)
        res = list()
        for id, value in result:
            res.append( {'id': id, 'value': value, 'data': member.jd_getyaml(id)} )
        return { 'code': 200, 'data': res, 'lenght': total }

    def get(self):
        args = request.args
        self.page = int(args['page'])
        self.numbers = int(args['numbers'])
        user = flask.ext.login.current_user
        member = user.getmember()
        total = 0
        res = list()
        code = 204
        if user.peopleID:
            code = 200
            doc = member.peo_getmd(user.peopleID).next()
            total, result = member.jd_correlation(doc=doc, basemodel='jdmatch',
                        uses=[self.jd_repo.name], page=self.page, numbers=self.numbers)
            for id, value in result:
                res.append( {'id': id, 'value': value, 'data': member.jd_getyaml(id)} )
        return { 'code': code, 'data': res, 'lenght': total }


class COmatchAPI(MatchbaseAPI):

    def __init__(self):
        super(COmatchAPI, self).__init__()
        self.cv_repo = flask.current_app.config['SVC_CV_REPO']

    def post(self):
        super(COmatchAPI, self).post()
        user = flask.ext.login.current_user
        member = user.getmember()
        total, result = member.jd_correlation(doc=self.doc, basemodel='comatch',
                    uses=[self.cv_repo.name], page=self.page, numbers=self.numbers)
        res = list()
        for longname, value in result:
            id, name = longname.split('.', 1)
            info = member.jd_getyaml(id)
            for company in info['experience']['company']:
                if company['name'] == name:
                    res.append({ 'id': id, 'value': value, 'data': company })
                    break
            else:
                raise Exception('Not found description')
        return { 'code': 200, 'data': res, 'lenght': total }


class POSmatchAPI(MatchbaseAPI):

    def __init__(self):
        super(POSmatchAPI, self).__init__()
        self.cv_repo = flask.current_app.config['SVC_CV_REPO']

    def post(self):
        super(POSmatchAPI, self).post()
        user = flask.ext.login.current_user
        member = user.getmember()
        total, result = member.jd_correlation(doc=self.doc, basemodel='posmatch',
                    uses=[self.cv_repo.name], page=self.page, numbers=self.numbers)
        res = list()
        for longname, value in result:
            try:
                id, longname = longname.split('.', 1)
                company, name = longname.rsplit('.', 1)
            except ValueError:
                continue
            info = member.jd_getyaml(id)
            for position in info['experience']['position']:
                at_company = position['at_company']
                pos_company = info['experience']['company'][at_company]['name']
                if pos_company == company and position['name'] == name:
                    res.append({ 'id': id, 'value': value, 'data': position })
                    break
            else:
                continue
        return { 'code': 200, 'data': res, 'lenght': total }


class PRJmatchAPI(MatchbaseAPI):

    def __init__(self):
        super(PRJmatchAPI, self).__init__()
        self.cv_repo = flask.current_app.config['SVC_CV_REPO']

    def post(self):
        super(PRJmatchAPI, self).post()
        user = flask.ext.login.current_user
        member = user.getmember()
        total, result = member.jd_correlation(doc=self.doc, basemodel='prjmatch',
                    uses=[self.cv_repo.name], page=self.page, numbers=self.numbers)
        res = list()
        for longname, value in result:
            try:
                id, longname = longname.split('.', 1)
                company, name = longname.rsplit('.', 1)
            except ValueError:
                continue
            info = member.jd_getyaml(id)
            for project in info['experience']['project']:
                if project['name'] == name:
                    res.append({ 'id': id, 'value': value, 'data': project })
                    break
            else:
                raise Exception('Not found description')
        return { 'code': 200, 'data': res, 'lenght': total }

import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import utils.builtin
import core.basedata
import extractor.information_explorer


class CompanyAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('coname', location = 'json')
        self.reqparse.add_argument('introduction', location = 'json')
        self.reqparse.add_argument('project', location = 'json')
        super(CompanyAPI, self).__init__()

    def get(self, name):
        project = args['project']
        result = self.svc_mult_cv.getproject(project).company_get(name)
        return { 'result': result }

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        project = args['project']
        coname = args['coname']
        if args['introduction'] is None:
            args['introduction'] = str()
        metadata = extractor.information_explorer.catch_coinfo(name=coname, stream=args)
        coobj = core.basedata.DataObject(metadata, data=args['introduction'].encode('utf-8'))
        result = self.svc_mult_cv.getproject(project).company_add(coobj, user.id)
        return { 'code': 200, 'data': result, 'message': 'Create new company successed.' }

class CompanyAllAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        super(CompanyAllAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('begin', location = 'json')
        self.reqparse.add_argument('length', location = 'json')

    def get(self):
        project = self.svc_mult_cv.getproject(projectname)
        return list(project.company.datas())

    def post(self):
        args = self.reqparse.parse_args()
        projectname = args['project']
        begin = args['begin']
        length = args['length']
        project = self.svc_mult_cv.getproject(projectname)
        data = []
        ids = sorted(list(project.company.ids))
        for id in ids[int(begin):int(begin+length)]:
            data.append(project.company.getyaml(id))
        return { 'code': 200, 'data': data }

#owner
class CustomerListAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        super(CustomerListAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        project = args['project']
        result = self.svc_mult_cv.getproject(project).company_customers()
        data = []
        for coname in result:
            co = self.svc_mult_cv.getproject(project).company_get(coname)
            data.append(co)
        return { 'code': 200, 'data': data }

#create, delete
class CustomerAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        super(CustomerAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('id', location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        projectname = args['project']
        project = self.svc_mult_cv.getproject(projectname)
        result = project.company.addcustomer(id, user.id)
        return { 'code': 200, 'data': result }

    def delete(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        projectname = args['project']
        project = self.svc_mult_cv.getproject(projectname)
        result = project.company.deletecustomer(id, user.id)
        return { 'code': 200, 'data': result }

#update info
class CompanyInfoUpdateAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        super(CompanyInfoUpdateAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('key', type = str, location = 'json')
        self.reqparse.add_argument('date', type = str, location = 'json')
        self.reqparse.add_argument('value', type = str, location = 'json')
        self.reqparse.add_argument('project', type = str, location = 'json')

    def put(self, id):
        args = self.reqparse.parse_args()
        user = flask.ext.login.current_user
        key = args['key']
        value = args['value']
        projectname = args['project']
        project = self.svc_mult_cv.getproject(projectname)
        data = project.company.updateinfo(id, key, value, user)
        if data is not None:
            response = { 'code': 200, 'data': data, 'message': 'Delete information success.' }
        else:
            response = { 'code': 400, 'message': 'Delete information error.'}

    def delete(self, id):
        args = self.reqparse.parse_args()
        user = flask.ext.login.current_user
        key = args['key']
        date = args['date']
        value = args['value']
        projectname = args['project']
        project = self.svc_mult_cv.getproject(projectname)
        data = project.company.deleteinfo(id, key, value, user, date)
        if data is not None:
            response = { 'code': 200, 'data': data, 'message': 'Delete information success.' }
        else:
            response = { 'code': 400, 'message': 'Delete information error.'}


class SearchCObyTextAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(SearchCObyTextAPI, self).__init__()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', type = str, location = 'json')
        self.reqparse.add_argument('search_text', location = 'json')
        self.reqparse.add_argument('page', type = int, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        cur_page = args['page']
        text = args['search_text']
        projectname = args['project']
        project = self.svc_mult_cv.getproject(projectname)
        results = project.company.search(text)
        yaml_results = project.company.search_yaml(text)
        results.update(yaml_results)
        count = 20
        datas, pages = self.paginate(project.company, list(results), cur_page, count)
        return {
            'code': 200,
            'data': {
                'keyword': text,
                'datas': datas,
                'pages': pages,
                'totals': len(results),
            }
        }

    def paginate(self, svc_co, results, cur_page, eve_count):
        if not cur_page:
            cur_page = 1
        sum = len(results)
        if sum%eve_count != 0:
            pages = sum/eve_count + 1
        else:
            pages = sum/eve_count
        datas = []
        for id in results[(cur_page-1)*eve_count:cur_page*eve_count]:
            datas.append({ 'cv_id': id, 'yaml_info': svc_co.getyaml(id) })
        return datas, pages

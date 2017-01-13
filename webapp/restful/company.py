import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import utils.builtin
import core.basedata
import extractor.information_explorer
import json

class CompanyAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('name', location = 'json')
        self.reqparse.add_argument('product', location = 'json')
        self.reqparse.add_argument('introduction', location = 'json')
        self.reqparse.add_argument('conumber', location = 'json')
        self.reqparse.add_argument('address', location = 'json')
        self.reqparse.add_argument('email', location = 'json')
        self.reqparse.add_argument('website', location = 'json')
        self.reqparse.add_argument('district', location = 'json')
        super(CompanyAPI, self).__init__()

    def get(self, name):
        project = args['project']
        result = self.svc_mult_cv.getproject(project).company_get(name)
        return { 'result': result }

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        project = args['project']
        coname = args['name']
        if args['introduction'] is None:
            args['introduction'] = str()
        metadata = extractor.information_explorer.catch_coinfo(name=coname, stream=args)
        coobj = core.basedata.DataObject(metadata, data=args['introduction'].encode('utf-8'))
        result = self.svc_mult_cv.getproject(project).company_add(coobj, user.id)
        if result:
            response = { 'code': 200, 'data': result, 'message': 'Create new company successed.' }
        else:
            response = { 'code': 400, 'data': result, 'message': 'Create new company failed.' }
        return response

class CompanyAllAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        super(CompanyAllAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('current_page', type = int, location = 'json')
        self.reqparse.add_argument('page_size', type = int, location = 'json')

    def get(self):
        project = self.svc_mult_cv.getproject(projectname)
        return list(project.company.datas())

    def post(self):
        args = self.reqparse.parse_args()
        projectname = args['project']
        current_page = args['current_page']
        page_size = args['page_size']
        project = self.svc_mult_cv.getproject(projectname)
        data = []
        ids = sorted(list(project.company.ids))
        for id in ids[(current_page-1)*page_size : current_page*page_size]:
            data.append(project.company.getyaml(id))
        return { 'code': 200, 'data': data, 'total': len(ids) }

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
        if result:
            response = { 'code': 200, 'message': 'Add customer success.' }
        else:
            response = { 'code': 400, 'message': 'Add customer fail.' }
        return response

    def delete(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        projectname = args['project']
        project = self.svc_mult_cv.getproject(projectname)
        result = project.company.deletecustomer(id, user.id)
        if result:
            response = { 'code': 200, 'message': 'Delete customer success.' }
        else:
            response = { 'code': 400, 'message': 'Delete customer fail.' }
        return response

#update info
class CompanyInfoUpdateAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        super(CompanyInfoUpdateAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', location = 'json')
        self.reqparse.add_argument('update_info', type= list, location = 'json')
        self.reqparse.add_argument('date', location = 'json')
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('key', location = 'json')
        self.reqparse.add_argument('value', location = 'json')

    def put(self):
        args = self.reqparse.parse_args()
        user = flask.ext.login.current_user
        id = args['id']
        update_info = args['update_info']
        projectname = args['project']
        project = self.svc_mult_cv.getproject(projectname)
        data = dict()
        for item in update_info:
            try:
                result = project.company.updateinfo(id, item['key'], item['value'], user.id)
            except AssertionError:
                continue
            data.update(result)
        if len(data) != 0:
            response = { 'code': 200, 'data': data, 'message': 'Update information success.' }
        else:
            response = { 'code': 400, 'message': 'Update information error.' }
        return response

    def delete(self):
        args = self.reqparse.parse_args()
        user = flask.ext.login.current_user
        id = args['id']
        key = args['key']
        date = args['date']
        value = args['value']
        projectname = args['project']
        project = self.svc_mult_cv.getproject(projectname)
        data = project.company.deleteinfo(id, key, value, user.id, date)
        if data is not None:
            response = { 'code': 200, 'data': data, 'message': 'Delete information success.' }
        else:
            response = { 'code': 400, 'message': 'Delete information error.'}
        return response


class SearchCObyTextAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(SearchCObyTextAPI, self).__init__()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', type = str, location = 'json')
        self.reqparse.add_argument('search_text', location = 'json')
        self.reqparse.add_argument('current_page', type = int, location = 'json')
        self.reqparse.add_argument('page_size', type = int, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        cur_page = args['current_page']
        page_size = args['page_size']
        text = args['search_text']
        projectname = args['project']
        project = self.svc_mult_cv.getproject(projectname)
        results = project.company.search(text)
        yaml_results = project.company.search_yaml(text)
        results.update(yaml_results)
        datas, pages, total = self.paginate(project.company, list(results), cur_page, page_size)
        return {
            'code': 200,
            'data': datas,
            'keyword': text,
            'pages': pages,
            'total': total
        }

    def paginate(self, svc_co, results, cur_page, eve_count):
        if not cur_page:
            cur_page = 1
        total = len(results)
        if total%eve_count != 0:
            pages = total/eve_count + 1
        else:
            pages = total/eve_count
        datas = []
        for id in results[(cur_page-1)*eve_count:cur_page*eve_count]:
            datas.append(svc_co.getyaml(id))
        return datas, pages, total


class CompanyUploadExcelAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(CompanyUploadExcelAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse.add_argument('files', type = str, location = 'json')
        self.reqparse.add_argument('project', type = str, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        user = flask.ext.login.current_user
        project_name = args['project']
        network_file = flask.request.files['files']
        project = self.svc_mult_cv.getproject(project_name)
        compare_result = project.company_compare_excel(network_file.read(), committer=user.id)
        infos = dict()
        for item in compare_result:
            coid = item[1]
            if coid not in infos:
                if project.corepo.exists(coid):
                    infos[coid] = project.company_get(coid)
                else:
                    infos[coid] = item[2][0]
        return {
            'code': 200,
            'data': compare_result,
            'info': infos
        }


class CompanyConfirmExcelAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(CompanyConfirmExcelAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse.add_argument('data', location = 'json')
        self.reqparse.add_argument('project', type = str, location = 'json')

    def post(self):
        datas = args['data']
        project_name = args['project']
        user = flask.ext.login.current_user
        project = self.svc_mult_cv.getproject(project_name)
        results = project.company_add_excel(datas, user.id)
        return {
            'code': 200,
            'data': results
        }

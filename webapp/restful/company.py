import json

import core.basedata
import extractor.information_explorer
import flask
import flask.ext.login
import utils.builtin
from flask.ext.restful import Resource, reqparse


class CompanyAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('name', location = 'json')
        self.reqparse.add_argument('introduction', location = 'json')
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
        ids = project.company.sorted_ids('modifytime')
        for id in ids[(current_page-1)*page_size : current_page*page_size]:
            data.append(project.company.getyaml(id))
        return { 'code': 200, 'data': data, 'total': len(ids) }


class AddedCompanyListAPI(Resource):
    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        super(AddedCompanyListAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('text', location = 'json')
    
    def post(self):
        args = self.reqparse.parse_args()
        projectname = args['project']
        text = args['text']
        project = self.svc_mult_cv.getproject(projectname)
        customer_ids = project.company_customers()
        company_ids = project.company.search('name: '+text)
        data = []
        for company_id in company_ids:
            if company_id in customer_ids:
                continue
            yaml = project.company.getyaml(company_id)
            data.append({
                'id': yaml['id'],
                'company_name': yaml['name']
            })
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
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        user = flask.ext.login.current_user
        id = args['id']
        update_info = args['update_info']
        projectname = args['project']
        project = self.svc_mult_cv.getproject(projectname)
        origin_info = project.company_get(id)
        for key in update_info:
            value = update_info[key]
            text = value['text']
            vtype = value['type']
            if vtype == 'PUT':
                origin_info[key] = value
            elif vtype == 'CREATE':
                data = self._listframe(value, user)
                origin_info[key].insert(0, data)
            elif vtype == 'DELETE':
                data = self._listframe(text, committer, value['date'])
                origin_info[key].remove(data)
        result = project.company_update_info(id, origin_info, user.id)
        if result:
            response = { 'code': 200, 'message': 'Update information success.' }
        else:
            response = { 'code': 400, 'message': 'Update information error.' }
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
        sorted_results = project.company.sorted_ids('modifytime', ids=results)
        datas, pages, total = self.paginate(project.company, sorted_results, cur_page, page_size)
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


class SearchCObyKeyAPI(Resource):

    def __init__(self):
        super(SearchCObyKeyAPI, self).__init__()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('current_page', type = int, location = 'json')
        self.reqparse.add_argument('page_size', type = int, location = 'json')
        self.reqparse.add_argument('search_key', location = 'json')
        self.reqparse.add_argument('search_text', location = 'json')
        self.reqparse.add_argument('project', type = str, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        cur_page = args['current_page']
        page_size = args['page_size']
        key = args['search_key']
        text = args['search_text']
        projectname = args['project']
        project = self.svc_mult_cv.getproject(projectname)
        results = project.company.search_key(key, text)
        sorted_results = project.company.sorted_ids('modifytime', ids=results)
        datas, pages, total = self.paginate(project.company, sorted_results, cur_page, page_size)
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
        project_name = flask.request.form['project']
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
        self.reqparse.add_argument('data', type = list, location = 'json')
        self.reqparse.add_argument('project', type = str, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        datas = args['data']
        project_name = args['project']
        user = flask.ext.login.current_user
        project = self.svc_mult_cv.getproject(project_name)
        results = project.company_add_excel(datas, user.id)
        return {
            'code': 200,
            'data': results
        }

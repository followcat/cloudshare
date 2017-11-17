import json
import math

import core.basedata
import extractor.information_explorer
import flask
import flask.ext.login
import utils.builtin
from flask.ext.restful import Resource, reqparse


class CompanyAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        self.svc_index = flask.current_app.config['SVC_INDEX']
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.svc_co_repo = flask.current_app.config['SVC_CO_REPO']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', location = 'json')
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('introduction', location = 'json')
        super(CompanyAPI, self).__init__()

    def get(self, id):
        user = flask.ext.login.current_user
        result = self.svc_co_repo.getyaml(id)
        return { 'code': 200,'result': result }

    def post(self, id):
        args = self.reqparse.parse_args()
        coname = args['name']
        projectname = args['project']
        if args['introduction'] is None:
            args['introduction'] = str()
        user = flask.ext.login.current_user
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        metadata = extractor.information_explorer.catch_coinfo(stream=args)
        coobj = core.basedata.DataObject(metadata, data=args['introduction'].encode('utf-8'))
        result = project.company_add(coobj, user.name)
        if result is True:
            self.svc_index.add(self.svc_index.config['CO_MEM'], coobj.metadata['id'],
                               coobj.metadata)
        if result:
            response = { 'code': 200, 'data': result, 'message': 'Create new company successed.' }
        else:
            response = { 'code': 400, 'data': result, 'message': 'Create new company failed.' }
        return response

class CompanyAllAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(CompanyAllAPI, self).__init__()
        self.svc_index = flask.current_app.config['SVC_INDEX']
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('page_size', type = int, location = 'json')
        self.reqparse.add_argument('current_page', type = int, location = 'json')

    def get(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        return list(project.company.datas())

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        cur_page = args['current_page']
        page_size = args['page_size']
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        index = self.svc_index.config['CO_MEM']
        total, searches = self.svc_index.search(index=index,
                                            doctype=[project.id],
                                            kwargs={'sort': {"modifytime": "desc"}},
                                            start=(cur_page-1)*page_size,
                                            size=page_size)
        pages = int(math.ceil(total/page_size))
        datas = list()
        for item in searches:
            datas.append(project.company_get(item['_id']))
        return {
            'code': 200,
            'data': datas,
            'total': total
        }


class AddedCompanyListAPI(Resource):
    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(AddedCompanyListAPI, self).__init__()
        self.svc_index = flask.current_app.config['SVC_INDEX']
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('text', location = 'json')
        self.reqparse.add_argument('project', location = 'json')
    
    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        text = args['text']
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        customer_ids = project.company_customers()
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        index = self.svc_index.config['CO_MEM']
        company_ids = self.svc_index.search(index=index, filterdict={'name': text},
                                            doctype=[project.id],
                                            size=5, onlyid=True)
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
class CompanyCustomerListAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        super(CompanyCustomerListAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        result = project.company_customers()
        data = []
        for coname in result:
            co = project.company_get(coname)
            data.append(co)
        return { 'code': 200, 'data': data }
    
#create, delete
class CompanyCustomerAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        super(CompanyCustomerAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', location = 'json')
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        result = project.company.addcustomer(id, user.name)
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
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        result = project.company.deletecustomer(id, user.name)
        if result:
            response = { 'code': 200, 'message': 'Delete customer success.' }
        else:
            response = { 'code': 400, 'message': 'Delete customer fail.' }
        return response

#update info
class CompanyInfoUpdateAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_index = flask.current_app.config['SVC_INDEX']
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        super(CompanyInfoUpdateAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', location = 'json')
        self.reqparse.add_argument('update_info', type= list, location = 'json')
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        projectname = args['project']
        update_info = args['update_info']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        origin_info = project.company_get(id)
        for each in update_info:
            key = each['key']
            vtype = each['type']
            value = each['value']
            content = value['content']
            if vtype == 'PUT':
                origin_info[key] = content
            elif vtype == 'CREATE':
                data = project.company._listframe(content, user.name)
                origin_info[key].insert(0, data)
            elif vtype == 'DELETE':
                data = project.company._listframe(content, value['author'], value['date'])
                origin_info[key].remove(data)
        result = project.company_update_info(id, origin_info, user.name)
        if result:
            co_info = project.company_get(id)
            self.svc_index.add(self.svc_index.config['CO_MEM'], project.id,
                               id, None, co_info)
        if result:
            response = { 'code': 200, 'message': 'Update information success.' }
        else:
            response = { 'code': 400, 'message': 'Update information error.' }
        return response


class SearchCObyKeyAPI(Resource):

    def __init__(self):
        super(SearchCObyKeyAPI, self).__init__()
        self.svc_index = flask.current_app.config['SVC_INDEX']
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('current_page', type = int, location = 'json')
        self.reqparse.add_argument('page_size', type = int, location = 'json')
        self.reqparse.add_argument('search_items', type = list, location = 'json')
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        cur_page = args['current_page']
        page_size = args['page_size']
        search_items = args['search_items']
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        index = self.svc_index.config['CO_MEM']
        total, searches = self.svc_index.search(index=index, filterdict=dict(search_items),
                                            doctype=[project.id],
                                            kwargs={'sort': {"modifytime": "desc"}},
                                            start=(cur_page-1)*page_size,
                                            size=page_size)
        pages = int(math.ceil(total/page_size))
        datas = list()
        for item in searches:
            datas.append(project.company_get(item['_id']))
        return {
            'code': 200,
            'data': datas,
            'pages': pages,
            'total': total
        }


class CompanyUploadExcelAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(CompanyUploadExcelAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.reqparse.add_argument('files', type = str, location = 'json')
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        user = flask.ext.login.current_user
        projectname = flask.request.form['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        network_file = flask.request.files['files']
        compare_result = project.company_compare_excel(network_file.read(),
                                                       committer=user.name)
        infos = dict()
        for item in compare_result:
            coid = item[1]
            if coid not in infos:
                if project.company.exists(coid):
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
        self.svc_index = flask.current_app.config['SVC_INDEX']
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.reqparse.add_argument('data', type = list, location = 'json')
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        datas = args['data']
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        results = project.company_add_excel(datas, user.name)
        for id in results:
            co_info = project.company_get(id)
            self.svc_index.add(self.svc_index.config['CO_MEM'], project.id,
                               id, None, co_info)
        return {
            'code': 200,
            'data': results
        }

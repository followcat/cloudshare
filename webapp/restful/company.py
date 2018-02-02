import math

import flask
import flask.ext.login
from flask import request
from flask.ext.restful import Resource, reqparse

import core.basedata
import extractor.information_explorer


class CompanyAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', location = 'json')
        for key in extractor.information_explorer.catch_biddinginfo({}):
            self.reqparse.add_argument(key, location = 'json')
        super(CompanyAPI, self).__init__()

    def get(self):
        args = request.args
        user = flask.ext.login.current_user
        member = user.getmember()
        project = dict(filter(lambda x: x[0] in ('project',), args.items()))
        result = member.bd_getyaml(args['id'], **project)
        return { 'code': 200,'result': result }

    def post(self):
        result = False
        args = self.reqparse.parse_args()
        coname = args['name']
        if args['introduction'] is None:
            args['introduction'] = str()
        user = flask.ext.login.current_user
        member = user.getmember()
        metadata = extractor.information_explorer.catch_biddinginfo(stream=args)
        coobj = core.basedata.DataObject(metadata, data=args['introduction'].encode('utf-8'))
        project = dict(filter(lambda x: x[0] in ('project',), args.items()))
        result = member.bd_add(coobj, committer=user.name, **project)
        if result:
            response = { 'code': 200, 'data': result, 'message': 'Create new company successed.' }
        else:
            response = { 'code': 400, 'data': result, 'message': 'Create new company failed.' }
        return response

class CompanyAllAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(CompanyAllAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('page_size', type = int, location = 'json')
        self.reqparse.add_argument('current_page', type = int, location = 'json')

    def get(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        projectname = args['project']
        member = user.getmember()
        project = member.getproject(projectname)
        return list(project.bd_datas())

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        cur_page = args['current_page']
        page_size = args['page_size']
        member = user.getmember()
        project = dict(filter(lambda x: x[0] in ('project',), args.items()))
        total, searches = member.bd_search(kwargs={'sort': {"modifytime": "desc"}},
                                            start=(cur_page-1)*page_size,
                                            size=page_size, **project)
        pages = int(math.ceil(float(total)/page_size))
        datas = list()
        for item in searches:
            info = member.bd_getyaml(item['_id'], **project)
            if info:
                datas.append(info)
            else:
                total -= 1
        return {
            'code': 200,
            'data': datas,
            'total': total
        }


class AddedCompanyListAPI(Resource):
    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(AddedCompanyListAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('text', location = 'json')
        self.reqparse.add_argument('project', location = 'json')
    
    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        text = args['text']
        member = user.getmember()
        project = dict(filter(lambda x: x[0] in ('project',), args.items()))
        company_ids = member.bd_search(filterdict={'name': text},
                                            size=5, onlyid=True, **project)
        data = []
        customer_ids = member.bd_customers(**project)
        for company_id in company_ids:
            if company_id in customer_ids:
                continue
            yaml = member.bd_getyaml(company_id, **project)
            data.append({
                'id': yaml['id'],
                'company_name': yaml['name']
            })
        return { 'code': 200, 'data': data }

#owner
class CompanyCustomerListAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        super(CompanyCustomerListAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('page_size', type = int, location = 'json')
        self.reqparse.add_argument('current_page', type = int, location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        cur_page = args['current_page']
        page_size = args['page_size']
        member = user.getmember()
        project = dict(filter(lambda x: x[0] in ('project',), args.items()))
        result = list(member.bd_customers(**project))
        total = len(result)
        pages = int(math.ceil(float(total)/page_size))
        data = list()
        for coname in result[(cur_page-1)*page_size:cur_page*page_size]:
            info = member.bd_getyaml(coname, **project)
            if info:
                data.append(info)
            else:
                total -= 1
        return { 'code': 200, 'data': data, 'pages': pages, 'totals': total}
    
#create, delete
class CompanyCustomerAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(CompanyCustomerAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', location = 'json')
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        member = user.getmember()
        project = dict(filter(lambda x: x[0] in ('project',), args.items()))
        coobj = core.basedata.DataObject({'id': id}, data='')
        result = member.bd_addcustomer(coobj, user.name, **project)
        if result:
            response = { 'code': 200, 'message': 'Add customer success.' }
        else:
            response = { 'code': 400, 'message': 'Add customer fail.' }
        return response

    def delete(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        member = user.getmember()
        project = dict(filter(lambda x: x[0] in ('project',), args.items()))
        result = member.bd_deletecustomer(id, user.name, **project)
        if result:
            response = { 'code': 200, 'message': 'Delete customer success.' }
        else:
            response = { 'code': 400, 'message': 'Delete customer fail.' }
        return response

#update info
class CompanyInfoUpdateAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(CompanyInfoUpdateAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', type=str, location='json')
        self.reqparse.add_argument('metadata', type=dict, location='json')

    def _update(self, bsobj, **args):
        user = flask.ext.login.current_user
        member = user.getmember()
        project = dict(filter(lambda x: x[0] in ('project',), args.items()))
        result = member.bd_modify(bsobj, committer=user.name, **project)
        if result:
            response = { 'code': 200, 'message': 'Update information success.' }
        else:
            response = { 'code': 400, 'message': 'Update information error.' }
        return response

    def post(self):
        args = self.reqparse.parse_args()
        metadata = args['metadata']
        bsobj = core.basedata.DataObject(metadata, data='')
        response = self._update(bsobj, **args)
        return response

    def delete(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        metadata = args['metadata']
        member = user.getmember()
        project = dict(filter(lambda x: x[0] in ('project',), args.items()))
        bsobj = core.basedata.DataObject(metadata, data='')
        result = member.bd_kick(bsobj, committer=user.name, **project)
        if result:
            response = { 'code': 200, 'message': 'Update information success.' }
        else:
            response = { 'code': 400, 'message': 'Update information error.' }
        return response

    def put(self):
        args = self.reqparse.parse_args()
        metadata = args['metadata']
        bsobj = core.basedata.DataObject(metadata, data='')
        response = self._update(bsobj, **args)
        return response


class SearchCObyKeyAPI(Resource):

    def __init__(self):
        super(SearchCObyKeyAPI, self).__init__()
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
        member = user.getmember()
        project = dict(filter(lambda x: x[0] in ('project',), args.items()))
        total, searches = member.bd_search(filterdict=dict(search_items),
                                            kwargs={'sort': {"modifytime": "desc"}},
                                            start=(cur_page-1)*page_size,
                                            size=page_size, **project)
        pages = int(math.ceil(float(total)/page_size))
        datas = list()
        for item in searches:
            info = member.bd_getyaml(item['_id'], **project)
            if info:
                datas.append(info)
            else:
                total -= 1
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
        self.reqparse.add_argument('project', type=str, location='form')

    def post(self):
        args = self.reqparse.parse_args()
        user = flask.ext.login.current_user
        member = user.getmember()
        project = dict(filter(lambda x: x[0] in ('project',), args.items()))
        network_file = flask.request.files['files']
        compare_result = member.bd_compare_excel(network_file.read(),
                                                 committer=user.name, **project)
        infos = dict()
        for item in compare_result:
            coid = item[1]
            if coid not in infos:
                if member.bd_exists(coid, **project):
                    infos[coid] = member.bd_getyaml(coid, **project)
                elif item[0] == 'projectadd':
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
        self.reqparse.add_argument('data', type = list, location = 'json')
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        datas = args['data']
        projectname = args['project']
        member = user.getmember()
        project = dict(filter(lambda x: x[0] in ('project',), args.items()))
        prj_results = member.bd_add_excel(datas, **project)
        infos = dict()
        results = { 'success': dict(), 'failed': dict() }
        for bdid in prj_results:
            result_info = member.bd_getyaml(bdid, **project)
            infos[bdid] = result_info
            result_key = 'success' if prj_results[bdid]['result'] is True else 'failed'
            results[result_key][bdid] = prj_results[bdid]
            if prj_results[bdid]['result'] is True:
                member.bd_indexadd(id=bdid, data=None, info=result_info, **project)
        return {
            'code': 200,
            'data': results,
            'info': infos
        }

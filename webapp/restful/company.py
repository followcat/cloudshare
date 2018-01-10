import json
import math

import flask
import flask.ext.login
from flask import request
from flask.ext.restful import Resource, reqparse

import core.basedata
import extractor.information_explorer
import utils.builtin


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
        projectname = args['project']
        user = flask.ext.login.current_user
        member = user.getmember()
        project = member.getproject(projectname)
        result = project.bd_getyaml(args['id'])
        return { 'code': 200,'result': result }

    def post(self):
        result = False
        args = self.reqparse.parse_args()
        coname = args['name']
        projectname = args['project']
        if args['introduction'] is None:
            args['introduction'] = str()
        user = flask.ext.login.current_user
        member = user.getmember()
        project = member.getproject(projectname)
        metadata = extractor.information_explorer.catch_biddinginfo(stream=args)
        coobj = core.basedata.DataObject(metadata, data=args['introduction'].encode('utf-8'))
        result = project.bd_add(coobj, committer=user.name)
        if result:
            info = project.bd_getyaml(coobj.metadata['id'])
            project = dict(filter(lambda x: x[0] in ('project',), args.items()))
            member.bd_indexadd(id=coobj.metadata['id'],
                               data=None, info=info, **project)
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
        projectname = args['project']
        member = user.getmember()
        project = dict(filter(lambda x: x[0] in ('project',), args.items()))
        total, searches = member.bd_search(kwargs={'sort': {"modifytime": "desc"}},
                                            start=(cur_page-1)*page_size,
                                            size=page_size, **project)
        pages = int(math.ceil(float(total)/page_size))
        datas = list()
        project = member.getproject(projectname)
        for item in searches:
            info = project.bd_getyaml(item['_id'])
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
        projectname = args['project']
        member = user.getmember()
        project = dict(filter(lambda x: x[0] in ('project',), args.items()))
        company_ids = member.bd_search(filterdict={'name': text},
                                            size=5, onlyid=True, **project)
        data = []
        project = member.getproject(projectname)
        customer_ids = project.bd_customers()
        for company_id in company_ids:
            if company_id in customer_ids:
                continue
            yaml = project.bd_getyaml(company_id)
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
        projectname = args['project']
        member = user.getmember()
        project = member.getproject(projectname)
        result = list(project.bd_customers())
        total = len(result)
        pages = int(math.ceil(float(total)/page_size))
        data = list()
        for coname in result[(cur_page-1)*page_size:cur_page*page_size]:
            info = project.bd_getyaml(coname)
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
        projectname = args['project']
        member = user.getmember()
        project = member.getproject(projectname)
        coobj = core.basedata.DataObject({'id': id}, data='')
        result = project.addcustomer(coobj, user.name)
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
        member = user.getmember()
        project = member.getproject(projectname)
        coobj = core.basedata.DataObject(metadata, data='')
        result = project.deletecustomer(id, user.name)
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
        self.reqparse.add_argument('id', type=str, location='json')
        self.reqparse.add_argument('key', type=str, location='json')
        self.reqparse.add_argument('date', type=str, location='json')
        self.reqparse.add_argument('project', type=str, location='json')
        self.reqparse.add_argument('author', type=unicode, location='json')
        self.reqparse.add_argument('content', type=unicode, location='json')

    def _update(self, id, info, project, committer, **args):
        result = project.bd_update_info(id, info, committer)
        if result:
            co_info = project.bd_getyaml(id)
            project = dict(filter(lambda x: x[0] in ('project',), args.items()))
            member.bd_indexadd(id=id, data=None, info=co_info, **project)
        if result:
            response = { 'code': 200, 'message': 'Update information success.' }
        else:
            response = { 'code': 400, 'message': 'Update information error.' }
        return response

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        key = args['key']
        author = args['author']
        content = args['content']
        projectname = args['project']
        member = user.getmember()
        project = member.getproject(projectname)
        origin_info = project.bd_getyaml(id)
        data = project.bidding._listframe(content, author)
        origin_info[key].insert(0, data)
        response = self._update(id, origin_info, project, user.name, **args)
        return response

    def delete(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        key = args['key']
        date = args['date']
        content = args['content']
        projectname = args['project']
        member = user.getmember()
        project = member.getproject(projectname)
        origin_info = project.bd_getyaml(id)
        data = project.bidding._listframe(content, user.name, date=date)
        origin_info[key].remove(data)
        response = self._update(id, origin_info, project, user.name, **args)
        return response

    def put(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        key = args['key']
        content = args['content']
        projectname = args['project']
        member = user.getmember()
        project = member.getproject(projectname)
        origin_info = project.bd_getyaml(id)
        origin_info[key] = content
        response = self._update(id, origin_info, project, user.name, **args)
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
        projectname = args['project']
        member = user.getmember()
        project = dict(filter(lambda x: x[0] in ('project',), args.items()))
        total, searches = member.bd_search(filterdict=dict(search_items),
                                            kwargs={'sort': {"modifytime": "desc"}},
                                            start=(cur_page-1)*page_size,
                                            size=page_size, **project)
        pages = int(math.ceil(float(total)/page_size))
        datas = list()
        project = member.getproject(projectname)
        for item in searches:
            info = project.bd_getyaml(item['_id'])
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
        self.reqparse.add_argument('files', type = str, location = 'json')
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        user = flask.ext.login.current_user
        projectname = flask.request.form['project']
        member = user.getmember()
        project = member.getproject(projectname)
        network_file = flask.request.files['files']
        compare_result = project.bd_compare_excel(network_file.read(),
                                                       committer=user.name)
        infos = dict()
        for item in compare_result:
            coid = item[1]
            if coid not in infos:
                if project.bd_exists(coid):
                    infos[coid] = project.bd_getyaml(coid)
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
        self.reqparse.add_argument('data', type = list, location = 'json')
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        datas = args['data']
        projectname = args['project']
        member = user.getmember()
        project = member.getproject(projectname)
        prj_results = project.bd_add_excel(datas, committer=user.name)
        infos = dict()
        results = { 'success': dict(), 'failed': dict() }
        for coid in prj_results:
            if project.bd_exists(coid):
                result_info = project.bd_get(coid)
            else:
                result_info = prj_results[coid][data][0]
            infos[coid] = result_info
            result_key = 'success' if prj_results[coid]['success'] is True else 'failed'
            results[result_key][coid] = prj_results[coid]
            if prj_results[coid]['success'] is True:
                co_info = project.bd_get(coid)
                project = dict(filter(lambda x: x[0] in ('project',), args.items()))
                member.bd_indexadd(id=coid, data=None, info=co_info, **project)
        return {
            'code': 200,
            'data': results,
            'info': infos
        }

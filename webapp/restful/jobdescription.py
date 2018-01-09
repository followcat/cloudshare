import math
import utils.builtin

import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import core.basedata


class JobDescriptionAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('jd_id', location = 'json')
        self.reqparse.add_argument('co_id', location = 'json')
        self.reqparse.add_argument('status', location = 'json')
        self.reqparse.add_argument('description', location = 'json')
        self.reqparse.add_argument('commentary', location = 'json')
        self.reqparse.add_argument('followup', location = 'json')
        self.reqparse.add_argument('project', location = 'json')
        super(JobDescriptionAPI, self).__init__()

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        jd_id = args['jd_id']
        projectname = args['project']
        member = user.getmember()
        project = member.getproject(projectname)
        result = project.jd_get(jd_id)
        co_id = result['company']
        co_name = project.bd_getyaml(co_id)['name']
        result['company_name'] = co_name
        return { 'code': 200, 'data': result }

    def put(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        info = {
            'id': args['jd_id'],
            'status': args['status'],
            'description': args['description'],
            'commentary': args['commentary'] if args['commentary'] else '',
            'followup': args['followup'] if args['followup'] else '',
        }
        jdobj = core.basedata.DataObject(info, data='')
        member = user.getmember()
        project = member.getproject(projectname)
        result = project.jd_modify(jdobj, user.name)
        if result is True:
            jd_info = project.jd_get(jd_id)
            project = dict(filter(lambda x: x[0] in ('project',), args.items()))
            member.jd_indexadd(member.es_config['JD_MEM'],
                               jd_id, None, jd_info, **project)
        if result: 
            response = { 'code': 200, 'data': result,
                         'message': 'Update job description successed.' }
        else:
            response = { 'code': 400, 'data': result,
                         'message': 'Update job description failed. You are not the committer.' }
        return response


class JobDescriptionUploadAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('jd_name', location = 'json')
        self.reqparse.add_argument('co_id', location = 'json')
        self.reqparse.add_argument('jd_description', location = 'json')
        self.reqparse.add_argument('commentary', location = 'json')
        self.reqparse.add_argument('followup', location = 'json')
        self.reqparse.add_argument('project', location = 'json')
        super(JobDescriptionUploadAPI, self).__init__()

    def post(self):
        result = False
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        projectname = args['project']
        member = user.getmember()
        project = member.getproject(projectname)
        info = {
            'id': utils.builtin.genuuid(),
            'name': args['jd_name'],
            'company': args['co_id'],
            'description': args['jd_description'],
            'committer': user.name,
            'commentary': args['commentary'] if args['commentary'] else '',
            'followup': args['followup'] if args['followup'] else '',
        }
        jdobj = core.basedata.DataObject(info, data='')
        result = project.jd_add(jdobj, committer=user.name)
        if result is True:
            id = jdobj.metadata['id']
            project = dict(filter(lambda x: x[0] in ('project',), args.items()))
            member.jd_indexadd(member.es_config['JD_MEM'],
                               id, None, jdobj.metadata, **project)
        if result:
            response = { 'code': 200, 'data': {'result': result, 'info': jdobj.metadata},
                         'message': 'Create job description successed.' }
        else:
            response = { 'code': 400, 'data': result,
                         'message': 'Create job description failed.\
                                     You are not the committer.' }
        return response


class JobDescriptionSearchAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        super(Resource, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', location = 'json')
        self.reqparse.add_argument('page_size', type = int, location = 'json')
        self.reqparse.add_argument('current_page', type = int, location = 'json')
        self.reqparse.add_argument('search_items', type = list, location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        cur_page = args['current_page']
        page_size = args['page_size']
        projectname = args['project']
        search_items = args['search_items']
        member = user.getmember()
        project = dict(filter(lambda x: x[0] in ('project',), args.items()))
        jd_index = member.es_config['JD_MEM']
        co_index = member.es_config['CO_MEM']
        search_ditems = dict(search_items)
        if 'company' in search_ditems:
            co_ids = project.bd_search(index=co_index, onlyid=True,
                                          filterdict={ 'name': search_ditems['company'] }, **project)
            search_ditems['company'] = co_ids
        total, searches = member.jd_search(index=jd_index,
                                                filterdict=search_ditems,
                                                start=(cur_page-1)*page_size,
                                                size=page_size, source=True, **project)
        pages = int(math.ceil(float(total)/page_size))
        datas = list()
        project = member.getproject(projectname)
        for item in searches:
            jd = item['_source']
            co_id = jd['company']
            co_name = project.bd_getyaml(co_id)['name']
            jd['company_name'] = co_name
            datas.append(jd)
        return {
            'code': 200,
            'data': datas,
            'pages': pages,
            'totals': total
        }

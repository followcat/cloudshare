import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource


class JobDescriptionAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        self.svc_index = flask.current_app.config['SVC_INDEX']
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
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
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        result = project.jd_get(jd_id)
        co_id = result['company']
        co_name = project.company_get(co_id)['name']
        result['company_name'] = co_name
        return { 'code': 200, 'data': result }

    def put(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        jd_id = args['jd_id']
        status = args['status']
        projectname = args['project']
        description = args['description']
        commentary = args['commentary'] if args['commentary'] else ''
        followup = args['followup'] if args['followup'] else ''
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        result = project.jd_modify(jd_id, description, status,
                                   commentary, followup, user.name)
        if result is True:
            jd_info = project.jd_get(jd_id)
            self.svc_index.add(self.svc_index.config['JD_MEM'], project.id,
                               jd_id, None, jd_info)
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
        self.svc_index = flask.current_app.config['SVC_INDEX']
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
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
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        info = {
            'name': args['jd_name'],
            'company': args['co_id'],
            'description': args['jd_description'],
            'committer': user.name,
            'commentary': args['commentary'] if args['commentary'] else '',
            'followup': args['followup'] if args['followup'] else '',
        }
        jdobj = project.storageJD.baseobj(info)
        mbr_result = member.jd_add(jdobj, committer=user.name)
        if mbr_result is True:
            result = project.jd_add(jdobj, committer=user.name)
        if result is True:
            id = jdobj.metadata['id']
            self.svc_index.add(self.svc_index.config['JD_MEM'], project.id,
                               id, None, jdobj.metadata)
        return { 'code': 200, 'data': result, 'id': id,
                 'message': 'Create job description successed.' }


class JobDescriptionListAPI(Resource):

    decorators = [flask.ext.login.login_required]
    
    def __init__(self):
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        super(JobDescriptionListAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        result = [jd for jd_id, jd in project.jd_datas()]
        for jd in result:
            co_id = jd['company']
            co_name = project.company_get(co_id)['name']
            jd['company_name'] = co_name
        return { 'code': 200, 'data': result }


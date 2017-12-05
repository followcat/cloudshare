# -*- coding: utf-8 -*-
import yaml

import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import core.basedata
import core.exception
import utils.timeout.thread
import extractor.information_explorer


upload = dict()
uploadeng = dict()


class UploadOriginsAPI(Resource):

    def get(self):
        results = [
                  { "id" : 1, "name" : u"前程无忧", "origin": "default"},
                  { "id" : 2, "name" : u"无忧精英", "origin": "jingying"},
                  { "id" : 3, "name" : u"智联招聘", "origin": "default"},
                  { "id" : 4, "name" : u"智联卓聘", "origin": "zhilian"},
                  { "id" : 5, "name" : u"猎聘", "origin": "liepin"},
                  { "id" : 6, "name" : u"领英", "origin": "default"},
                  { "id" : 7, "name" : u"大街网", "origin": "default"},
                  { "id" : 6, "name" : u"中华英才", "origin": "yingcai"},
                  { "id" : 8, "name" : u"Cold Call", "origin": "default"},
                  { "id" : 9, "name" : u"其他", "origin": "default"}
                ]
        return { 'code': 200, 'data': results }


class UploadCVAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(UploadCVAPI, self).__init__()
        self.svc_min = flask.current_app.config['SVC_MIN']
        self.svc_index = flask.current_app.config['SVC_INDEX']
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.svc_mult_peo = flask.current_app.config['SVC_MULT_PEO']
        self.svc_docpro = flask.current_app.config['SVC_DOCPROCESSOR']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('files', type=str, location='json')
        self.reqparse.add_argument('updates', type=list, location='json')

    def putparam(self):
        self.user = flask.ext.login.current_user
        self.args = self.reqparse.parse_args()
        self.updates = self.args['updates']
        self.member = self.svc_members.defaultmember
        self.project = self.member.getproject()
        self.projectid = self.project.id
        self.modelname = self.project.modelname

    def put(self):
        self.putparam()
        names = []
        results = []
        documents = []
        for item in self.updates:
            status = 'failed'
            self.uploaddata = upload[self.user.name].pop(item['filename'])
            self.cvobj = self.uploaddata['CV']
            cvobj=self.cvobj
            if cvobj is not None:
                id = cvobj.metadata['id']
                for key, value in item.iteritems():
                    if key is not u'id':
                        cvobj.metadata[key] = value
                try:
                    result = self.project.cv_add(cvobj, self.user.name, unique=True)
                    if result['repo_cv_result']:
                        md = self.project.cv_getmd(id)
                        self.svc_index.add(self.svc_index.config['CV_MEM'], self.project.id,
                                           id, md, cvobj.metadata)
                    if result['project_cv_result']:
                        result['member_cv_result'] = self.member.cv_add(cvobj, self.user.name,
                                                                        unique=True)
                        status = 'success'
                        # Add to CV database and project
                        message = '200'
                        names.append(cvobj.ID)
                        documents.append(cvobj.data)
                        if not result['repo_cv_result']:
                            # Existed in other project
                            message = '201'
                    else:
                        status = 'success'
                        # Resume existed in database and project
                        message = '202'
                except core.exception.NotExistsContactException:
                    # The contact information is empty
                    message = '203'
                results.append({ 'id': id,
                                 'status': status,
                                 'message': message,
                                 'filename': item['filename'] })
        if self.projectid not in self.svc_min.sim[self.modelname]:
            self.svc_min.init_sim(self.modelname, self.projectid)
        else:
            self.svc_min.sim[self.modelname][self.projectid].add_documents(names, documents)
        return { 'code': 200, 'data': results }

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        if user.name not in upload:
            upload[user.name] = dict()
        origin = flask.request.form['origin']
        network_file = flask.request.files['files']
        filename = network_file.filename
        filepro = self.svc_docpro(network_file, filename.encode('utf-8'),
                                  flask.current_app.config['UPLOAD_TEMP'])
        if filepro.result is False:
            return { 'code': 401, 'data': { 'result': False,
                                            'resultid': filepro.resultcode,
                                            'name': '', 'filename': filename } }
        yamlinfo = extractor.information_explorer.catch_cvinfo(
                                            filepro.markdown_stream.decode('utf8'),
                                            filename, fix_func=origin, timing=True)
        filepro.renameconvert(yamlinfo['id'])
        dataobj = core.basedata.DataObject(metadata=yamlinfo,
                                           data=filepro.markdown_stream,)
        if not dataobj.metadata['name']:
            dataobj.metadata['name'] = utils.chsname.name_from_filename(filename)
        unique_peo = ('unique_id' not in yamlinfo or
                      self.svc_mult_peo.unique(dataobj))
        unique_id = yamlinfo['unique_id'] if 'unique_id' in yamlinfo else yamlinfo['id']
        upload[user.name][filename] = { 'CV': dataobj, 'unique_id': unique_id }
        return { 'code': 200, 'data': { 'result': filepro.result,
                                        'resultid': filepro.resultcode,
                                        'unique_peo': unique_peo,
                                        'unique_id': unique_id,
                                        'name': dataobj.metadata['name'],
                                        'filename': filename } }


class UserUploadCVAPI(UploadCVAPI):

    def __init__(self):
        super(UserUploadCVAPI, self).__init__()
        self.reqparse.add_argument('setpeople', type=bool, location='json')

    def put(self):
        args = self.reqparse.parse_args()
        setpeople = args['setpeople']
        result = super(UserUploadCVAPI, self).put()
        if result['data'][0]['status'] == 'success' and setpeople:
            self.user.peopleID = self.uploaddata['unique_id']
        return result

    def post(self):
        result = super(UserUploadCVAPI, self).post()
        if result['data']['result'] is True:
            result['data']['user_peo'] = False
            user = flask.ext.login.current_user
            if user.peopleID == result['data']['unique_id']:
                result['data']['user_peo'] = True
        return result


class MemberUploadCVAPI(UploadCVAPI):

    def __init__(self):
        super(MemberUploadCVAPI, self).__init__()
        self.reqparse.add_argument('project', location = 'json')

    def putparam(self):
        super(MemberUploadCVAPI, self).putparam()
        projectname = self.args['project']
        self.member = self.user.getmember(self.svc_members)
        self.project = self.member.getproject(projectname)
        self.projectid = self.project.id
        self.modelname = self.project.modelname


class UploadEnglishCVAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(UploadEnglishCVAPI, self).__init__()
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.svc_docpro = flask.current_app.config['SVC_DOCPROCESSOR']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('file', type = str, location = 'json')
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('project', location = 'json')

    def get(self):
        user = flask.ext.login.current_user
        dataobj = uploadeng[user.name]['CV']
        md = dataobj.preview_data()
        return { 'code': 200, 'data': { 'markdown': md } }

    def put(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        dataobj = uploadeng[user.name]['CV']
        result = project.cv_add_eng(id, dataobj, user.name)
        uploadeng[user.name] = None
        en_html = project.cv_getmd_en(id)
        return { 'code': 200, 'data': { 'status': result, 'en_html': en_html } }

    def post(self):
        user = flask.ext.login.current_user
        network_file = flask.request.files['file']
        filename = network_file.filename
        filepro = self.svc_docpro(network_file, filename.encode('utf-8'),
                                  flask.current_app.config['UPLOAD_TEMP'])
        yamlinfo = extractor.information_explorer.catch_cvinfo(
                                              stream=filepro.markdown_stream.decode('utf8'),
                                              filename=filepro.base.base, catch_info=False)
        dataobj = core.basedata.DataObject(metadata=yamlinfo,
                                           data=filepro.markdown_stream)
        uploadeng[user.name] = { 'data': dataobj }
        return { 'code': 200, 'data': { 'status': filepro.result, 'url': '/uploadpreview' } }


class UploadCVPreviewAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_mult_peo = flask.current_app.config['SVC_MULT_PEO']
        super(UploadCVPreviewAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('filename', location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        filename = args['filename']
        uploaddata = upload[user.name][filename]
        dataobj = uploaddata['CV']
        unique_id = uploaddata['unique_id']
        md = dataobj.preview_data()
        yaml_info = dataobj.metadata
        try:
            people_info = self.svc_mult_peo.getyaml(unique_id)
            cvs = people_info['cv']
        except (TypeError, IOError, KeyError) as e:
            cvs = []
        return { 'code': 200, 'data': { 'filename': filename,
                                        'markdown': md,
                                        'yaml_info': yaml_info,
                                        'cv': cvs } }

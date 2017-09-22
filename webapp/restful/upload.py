import yaml

import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import core.basedata
import core.exception
import utils.timeout.process
import utils.timeout.exception
import extractor.information_explorer


upload = dict()
uploadeng = dict()

class UploadCVAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_members = flask.current_app.config['SVC_MEMBERS']
        self.svc_mult_peo = flask.current_app.config['SVC_MULT_PEO']
        self.svc_min = flask.current_app.config['SVC_MIN']
        self.svc_index = flask.current_app.config['SVC_INDEX']
        self.svc_docpro = flask.current_app.config['SVC_DOCPROCESSOR']
        super(UploadCVAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('files', type = str, location = 'json')
        self.reqparse.add_argument('updates', type = list, location = 'json')
        self.reqparse.add_argument('project', location = 'json')

    def put(self):
        results = []
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        updates = args['updates']
        projectname = args['project']
        names = []
        documents = []
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        for item in updates:
            status = 'failed'
            cvobj = upload[user.name].pop(item['filename'])
            if cvobj is not None:
                id = cvobj.metadata['id']
                for key, value in item.iteritems():
                    if key is not u'id':
                        cvobj.metadata[key] = value
                if 'unique_id' in cvobj.metadata:
                    try:
                        result = project.cv_add(cvobj, user.name, unique=True)
                        if result['repo_cv_result']:
                            self.svc_index.add(cvobj.metadata['id'], cvobj.metadata)
                        if result['project_cv_result']:
                            result['member_cv_result'] = member.cv_add(cvobj, user.name,
                                                                       unique=True)
                            status = 'success'
                            message = 'Add to CV database and project.'
                            names.append(cvobj.name.md)
                            documents.append(cvobj.data)
                            if not result['repo_cv_result']:
                                message = 'Existed in other project.'
                        else:
                            message = 'Resume existed in database and project.'
                    except core.exception.NotExistsContactException:
                        message = 'The contact information is empty.'
                else:
                    message = 'Unable to extract personal information, please modify and try again'
                results.append({ 'id': id,
                                 'status': status,
                                 'message': message,
                                 'filename': item['filename'] })
        if projectname in self.svc_min.sim:
            self.svc_min.sim[projectname][projectname].add_documents(names, documents)
        return { 'code': 200, 'data': results }

    def post(self):
        user = flask.ext.login.current_user
        if user.name not in upload:
            upload[user.name] = dict()
        network_file = flask.request.files['files']
        filename = network_file.filename
        filepro = self.svc_docpro(network_file, filename.encode('utf-8'),
                                  flask.current_app.config['UPLOAD_TEMP'])
        if filepro.result is False:
            return { 'code': 401, 'data': { 'result': False,
                                            'resultid': filepro.resultcode,
                                            'name': '', 'filename': filename } }
        try:
            yamlinfo = utils.timeout.process.process_timeout_call(
                                 extractor.information_explorer.catch_cvinfo, 120,
                                 kwargs={'stream': filepro.markdown_stream.decode('utf8'),
                                         'filename': filename})
        except utils.timeout.process.KilledExecTimeout as e:
            return { 'code': 401, 'data': { 'result': False,
                                            'resultid': '',
                                            'name': '', 'filename': filename } }
        filepro.renameconvert(yamlinfo['id'])
        dataobj = core.basedata.DataObject(metadata=yamlinfo,
                                           data=filepro.markdown_stream,)
        if not dataobj.metadata['name']:
            dataobj.metadata['name'] = utils.chsname.name_from_filename(filename)
        unique_peo = ('unique_id' not in yamlinfo or
                      self.svc_mult_peo.unique(dataobj.metadata['unique_id']))
        upload[user.name][filename] = dataobj
        return { 'code': 200, 'data': { 'result': filepro.result,
                                        'resultid': filepro.resultcode,
                                        'unique_peo': unique_peo,
                                        'name': dataobj.metadata['name'],
                                        'filename': filename } }


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
        dataobj = uploadeng[user.name]
        md = dataobj.preview_data()
        return { 'code': 200, 'data': { 'markdown': md } }

    def put(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        projectname = args['project']
        member = user.getmember(self.svc_members)
        project = member.getproject(projectname)
        dataobj = uploadeng[user.name]
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
        uploadeng[user.name] = dataobj
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
        dataobj = upload[user.name][filename]
        md = dataobj.preview_data()
        yaml_info = dataobj.metadata
        try:
            people_info = self.svc_mult_peo.getyaml(yaml_info['unique_id'])
            cvs = people_info['cv']
        except (TypeError, IOError, KeyError) as e:
            cvs = []
        return { 'code': 200, 'data': { 'filename': filename,
                                        'markdown': md,
                                        'yaml_info': yaml_info,
                                        'cv': cvs } }

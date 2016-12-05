import yaml

import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import utils.chsname
import utils.timeout.process
import utils.timeout.exception
import core.basedata
import core.docprocessor
import extractor.information_explorer


upload = dict()
uploadeng = dict()

class UploadCVAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.svc_peo = flask.current_app.config['SVC_PEO_STO']
        self.svc_min = flask.current_app.config['SVC_MIN']
        super(UploadCVAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('files', type = str, location = 'json')
        self.reqparse.add_argument('updates', type = list, location = 'json')
        self.reqparse.add_argument('project', type = str, location = 'json')

    def put(self):
        results = []
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        updates = args['updates']
        project = args['project']
        names = []
        documents = []
        project_name = self.svc_mult_cv.getproject(project).name
        for item in updates:
            id = ''
            status = 'fail'
            message = 'The contact information is existend.'
            cvobj = upload[user.id].pop(item['filename'])
            if cvobj is not None:
                id = cvobj.metadata['id']
                for key, value in item.iteritems():
                    if key is not u'id':
                        cvobj.metadata[key] = value
                if 'unique_id' in cvobj.metadata:
                    peopmeta = extractor.information_explorer.catch_peopinfo(cvobj.metadata,
                                                                cvobj.metadata['unique_id'])
                    peopobj = core.basedata.DataObject(data='', metadata=peopmeta)
                    peo_result = self.svc_peo.add(peopobj, user.id)
                cv_result = self.svc_mult_cv.add(cvobj, user.id,
                                                 project_name, unique=True)
                if cv_result is True:
                    names.append(cvobj.name.md)
                    documents.append(cvobj.data)
                    status = 'success'
                    message = 'Upload success.'
            results.append({ 'id': id,
                             'status': status,
                             'message': message,
                             'filename': item['filename'] })
        self.svc_min.sim[project_name][project_name].add_documents(names, documents)
        return { 'code': 200, 'data': results }

    def post(self):
        user = flask.ext.login.current_user
        if user.id not in upload:
            upload[user.id] = dict()
        network_file = flask.request.files['files']
        filename = network_file.filename
        filepro = core.docprocessor.Processor(network_file, filename.encode('utf-8'),
                                              flask.current_app.config['UPLOAD_TEMP'])
        if filepro.result is False:
            return { 'code': 401, 'data': { 'result': False,
                                            'resultid': filepro.resultcode,
                                            'name': '', 'filename': filename } }
        try:
            yamlinfo = utils.timeout.process.process_timeout_call(
                                 extractor.information_explorer.catch_cvinfo, 120,
                                 kwargs={'stream': filepro.markdown_stream.decode('utf8'),
                                         'filename': filepro.base.base})
        except utils.timeout.process.KilledExecTimeout as e:
            return { 'code': 401, 'data': { 'result': False,
                                            'resultid': '',
                                            'name': '', 'filename': filename } }
        filepro.renameconvert(yamlinfo['id'])
        dataobj = core.basedata.DataObject(data=filepro.markdown_stream,
                                           metadata=yamlinfo)
        if not dataobj.metadata['name']:
            dataobj.metadata['name'] = utils.chsname.name_from_filename(filename)
        name = dataobj.metadata['name']
        unique_peo = False
        if 'unique_id' not in dataobj.metadata:
            unique_peo = True
        else:
            unique_peo = self.svc_peo.unique(dataobj.metadata['unique_id'])
        upload[user.id][filename] = dataobj
        return { 'code': 200, 'data': { 'result': filepro.result,
                                        'resultid': filepro.resultcode,
                                        'unique_peo': unique_peo,
                                        'name': name, 'filename': filename } }


class UploadEnglishCVAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(UploadEnglishCVAPI, self).__init__()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('file', type = str, location = 'json')
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('project', type = str, location = 'json')

    def get(self):
        user = flask.ext.login.current_user
        dataobj = uploadeng[user.id]
        md = dataobj.preview_data()
        return { 'code': 200, 'data': { 'markdown': md } }

    def put(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        project = args['project']
        yaml_data = self.svc_mult_cv.getproject(project).cv_getyaml(id)
        dataobj = uploadeng[user.id]
        result = self.svc_mult_cv.add_md(dataobj, user.id)
        yaml_data['enversion'] = dataobj.ID.md
        self.svc_mult_cv.modify(id + '.yaml', yaml.safe_dump(yaml_data, allow_unicode=True),
                                committer=user.id)
        user.uploadeng = None
        en_html = self.svc_mult_cv.getproject(project).cv_getmd_en(id)
        return { 'code': 200, 'data': { 'status': result, 'en_html': en_html } }

    def post(self):
        user = flask.ext.login.current_user
        network_file = flask.request.files['file']
        filename = network_file.filename
        filepro = core.docprocessor.Processor(network_file,
                                              filename.encode('utf-8'),
                                              flask.current_app.config['UPLOAD_TEMP'])
        yamlinfo = extractor.information_explorer.catch_cvinfo(
                                              stream=filepro.markdown_stream.decode('utf8'),
                                              filename=filepro.base.base, catch_info=False)
        dataobj = core.basedata.DataObject(data=filepro.markdown_stream,
                                           metadata=yamlinfo)
        uploadeng[user.id] = dataobj
        return { 'code': 200, 'data': { 'status': filepro.result, 'url': '/uploadpreview' } }


class UploadCVPreviewAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_peo = flask.current_app.config['SVC_PEO_STO']
        super(UploadCVPreviewAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('filename', location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        filename = args['filename']
        dataobj = upload[user.id][filename]
        md = dataobj.preview_data()
        yaml_info = dataobj.metadata
        try:
            people_info = self.svc_peo.getyaml(yaml_info['unique_id'])
            cvs = people_info['cv']
        except IOError:
            cvs = []
        except KeyError:
            cvs = []
        return { 'code': 200, 'data': { 'filename': filename,
                                        'markdown': md,
                                        'yaml_info': yaml_info,
                                        'cv': cvs } }

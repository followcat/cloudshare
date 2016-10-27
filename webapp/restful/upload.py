import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import utils.chsname
import core.converterutils
import services.curriculumvitae


upload = dict()
uploadeng = dict()

class UploadCVAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
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
            cvobj = upload[user.id].pop(item['filename'])
            if cvobj is not None:
                id = cvobj.metadata['id']
                for key, value in item.iteritems():
                    if key is not u'id':
                        cvobj.metadata[key] = value
                result = self.svc_mult_cv.add(cvobj, user.id, project_name, unique=True)
                if result is True:
                    names.append(cvobj.name.md)
                    documents.append(cvobj.markdown())
                    status = 'success'
            results.append({ 'id': id,
                             'status': status,
                             'filename': item['filename'] })
        self.svc_min.sim[def_cv_name][def_cv_name].add_documents(names, documents)
        return { 'code': 200, 'data': results }

    def post(self):
        user = flask.ext.login.current_user
        if user.id not in upload:
            upload[user.id] = dict()
        network_file = flask.request.files['files']
        filename = network_file.filename.encode('utf-8')
        filepro = core.converterutils.FileProcesser(network_file, filename,
                                                    flask.current_app.config['UPLOAD_TEMP'])
        cvobj = services.curriculumvitae.CurriculumVitaeObject(filepro.name,
                                                               filepro.markdown_stream,
                                                               filepro.yamlinfo)
        upload[user.id][filename] = None
        name = ''
        if filepro.result is True:
            if not cvobj.metadata['name']:
                #u_filename = filename.encode('utf-8')
                cvobj.metadata['name'] = utils.chsname.name_from_filename(filename)
            name = cvobj.metadata['name']
            upload[user.id][filename] = cvobj
        return { 'code': 200, 'data': { 'result': filepro.result,
                                        'resultid': filepro.resultcode,
                                        'name': name, 'filename': filename } }


class UploadEnglishCVAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(UploadEnglishCV, self).__init__()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('file', type = str, location = 'json')
        self.reqparse.add_argument('name', type = str, location = 'json')

    def get(self):
        user = flask.ext.login.current_user
        cvobj = uploadeng[user.id]
        md = cvobj.preview_markdown()
        return { 'result': { 'markdown': md } }

    def put(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        name = core.outputstorage.ConvertName(args['name'])
        yaml_data = self.svc_mult_cv.getyaml(name)
        cvobj = uploadeng[user.id]
        result = self.svc_mult_cv.add_md(cvobj, user.id)
        yaml_data['enversion'] = cvobj.name.md
        svc_mult_cv.modify(name.yaml, yaml.safe_dump(yaml_data, allow_unicode=True),
                      committer=user.id)
        user.uploadeng = None
        return { 'result': result }

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        network_file = args['file']
        filename = network_file.filename
        filepro = core.converterutils.FileProcesser(network_file,
                                                    filename.encode('utf-8'),
                                                    flask.current_app.config['UPLOAD_TEMP'])
        cvobj = services.curriculumvitae.CurriculumVitaeObject(filepro.name,
                                                               filepro.markdown_stream,
                                                               filepro.yamlinfo)
        uploadeng[user.id] = cvobj
        return { 'result': filepro.result }


class UploadCVPreviewAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(UploadCVPreviewAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = str, location = 'json')

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        upobj = upload[user.id][id]
        md = upobj.preview_markdown()
        yaml_info = upobj.filepro.yamlinfo
        return { 'code': 200, 'data': { 'id': id, 'markdown': md, 'yaml_info': yaml_info } }
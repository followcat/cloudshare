import yaml

import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import utils.chsname
import core.basedata
<<<<<<< HEAD
=======
import core.docprocessor
>>>>>>> fc1cdc32fe06167ea7f367bb4238100734f270f1
import extractor.information_explorer


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
            message = 'The contact information is existend.'
            cvobj = upload[user.id].pop(item['filename'])
            if cvobj is not None:
                id = cvobj.metadata['id']
                for key, value in item.iteritems():
                    if key is not u'id':
                        cvobj.metadata[key] = value
                result = self.svc_mult_cv.add(cvobj, user.id, project_name, unique=True)
                if result is True:
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
        yamlinfo = extractor.information_explorer.catch_cvinfo(
                                              filepro.markdown_stream.decode('utf8'),
                                              filepro.base.base, filepro.name.base)
        dataobj = core.basedata.DataObject(filepro.name, filepro.markdown_stream,
                                           yamlinfo)
        upload[user.id][filename] = None
        name = ''
        if filepro.result is True:
            if not dataobj.metadata['name']:
                dataobj.metadata['name'] = utils.chsname.name_from_filename(filename)
            name = dataobj.metadata['name']
            upload[user.id][filename] = dataobj
        return { 'code': 200, 'data': { 'result': filepro.result,
                                        'resultid': filepro.resultcode,
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
        return { 'result': { 'markdown': md } }

    def put(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['id']
        project = args['project']
        yaml_data = self.svc_mult_cv.getproject(project).getyaml(id)
        dataobj = uploadeng[user.id]
        result = self.svc_mult_cv.add_md(dataobj, user.id)
        yaml_data['enversion'] = dataobj.ID.md
        self.svc_mult_cv.modify(id + '.yaml', yaml.safe_dump(yaml_data, allow_unicode=True),
                                committer=user.id)
        user.uploadeng = None
        en_html = self.svc_mult_cv.getproject(project).getmd_en(id)
        return { 'code': 200, 'data': { 'status': result, 'en_html': en_html } }

    def post(self):
        user = flask.ext.login.current_user
        network_file = flask.request.files['file']
        filename = network_file.filename
        filepro = core.docprocessor.Processor(network_file,
                                              filename.encode('utf-8'),
                                              flask.current_app.config['UPLOAD_TEMP'])
        yamlinfo = extractor.information_explorer.catch_cvinfo(
                                              filepro.markdown_stream.decode('utf8'),
                                              filepro.base.base, filepro.name.base)
        dataobj = core.basedata.DataObject(filepro.name, filepro.markdown_stream,
                                           yamlinfo)
        uploadeng[user.id] = dataobj
        return { 'code': 200, 'data': { 'status': filepro.result, 'url': '/preview' } }


class UploadCVPreviewAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
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
        return { 'code': 200, 'data': { 'filename': filename, 'markdown': md, 'yaml_info': yaml_info } }
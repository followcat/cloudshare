import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import utils.chsname
import services.curriculumvitae

upload = dict()
uploadeng = dict()

class UploadCVAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_cv = flask.current_app.config['SVC_CV']
        self.svc_min = flask.current_app.config['SVC_MIN']
        super(UploadCVAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('files', type = str, location = 'json')
        self.reqparse.add_argument('updates', type = list, location = 'json')

    def put(self):
        results = dict()
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        updates = args['updates']
        for item in updates:
            upobj = upload[user.id].pop(item['id'])
            for key, value in item.iteritems():
                if key in upobj.filepro.yamlinfo and key is not u'id':
                    upobj.filepro.yamlinfo[key] = value
            result = self.svc_cv.add(upobj, user.id)
            results[item['id']] = result
        def_cv_name = self.svc_cv.default.name
        self.svc_min.sim[def_cv_name].update([self.svc_cv.default])
        return { 'code': 200, 'result': results }

    def post(self):
        user = flask.ext.login.current_user
        netword_file = flask.request.files['files']
        filename = netword_file.filename
        upobj = services.curriculumvitae.CurriculumVitaeObject(filename,
                                                netword_file,
                                                flask.current_app.config['UPLOAD_TEMP'])
        id = ''
        name = ''
        if upobj.result is True:
            if not upobj.filepro.yamlinfo['name']:
                #u_filename = filename.encode('utf-8')
                upobj.filepro.yamlinfo['name'] = utils.chsname.name_from_filename(filename)
            if user.id not in upload:
                upload[user.id] = dict()
            upload[user.id][upobj.ID] = upobj
            name = upobj.filepro.yamlinfo['name']
            id = upobj.filepro.yamlinfo['id']
        return { 'code': 200, 'data': { 'result': upobj.result,
                                        'resultid': upobj.resultid,
                                        'name': name, 'id': id } }


class UploadEnglishCVAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(UploadEnglishCV, self).__init__()
        self.svc_cv = flask.current_app.config['SVC_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('file', type = str, location = 'json')
        self.reqparse.add_argument('name', type = str, location = 'json')

    def get(self):
        user = flask.ext.login.current_user
        upobj = user.uploadeng
        md = upobj.preview_markdown()
        return { 'result': { 'markdown': md } }

    def put(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        name = core.outputstorage.ConvertName(args['name'])
        yaml_data = self.svc_cv.getyaml(name)
        upobj = uploadeng[user.id]
        result = self.svc_cv.add_md(upobj, user.id)
        yaml_data['enversion'] = upobj.filepro.name.md
        svc_cv.modify(name.yaml, yaml.safe_dump(yaml_data, allow_unicode=True),
                      committer=user.id)
        user.uploadeng = None
        return { 'result': result }

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        network_file = args['file']
        upobj = services.curriculumvitae.CurriculumVitaeObject(network_file.filename,
                                                network_file,
                                                flask.current_app.config['UPLOAD_TEMP'])
        uploadeng[user.id] = upobj
        return { 'result': upobj.result }


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
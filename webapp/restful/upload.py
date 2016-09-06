import pickle

import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import services.curriculumvitae


class UploadCVAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        self.svc_cv = flask.current_app.config['SVC_CV']
        self.svc_min = flask.current_app.config['SVC_MIN']
        super(UploadCVAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('files', type = str, location = 'json')
        self.reqparse.add_argument('index', type = int, location = 'json')
        self.reqparse.add_argument('updates', type = dict, location = 'json')

    def get(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        id = args['index']
        upobj = flask.session[user.id]['upload'][id]
        md = upobj.preview_markdown()
        yamlinfo = upobj.filepro.yamlinfo
        return { 'result': { 'markdown': md, 'yaml_info': yaml_info } }

    def put(self):
        results = dict()
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        updates = json.loads(args['updates'])
        for id in updates:
            upobj = flask.session[user.id]['upload'].pop(id)
            for key, value in updates[id].iteritems():
                if key in upobj.filepro.yamlinfo:
                    upobj.filepro.yamlinfo[key] = value
            result = self.svc_cv.add(upobj, user.id)
            results[id] = result
        def_cv_name = self.svc_cv.default.name
        self.svc_min.sim[def_cv_name].update([self.svc_cv.default])
        return { 'result': results }

    def post(self):
        if 'upload' not in flask.session[user.id]:
            flask.session[user.id]['upload'] = dict()
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        netword_file = args['files']
        filename = netword_file.filename
        upobj = services.curriculumvitae.CurriculumVitaeObject(filename,
                                                netword_file,
                                                flask.current_app.config['UPLOAD_TEMP'])
        if not upobj.filepro.yamlinfo['name']:
            u_filename = filename.encode('utf-8')
            upobj.filepro.yamlinfo['name'] = tools.batching.name_from_filename(u_filename)
        flask.session[user.id]['upload'][upobj.ID] = upobj
        flask.session.modified = True
        return flask.jsonify(result=upobj.result, name=upobj.filepro.yamlinfo['name'])


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
        upobj = flask.session[user.id]['uploadeng']
        md = upobj.preview_markdown()
        return { 'result': { 'markdown': md } }

    def put(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        name = core.outputstorage.ConvertName(args['name'])
        yaml_data = self.svc_cv.getyaml(name)
        upobj = flask.session[user.id]['uploadeng']
        result = self.svc_cv.add_md(upobj, user.id)
        yaml_data['enversion'] = upobj.filepro.name.md
        svc_cv.modify(name.yaml, yaml.safe_dump(yaml_data, allow_unicode=True),
                      committer=user.id)
        flask.session[user.id]['uploadeng'] = None
        return { 'result': result }

    def post(self):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        network_file = args['file']
        upobj = services.curriculumvitae.CurriculumVitaeObject(network_file.filename,
                                                network_file,
                                                flask.current_app.config['UPLOAD_TEMP'])
        flask.session[user.id]['uploadeng'] = upobj
        flask.session.modified = True
        return { 'result': upobj.result }

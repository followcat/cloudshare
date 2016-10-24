import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import core.outputstorage
import core.converterutils


class CurrivulumvitaeAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(CurrivulumvitaeAPI, self).__init__()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('project', type = str, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        id = args['id']
        project = args['project']
        html = self.svc_mult_cv.getproject(project).gethtml(id)
        yaml = self.svc_mult_cv.getproject(project).getyaml(id)
        return { 'code': 200, 'data': { 'html': html, 'yaml_info': yaml } }


class CurrivulumvitaeMDAPI(CurrivulumvitaeAPI):

    def __init__(self):
        super(CurrivulumvitaeMDAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('mddata', type = str, location = 'json')


    def get(self, id):
        md = self.svc_mult_cv.getmd(id)
        html = core.converterutils.md_to_html(md)
        return { 'result': html }

    def put(self, id):
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        md_data = args['mddata']
        name = core.outputstorage.ConvertName(id)
        self.svc_mult_cv.modify(name.md, md_data.encode('utf-8'), committer=user.id)
        return { 'result': True }


class CurrivulumvitaeYAMLAPI(CurrivulumvitaeAPI):

    def __init__(self):
        super(CurrivulumvitaeYAMLAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('yamlinfo', type = str, location = 'json')

    def get(self, id):
        yamlinfo = self.svc_mult_cv.getyaml(id)
        return { 'result': yamlinfo }

    def put(self, id):
        result = True
        user = flask.ext.login.current_user
        args = self.reqparse.parse_args()
        updateinfo = args['yamlinfo']
        name = core.outputstorage.ConvertName(id)
        yamlinfo = self.svc_mult_cv.getyaml(filename)
        commit_string = "File %s: " % (name.yaml)
        for key, value in updateinfo.iteritems():
            if key in yamlinfo:
                if key in ['tag', 'tracking', 'comment']:
                    yamlinfo[key].insert(0, {'author': user.id, 'content': value})
                    commit_string += " Add %s." % (key)
                else:
                    yamlinfo[key] = value
                    commit_string += " Modify %s to %s." % (key, value)
            else:
                result = False
                break
        else:
            self.svc_mult_cv.modify(name.yaml,
                                    yaml.safe_dump(yamlinfo, allow_unicode=True),
                                    commit_string.encode('utf-8'), user.id)
        return { 'result': result }


class UpdateCurrivulumvitaeInformation(Resource):
    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(UpdateCurrivulumvitaeInformation, self).__init__()
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('project', type = str, location = 'json')
        self.reqparse.add_argument('update_info', type = dict, location = 'json')

    def put(self):
        args = self.reqparse.parse_args()
        user = flask.ext.login.current_user
        id = args['id']
        project = args['project']
        update_info = args['update_info']

        for key, value in update_info.iteritems():
            data = self.svc_mult_cv.getproject(project).updateinfo(id, key, value, user.id)
            if data is not None:
                response = { 'code': 200, 'data': data, 'message': 'Update information success.' }
            else:
                response = { 'code': 400, 'message': 'Update information error.'}
                break
        return response

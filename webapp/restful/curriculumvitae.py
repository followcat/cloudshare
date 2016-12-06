import flask
import flask.ext.login
from flask.ext.restful import reqparse
from flask.ext.restful import Resource
import utils.builtin  

class CurrivulumvitaeAPI(Resource):

    decorators = [flask.ext.login.login_required]

    def __init__(self):
        super(CurrivulumvitaeAPI, self).__init__()
        self.svc_peo = flask.current_app.config['SVC_PEO_STO']
        self.svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('project', type = str, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        id = args['id']
        project = args['project']
        html = self.svc_mult_cv.gethtml(id, projectname=project)
        yaml = self.svc_mult_cv.getyaml(id, projectname=project)
        user = flask.ext.login.current_user
        result = user.getbookmark()
        if yaml['id'] in result:
            yaml['collected'] = True
        else:
            yaml['collected'] = False
        en_html = ''
        yaml['date'] = utils.builtin.strftime(yaml['date'])
        if 'enversion' in yaml:
            en_html = self.svc_mult_cv.getproject(project).cv_getmd_en(id)
        return { 'code': 200, 'data': { 'html': html, 'en_html': en_html, 'yaml_info': yaml } }


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
            data = self.svc_mult_cv.getproject(project).cv_updateyaml(id, key, value, user.id)
            if data is not None:
                response = { 'code': 200, 'data': data, 'message': 'Update information success.' }
            else:
                response = { 'code': 400, 'message': 'Update information error.'}
                break
        return response

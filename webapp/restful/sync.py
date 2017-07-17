import flask
from flask.ext.restful import Resource, reqparse

import services.cvstoragesync


class BrowserSyncAPI(Resource):

    def __init__(self):
        super(BrowserSyncAPI, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.svc_cv_sto = flask.current_app.config['SVC_CV_STO']
        self.svc_peo_sto = flask.current_app.config['SVC_PEO_STO']
        self.reqparse.add_argument('url', type = unicode, location = 'json')
        self.reqparse.add_argument('html', type = unicode, location = 'json')

    def post(self):
        args = self.reqparse.parse_args()
        url = args['url']
        html = args['html']
        id = ''
        result = False
        if 'liepin' in url:
            lpso = services.cvstoragesync.LiepinPluginSyncObject(url, html)
            result = lpso.add_new(self.svc_cv_sto, self.svc_peo_sto)
        if result is True:
            id = lpso.info['id']
        return {'code': 200, 'url': url, 'result': result, 'id': id}

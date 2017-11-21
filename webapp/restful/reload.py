import flask
from flask.ext.restful import Resource


class SyncReloadAPI(Resource):

    def get(self):
        result = False
        ip = flask.request.remote_addr
        if ip == '127.0.0.1':
            reload_method = flask.current_app.config['SYNC_METHOD_RELOAD']
            reloaded_obj = reload_method()
            flask.current_app.config.from_object(reloaded_obj)
            result = True
        return {'code': 200, 'result': result}

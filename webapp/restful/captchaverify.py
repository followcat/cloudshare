import string
import random

import flask
import captcha.image
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

class CaptchaAPI(Resource):

    code_numbers = 4

    def __init__(self):
        super(CaptchaAPI, self).__init__()
        self.cache = flask.current_app.cache
        self.imagecaptcha = captcha.image.ImageCaptcha()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('code', type = str, location = 'json')

    def get(self):
        assert '_id' in flask.session
        code = ''.join(random.SystemRandom().choice(string.ascii_uppercase +
                           string.digits) for _ in range(self.code_numbers))
        self.cache.set(flask.session['_id'], code, timeout=30)
        imagecsIO = self.imagecaptcha.generate(code)
        return flask.send_file(imagecsIO, attachment_filename="captcha.png",
                               as_attachment=True, mimetype='image/png')

    def post(self):
        args = self.reqparse.parse_args()
        code = args['code']
        result = False
        cachecode = self.cache.get(flask.session['_id'])
        if cachecode is not None and code.lower() == cachecode.lower():
                result = True
        self.cache.delete(flask.session['_id'])
        return { 'code': 200, 'result': result }

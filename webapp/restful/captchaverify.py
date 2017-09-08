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
        self.imagecaptcha = captcha.image.ImageCaptcha()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('code', type = str, location = 'json')

    def get(self):
        if 'verifycode' in flask.session and flask.session['verifycode'] is not None:
            code = flask.session['verifycode']
        else:
            code = ''.join(random.SystemRandom().choice(string.ascii_uppercase +
                           string.digits) for _ in range(self.code_numbers))
            flask.session['verifycode'] = code
            flask.session.modified = True
        imagecsIO = self.imagecaptcha.generate(code)
        return flask.send_file(imagecsIO, attachment_filename="captcha.png",
                               as_attachment=True, mimetype='image/png')

    def post(self):
        args = self.reqparse.parse_args()
        code = args['code']
        result = False
        if 'verifycode' in flask.session and flask.session['verifycode']:
            if code.lower() == flask.session['verifycode'].lower():
                flask.session['verifycode'] = None
                flask.session.modified = True
                result = True
        return { 'code': 200, 'result': result }

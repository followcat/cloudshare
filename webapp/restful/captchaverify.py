import string
import random

import flask
import captcha.image
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

class CaptchaAPI(Resource):

    code_numbers = 4
    cache_timeout = 30
    prefix = 'captcha_code'

    def __init__(self):
        super(CaptchaAPI, self).__init__()
        self.cache = flask.current_app.cache

    def hashname(self, id, prefix):
        return '-'.join([prefix, id])

    def updatecache(self, id, prefix):
        code = ''.join([random.SystemRandom().choice(string.ascii_uppercase +
                        string.digits) for _ in range(self.code_numbers)])
        cachename = self.hashname(flask.session['_id'], prefix)
        self.cache.set(cachename, code, timeout=self.cache_timeout)

    def getcache(self, id, prefix):
        cachename = self.hashname(flask.session['_id'], prefix)
        code = self.cache.get(cachename)
        return code

    def deletecache(self, id, prefix):
        cachename = self.hashname(flask.session['_id'], prefix)
        self.cache.delete(cachename)

    def get(self):
        assert '_id' in flask.session
        self.imagecaptcha = captcha.image.ImageCaptcha()
        self.updatecache(flask.session['_id'], self.prefix)
        code = self.getcache(flask.session['_id'], self.prefix)
        imagecsIO = self.imagecaptcha.generate(code)
        return flask.send_file(imagecsIO, attachment_filename="captcha.png",
                               as_attachment=True, mimetype='image/png')


class SMSAPI(CaptchaAPI):

    prefix = 'sms_code'
    cache_timeout = 60

    def get(self, code):
        result = False
        cachecode = self.getcache(flask.session['_id'], CaptchaAPI.prefix)
        if cachecode is not None and code.lower() == cachecode.lower():
            self.updatecache(flask.session['_id'], self.prefix)
            smscode = self.getcache(flask.session['_id'], self.prefix)
            print smscode
            result = True
        self.deletecache(flask.session['_id'], CaptchaAPI.prefix)
        return { 'code': 200, 'result': result }

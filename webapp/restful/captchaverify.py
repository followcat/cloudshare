import uuid
import string
import random

import flask
import captcha.image
from flask.ext.restful import reqparse
from flask.ext.restful import Resource

import utils.alisms
import utils.builtin


class CaptchaAPI(Resource):

    prefix = 'captcha_code'
    code_numbers = 4
    cache_timeout = 30
    code_type = string.ascii_uppercase + string.digits

    def __init__(self):
        super(CaptchaAPI, self).__init__()
        self.cache = flask.current_app.cache

    def hashname(self, id, prefix):
        return '-'.join([prefix, id])

    def updatecache(self, id, prefix):
        code = ''.join([random.SystemRandom().choice(self.code_type)
                        for _ in range(self.code_numbers)])
        cachename = self.hashname(flask.session['_id'], prefix)
        self.cache.set(cachename, code, timeout=self.cache_timeout)
        return code

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
        code = self.updatecache(flask.session['_id'], self.prefix)
        imagecsIO = self.imagecaptcha.generate(code)
        send = flask.send_file(imagecsIO, attachment_filename="captcha.png",
                               add_etags=False, as_attachment=True,
                               mimetype='image/png')
        send.set_etag(utils.builtin.hash(code))
        return send


class SMSAPI(CaptchaAPI):

    prefix = 'sms_code'
    code_numbers = 6
    cache_timeout = 600
    code_type = string.digits

    def __init__(self):
        super(SMSAPI, self).__init__()
        access_info = flask.current_app.config['ACCESS']
        self.REGION = access_info['REGION']
        self.ACCESS_KEY_ID = access_info['ACCESS_KEY_ID']
        self.ACCESS_KEY_SECRET = access_info['ACCESS_KEY_SECRET']
        self.template_code = access_info['SMS_TEMPLATE_CODE']
        self.sign_name = access_info['SMS_SIGN_NAME']

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('phone', type = str, location = 'json')

    def post(self, code):
        result = False
        args = self.reqparse.parse_args()
        phone = args['phone']
        cachecode = self.getcache(flask.session['_id'], CaptchaAPI.prefix)
        if code.lower() == cachecode.lower():
            result = True
            if cachecode is not None:
                smscode = self.updatecache(flask.session['_id'], self.prefix)
                business_id = uuid.uuid1()
                params = "{\"code\":\"%s\"}"%smscode
                response = utils.alisms.send_sms(self.ACCESS_KEY_ID,
                                                 self.ACCESS_KEY_SECRET,
                                                 self.REGION, business_id, phone,
                                                 self.sign_name,
                                                 self.template_code, params)
                result = True
        self.deletecache(flask.session['_id'], CaptchaAPI.prefix)
        return { 'code': 200, 'result': result }

# -*- coding: utf-8 -*-
import os
import datetime

import flask
import jinja2.ext
import flask.ext.login
from flask import request

import webapp.ext.views
import webapp.jsonencoder
import demoapp.restful.initializtion

app = flask.Flask(__name__, template_folder="../webapp/templates_dist"
                          , static_folder="../webapp/static")
app.config.from_object('demoapp.settings')
app.json_encoder = webapp.jsonencoder.CustomJSONEncoder
app.jinja_env.add_extension(jinja2.ext.loopcontrols)
webapp.ext.views.configure(app)
demoapp.restful.initializtion.initialize(app)


if __name__ == '__main__':
    app.debug = True
    if not app.debug:
        import logging
        logger = logging.getLogger()
        demoapplogger = logger.root.getChild('demoapp')
        handler = logging.handlers.RotatingFileHandler('demoapp_flask.log')
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s: \t%(message)s")
        handler.setFormatter(formatter)
        demoapplogger.addHandler(handler)

        @app.before_request
        def before_request_logging():
            logger = logging.getLogger('demoapp')
            user = ''
            try:
                user = flask.ext.login.current_user.name
            except AttributeError:
                pass
            ipaddr = request.remote_addr
            url = '/'+request.url.replace(request.url_root, '')
            method = request.environ.get('REQUEST_METHOD')
            protocol = request.environ.get('SERVER_PROTOCOL')
            date = datetime.datetime.today().strftime('[%d/%b/%Y %H:%M:%S]')
            info = ' '.join([
                ipaddr,
                '- -',
                date,
                '"'+method,
                url,
                protocol+'"',
                'code',
                user,
                '-'])
            logger.info(info)
    app.run(host='0.0.0.0', port=4888, threaded=True)

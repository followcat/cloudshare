import os
import logging
import datetime

import flask.ext.login
from flask import request


def init_webapp_userlog(app):
    LOG_PATH = 'log'
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)
    logger = logging.getLogger()
    webapplogger = logger.root.getChild('webapp')
    handler = logging.handlers.RotatingFileHandler(os.path.join(LOG_PATH, 'webapp_flask.log'))
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s: \t%(message)s")
    handler.setFormatter(formatter)
    webapplogger.addHandler(handler)

    @app.before_request
    def before_request_logging():
        logger = logging.getLogger('webapp')
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
        info = ' '.join([ipaddr, '- -', date, '"'+method, url,
                        protocol+'"', 'code', user, '-'])
        logger.info(info)

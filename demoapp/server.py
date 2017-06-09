# -*- coding: utf-8 -*-
import os
import flask
import jinja2.ext

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
        handler = logging.handlers.RotatingFileHandler('demoapp_flask.log')
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s: \t%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    app.run(host='0.0.0.0', port=4888, threaded=True)

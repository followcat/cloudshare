# -*- coding: utf-8 -*-
import os
import flask
import jinja2.ext

import webapp.ext.views
import demoapp.restful.initializtion


import webapp.jsonencoder

app = flask.Flask(__name__, template_folder="../webapp/templates_dist")
app.config.from_object('demoapp.settings')
app.json_encoder = webapp.jsonencoder.CustomJSONEncoder
app.jinja_env.add_extension(jinja2.ext.loopcontrols)
webapp.ext.views.configure(app)
demoapp.restful.initializtion.initialize(app)

@app.route('/static/<path:path>')
def static_proxy(path):
  return flask.send_from_directory('../static', path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4888, threaded=True)

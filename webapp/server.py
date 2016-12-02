# -*- coding: utf-8 -*-
import os
import flask
import flask.ext.session
import jinja2.ext

import ext.views
import webapp.restful.initializtion


import webapp.jsonencoder

app = flask.Flask(__name__, template_folder="templates_dist")
app.config.from_object('webapp.settings')
app.json_encoder = webapp.jsonencoder.CustomJSONEncoder
app.jinja_env.add_extension(jinja2.ext.loopcontrols)
ext.views.configure(app)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
sess = flask.ext.session.Session()
sess.init_app(app)
webapp.restful.initializtion.initialize(app)

@app.route("/download/<path:filename1>/<path:filename2>")
def download(filename1, filename2):
    import os
    directory = os.path.join(flask.current_app.root_path,
                             '..', app.config['UPLOAD_TEMP'], 'source')
    if os.path.exists(os.path.join(directory, filename1)):
        return flask.send_from_directory(directory, filename1, as_attachment=True)
    else:
        return flask.send_from_directory(directory, filename2, as_attachment=True)

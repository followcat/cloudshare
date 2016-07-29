# -*- coding: utf-8 -*-
import flask
import flask.ext.session
import jinja2.ext
import ext.views
import os

app = flask.Flask(__name__, template_folder="templates_dist")
app.config.from_object('webapp.settings')
app.jinja_env.add_extension(jinja2.ext.loopcontrols)
ext.views.configure(app)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
sess = flask.ext.session.Session()
sess.init_app(app)

@app.route("/download/<path:filename>")
def download(filename):
    directory = os.path.join(flask.current_app.root_path, '..',app.config['UPLOAD_TEMP'], 'source')
    return flask.send_from_directory(directory, filename, as_attachment=True)

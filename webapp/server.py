# -*- coding: utf-8 -*-
import flask
import flask.ext.session
import jinja2.ext
import ext.views

app = flask.Flask(__name__)
app.config.from_object('webapp.settings')
app.jinja_env.add_extension(jinja2.ext.loopcontrols)
ext.views.configure(app)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
sess = flask.ext.session.Session()
sess.init_app(app)

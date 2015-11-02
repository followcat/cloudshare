# -*- coding: utf-8 -*-
import flask
import flask.ext.session

import ext.views

app = flask.Flask(__name__)
app.config.from_object('webapp.settings')
ext.views.configure(app)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
sess = flask.ext.session.Session()
sess.init_app(app)

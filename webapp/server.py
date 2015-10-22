# -*- coding: utf-8 -*-
import flask
import flask.ext.session

import ext.views
import webapp.core.account

app = flask.Flask(__name__)
app.config.from_object('webapp.settings')
ext.views.configure(app)
sess = flask.ext.session.Session()
webapp.core.account.init_login(app)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

sess.init_app(app)

# -*- coding: utf-8 -*-
import flask

import ext.views
import webapp.core.account


app = flask.Flask(__name__)
app.config.from_object('webapp.settings')
ext.views.configure(app)
webapp.core.account.init_login(app)

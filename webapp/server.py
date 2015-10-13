# -*- coding: utf-8 -*-
import flask

import ext.views


app = flask.Flask(__name__)
app.config.from_object('webapp.settings')
ext.views.configure(app)

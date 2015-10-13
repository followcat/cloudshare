# -*- coding: utf-8 -*-
import flask

import ext.views


app = flask.Flask(__name__)
ext.views.configure(app)

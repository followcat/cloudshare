import flask
import codecs

from flask.ext.restful import reqparse
from flask.ext.restful import Resource

class FeatureAPI(Resource):

    def __init__(self):
        super(FeatureAPI, self).__init__()

    def get(self):
        with codecs.open('webapp/features.md', 'r', encoding='utf-8') as fp:
            data = fp.read()
        return { 'code': 200, 'data': data }
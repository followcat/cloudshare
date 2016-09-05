from flask.ext.restful import Resource

import utils.builtin


class StrftimeAPI(Resource):

    def get(self, number):
       date = utils.builtin.strftime(number)
       return { 'result': date }

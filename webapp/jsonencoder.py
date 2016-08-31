import flask.json


class CustomJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return JSONEncoder.default(self, obj)

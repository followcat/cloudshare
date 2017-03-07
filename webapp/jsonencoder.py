import flask.json


class CustomJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return flask.json.JSONEncoder.default(self, obj)

import os.path

import flask
import flask.views

import core.mining.info
import core.outputstorage


class Company(flask.views.MethodView):

    def get(self):
        repo = flask.current_app.config['DATA_DB']
        search_text = flask.request.args['search_text']
        searches = repo.grep(search_text)
        result = core.mining.info.company(repo, searches, search_text)
        return flask.jsonify(result=result)


class OneRegion(flask.views.MethodView):

    def get(self):
        repo = flask.current_app.config['DATA_DB']
        markdown_id = flask.request.args['md_id']
        name = core.outputstorage.ConvertName(markdown_id)
        with open(os.path.join(repo.repo.path, name.md)) as f:
            stream = f.read()
        result = core.mining.info.region(stream.decode('utf-8'))
        return flask.jsonify(result=result)
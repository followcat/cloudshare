import codecs
import os.path

import flask
import flask.views

import core.mining.info
import core.outputstorage


class Position(flask.views.MethodView):

    def get(self):
        repo = flask.current_app.config['DATA_DB']
        search_text = flask.request.args['search_text']
        searches = repo.grep(search_text)
        result = dict()
        for search in searches:
            with codecs.open(os.path.join(repo.repo.path, search),
                             'r', encoding='utf-8') as file:
                md_data = file.read()
            positions = core.mining.info.position(repo, md_data, search_text)
            for position in positions:
                if position not in result:
                    result[position] = []
                result[position].append(search)
        return flask.jsonify(result=result)


class Region(flask.views.MethodView):

    def get(self):
        repo = flask.current_app.config['DATA_DB']
        markdown_ids = flask.request.args['md_ids']
        result = []
        for id in markdown_ids:
            name = core.outputstorage.ConvertName(id)
            with codecs.open(os.path.join(repo.repo.path, name.md),
                             'r', encoding='utf-8') as file:
                stream = file.read()
            result.append(core.mining.info.region(stream))
        return flask.jsonify(result=result)


class Capacity(flask.views.MethodView):

    def get(self):
        repo = flask.current_app.config['DATA_DB']
        markdown_ids = flask.request.args['md_ids']
        result = []
        for id in markdown_ids:
            name = core.outputstorage.ConvertName(id)
            with codecs.open(os.path.join(repo.repo.path, name.md),
                             'r', encoding='utf-8') as file:
                stream = file.read()
            result.append(core.mining.info.capacity(stream))
        return flask.jsonify(result=result)

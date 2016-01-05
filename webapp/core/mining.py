import codecs
import os.path

import flask
import flask.views

import utils.builtin
import core.mining.info
import core.mining.lsimodel
import core.outputstorage

import json


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
            name = core.outputstorage.ConvertName(search)
            try:
                yaml_data = utils.builtin.load_yaml(repo.repo.path, name.yaml)
            except IOError:
                continue
            for position in positions:
                if position not in result:
                    result[position] = []
                result[position].append({search: yaml_data})
        return flask.jsonify(result=result)


class Region(flask.views.MethodView):

    def post(self):
        repo = flask.current_app.config['DATA_DB']
        markdown_ids = flask.request.form['md_ids']
        markdown_ids = json.loads(markdown_ids)
        result = []
        for id in markdown_ids:
            name = core.outputstorage.ConvertName(id)
            with codecs.open(os.path.join(repo.repo.path, name.md),
                             'r', encoding='utf-8') as file:
                stream = file.read()
            result.append(core.mining.info.region(stream))
        return flask.jsonify(result=result)


class Capacity(flask.views.MethodView):

    def post(self):
        repo = flask.current_app.config['DATA_DB']
        markdown_ids = flask.request.form['md_ids']
        markdown_ids = json.loads(markdown_ids)
        result = []
        for id in markdown_ids:
            name = core.outputstorage.ConvertName(id)
            with codecs.open(os.path.join(repo.repo.path, name.md),
                             'r', encoding='utf-8') as file:
                stream = file.read()
            result.append(core.mining.info.capacity(stream))
        return flask.jsonify(result=result)

class LSI(flask.views.MethodView):

    def get(self):
        if flask.current_app.config['LSI_MODEL'] is None:
            flask.current_app.config['LSI_MODEL'] = core.mining.lsimodel.LSImodel('repo')
            flask.current_app.config['LSI_MODEL'].setup()
        lsi = flask.current_app.config['LSI_MODEL']
        doc = flask.request.args['doc']
        result = lsi.probability(doc)
        kv = dict()
        s = "<html>"
        for each in result[:20]:
            kv[each[0]] = str(each[1])
            s += "<a href=/show/"+lsi.names[each[0]]+">"+str(each[1])+"</a></br>"
        s += "</html>"
        return s



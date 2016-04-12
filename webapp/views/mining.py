import codecs
import os.path

import flask
import flask.views

import utils.builtin
import core.mining.info
import core.mining.valuable
import core.outputstorage

import json


class Position(flask.views.MethodView):

    def post(self):
        repo = flask.current_app.config['DATA_DB']
        search_text = flask.request.form['search_text']
        if 'md_ids' in flask.request.form and len(search_text) > 0:
            searches = json.loads(flask.request.form['md_ids'])
        else:
            searches = repo.grep(search_text)
        result = dict()
        for search in searches:
            name = core.outputstorage.ConvertName(search)
            with codecs.open(os.path.join(repo.repo.path, name.md),
                             'r', encoding='utf-8') as file:
                md_data = file.read()
            positions = core.mining.info.position(repo, md_data, search_text)
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
            result.append({'md':id, 'capacity': core.mining.info.capacity(stream)})
        return flask.jsonify(result=result)


class LSI(flask.views.MethodView):

    def get(self):
        if 'search_textarea' in flask.request.args:
            repo = flask.current_app.config['DATA_DB']
            lsi = flask.current_app.config['LSI_MODEL']
            doc = flask.request.args['search_textarea']
            result = lsi.probability(doc)
            kv = dict()
            datas = []
            for each in result[:20]:
                kv[each[0]] = str(each[1])
                name = core.outputstorage.ConvertName(lsi.names[each[0]])
                yaml_info = utils.builtin.load_yaml(repo.repo.path, name.yaml)
                info = {
                    'author': yaml_info['committer'],
                    'time': utils.builtin.strftime(yaml_info['date']),
                    'match': str(each[1])
                }
                datas.append([name, yaml_info, info])
            return flask.render_template('lsipage.html',result=datas, search_textarea=doc)
        else:
            return flask.render_template('lsipage.html')

    def post(self):
        repo = flask.current_app.config['DATA_DB']
        lsi = flask.current_app.config['LSI_MODEL']
        doc = flask.request.form['doc']
        result = lsi.probability(doc)
        kv = dict()
        datas = []
        for each in result[1:9]:
            kv[each[0]] = str(each[1])
            name = core.outputstorage.ConvertName(lsi.names[each[0]])
            yaml_info = utils.builtin.load_yaml(repo.repo.path, name.yaml)
            info = {
                'author': yaml_info['committer'],
                'time': utils.builtin.strftime(yaml_info['date']),
                'match': str(each[1])
            }
            datas.append([name, yaml_info, info])
        return flask.jsonify(result=datas)        

class Valuable(flask.views.MethodView):

    def get(self):
        lsi = flask.current_app.config['LSI_MODEL']
        doc = flask.request.args['search_textarea']
        result = core.mining.valuable.rate(lsi, doc)
        repo = flask.current_app.config['DATA_DB']
        response = dict()
        datas = []
        for index in result:
            item = dict()
            item['description'] = index[0]
            values = []
            for match_item in index[1]:
                name = match_item[0]
                yaml_data = utils.builtin.load_yaml(repo.repo.path, name + '.yaml')
                yaml_data['match'] = match_item[1]
                values.append(yaml_data)
            item['value'] = values
            datas.append(item)
        response['data'] = datas
        return flask.jsonify(response)

    def post(self):
        lsi = lsi = flask.current_app.config['LSI_MODEL']
        doc = flask.request.form['search_textarea']
        name_list = flask.request.form['name_list']
        name_list = json.loads(name_list)
        result = core.mining.valuable.rate(lsi, doc, name_list=name_list)
        repo = flask.current_app.config['DATA_DB']
        response = dict()
        datas = []
        for index in result:
            item = dict()
            item['description'] = index[0]
            values = []
            for match_item in index[1]:
                name = match_item[0]
                yaml_data = utils.builtin.load_yaml(repo.repo.path, name + '.yaml')
                yaml_data['match'] = match_item[1]
                values.append(yaml_data)
            item['value'] = values
            datas.append(item)
        response['data'] = datas
        return flask.jsonify(response)
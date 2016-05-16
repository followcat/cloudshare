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
        repo_cv = flask.current_app.config['REPO_CV']
        search_text = flask.request.form['search_text']
        if 'md_ids' in flask.request.form and len(search_text) > 0:
            searches = json.loads(flask.request.form['md_ids'])
        else:
            searches = repo_cv.search(search_text)
        result = dict()
        for search in searches:
            name = core.outputstorage.ConvertName(search)
            with codecs.open(os.path.join(repo_cv.repo_path, name.md),
                             'r', encoding='utf-8') as file:
                md_data = file.read()
            positions = core.mining.info.position(md_data, search_text)
            try:
                yaml_data = utils.builtin.load_yaml(repo_cv.repo_path, name.yaml)
            except IOError:
                continue
            for position in positions:
                if position not in result:
                    result[position] = []
                result[position].append({search: yaml_data})
        return flask.jsonify(result=result)


class Region(flask.views.MethodView):

    def post(self):
        repo_cv = flask.current_app.config['REPO_CV']
        markdown_ids = flask.request.form['md_ids']
        markdown_ids = json.loads(markdown_ids)
        result = []
        for id in markdown_ids:
            name = core.outputstorage.ConvertName(id)
            with codecs.open(os.path.join(repo_cv.repo_path, name.md),
                             'r', encoding='utf-8') as file:
                stream = file.read()
            result.append(core.mining.info.region(stream))
        return flask.jsonify(result=result)


class Capacity(flask.views.MethodView):

    def post(self):
        repo_cv = flask.current_app.config['REPO_CV']
        markdown_ids = flask.request.form['md_ids']
        markdown_ids = json.loads(markdown_ids)
        result = []
        for id in markdown_ids:
            name = core.outputstorage.ConvertName(id)
            with codecs.open(os.path.join(repo_cv.repo_path, name.md),
                             'r', encoding='utf-8') as file:
                stream = file.read()
            result.append({'md':id, 'capacity': core.mining.info.capacity(stream)})
        return flask.jsonify(result=result)


class LSI(flask.views.MethodView):

    def get(self):
        repo_cv = flask.current_app.config['REPO_CV']
        lsi = flask.current_app.config['LSI_MODEL']
        repo_jd = flask.current_app.config['REPO_JD']
        jd_id = flask.request.args['jd_id']
        jd_yaml = utils.builtin.load_yaml(repo_jd.repo_path, jd_id + '.yaml')
        doc = jd_yaml['description']
        result = lsi.probability(doc)
        kv = dict()
        datas = []
        for each in result[:20]:
            kv[each[0]] = str(each[1])
            name = core.outputstorage.ConvertName(lsi.names[each[0]])
            yaml_info = utils.builtin.load_yaml(repo_cv.repo_path, name.yaml)
            info = {
                'author': yaml_info['committer'],
                'time': utils.builtin.strftime(yaml_info['date']),
                'match': str(each[1])
            }
            datas.append([name, yaml_info, info])
        return flask.render_template('lsipage.html',result=datas, button_bar=True)

    def post(self):
        repo_cv = flask.current_app.config['REPO_CV']
        lsi = flask.current_app.config['LSI_MODEL']
        doc = flask.request.form['search_text']
        result = lsi.probability(doc)
        kv = dict()
        datas = []
        for each in result[2:10]:
            kv[each[0]] = str(each[1])
            name = core.outputstorage.ConvertName(lsi.names[each[0]])
            yaml_info = utils.builtin.load_yaml(repo_cv.repo_path, name.yaml)
            info = {
                'author': yaml_info['committer'],
                'time': utils.builtin.strftime(yaml_info['date']),
                'match': str(each[1])
            }
            datas.append([name, yaml_info, info])
        # return flask.jsonify(result=datas)
        return flask.render_template('lsipage.html',result=datas, button_bar=False)


class Valuable(flask.views.MethodView):

    def post(self):
        lsi = flask.current_app.config['LSI_MODEL']
        repo_jd = flask.current_app.config['REPO_JD']
        jd_id = flask.request.form['jd_id']
        jd_yaml = utils.builtin.load_yaml(repo_jd.repo_path, jd_id + '.yaml')
        doc = jd_yaml['description']
        name_list = flask.request.form['name_list']
        name_list = json.loads(name_list)
        if len(name_list) == 0:
            result = core.mining.valuable.rate(lsi, doc)
        else:
            result = core.mining.valuable.rate(lsi, doc, name_list=name_list)
        repo_cv = flask.current_app.config['REPO_CV']
        response = dict()
        datas = []
        for index in result:
            item = dict()
            item['description'] = index[0]
            values = []
            for match_item in index[1]:
                name = match_item[0]
                yaml_data = utils.builtin.load_yaml(repo_cv.repo_path, name + '.yaml')
                yaml_data['match'] = match_item[1]
                values.append(yaml_data)
            item['value'] = values
            datas.append(item)
        response['data'] = datas
        response['max'] = 100
        return flask.jsonify(response)

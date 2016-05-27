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
        svc_cv = flask.current_app.config['SVC_CV']
        search_text = flask.request.form['search_text']
        if 'md_ids' in flask.request.form and len(search_text) > 0:
            searches = json.loads(flask.request.form['md_ids'])
        else:
            searches = svc_cv.search(search_text)
        result = dict()
        for name in searches:
            md_data = svc_cv.getmd(name)
            positions = core.mining.info.position(md_data, search_text)
            try:
                yaml_data = svc_cv.getyaml(name)
            except IOError:
                continue
            for position in positions:
                if position not in result:
                    result[position] = []
                result[position].append({name: yaml_data})
        return flask.jsonify(result=result)


class Region(flask.views.MethodView):

    def post(self):
        svc_cv = flask.current_app.config['SVC_CV']
        markdown_ids = flask.request.form['md_ids']
        markdown_ids = json.loads(markdown_ids)
        result = []
        for id in markdown_ids:
            name = core.outputstorage.ConvertName(id)
            with codecs.open(os.path.join(svc_cv.repo_path, name.md),
                             'r', encoding='utf-8') as file:
                stream = file.read()
            result.append(core.mining.info.region(stream))
        return flask.jsonify(result=result)


class Capacity(flask.views.MethodView):

    def post(self):
        svc_cv = flask.current_app.config['SVC_CV']
        markdown_ids = flask.request.form['md_ids']
        markdown_ids = json.loads(markdown_ids)
        result = []
        for id in markdown_ids:
            name = core.outputstorage.ConvertName(id)
            with codecs.open(os.path.join(svc_cv.repo_path, name.md),
                             'r', encoding='utf-8') as file:
                stream = file.read()
            result.append({'md':id, 'capacity': core.mining.info.capacity(stream)})
        return flask.jsonify(result=result)


class LSI(flask.views.MethodView):

    def get(self):
        svc_cv = flask.current_app.config['SVC_CV']
        sim = flask.current_app.config['LSI_SIM']
        svc_jd = flask.current_app.config['SVC_JD']
        jd_id = flask.request.args['jd_id']
        jd_yaml = svc_jd.get(jd_id+'.yaml')
        doc = jd_yaml['description']
        datas = self.process(sim, svc_cv, doc)
        return flask.render_template('lsipage.html',result=datas, button_bar=True)

    def post(self):
        svc_cv = flask.current_app.config['SVC_CV']
        sim = flask.current_app.config['LSI_SIM']
        doc = flask.request.form['search_text']
        datas = self.process(sim, svc_cv, doc)
        return flask.render_template('lsipage.html',result=datas, button_bar=True)

    def process(self, sim, svc, doc):
        datas = []
        for name, score in sim.probability(doc)[:50]:
            yaml_info = svc.getyaml(name)
            info = {
                'author': yaml_info['committer'],
                'time': utils.builtin.strftime(yaml_info['date']),
                'match': score
            }
            datas.append([name, yaml_info, info])
        return datas


class Valuable(flask.views.MethodView):

    def post(self):
        sim = flask.current_app.config['LSI_SIM']
        svc_jd = flask.current_app.config['SVC_JD']
        jd_id = flask.request.form['jd_id']
        jd_yaml = svc_jd.get(jd_id + '.yaml')
        doc = jd_yaml['description']
        name_list = flask.request.form['name_list']
        name_list = json.loads(name_list)
        if len(name_list) == 0:
            result = core.mining.valuable.rate(sim, doc)
        else:
            result = core.mining.valuable.rate(sim, doc, name_list=name_list)
        svc_cv = flask.current_app.config['SVC_CV']
        response = dict()
        datas = []
        for index in result:
            item = dict()
            item['description'] = index[0]
            values = []
            for match_item in index[1]:
                name = match_item[0]
                yaml_data = svc_cv.getyaml(name+'.yaml')
                yaml_data['match'] = match_item[1]
                values.append(yaml_data)
            item['value'] = values
            datas.append(item)
        response['data'] = datas
        response['max'] = 100
        return flask.jsonify(response)

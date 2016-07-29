import codecs
import os.path

import json
import flask
import flask.views

import utils.builtin
import core.mining.info
import core.mining.valuable
import core.outputstorage


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
            stream = svc_cv.getmd(id)
            result.append(core.mining.info.region(stream))
        return flask.jsonify(result=result)


class Capacity(flask.views.MethodView):

    def post(self):
        svc_cv = flask.current_app.config['SVC_CV']
        markdown_ids = flask.request.form['md_ids']
        markdown_ids = json.loads(markdown_ids)
        result = []
        for id in markdown_ids:
            stream = svc_cv.getmd(id)
            result.append({'md':id, 'capacity': core.mining.info.capacity(stream)})
        return flask.jsonify(result=result)


class LSI(flask.views.MethodView):

    def get(self):
        search = False
        svc_cv = flask.current_app.config['SVC_CV']
        miner = flask.current_app.config['SVC_MIN']
        svc_jd = flask.current_app.config['SVC_JD']
        sim_names = miner.addition_names()
        uses = miner.default_names()
        if 'uses' in flask.request.args and flask.request.args['uses']:
            uses.extend(flask.request.args['uses'].split(','))
        if 'jd_id' in flask.request.args:
            jd_id = flask.request.args['jd_id']
            jd_yaml = svc_jd.get(jd_id+'.yaml')
            doc = jd_yaml['description']
            param = 'jd_id='+jd_id
        elif 'jd_doc' in flask.request.args:
            doc = flask.request.args['jd_doc']
            param = 'jd_doc='+doc
        filterdict = None
        name = ""
        current_places = ""
        expectation_places = ""
        education = ""
        gender = ""
        marital_status = ""
        filterdict = dict()
        if 'currentPlaces' in flask.request.args and flask.request.args['currentPlaces']:
            filterdict['current_places'] = flask.request.args['currentPlaces'].split()
        if 'expectationPlaces' in flask.request.args and flask.request.args['expectationPlaces']:
            filterdict['expectation_places'] = flask.request.args['expectationPlaces'].split()
        if 'education' in flask.request.args and flask.request.args['education']:
            filterdict['education'] = flask.request.args['education'].split(',')
        if 'gender' in flask.request.args and flask.request.args['gender']:
            filterdict['gender'] = flask.request.args['gender'].split(',')
        if 'marriedStatus' in flask.request.args and flask.request.args['marriedStatus']:
            filterdict['marital_status'] = flask.request.args['marriedStatus'].split(',')
        cur_page = flask.request.args.get('page', '1')
        cur_page = int(cur_page)
        count = 20
        datas, pages, totals = self.process(miner, uses, svc_cv, doc, cur_page, count, filterdict)

        return flask.render_template('lsipage.html',result=datas,
                                     button_bar=True, sim_names=sim_names,
                                     cur_page=cur_page,
                                     pages=pages, param=param, nums=totals)

    def process(self, miner, uses, svc, doc, cur_page, eve_count, filterdict=None):
        index = flask.current_app.config['SVC_INDEX']
        if not cur_page:
            cur_page = 1
        datas = []
        result = miner.probability(doc, uses=uses)
        if filterdict:
            filteset = index.get(filterdict, uses=uses)
            result = filter(lambda x: os.path.splitext(x[0])[0] in filteset, result)
        totals = len(result)
        if totals%eve_count != 0:
            pages = totals/eve_count + 1
        else:
            pages = totals/eve_count
        for name, score in result[(cur_page-1)*eve_count:cur_page*eve_count]:
            cname = core.outputstorage.ConvertName(name)
            yaml_info = svc.getyaml(cname.yaml)
            info = {
                'author': yaml_info['committer'],
                'time': utils.builtin.strftime(yaml_info['date']),
                'match': score
            }
            datas.append([cname.md, yaml_info, info])
        return datas, pages, totals


class Similar(flask.views.MethodView):

    def post(self):
        svc_cv = flask.current_app.config['SVC_CV']
        miner = flask.current_app.config['SVC_MIN']
        doc = flask.request.form['doc']
        datas = []
        for name, score in miner.probability(doc)[:7]:
            cname = core.outputstorage.ConvertName(name)
            yaml_info = svc_cv.getyaml(cname.yaml)
            info = {
                'author': yaml_info['committer'],
                'time': utils.builtin.strftime(yaml_info['date']),
                'match': score
            }
            datas.append([cname.md, yaml_info, info])
        return flask.jsonify({'result': datas})


class Valuable(flask.views.MethodView):

    def post(self):
        miner = flask.current_app.config['SVC_MIN']
        svc_cv = flask.current_app.config['SVC_CV']
        svc_jd = flask.current_app.config['SVC_JD']
        if 'jd_id' in flask.request.form:
            jd_id = flask.request.form['jd_id']
            jd_yaml = svc_jd.get(jd_id+'.yaml')
            doc = jd_yaml['description']
        elif 'jd_doc' in flask.request.form:
            doc = flask.request.form['jd_doc']
        name_list = flask.request.form['name_list']
        uses = miner.default_names()
        uses.extend(json.loads(flask.request.form['uses']))
        name_list = json.loads(name_list)
        if len(name_list) == 0:
            result = core.mining.valuable.rate(miner, svc_cv, doc, uses=uses)
        else:
            result = core.mining.valuable.rate(miner, svc_cv, doc,
                                               uses=uses, name_list=name_list)
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

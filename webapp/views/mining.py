import flask
import flask.views

import utils.builtin
import core.outputstorage


class Similar(flask.views.MethodView):

    def post(self):
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        miner = flask.current_app.config['SVC_MIN']
        doc = flask.request.form['doc']
        basemodel = svc_mult_cv.default.name
        datas = []
        for name, score in miner.probability(basemodel, doc)[1:6]:
            cname = core.outputstorage.ConvertName(name)
            yaml_info = svc_mult_cv.getyaml(cname.yaml)
            info = {
                'author': yaml_info['committer'],
                'time': utils.builtin.strftime(yaml_info['date']),
                'match': score,
                'md_filename': cname.md
            }
            yaml_info.update(info)
            datas.append(yaml_info)
        return flask.jsonify({'result': datas})

import flask
import flask.views
import flask.ext.login


class AddJobDescription(flask.views.MethodView):

    @flask.ext.login.login_required
    def post(self):
        co_name = flask.request.form['coname']
        jd_name = flask.request.form['jdname']
        description = flask.request.form['description']
        user = flask.ext.login.current_user
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        status = 'Opening'
        result = svc_mult_cv.default.jd_add(co_name, jd_name, description, user.id, status)
        return flask.jsonify(result=result)


class ModifyJobDescription(flask.views.MethodView):

    @flask.ext.login.login_required
    def post(self):
        id = flask.request.form['id']
        description = flask.request.form['description']
        status = flask.request.form['status']
        user = flask.ext.login.current_user
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        result = svc_mult_cv.default.jd_modify(id, description, status, user.id)
        return flask.jsonify(result=result)


class SearchJobDescription(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        keyword = flask.request.form['keyword']
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        results = svc_mult_cv.default.jd_search(keyword)
        return flask.jsonify(result=results)


class ListJobDescription(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        names = svc_mult_cv.default.company_names()
        results = svc_mult_cv.default.jd_lists()
        datas = []
        status = flask.request.args['status']
        if status == 'Closed':
            for e in results:
                if 'status' in e and e['status'] == 'Closed':
                    datas.append(e)
        else:
            for e in results:
                if 'status' in e and e['status'] == 'Closed':
                    continue
                else:
                    datas.append(e)
        return flask.render_template('jdview.html', result=datas, status=status, names=names)


class ResumeToJobDescription(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self, filename, status):
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        names = svc_mult_cv.default.company_names()
        results = svc_mult_cv.default.jd_lists()
        datas = []
        if status == 'Closed':
            for e in results:
                if 'status' in e and e['status'] == 'Closed':
                    datas.append(e)
        else:
            for e in results:
                if 'status' in e and e['status'] == 'Closed':
                    continue
                else:
                    datas.append(e)
        return flask.render_template('jdview.html', result=datas, status=status, filename=filename, names=names)

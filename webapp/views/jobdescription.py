import flask
import flask.views
import flask.ext.login


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

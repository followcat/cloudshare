import flask.views
import flask.ext.login


class AddCompany(flask.views.MethodView):

    @flask.ext.login.login_required
    def post(self):
        name = flask.request.form['name']
        introduction = flask.request.form['introduction']
        user = flask.ext.login.current_user
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        result = svc_mult_cv.default.company_add(name, introduction, user.id)
        return flask.jsonify(result=result)


class ListCompany(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        names = svc_mult_cv.default.company_names()
        return flask.render_template('companyview.html', result=names)


class CompanyByName(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        name = flask.request.form['name']
        svc_mult_cv = flask.current_app.config['SVC_MULT_CV']
        co = svc_mult_cv.default.company_get(name)
        return flask.jsonify(result=co)

import flask.views
import flask.ext.login


class AddCompany(flask.views.MethodView):

    @flask.ext.login.login_required
    def post(self):
        name = flask.request.form['name']
        introduction = flask.request.form['introduction']
        user = flask.ext.login.current_user
        svccv = flask.current_app.config['SVC_CV']
        result = svccv.default.company_add(name, introduction, user.id)
        return flask.jsonify(result=result)


class ListCompany(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        svccv = flask.current_app.config['SVC_CV']
        names = svccv.default.company_names()
        return flask.render_template('companyview.html', result=names)


class CompanyByName(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        name = flask.request.form['name']
        svccv = flask.current_app.config['SVC_CV']
        co = svccv.default.company_get(name)
        return flask.jsonify(result=co)

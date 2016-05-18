import flask.views
import flask.ext.login


class AddCompany(flask.views.MethodView):

    @flask.ext.login.login_required
    def post(self):
        name = flask.request.form['name']
        introduction = flask.request.form['introduction']
        user = flask.ext.login.current_user
        repocompany = flask.current_app.config['REPO_CO']
        result = repocompany.add(name, introduction, user.id)
        return flask.jsonify(result=result)


class ListCompany(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        repocompany = flask.current_app.config['REPO_CO']
        names = repocompany.names()
        return flask.render_template('companyview.html', result=names)


class CompanyByName(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        name = flask.request.form['name']
        repocompany = flask.current_app.config['REPO_CO']
        co = repocompany.company(name)
        return flask.jsonify(result=co)

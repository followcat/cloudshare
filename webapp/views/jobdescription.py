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
        svcjd = flask.current_app.config['SVC_JD']
        result = svcjd.add(co_name, jd_name, description, user.id)
        return flask.jsonify(result=result)


class ModifyJobDescription(flask.views.MethodView):

    @flask.ext.login.login_required
    def post(self):
        id = flask.request.form['id']
        description = flask.request.form['description']
        user = flask.ext.login.current_user
        svcjd = flask.current_app.config['SVC_JD']
        result = svcjd.modify(id, description, user.id)
        return flask.jsonify(result=result)


class SearchJobDescription(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        keyword = flask.request.form['keyword']
        svcjd = flask.current_app.config['SVC_JD']
        results = svcjd.search(keyword)
        return flask.jsonify(result=results)


class ListJobDescription(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        svcjd = flask.current_app.config['SVC_JD']
        repocompany = flask.current_app.config['SVC_CO']
        names = repocompany.names()
        results = svcjd.lists()
        return flask.render_template('jdview.html', result=results, names=names)


class ResumeToJobDescription(flask.views.MethodView):
    
    @flask.ext.login.login_required
    def get(self, filename):
        svcjd = flask.current_app.config['SVC_JD']
        repocompany = flask.current_app.config['SVC_CO']
        names = repocompany.names()
        results = svcjd.lists()
        return flask.render_template('jdview.html', result=results, filename=filename, names=names)

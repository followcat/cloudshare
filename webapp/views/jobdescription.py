import os.path
import flask
import yaml
import uuid

import webapp.views.exception


class RepoJobDescription(object):
    """
        >>> import shutil
        >>> import utils.builtin
        >>> import webapp.views.company
        >>> import webapp.views.jobdescription
        >>> import repointerface.gitinterface
        
        >>> co_repo_name = 'webapp/views/test_co_repo'
        >>> co_interface = repointerface.gitinterface.GitInterface(co_repo_name)
        >>> repocompany = webapp.views.company.RepoCompany(co_interface)
        >>> repocompany.add('CompanyA', 'This is Co.A', 'Dever')
        True

        >>> jd_repo_name = 'webapp/views/test_jd_repo'
        >>> jd_interface = repointerface.gitinterface.GitInterface(jd_repo_name)
        >>> repojd = webapp.views.jobdescription.RepoJobDescription(jd_interface, repocompany)
        >>> repojd.add('CompanyA', 'JD-A', 'JD-A description', 'Dever')
        True
        >>> results = repojd.search('JD-A')
        >>> data = utils.builtin.load_yaml(repojd.repo.repo.path, results[0])
        >>> data['description']
        'JD-A description'
        >>> repojd.modify(data['id'], 'JD-B description', 'Dever')
        True
        >>> data = utils.builtin.load_yaml(repojd.repo.repo.path, results[0])
        >>> data['description']
        'JD-B description'

        >>> shutil.rmtree(jd_repo_name)
        >>> shutil.rmtree(co_repo_name)
    """

    def __init__(self, repo, repo_co):
        self.repo = repo
        self.repo_co = repo_co
        self.info = ""

    def add(self, company, name, description, committer):
        try:
            self.repo_co.company(company)
        except webapp.views.exception.NotExistsCompany:
            self.info = "NotExistsCompany."
            return False

        id = uuid.uuid1()
        hex_id = id.get_hex()
        data = {
            'name': name,
            'id': hex_id,
            'company': company,
            'description': description,
            'committer': committer
        }
        filename = self.filename(hex_id)
        with open(os.path.join(self.repo.repo.path, filename), 'w') as f:
            f.write(yaml.dump(data))
        self.repo.add_files(filename, "Add job description file: " + filename)
        return True

    def modify(self, hex_id, description, committer):
        filename = self.filename(hex_id)
        data = None
        with open(os.path.join(self.repo.repo.path, filename), 'r') as f:
            data = yaml.load(f.read())
        data['description'] = description
        dump_data = yaml.dump(data)
        self.repo.modify_file(filename, dump_data,
                              message="Modify job description: " + filename,
                              committer=committer)
        return True

    def filename(self, hex_id):
        return hex_id + '.yaml'

    def search(self, keyword):
        return self.repo.grep_yaml(keyword)


class AddJobDescription(flask.views.MethodView):

    @flask.ext.login.login_required
    def post(self):
        co_name = flask.request.form['coname']
        jd_name = flask.request.form['jdname']
        description = flask.request.form['description']
        user = flask.ext.login.current_user
        repojd = flask.current_app.config['REPO_JD']
        result = repojd.add(co_name, jd_name, description, user.id)
        return flask.jsonify(result=result)


class ModifyJobDescription(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        id = flask.request.form['id']
        description = flask.request.form['description']
        user = flask.ext.login.current_user
        repojd = flask.current_app.config['REPO_JD']
        result = repojd.modify(id, description, user.id)
        return flask.jsonify(result=result)

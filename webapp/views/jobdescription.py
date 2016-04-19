import glob
import uuid
import os.path
import flask
import yaml
import flask.views
import flask.ext.login

import utils.builtin
import webapp.views.exception


class RepoJobDescription(object):
    """
        >>> import shutil
        >>> import utils.builtin
        >>> import webapp.views.company
        >>> import webapp.views.jobdescription
        >>> import repointerface.gitinterface
        
        >>> repo_name = 'webapp/views/test_repo'
        >>> interface = repointerface.gitinterface.GitInterface(repo_name)
        >>> repocompany = webapp.views.company.RepoCompany(interface)
        >>> repocompany.add('CompanyA', 'This is Co.A', 'Dever')
        True

        >>> repojd = webapp.views.jobdescription.RepoJobDescription(interface, repocompany)
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
        >>> lists = repojd.lists()
        >>> lists[0]['company'], lists[0]['description']
        ('CompanyA', 'JD-B description')
        >>> shutil.rmtree(repo_name)
    """
    path = 'JD'

    def __init__(self, repo, repo_co):
        self.repo = repo
        self.repo_path = self.repo.repo.path + "/" + self.path
        self.repo_co = repo_co
        self.info = ""
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)

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
        file_path = os.path.join(self.repo_path, filename)
        with open(file_path, 'w') as f:
            f.write(yaml.dump(data))
        self.repo.add_files(os.path.join(self.path, filename),
                            "Add job description file: " + filename)
        return True

    def modify(self, hex_id, description, committer):
        filename = self.filename(hex_id)
        data = utils.builtin.load_yaml(self.repo_path, filename)
        data['description'] = description
        dump_data = yaml.dump(data)
        self.repo.modify_file(os.path.join(self.path, filename), dump_data,
                              message="Modify job description: " + filename,
                              committer=committer)
        return True

    def filename(self, hex_id):
        return hex_id + '.yaml'

    def search(self, keyword):
        return self.repo.grep_yaml(keyword)

    def lists(self):
        results = []
        for pathfile in glob.glob(os.path.join(self.repo_path, '*.yaml')):
            filename = pathfile.split('/')[-1]
            data = utils.builtin.load_yaml(self.repo_path, filename)
            results.append(data)
        return results


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


class SearchJobDescription(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        keyword = flask.request.form['keyword']
        repojd = flask.current_app.config['REPO_JD']
        results = repojd.search(keyword)
        return flask.jsonify(result=results)


class ListJobDescription(flask.views.MethodView):

    @flask.ext.login.login_required
    def get(self):
        repojd = flask.current_app.config['REPO_JD']
        results = repojd.lists()
        return flask.render_template('jdview.html', result=results)

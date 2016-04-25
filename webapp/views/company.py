import os

import yaml
import flask.views
import flask.ext.login

import webapp.views.exception


class RepoCompany(object):
    """
        >>> import shutil
        >>> import webapp.views.company
        >>> import repointerface.gitinterface
        >>> repo_name = 'webapp/views/test_repo'
        >>> interface = repointerface.gitinterface.GitInterface(repo_name)
        >>> repocompany = webapp.views.company.RepoCompany(interface)
        >>> repocompany.COMPANYS
        []
        >>> repocompany.add('CompanyA', 'This is Co.A', 'Dever')
        True
        >>> co = repocompany.company('CompanyA')
        >>> co['name']
        'CompanyA'
        >>> co['introduction']
        'This is Co.A'
        >>> repocompany.add('CompanyA', 'This is Co.A', 'Dever') # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        ExistsCompany: CompanyA
        >>> repocompany.names()
        ['CompanyA']
        >>> repocompany.company('CompanyB') # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        NotExistsCompany
        >>> shutil.rmtree(repo_name)
    """
    company_filename = 'company.yaml'
    path = 'CO'

    def __init__(self, repo):
        self.repo = repo
        self.repo_path = self.repo.repo.path + "/" + self.path
        self.file_path = os.path.join(self.repo_path, self.company_filename)
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)

    @property
    def COMPANYS(self):
        company_file = self.repo.repo.get_named_file(
            os.path.join('..', self.path, self.company_filename))
        if company_file is None:
            self.create()
            company_file = self.repo.repo.get_named_file(
                os.path.join('..', self.path, self.company_filename))
        data = yaml.load(company_file.read())
        company_file.close()
        return data

    def create(self):
        empty_list = []
        with open(self.file_path, 'w') as f:
            f.write(yaml.dump(empty_list))
        self.repo.add_files(self.file_path, "Add company file.")

    def add(self, name, introduction, committer):
        companys = self.COMPANYS
        for company in companys:
            if company['name'] == name:
                raise webapp.views.exception.ExistsCompany(name)
        data = {
            'name': name,
            'committer': committer,
            'introduction': introduction,
        }
        companys.append(data)
        dump_data = yaml.dump(companys)
        message = "Add company: " + name
        self.repo.modify_file(os.path.join(self.path, self.company_filename),
                              dump_data, message=message.encode('utf-8'),
                              committer=committer)
        return True

    def company(self, name):
        result = None
        companys = self.COMPANYS
        for company in companys:
            if company['name'] == name:
                result = company
                break
        else:
            raise webapp.views.exception.NotExistsCompany
        return result

    def names(self):
        names = [company['name'] for company in self.COMPANYS]
        return names


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

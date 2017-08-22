import os
import glob

import core.basedata
import utils.builtin
import services.project
import services.base.service
import services.simulationacc

import sources.industry_id


class Customer(services.base.service.Service):

    commitinfo = 'Customer'
    PRJ_PATH = 'projects'
    ACC_PATH = 'accounts'
    config_file = 'config.yaml' 

    def __init__(self, acc_repos, co_repos, cv_repos, mult_peo, path, name, iotype='git'):
        super(Customer, self).__init__(path, name, iotype=iotype)
        self.name = name
        self.path = path
        self.co_repos = co_repos
        self.cv_repos = cv_repos
        self.mult_peo = mult_peo
        self.projects_path = os.path.join(path, self.PRJ_PATH)
        self.accounts_path = os.path.join(path, self.ACC_PATH)
        self.load_projects()
        self.accounts = services.simulationacc.SimulationACC(self.accounts_path, name,
                                                             acc_repos)
        self.config = dict()
        try:
            self.load()
        except IOError:
            pass

    def load(self):
        self.config = utils.builtin.load_yaml(self.path, self.config_file)

    def save(self):
        utils.builtin.save_yaml(self.config, self.path, self.config_file,
                                default_flow_style=False)

    def setup(self, classify, committer=None, config=None):
        if config is None:
            config = {}
        if not os.path.exists(os.path.join(self.path, self.config_file)):
            self.update(classify, committer)
        self.config.update(config)
        self.save()

    def use(self, id):
        result = None
        if self.accounts.exists(id):
            result = self
        return result

    def load_projects(self):
        if not os.path.exists(self.projects_path):
            os.makedirs(self.projects_path)
        self.projects = dict()
        for path in glob.glob(os.path.join(self.projects_path, '*')):
            if os.path.isdir(path):
                name = os.path.split(path)[1]
                tmp_project = services.project.Project(path, self.co_repos, self.cv_repos,
                                                       self.mult_peo, name)
                tmp_project.setup()
                self.projects[name] = tmp_project

    def add_project(self, name, classify, autosetup=False, autoupdate=False):
        result = False
        if name not in self.projects:
            path = os.path.join(self.projects_path, name)
            tmp_project = services.project.Project(path, self.co_repos, self.cv_repos,
                                                   self.mult_peo, name)
            tmp_project.setup(classify, config={'autosetup': autosetup,
                                                'autoupdate': autoupdate})
            self.projects[name] = tmp_project
            result = True
        return result

    def add_account(self, inviter_id, invited_id, committer, creator=False):
        result = False
        if creator is True or self.accounts.exists(inviter_id):
            bsobj = core.basedata.DataObject(metadata={'id': invited_id}, data=None)
            result = self.accounts.add(bsobj, committer=committer)
        return result

    def rm_account(self, inviter_id, invited_id, committer):
        result = False
        if self.accounts.exists(inviter_id) and self.accounts.exists(invited_id):
            result = self.accounts.remove(invited_id, committer=committer)
        return result

    def getproject(self, projectname):
        return self.projects[projectname]

    def getnums(self):
        result = dict()
        result['total'] = 0
        for name in self.projects:
            project = self.projects[name]
            numbers = project.cv_numbers()
            result[name] = numbers
            result['total'] += numbers
        return result

    def backup(self, path):
        customer_path = os.path.join(path, self.name)
        for name in self.projects:
            project = self.projects[name]
            project.backup(customer_path)
        self.accounts.backup(customer_path)


class DefaultCustomer(Customer):

    default_name = 'default'
    default_model = 'medical'

    def __init__(self, acc_repos, co_repos, cv_repos, mult_peo, path,
                 name='default', iotype='git'):
        super(DefaultCustomer, self).__init__(acc_repos, co_repos, cv_repos,
                                              mult_peo, path, name, iotype=iotype)
        if self.default_name not in self.projects:
            super(DefaultCustomer, self).add_project(self.default_name,
                                                     sources.industry_id.sources)
        self.projects[self.default_name]._modelname = 'medical'

    def use(self, id):
        return self

    def getproject(self, projectname=None):
        return self.projects[self.default_name]

    def add_account(self, **kwargs):
        return False

    def add_project(self, **kwargs):
        return False

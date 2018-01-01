import os
import glob

import core.basedata
import utils.builtin
import services.company
import services.project
import services.secret
import services.curriculumvitae
import services.simulationcv
import services.simulationco
import services.simulationacc
import services.simulationpeo
import services.base.kv_storage
import services.operator.search
import services.operator.checker
import services.operator.combine
import services.operator.multiple

import sources.industry_id
import extractor.information_explorer


class SimulationMember(services.base.kv_storage.KeyValueStorage):

    commitinfo = 'Member'
    config_file = 'config.yaml'

    YAML_TEMPLATE = (
        ('storageCV',           str),
        ('storagePEO',          str),
        ('limitPEO',            str),
        ('storageCO',           str),
        ('storageJD',           str),
    )

    def setup(self, info):
        info['id'] = self.config_file
        bsobj = core.basedata.DataObject(metadata=info, data=None)
        return self.modify(bsobj, committer=self.commitinfo, do_commit=True)


class Member(services.operator.combine.Combine):

    PEO_PATH = 'people'
    PRJ_PATH = 'projects'
    ACC_PATH = 'accounts'
    CO_PATH = 'companies'
    JD_PATH = 'jobdescriptions'
    CV_PATH = 'curriculumvitaes'

    default_model = 'default'
    max_project_nums = 3

    def __init__(self, data_service, **kwargs):
        """"""
        super(Member, self).__init__(data_service, **kwargs)
        assert 'people' in kwargs
        assert 'company' in kwargs
        assert 'bidding' in kwargs
        assert 'search_engine' in kwargs
        assert 'jobdescription' in kwargs
        assert 'curriculumvitae' in kwargs
        self.name = data_service.name
        self.path = data_service.path
        self.config_file = data_service.config_file
        self.cv_path = os.path.join(self.path, self.CV_PATH)
        self.jd_path = os.path.join(self.path, self.JD_PATH)
        self.co_path = os.path.join(self.path, self.CO_PATH)
        self.peo_path = os.path.join(self.path, self.PEO_PATH)
        self.bd_repos = kwargs['bidding']['bd']
        self.co_repos = kwargs['company']['co']
        self.cv_repos = kwargs['curriculumvitae']['cv']
        self.jd_repos = kwargs['jobdescription']['jd']
        self.mult_peo = kwargs['people']['peo']
        self.search_engine = kwargs['search_engine']['idx']
        self.es_config = kwargs['search_engine']['config']
        self.projects_path = os.path.join(self.path, self.PRJ_PATH)
        self.accounts_path = os.path.join(self.path, self.ACC_PATH)
        self.company = services.operator.checker.Filter(
                data_service=services.operator.multiple.Multiple(kwargs['company']['co']),
                operator_service=services.simulationco.SelectionCO(self.co_path, self.name))
        self.curriculumvitae = services.operator.multiple.Multiple(
                [services.curriculumvitae.SearchIndex(services.operator.checker.Filter(
                    data_service=services.operator.split.SplitData(
                        data_service=kwargs['curriculumvitae']['repo'],
                        operator_service=services.simulationcv.SimulationCV(self.cv_path, self.name)),
                    operator_service=services.simulationcv.SelectionCV(self.cv_path, self.name))),
                services.operator.split.SplitData(
                    data_service=services.secret.Private(
                        data_service=kwargs['curriculumvitae']['storage'],
                        operator_service=services.simulationcv.SelectionCV(self.cv_path, self.name)),
                    operator_service=services.simulationcv.SimulationCV(self.cv_path, self.name)),
                ])
        self.people = services.operator.checker.Filter(
                data_service=services.operator.split.SplitData(
                    data_service=services.operator.multiple.Multiple(kwargs['people']['peo']),
                    operator_service=services.simulationpeo.SimulationPEO(self.peo_path, self.name)),
                operator_service=services.base.name_storage.NameStorage(self.peo_path, self.name))
        self.config_service = self.data_service
        self.config = dict()
        try:
            self.load()
        except IOError:
            pass
        if not os.path.exists(self.projects_path):
            os.makedirs(self.projects_path)
        self.idx_setup()

    def idx_setup(self):
        self.curriculumvitae.services[0].setup(self.search_engine, self.es_config['CV_MEM'])

    def idx_updatesvc(self):
        self.curriculumvitae.services[0].updatesvc(self.es_config['CV_MEM'], self.id, numbers=1000)

    def load(self):
        config = self.config_service.getyaml(self.config_file)
        if 'id' not in self.config:
            self.config['id'] = utils.builtin.hash(self.name)
        if config:
            self.config.update(config)

    def save(self):
        return self.config_service.setup(self.config)

    def setup(self, config=None, committer=None):
        if config is None:
            config = {}
        modified = False
        for key in config:
            if key not in self.config or self.config[key] != config[key]:
                self.config[key] = config[key]
                modified = True
        if modified:
            self.save()
        self.load_projects()
        self.accounts = services.operator.checker.Checker(
                data_service=services.simulationacc.SimulationACC(self.accounts_path, self.name),
                operator_service=services.simulationacc.SelectionACC(self.accounts_path, self.name))

    def use(self, id):
        result = None
        if self.accounts.exists(id):
            result = self
        return result

    def get_admins(self):
        return self.administrator

    def check_admin(self, id):
        return id in self.administrator

    def add_admin(self, inviter_id, invited_id, creator=False):
        result = False
        if creator is True or (self.check_admin(inviter_id) and
                               self.check_admin(invited_id) is False):
            self.administrator.add(invited_id)
            self.save()
            result = True
        return result

    def delete_admin(self, inviter_id, invited_id):
        result = False
        if len(self.administrator) > 1:
            if self.check_admin(inviter_id):
                if self.check_admin(invited_id):
                    self.administrator.remove(invited_id)
                    self.save()
                    result = True
        return result

    @property
    def id(self):
        return self.config['id']

    @property
    def storagePEO(self):
        result = None
        servicename = self.config['storagePEO']
        for each in self.mult_peo[0].peoples:
            if each.name == servicename:
                result = each
                break
        return result

    @property
    def limitPEO(self):
        result = None
        servicename = self.config['limitPEO']
        for each in self.mult_peo[0].peoples:
            if each.name == servicename:
                result = each
                break
        return result

    @property
    def administrator(self):
        if 'administrator' not in self.config:
            self.config['administrator'] = set()
            self.save()
        return self.config['administrator']

    def load_projects(self):
        self.projects = dict()
        for path in glob.glob(os.path.join(self.projects_path, '*')):
            if os.path.isdir(path):
                str_name = os.path.split(path)[1]
                name = unicode(str_name, 'utf-8')
                tmp_project = services.project.Project(services.project.SimulationProject(unicode(path, 'utf-8'), name),
                                                bidding={'bd': self.bd_repos}, jobdescription={'jd': self.jd_repos}, 
                                                search_engine={'idx': self.search_engine, 'config': self.es_config})
                tmp_project.setup(config={'id':         utils.builtin.hash(self.name+name),
                                          'autosetup':  False,
                                          'autoupdate': False,
                                          'storageCO':  self.config['storageCO'],
                                          'storageJD':  self.config['storageJD']})
                if not tmp_project.config['autosetup'] and not tmp_project.config['autoupdate']:
                    tmp_project._modelname = self.default_model
                self.projects[name] = tmp_project

    def exists_project(self, name):
        return name in self.projects

    def add_project(self, name, adminID, autosetup=False, autoupdate=False):
        result = False
        max_project_nums = self.config['max_project_nums'] if 'max_project_nums'\
                            in self.config else self.max_project_nums
        if self.check_admin(adminID) and len(self.projects) < max_project_nums:
            result = self._add_project(name, autosetup=autosetup, autoupdate=autoupdate)
        return result

    def _add_project(self, name, autosetup=False, autoupdate=False):
        result = False
        if len(name)>0 and name not in self.projects:
            path = os.path.join(self.projects_path, name)
            tmp_project = services.project.Project(services.project.SimulationProject(path, name),
                                                bidding={'bd': self.bd_repos}, jobdescription={'jd': self.jd_repos}, 
                                                search_engine={'idx': self.search_engine, 'config': self.es_config})
            tmp_project.setup(config={'id':           utils.builtin.hash(self.name+name),
                                      'autosetup':    autosetup,
                                      'autoupdate':   autoupdate,
                                      'storageCO':    self.config['storageCO'],
                                      'storageJD':    self.config['storageJD']})
            tmp_project._modelname = self.default_model
            self.projects[name] = tmp_project
            result = True
        return result

    def join(self, inviter_id, invited_id, committer, creator=False):
        result = False
        if creator is True or self.check_admin(inviter_id):
            bsobj = core.basedata.DataObject(metadata={'id': invited_id}, data=None)
            result = self.accounts.add(bsobj, committer=committer)
        if creator is True and result is True:
            self.add_admin(inviter_id, invited_id, creator=creator)
        return result

    def quit(self, inviter_id, invited_id, committer):
        result = False
        if self.accounts.exists(invited_id):
            if self.check_admin(inviter_id) or inviter_id == invited_id:
                if len(self.accounts.ids) > 1:
                    result = self.accounts.remove(invited_id, committer=committer)
            if result is True:
                if member.check_admin(invited_id) is True:
                    result = self.delete_admin(self.id, invited_id)
        return result

    def cv_add(self, cvobj, committer=None, unique=True, do_commit=True):
        result = self.curriculumvitae.add(cvobj, committer, unique=unique,
                                                               do_commit=do_commit)
        if result:
            peopmeta = extractor.information_explorer.catch_peopinfo(cvobj.metadata)
            peopobj = core.basedata.DataObject(data='', metadata=peopmeta)
            name = core.outputstorage.ConvertName(peopobj.name)
            if unique is True and self.peo_unique(peopobj) is False:
                result = self.peo_modify(peopobj, committer, unique=unique, do_commit=do_commit)
            else:
                result = self.peo_add(peopobj, committer, unique=unique, do_commit=do_commit)
        if result:
            for meta in extractor.information_explorer.catch_coinfo(cvobj.metadata):
                coobj = core.basedata.DataObject(data='', metadata=meta)
                name = core.outputstorage.ConvertName(coobj.name)
                if unique is True and self.co_unique(coobj) is False:
                    co_result = self.co_modify(coobj, committer, unique=unique, do_commit=do_commit)
                else:
                    co_result = self.co_add(coobj, committer, unique=unique, do_commit=do_commit)
                if result:
                    result = co_result
        return result

    def cv_add_eng(self, id, cvobj, committer):
        yaml_data = self.curriculumvitae.getyaml(id)
        result = self.curriculumvitae.add_md(cvobj, committer)
        yaml_data['enversion'] = cvobj.ID.md
        self.curriculumvitae.modify(id+'.yaml', utils.builtin.dump_yaml(yaml_data), committer=committer)
        return result

    def cv_numbers(self):
        return self.curriculumvitae.NUMS

    def cv_updateyaml(self, id, key, value, username):
        result = None
        if key in dict(self.curriculumvitae.YAML_TEMPLATE):
            try:
                result = self.curriculumvitae.updateinfo(id, key, value, username)
            except AssertionError:
                pass
        return result

    def cv_projects(self, id):
        return [p.name for p in self.projects.values() if p.exists(id)]

    def peo_getyaml(self, id):
        yaml = self.people.getyaml(id)
        try:
            for cv_id in yaml['cv']:
                if not self.curriculumvitae.exists(cv_id):
                    yaml['cv'].remove(cv_id)
        except TypeError:
            pass
        return yaml

    def peo_getinfo(self, id):
        info = self.people.getyaml(id)
        try:
            for id in info['cv']:
                if self.curriculumvitae.exists(id):
                    yield self.curriculumvitae.getinfo(id)
        except TypeError:
            pass

    def peo_getmd(self, id):
        info = self.people.getyaml(id)
        try:
            for id in info['cv']:
                if self.curriculumvitae.exists(id):
                    yield self.curriculumvitae.getmd(id)
        except TypeError:
            pass

    def peo_updateyaml(self, id, key, value, username):
        result = None
        try:
            result = self.people.updateinfo(id, key, value, username)
        except AssertionError:
            pass
        return result

    def peo_deleteyaml(self, id, key, value, username, date):
        return self.people.deleteinfo(id, key, value, username, date)

    def company_add(self, coobj, committer=None, unique=True, do_commit=True):
        result = self.company.add(coobj, committer, unique=unique, do_commit=do_commit)
        return result

    def getproject(self, projectname):
        return self.projects[projectname]

    def getnums(self):
        result = dict()
        result['total'] = 0
        numbers = self.cv_numbers()
        result[self.name] = numbers
        result['total'] += numbers
        return result

    def backup(self, path):
        member_path = os.path.join(path, self.name)
        projects_path = os.path.join(member_path, 'projects')
        accounts_path = os.path.join(member_path, 'accounts')
        companies_path = os.path.join(member_path, 'companies')
        jobdescriptions_path = os.path.join(member_path, 'jobdescriptions')
        curriculumvitaes_path = os.path.join(member_path, 'curriculumvitaes')
        utils.builtin.assure_path_exists(member_path)
        utils.builtin.assure_path_exists(projects_path)
        utils.builtin.assure_path_exists(accounts_path)
        utils.builtin.assure_path_exists(companies_path)
        utils.builtin.assure_path_exists(jobdescriptions_path)
        utils.builtin.assure_path_exists(curriculumvitaes_path)
        for name in self.projects:
            project = self.projects[name]
            project.backup(projects_path)
        self.accounts.backup(accounts_path)
        self.curriculumvitae.backup(curriculumvitaes_path)


class DefaultMember(Member):

    def load_projects(self):
        super(DefaultMember, self).load_projects()
        if self.default_model not in self.projects:
            super(DefaultMember, self)._add_project(self.default_model)
        self.projects[self.default_model]._modelname = self.default_model

    def use(self, id):
        return self

    def getproject(self, projectname=None):
        return self.projects[self.default_model]

    def add_admin(self, **kwargs):
        return False

    def join(self, **kwargs):
        return False

    def add_project(self, **kwargs):
        return False

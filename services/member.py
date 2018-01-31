import os
import glob
import functools

import core.basedata
import utils.builtin
import services.secret
import services.company
import services.project
import services.matching
import services.curriculumvitae
import services.simulationcv
import services.simulationco
import services.simulationacc
import services.simulationpeo
import services.base.kv_storage
import services.base.name_storage
import services.operator.search
import services.operator.checker
import services.operator.combine
import services.operator.multiple

import sources.industry_id
import extractor.information_explorer


class SimulationMember(services.base.kv_storage.KeyValueStorage):

    YAML_TEMPLATE = (
        ('id',                  str),
        ('name',                str),
        ('model',               functools.partial(str, object='default')),
        ('administrator',       list),
    )

    def add(self, bsobj, *args, **kwargs):
        if not isinstance(bsobj, core.basedata.DataObject):
            bsobj.append_id(utils.builtin.hash(bsobj.ID))
        return super(SimulationMember, self).add(bsobj, *args, **kwargs)


class CommonMember(services.operator.combine.Combine):

    PEO_PATH = 'people'
    CO_PATH = 'companies'
    FIRM_PATH = 'firms'

    commitinfo = 'Member'

    def __init__(self, data_service, **kwargs):
        """"""
        super(CommonMember, self).__init__(data_service, **kwargs)
        assert 'people' in kwargs
        assert 'company' in kwargs
        assert 'search_engine' in kwargs
        self.mult_peo = kwargs['people']['peo']
        self.search_engine = kwargs['search_engine']['idx']
        self.es_config = kwargs['search_engine']['config']
        self.config_service = self.data_service
        self.config = dict()

    def use(self, id):
        pass

    def get_admins(self):
        return self.administrator

    def check_admin(self, id):
        return id in self.administrator

    def add_admin(self, inviter_id, invited_id, creator=False):
        result = False
        if creator is True or (self.check_admin(inviter_id) and
                               self.check_admin(invited_id) is False):
            self.administrator.add(invited_id)
            self.config_service.modify(core.basedata.DataObject(metadata=self.config, data=None))
            result = True
        return result

    def delete_admin(self, inviter_id, invited_id):
        result = False
        if len(self.administrator) > 1:
            if self.check_admin(inviter_id):
                if self.check_admin(invited_id):
                    self.administrator.remove(invited_id)
                    self.config_service.modify(core.basedata.DataObject(metadata=self.config, data=None))
                    result = True
        return result

    def setup(self, info):
        try:
            bsobj = core.basedata.DataObject(metadata=info, data=None)
            result = self.config_service.modify(bsobj, committer=self.commitinfo, do_commit=True)
        except AssertionError:
            bsobj = core.basedata.DataObjectWithoutId(metadata=info, data=None)
            result = self.config_service.add(bsobj, committer=self.commitinfo, do_commit=True)
        if result:
            self.config = self.config_service.getyaml(bsobj.ID)
        self.name = self.config['name']
        self.path = os.path.join(self.config_service.path.replace('config/', ''), self.name)
        self.co_path = os.path.join(self.path, self.CO_PATH)
        self.peo_path = os.path.join(self.path, self.PEO_PATH)
        self.firm_path = os.path.join(self.path, self.FIRM_PATH)
        self.people = services.operator.checker.Filter(
                data_service=services.operator.split.SplitData(
                    data_service=services.operator.multiple.Multiple(self.mult_peo),
                    operator_service=services.simulationpeo.SimulationPEO(self.peo_path, self.name)),
                operator_service=services.base.name_storage.NameStorage(self.peo_path, self.name))
        return result

    @property
    def id(self):
        return self.config['id']

    @property
    def modelname(self):
        return self.config['model']

    @property
    def administrator(self):
        if 'administrator' not in self.config:
            self.config['administrator'] = set()
            self.config_service.modify(core.basedata.DataObject(metadata=self.config, data=None))
        return self.config['administrator']

    def peo_getyaml(self, id):
        yaml = self.people.getyaml(id)
        return yaml

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

    def getnums(self):
        result = dict()
        result['total'] = 0
        return result

    def backup(self, path):
        member_path = os.path.join(path, self.name)
        firms_path = os.path.join(member_path, self.FIRM_PATH)
        people_path = os.path.join(member_path, self.PEO_PATH)
        companies_path = os.path.join(member_path, self.CO_PATH)
        utils.builtin.assure_path_exists(firms_path)
        utils.builtin.assure_path_exists(member_path)
        utils.builtin.assure_path_exists(people_path)
        utils.builtin.assure_path_exists(companies_path)
        self.people.backup(firms_path)
        self.people.backup(people_path)
        self.company.backup(companies_path)


class DefaultMember(CommonMember):

    JD_PATH = 'jobdescriptions'
    CV_PATH = 'curriculumvitaes'

    default_model = 'default'

    def __init__(self, data_service, **kwargs):
        """"""
        super(DefaultMember, self).__init__(data_service, **kwargs)
        assert 'matching' in kwargs
        assert 'jobdescription' in kwargs
        assert 'curriculumvitae' in kwargs
        self.cv_repo = kwargs['curriculumvitae']['cvrepo']
        self.co_repo = kwargs['company']['corepo']
        self.co_storage = kwargs['company']['costorage']
        self.cv_storage = kwargs['curriculumvitae']['cvstorage']
        self.jd_blocks = kwargs['jobdescription']['jd']

    def __getattr__(self, attr):
        method = super(DefaultMember, self).__getattr__(attr)
        return functools.partial(self.set_doctype, doctype=self.id, method=method, attr=attr)

    def set_doctype(self, *args, **kwargs):
        attr = kwargs.pop('attr')
        doctype = kwargs.pop('doctype')
        method = kwargs.pop('method')
        if attr.endswith('_search'):
            if attr.startswith('co'):
                kwargs['doctype'] = None
            else:
                kwargs['doctype'] = [doctype]
        else:
            for key in ('_indexadd', '_add', '_modify', '_kick'):
                if attr.endswith(key):
                    kwargs['doctype'] = doctype
                    break
        return method(*args, **kwargs)

    def idx_setup(self):
        self.jobdescription.setup(self.search_engine, self.es_config['JD_MEM'])
        self.curriculumvitae.services[0].data_service.setup(self.search_engine, self.es_config['CV_MEM'])

    def idx_updatesvc(self):
        self.jobdescription.updatesvc(self.es_config['JD_MEM'], self.id, numbers=1000)
        self.curriculumvitae.services[0].updatesvc(self.es_config['CV_MEM'], self.id, numbers=1000)

    def use(self, id):
        return self

    def setup(self, config=None, committer=None):
        result = super(DefaultMember, self).setup(config)
        self.cv_path = os.path.join(self.path, self.CV_PATH)
        self.jd_path = os.path.join(self.path, self.JD_PATH)
        self.curriculumvitae = services.operator.multiple.Multiple(
                [services.matching.Similarity(
                    data_service=services.curriculumvitae.SearchIndex(services.operator.checker.Filter(
                            data_service=services.operator.split.SplitData(
                                data_service=self.cv_repo,
                                operator_service=services.simulationcv.SimulationCV(self.cv_path, self.name)),
                            operator_service=services.simulationcv.SelectionCV(self.cv_path, self.name))),
                    operator_service=self.matching),
                services.operator.split.SplitData(
                            data_service=services.secret.Private(
                                data_service=services.operator.multiple.Multiple(self.cv_storage),
                                operator_service=services.simulationcv.SelectionCV(self.cv_path, self.name)),
                            operator_service=services.simulationcv.SimulationCV(self.cv_path, self.name)),
                ])
        self.company = services.operator.multiple.Multiple(
                [services.company.SearchIndex(services.operator.checker.Filter(
                    data_service=services.operator.split.SplitData(
                        data_service=self.co_repo,
                        operator_service=services.simulationco.SimulationCO(self.firm_path, self.name)),
                    operator_service=services.simulationco.SelectionCO(self.firm_path, self.name))),
                services.operator.split.SplitData(
                    data_service=self.co_storage,
                    operator_service=services.simulationco.SimulationCO(self.firm_path, self.name)),
                ])
        self.jobdescription = services.jobdescription.SearchIndex(services.secret.Secret(
                services.operator.multiple.Multiple(self.jd_blocks)))
        self.idx_setup()
        self.mch_setup()
        return result

    def mch_setup(self):
        self.curriculumvitae.services[0].setup(self.modelname, [self.id])

    def cv_add(self, cvobj, committer=None, unique=True, do_commit=True, **kwargs):
        kwargs['doctype'] = self.id
        kwargs['simname'] = self.id
        result = self.curriculumvitae.add(cvobj, committer, unique=unique,
                                          do_commit=do_commit, **kwargs)
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

    def peo_getyaml(self, id):
        yaml = super(DefaultMember, self).peo_getyaml(id)
        try:
            for cv_id in yaml['cv']:
                if not self.curriculumvitae.exists(cv_id):
                    yaml['cv'].remove(cv_id)
        except TypeError:
            pass
        return yaml

    def peo_getinfo(self, id):
        info = super(DefaultMember, self).peo_getyaml(id)
        try:
            for id in info['cv']:
                if self.curriculumvitae.exists(id):
                    yield self.curriculumvitae.getinfo(id)
        except TypeError:
            pass

    def peo_getmd(self, id):
        info = super(DefaultMember, self).peo_getyaml(id)
        try:
            for id in info['cv']:
                if self.curriculumvitae.exists(id):
                    yield self.curriculumvitae.getmd(id)
        except TypeError:
            pass

    def getnums(self):
        result = super(DefaultMember, self).getnums()
        numbers = self.cv_numbers()
        result[self.name] = numbers
        result['total'] += numbers
        return result

    def backup(self, path):
        super(DefaultMember, self).backup(path)
        member_path = os.path.join(path, self.name)
        curriculumvitaes_path = os.path.join(member_path, self.CV_PATH)
        utils.builtin.assure_path_exists(curriculumvitaes_path)
        self.curriculumvitae.backup(curriculumvitaes_path)


class Member(DefaultMember):

    PRJ_PATH = 'projects'
    ACC_PATH = 'accounts'

    max_project_nums = 3

    def __init__(self, data_service, **kwargs):
        """"""
        super(Member, self).__init__(data_service, **kwargs)
        assert 'bidding' in kwargs
        self.bd_blocks = kwargs['bidding']['bd']

    def __getattr__(self, attr):
        for key in ['bd', 'jd']:
            if attr.startswith(key+'_'):
                return functools.partial(self.call_project, attr=attr)
        return super(Member, self).__getattr__(attr)

    def call_project(self, *args, **kwargs):
        attr = kwargs.pop('attr')
        try:
            project_name = kwargs.pop('project')
        except KeyError:
            raise KeyError('Missing project')
        try:
            project = self.projects[project_name]
        except KeyError:
            raise ValueError('Invalid project name: %s' %(project_name))
        return self.set_doctype(*args, attr=attr, doctype=project.id, method=getattr(project, attr), **kwargs)

    def setup(self, config=None, committer=None):
        result = super(Member, self).setup(config)
        self.projects_path = os.path.join(self.path, self.PRJ_PATH)
        self.accounts_path = os.path.join(self.path, self.ACC_PATH)
        self.active_projects = services.base.name_storage.NameStorage(os.path.join(self.path, 'projects'), 'prjlist')
        self.project_details = services.project.SimulationProject(unicode(os.path.join(self.path, 'projects', 'config'), 'utf-8'), 'prjconfig')
        if not os.path.exists(self.projects_path):
            os.makedirs(self.projects_path)
        self.load_projects()
        self.accounts = services.operator.checker.Checker(
                data_service=services.simulationacc.SimulationACC(self.accounts_path, self.name),
                operator_service=services.simulationacc.SelectionACC(self.accounts_path, self.name))
        return result

    def use(self, id):
        result = None
        if self.accounts.exists(id):
            result = self
        return result

    def load_projects(self):
        self.projects = dict()
        for project_id in self.active_projects.ids:
            project_info = self.project_details.getyaml(project_id)
            project_path = os.path.join(self.path, 'projects', project_info['name'])
            if os.path.isdir(project_path):
                str_name = os.path.split(project_path)[1]
                name = unicode(str_name, 'utf-8')
                tmp_project = services.project.Project(self.project_details,
                                                matching={'mch': self.matching},
                                                bidding={'bd': self.bd_blocks},
                                                jobdescription={'jd': self.jd_blocks},
                                                search_engine={'idx': self.search_engine,
                                                               'config': self.es_config})
                tmp_project.setup(info={'id':      project_id,
                                        'name':       project_info['name'],
                                        'autosetup':  False,
                                        'autoupdate': False})
                if not tmp_project.config['autosetup'] and not tmp_project.config['autoupdate']:
                    tmp_project._modelname = self.default_model
                self.projects[name] = tmp_project

    def idx_updatesvc(self):
        self.curriculumvitae.services[0].updatesvc(self.es_config['CV_MEM'], self.id, numbers=1000)
        for prjname, prj in self.projects.items():
            prj.idx_updatesvc()

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
            tmp_project = services.project.Project(self.project_details,
                                                   matching={'mch': self.matching},
                                                   bidding={'bd': self.bd_blocks},
                                                   jobdescription={'jd': self.jd_blocks},
                                                   search_engine={'idx': self.search_engine,
                                                                  'config': self.es_config})
            tmp_project.setup(info={'name':         name,
                                    'autosetup':    autosetup,
                                    'autoupdate':   autoupdate})
            self.active_projects.add(core.basedata.DataObject(metadata=tmp_project.config, data=''))
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
                if self.check_admin(invited_id) is True:
                    result = self.delete_admin(inviter_id, invited_id)
        return result

    def cv_projects(self, id):
        return [p.name for p in self.projects.values() if p.exists(id)]

    def getproject(self, projectname):
        return self.projects[projectname]

    def backup(self, path):
        super(Member, self).backup(path)
        member_path = os.path.join(path, self.name)
        projects_path = os.path.join(member_path, self.PRJ_PATH)
        accounts_path = os.path.join(member_path, self.ACC_PATH)
        utils.builtin.assure_path_exists(projects_path)
        utils.builtin.assure_path_exists(accounts_path)
        for name in self.projects:
            project = self.projects[name]
            project.backup(projects_path)
        self.accounts.backup(accounts_path)


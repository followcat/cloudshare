import os
import glob

import core.basedata
import utils.builtin
import services.company
import services.project
import services.secret
import services.simulationcv
import services.simulationco
import services.simulationacc
import services.simulationpeo
import services.multipeople
import services.base.kv_storage
import services.operator.facade
import services.operator.checker
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
        return self.saveinfo(self.config_file, info, commitinfo, committer=commitinfo, do_commit=True)


class Member(services.operator.facade.Facade):

    PEO_PATH = 'people'
    PRJ_PATH = 'projects'
    ACC_PATH = 'accounts'
    CO_PATH = 'companies'
    JD_PATH = 'jobdescriptions'
    CV_PATH = 'curriculumvitaes'

    default_model = 'default'
    max_project_nums = 3

    def __init__(self, data_service, acc_repos, co_repos, cv_repos, jd_repos,
                 mult_peo):
        super(Member, self).__init__(data_service)
        self.name = data_service.name
        self.path = data_service.path
        self.config_file = data_service.config_file
        self.cv_path = os.path.join(self.path, self.CV_PATH)
        self.jd_path = os.path.join(self.path, self.JD_PATH)
        self.co_path = os.path.join(self.path, self.CO_PATH)
        self.peo_path = os.path.join(self.path, self.PEO_PATH)
        self.co_repos = co_repos
        self.cv_repos = cv_repos
        self.jd_repos = jd_repos
        self.mult_peo = mult_peo
        self.acc_repos = acc_repos
        self.projects_path = os.path.join(self.path, self.PRJ_PATH)
        self.accounts_path = os.path.join(self.path, self.ACC_PATH)
        self.company = services.operator.checker.Filter(
                data_service=services.operator.split.SplitData(
                    data_service=services.operator.multiple.Multiple(co_repos),
                    operator_service=services.simulationco.SimulationCO(self.co_path, self.name)),
                operator_service=services.simulationco.SelectionCO(self.co_path, self.name))
        self.curriculumvitae = services.secret.Private(
                data_service=services.operator.split.SplitData(
                        data_service=services.operator.multiple.Multiple(cv_repos),
                        operator_service=services.simulationcv.SimulationCV(self.cv_path, self.name)),
                operator_service=services.simulationcv.SelectionCV(self.cv_path, self.name)
                )
        self.people = services.operator.checker.Filter(
                data_service=services.operator.split.SplitData(
                    data_service=services.multipeople.MultiPeople(mult_peo),
                    operator_service=services.simulationpeo.SimulationPEO(self.peo_path, self.name)),
                operator_service=services.base.name_storage.NameStorage(self.peo_path, self.name))
        self.jobdescriptions = services.operator.checker.Filter(
                data_service=services.operator.multiple.Multiple(jd_repos),
                operator_service=services.base.name_storage.NameStorage(self.jd_path, self.name))
        self.config_service = self.data_service
        self.config = dict()
        try:
            self.load()
        except IOError:
            pass
        if not os.path.exists(self.projects_path):
            os.makedirs(self.projects_path)

    def load(self):
        config = self.config_service.getyaml(self.config_file)
        if config:
            self.config.update(config)

    def save(self):
        return self.config_service.saveinfo(self.config_file, self.config, committer=None, message="Update config file.")

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
                data_service=services.operator.split.SplitData(
                    data_service=services.operator.multiple.Multiple(self.acc_repos),
                    operator_service=services.simulationacc.SimulationACC(self.accounts_path, self.name)),
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
                                                       self.co_repos, [self.jobdescriptions])
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
                                                   self.co_repos, [self.jobdescriptions])
            tmp_project.setup(config={'id':           utils.builtin.hash(self.name+name),
                                      'autosetup':    autosetup,
                                      'autoupdate':   autoupdate,
                                      'storageCO':    self.config['storageCO'],
                                      'storageJD':    self.config['storageJD']})
            tmp_project._modelname = self.default_model
            self.projects[name] = tmp_project
            result = True
        return result

    def add_account(self, inviter_id, invited_id, committer, creator=False):
        result = False
        if creator is True or self.check_admin(inviter_id):
            bsobj = core.basedata.DataObject(metadata={'id': invited_id}, data=None)
            result = self.accounts.add(bsobj, committer=committer)
        if creator is True and result is True:
            self.add_admin(inviter_id, invited_id, creator=creator)
        return result

    def rm_account(self, inviter_id, invited_id, committer):
        result = False
        if self.accounts.exists(invited_id):
            if self.check_admin(inviter_id) or inviter_id == invited_id:
                if len(self.accounts.ids) > 1:
                    result = self.accounts.remove(invited_id, committer=committer)
        return result

    def cv_add(self, cvobj, committer=None, unique=True, do_commit=True):
        result = {
            'repo_cv_result' : False,
            'repo_peo_result' : False,
            'member_cv_result' : False,
            'member_peo_result' : False
        }
        result['member_cv_result'] = self.curriculumvitae.add(cvobj, committer, unique=unique,
                                                               do_commit=do_commit)
        if result['member_cv_result']:
            peopmeta = extractor.information_explorer.catch_peopinfo(cvobj.metadata)
            peopobj = core.basedata.DataObject(data='', metadata=peopmeta)
            peoresult = self.peo_add(peopobj, committer, unique=unique, do_commit=do_commit)
            result.update(peoresult)
        return result

    def cv_add_eng(self, id, cvobj, committer):
        yaml_data = self.curriculumvitae.getyaml(id)
        result = self.curriculumvitae.add_md(cvobj, committer)
        yaml_data['enversion'] = cvobj.ID.md
        self.curriculumvitae.modify(id+'.yaml', utils.builtin.dump_yaml(yaml_data), committer=committer)
        return result

    def cv_yamls(self):
        return self.curriculumvitae.yamls()

    def cv_names(self):
        return self.curriculumvitae.names()

    def cv_datas(self):
        return self.curriculumvitae.datas()

    def cv_gethtml(self, id):
        return self.curriculumvitae.gethtml(id)

    def cv_getmd(self, id):
        return self.curriculumvitae.getmd(id)

    def cv_getmd_en(self, id):
        return self.curriculumvitae.getmd_en(id)

    def cv_numbers(self):
        return self.curriculumvitae.NUMS

    def cv_ids(self):
        return self.curriculumvitae.ids

    def cv_timerange(self, start_y, start_m, start_d, end_y, end_m, end_d):
        return self.curriculumvitae.timerange(start_y, start_m, start_d,
                                              end_y, end_m, end_d)

    def cv_history(self, author=None, entries=10, skip=0):
        return self.curriculumvitae.history(author, entries, skip)

    def cv_getyaml(self, id):
        return self.curriculumvitae.getyaml(id)

    def cv_updateyaml(self, id, key, value, username):
        result = None
        if key in dict(self.curriculumvitae.YAML_TEMPLATE):
            try:
                result = self.curriculumvitae.updateinfo(id, key, value, username)
            except AssertionError:
                pass
        return result

    def cv_projects(self, id):
        return [p.name for p in self.projects.values()]

    def peo_add(self, peopobj, committer=None, unique=True, do_commit=True):
        result = {
            'repo_peo_result' : False,
            'project_peo_result' :False,
        }
        result['project_peo_result'] = self.people.add(peopobj, committer,
                                                       unique=unique, do_commit=do_commit)
        return result

    def peo_getinfo(self, id):
        info = self.people.getyaml(id)
        for id in info['cv']:
            if self.curriculumvitae.exists(id):
                yield self.curriculumvitae.getinfo(id)

    def peo_getmd(self, id):
        info = self.people.getyaml(id)
        for id in info['cv']:
            if self.curriculumvitae.exists(id):
                yield self.curriculumvitae.getmd(id)

    def peo_getyaml(self, id):
        return self.people.getyaml(id)

    def peo_updateyaml(self, id, key, value, username):
        result = None
        try:
            result = self.people.updateinfo(id, key, value, username)
        except AssertionError:
            pass
        return result

    def peo_deleteyaml(self, id, key, value, username, date):
        return self.people.deleteinfo(id, key, value, username, date)

    def jd_add(self, jdobj, committer=None, unique=True, do_commit=True):
        result = self.jobdescriptions.add(jdobj, committer,
                                          unique=unique, do_commit=do_commit)
        return result

    def company_add(self, coobj, committer=None, unique=True, do_commit=True):
        result = self.company.add(coobj, committer, unique=unique, do_commit=do_commit)
        return result

    def company_add_excel(self, items, committer=None):
        results = dict()
        member_result = set()
        for item in items:
            if item[0] == 'projectadd':
                yamlname = core.outputstorage.ConvertName(item[1]).yaml
                coobj = core.basedata.DataObject(*item[2][:2])
                member_result.add(self.company.ids_file)
                member_result.add(os.path.join(self.company.YAML_DIR, yamlname))
                result = self.company.add(coobj, committer=item[2][-1], do_commit=False)
                results[item[1]] = result
        self.company.interface.do_commit(list(member_result), committer=committer)
        return results

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
        self.jobdescriptions.backup(jobdescriptions_path)
        self.curriculumvitae.backup(curriculumvitaes_path)


class DefaultMember(Member):

    default_name = 'default'

    def load_projects(self):
        super(DefaultMember, self).load_projects()
        if self.default_name not in self.projects:
            super(DefaultMember, self)._add_project(self.default_name)
        self.projects[self.default_name]._modelname = self.default_model

    def use(self, id):
        return self

    def getproject(self, projectname=None):
        return self.projects[self.default_name]

    def add_admin(self, **kwargs):
        return False

    def add_account(self, **kwargs):
        return False

    def add_project(self, **kwargs):
        return False

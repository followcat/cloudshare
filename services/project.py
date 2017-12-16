import os

import utils.builtin
import core.outputstorage
import sources.industry_id
import services.base.service
import services.base.kv_storage
import services.operator.split
import services.operator.facade
import services.operator.checker
import services.operator.multiple
import services.simulationco
import services.simulationcustomer


class SimulationProject(services.base.kv_storage.KeyValueStorage):

    commitinfo = 'Project'
    config_file = 'config.yaml'

    YAML_TEMPLATE = (
        ('id',                  str),
        ('autosetup',           bool),
        ('autoupdate',          bool),
        ('storageCO',           str),
        ('storageJD',           str),
    )

    def setup(self, info):
        return self.saveinfo(self.config_file, info, commitinfo, committer=commitinfo, do_commit=True)


class Project(services.operator.facade.Facade):

    CO_PATH = 'CO'
    JD_PATH = 'JD'

    def __init__(self, data_service, co_repos, jd_repos):
        super(Project, self).__init__(data_service)
        self.name = data_service.name
        self.path = data_service.path
        self.config_file = data_service.config_file
        self.co_repos = co_repos
        self.jd_repos = jd_repos
        copath = os.path.join(self.path, self.CO_PATH)
        jdpath = os.path.join(self.path, self.JD_PATH)

        self.company = services.operator.checker.Filter(
                data_service=services.operator.split.SplitData(
                    data_service=services.operator.multiple.Multiple(co_repos),
                    operator_service=services.simulationco.SimulationCO(copath, self.name)),
                operator_service=services.simulationco.SelectionCO(copath, self.name))
        self.customer = services.operator.checker.Selector(
                data_service=self.company,
                operator_service=services.simulationcustomer.SelectionCustomer(copath, self.name))
        self.jobdescription = services.operator.checker.Filter(
                data_service=services.operator.multiple.Multiple(jd_repos),
                operator_service=services.base.name_storage.NameStorage(jdpath, self.name))
        self.config_service = self.data_service
        self.config = dict()
        try:
            self.load()
        except IOError:
            pass

    def load(self):
        self.config = self.config_service.getyaml(self.config_file)
        self.config['name'] = self.name
        if 'id' not in self.config:
            self.config['id'] = utils.builtin.genuuid()
        if 'model' not in self.config:
            self.config['model'] = 'default'

    def save(self):
        return self.config_service.saveinfo(self.config_file, self.config, committer=None, message="Update config file.")

    def setup(self, committer=None, config=None):
        self.setconfig(config)

    def setconfig(self, config=None):
        if config is None:
            config = {}
        modified = False
        for key in config:
            if key not in self.config or self.config[key] != config[key]:
                self.config[key] = config[key]
                modified = True
        if modified:
            self.save()

    @property
    def storageCO(self):
        result = None
        servicename = self.config['storageCO']
        for corepo in self.co_repos:
            if isinstance(corepo, services.simulationco.SimulationCO):
                for each in corepo.storages:
                    if each.name == servicename:
                        result = each
                        break
            elif corepo.name == servicename:
                result = corepo
            if result is not None:
                break
        return result

    @property
    def storageJD(self):
        result = None
        servicename = self.config['storageJD']
        for jdrepo in self.jd_repos:
            if isinstance(jdrepo, services.simulationjd.SimulationJD):
                for each in jdrepo.storages:
                    if each.name == servicename:
                        result = each
                        break
            elif jdrepo.name == servicename:
                result = jdrepo
            if result is not None:
                break
        return result

    @property
    def modelname(self):
        return self.config['model']

    @property
    def id(self):
        return self.config['id']

    def company_update_info(self, id, info, committer):
        result = False
        if self.company.exists(id):
            repo_result = self.storageCO.saveinfo(id, info, "Update %s information."%id,
                                                  committer)
            project_result = self.company.update_info(id, info, committer)
            result = repo_result or project_result
        return result

    def company_compare_excel(self, stream, committer):
        outputs = list()
        outputs.extend(self.storageCO.compare_excel(stream, committer))
        outputs.extend(self.company.compare_excel(stream, committer))
        return outputs

    def company_add_excel(self, items, committer):
        results = dict()
        repo_result = set()
        project_result = set()
        for item in items:
            yamlname = core.outputstorage.ConvertName(item[1]).yaml
            result = None
            success = False
            if item[0] == 'companyadd':
                baseobj = core.basedata.DataObject(*item[2][:2])
                try:
                    result = self.storageCO.add(baseobj, committer=item[2][-1], do_commit=False)
                    success = True
                except Exception:
                    success = False
                if success is True:
                    repo_result.add(yamlname)
            elif item[0] == 'projectadd':
                baseobj = core.basedata.DataObject(*item[2][:2])
                try:
                    result = self.company.add(baseobj, committer=item[2][-1], do_commit=False)
                    success = True
                except Exception:
                    success = False
                if success is True:
                    project_result.add(self.company.ids_file)
                    project_result.add(os.path.join(self.company.YAML_DIR, yamlname))
            elif item[0] == 'listadd':
                try:
                    result = self.company.updateinfo(*item[2], do_commit=False)
                    success = True
                except Exception:
                    success = False
                if success is True:
                    project_result.add(os.path.join(self.company.YAML_DIR, yamlname))
            else:
                success = False
            results[item[1]] = {'data': item, 'success': success, 'result': result}
        self.storageCO.interface.do_commit(list(repo_result), committer=committer)
        self.company.interface.do_commit(list(project_result), committer=committer)
        return results

    def company_add(self, coobj, committer=None, unique=True, yamlfile=True, mdfile=False):
        result = {
            'repo_result' : False,
            'project_result' : False
        }
        result['repo_result'] = self.storageCO.add(coobj, committer, unique, yamlfile, mdfile)
        if result['repo_result']:
            result['project_result'] = self.company.add(coobj, committer, unique,
                                                        yamlfile, mdfile)
        return result

    def company_get(self, name):
        return self.company.getyaml(name)

    def company_names(self):
        return self.company.ids

    def company_customers(self):
        return self.customer.ids

    def addcustomer(self, coobj, user=None, do_commit=True):
        return self.customer.add(coobj, committer=user, do_commit=do_commit)

    def deletecustomer(self, coobj, user=None, do_commit=True):
        return self.customer.remove(coobj, committer=user, do_commit=do_commit)

    def jd_get(self, id):
        return self.jobdescription.getyaml(id)

    def jd_add(self, jdobj, committer=None, unique=True, do_commit=True):
        result = {
            'repo_result' : False,
            'project_result' : False
        }
        if jdobj.metadata['company'] in self.company.customers:
            result['repo_result'] = self.storageJD.add(jdobj, committer,
                                                       unique=unique, do_commit=do_commit)
            if result['repo_result']:
                result['project_result'] = self.jobdescription.add(jdobj, committer,
                                                                unique=unique,
                                                                do_commit=do_commit)
        return result

    def jd_modify(self, id, description, status, commentary, followup, committer):
        result = False
        if self.jobdescription.exists(id):
            result = self.storageJD.modify(id, description, status,
                                           commentary, followup, committer)
        return result

    def jd_datas(self):
        return self.jobdescription.datas()

    def backup(self, path):
        backup_path = os.path.join(path, self.name)
        project_path = os.path.join(backup_path, 'project')
        jd_path = os.path.join(backup_path, 'jobdescription')
        co_path = os.path.join(backup_path, 'company')
        utils.builtin.assure_path_exists(project_path)
        utils.builtin.assure_path_exists(jd_path)
        utils.builtin.assure_path_exists(co_path)
        self.config_service.backup(project_path, bare=True)
        self.jobdescription.backup(jd_path, bare=True)
        self.company.backup(co_path, bare=True)

import os

import utils.builtin
import core.outputstorage
import sources.industry_id
import services.bidding
import services.jobdescription
import services.base.service
import services.base.kv_storage
import services.operator.split
import services.operator.combine
import services.operator.checker
import services.operator.multiple
import services.simulationbd
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
        info['id'] = self.config_file
        bsobj = core.basedata.DataObject(metadata=info, data=None)
        return self.modify(bsobj, committer=self.commitinfo, do_commit=True)


class Project(services.operator.combine.Combine):

    CO_PATH = 'CO'
    JD_PATH = 'JD'

    def __init__(self, data_service, **kwargs):
        super(Project, self).__init__(data_service, **kwargs)
        assert 'bidding' in kwargs
        assert 'search_engine' in kwargs
        assert 'jobdescription' in kwargs
        self.name = data_service.name
        self.path = data_service.path
        self.config_file = data_service.config_file
        self.bd_repos = kwargs['bidding']['bd']
        self.jd_repos = kwargs['jobdescription']['jd']
        self.search_engine = kwargs['search_engine']['idx']
        self.es_config = kwargs['search_engine']['config']
        copath = os.path.join(self.path, self.CO_PATH)
        jdpath = os.path.join(self.path, self.JD_PATH)

        self.bidding = services.bidding.SearchIndex(services.operator.checker.Filter(
                data_service=services.operator.split.SplitData(
                    data_service=services.operator.multiple.Multiple(self.bd_repos),
                    operator_service=services.simulationbd.SimulationBD(copath, self.name)),
                operator_service=services.simulationbd.SelectionBD(copath, self.name)))
        self.customer = services.operator.checker.Selector(
                data_service=self.bidding,
                operator_service=services.simulationcustomer.SelectionCustomer(copath, self.name))
        self.jobdescription = services.jobdescription.SearchIndex(services.operator.checker.Filter(
                data_service=services.operator.multiple.Multiple(self.jd_repos),
                operator_service=services.base.name_storage.NameStorage(jdpath, self.name)))
        self.config_service = self.data_service
        self.config = dict()
        try:
            self.load()
        except IOError:
            pass
        self.idx_setup()

    def idx_setup(self):
        self.bidding.setup(self.search_engine, self.es_config['CO_MEM'])
        self.jobdescription.setup(self.search_engine, self.es_config['JD_MEM'])

    def idx_updatesvc(self):
        self.bidding.updatesvc(self.es_config['CO_MEM'], self.id, numbers=1000)
        self.jobdescription.updatesvc(self.es_config['JD_MEM'], self.id, numbers=1000)

    def load(self):
        self.config = self.config_service.getyaml(self.config_file)
        self.config['name'] = self.name
        if 'id' not in self.config:
            self.config['id'] = utils.builtin.genuuid()
        if 'model' not in self.config:
            self.config['model'] = 'default'

    def save(self):
        return self.config_service.setup(self.config)

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
        for repo in self.bd_repos:
            if isinstance(repo, services.simulationbd.SimulationBD):
                for each in repo.storages:
                    if each.name == servicename:
                        result = each
                        break
            elif repo.name == servicename:
                result = repo
            if result is not None:
                break
        return result

    @property
    def modelname(self):
        return self.config['model']

    @property
    def id(self):
        return self.config['id']

    def bd_update_info(self, id, info, committer):
        result = False
        if self.bidding.exists(id):
            info['id'] = id
            bsobj = core.basedata.DataObject(metadata=info, data=None)
            repo_result = self.storageCO.modify(bsobj, "Update %s information."%id,
                                                  committer)
            project_result = self.bidding.modify(bsobj, committer)
            result = repo_result or project_result
        return result

    def bd_compare_excel(self, stream, committer):
        outputs = list()
        outputs.extend(self.storageCO.compare_excel(stream, committer))
        outputs.extend(self.bidding.compare_excel(stream, committer))
        return outputs

    def bd_add_excel(self, items, committer):
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
                    result = self.bidding.add(baseobj, committer=item[2][-1], do_commit=False)
                    success = True
                except Exception:
                    success = False
                if success is True:
                    project_result.add(self.bidding.ids_file)
                    project_result.add(os.path.join(self.bidding.YAML_DIR, yamlname))
            elif item[0] == 'listadd':
                try:
                    result = self.bidding.updateinfo(*item[2], do_commit=False)
                    success = True
                except Exception:
                    success = False
                if success is True:
                    project_result.add(os.path.join(self.bidding.YAML_DIR, yamlname))
            else:
                success = False
            results[item[1]] = {'data': item, 'success': success, 'result': result}
        self.storageCO.interface.do_commit(list(repo_result), committer=committer)
        self.bidding.interface.do_commit(list(project_result), committer=committer)
        return results

    def bd_names(self):
        return self.bidding.ids

    def bd_customers(self):
        return self.customer.ids

    def addcustomer(self, coobj, user=None, do_commit=True):
        return self.customer.add(coobj, committer=user, do_commit=do_commit)

    def deletecustomer(self, coobj, user=None, do_commit=True):
        return self.customer.remove(coobj, committer=user, do_commit=do_commit)

    def jd_get(self, id):
        return self.jobdescription.getyaml(id)

    def jd_add(self, jdobj, committer=None, unique=True, do_commit=True):
        result = False
        if jdobj.metadata['company'] in self.bidding.customers:
            result = self.jobdescription.add(jdobj, committer,
                                                       unique=unique, do_commit=do_commit)
        return result

    def jd_modify(self, id, description, status, commentary, followup, committer):
        result = False
        if self.jobdescription.exists(id):
            result = self.jobdescription.modify(id, description, status,
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
        self.bidding.backup(co_path, bare=True)

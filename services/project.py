import os
import functools

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

    YAML_TEMPLATE = (
        ('id',                  str),
        ('name',                str),
        ('model',               functools.partial(str, object='default')),
        ('autosetup',           bool),
        ('autoupdate',          bool),
    )

    def add(self, bsobj, *args, **kwargs):
        if not isinstance(bsobj, core.basedata.DataObject):
            bsobj.append_id(utils.builtin.genuuid())
        return super(SimulationProject, self).add(bsobj, *args, **kwargs)


class Project(services.operator.combine.Combine):

    CO_PATH = 'CO'
    JD_PATH = 'JD'

    commitinfo = 'Project'

    def __init__(self, data_service, **kwargs):
        super(Project, self).__init__(data_service, **kwargs)
        assert 'bidding' in kwargs
        assert 'matching' in kwargs
        assert 'search_engine' in kwargs
        assert 'jobdescription' in kwargs
        self.bd_blocks = kwargs['bidding']['bd']
        self.jd_blocks = kwargs['jobdescription']['jd']
        self.search_engine = kwargs['search_engine']['idx']
        self.es_config = kwargs['search_engine']['config']

        self.config_service = self.data_service
        self.config = dict()

    def idx_setup(self):
        self.bidding.setup(self.search_engine, self.es_config['BD_MEM'])
        self.jobdescription.setup(self.search_engine, self.es_config['JD_MEM'])

    def idx_updatesvc(self):
        self.bidding.updatesvc(self.es_config['BD_MEM'], self.id, numbers=1000)
        self.jobdescription.updatesvc(self.es_config['JD_MEM'], self.id, numbers=1000)

    @property
    def modelname(self):
        return self.config['model']

    @property
    def id(self):
        return self.config['id']

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
        copath = os.path.join(self.path, self.CO_PATH)
        jdpath = os.path.join(self.path, self.JD_PATH)
        self.bidding = services.bidding.SearchIndex(services.operator.checker.Filter(
                data_service=services.operator.split.SplitData(
                    data_service=services.operator.multiple.Multiple(self.bd_blocks),
                    operator_service=services.simulationbd.SimulationBD(copath, self.name)),
                operator_service=services.simulationbd.SelectionBD(copath, self.name)))
        self.customer = services.operator.checker.Selector(
                data_service=self.bidding,
                operator_service=services.simulationcustomer.SelectionCustomer(copath, self.name))
        self.jobdescription = services.jobdescription.SearchIndex(services.operator.checker.Filter(
                data_service=services.operator.multiple.Multiple(self.jd_blocks),
                operator_service=services.base.name_storage.NameStorage(jdpath, self.name)))
        self.idx_setup()
        return result

    def mch_probability_by_id(self, doc, ids, uses=None, top=10000, **kwargs):
        return self.matching.probability_by_id(self.modelname, doc, ids, uses=uses, top=top)

    def mch_probability_by_ids(self, doc, ids, uses=None, top=10000, **kwargs):
        return self.matching.probability_by_ids(self.modelname, doc, ids, uses=uses, top=top)

    def mch_valuable_rate(self, name_list, member, doc, top, **kwargs):
        return self.matching.valuable_rate(name_list, self.modelname, member, doc, top)

    def mch_add_documents(self, names, documents, **kwargs):
        # FIXME: Does not work for member without project (User upload)
        if self.id not in self.matching.sim[self.modelname]:
            self.matching.init_sim(self.modelname, self.id)
        else:
            self.matching.sim[self.modelname][self.id].add_documents(names, documents)
            self.matching.sim[self.modelname][self.id].save()

    def bd_update_info(self, id, info, committer):
        result = False
        if self.bidding.exists(id):
            info['id'] = id
            bsobj = core.basedata.DataObject(metadata=info, data=None)
            result = self.bidding.modify(bsobj, committer)
        return result

    def bd_compare_excel(self, stream, committer):
        outputs = list()
        bd = self.bidding.compare_excel(stream, committer)
        for each in bd:
            print each[0]
        outputs.extend(bd)
        return outputs

    def bd_add_excel(self, items, committer):
        results = dict()
        for item in items:
            yamlname = core.outputstorage.ConvertName(item[1]).yaml
            result = None
            success = False
            if item[0] in ['companyadd', 'projectadd']:
                baseobj = core.basedata.DataObject(*item[2][:2])
                try:
                    result = self.bidding.add(baseobj, committer=item[2][-1])
                    success = True
                except Exception:
                    pass
            elif item[0] == 'listadd':
                try:
                    result = self.bidding.updateinfo(*item[2])
                    success = True
                except Exception:
                    pass
            results[item[1]] = {'data': item, 'success': success, 'result': result}
        return results

    def bd_names(self):
        return self.bidding.ids

    def bd_customers(self):
        return self.customer.ids

    def bd_addcustomer(self, coobj, user=None, do_commit=True):
        return self.customer.add(coobj, committer=user, do_commit=do_commit)

    def bd_deletecustomer(self, id, user=None, do_commit=True):
        return self.customer.remove(id, committer=user, do_commit=do_commit)

    def jd_get(self, id):
        return self.jobdescription.getyaml(id)

    def jd_add(self, jdobj, committer=None, unique=True, do_commit=True, **kwargs):
        result = False
        if jdobj.metadata['company'] in self.bidding.customers:
            result = self.jobdescription.add(jdobj, committer,
                                             unique=unique, do_commit=do_commit, **kwargs)
        return result

    def jd_modify(self, id, description, status, commentary, followup, committer, **kwargs):
        result = False
        if self.jobdescription.exists(id):
            result = self.jobdescription.modify(id, description, status,
                                           commentary, followup, committer, **kwargs)
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

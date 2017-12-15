import services.base.kv_storage
import services.base.name_storage


class SelectionCustomer(services.base.name_storage.NameStorage):

    ids_file = 'customers.json'


class SimulationCustomer(services.base.kv_storage.KeyValueStorage):

    YAML_DIR = 'YAML'
    YAML_TEMPLATE = (
    )

    list_item = {}
    fix_item  = {}

    def _templateinfo(self, committer):
        info = super(SimulationCustomer, self)._templateinfo(committer)
        info['responsible'] = committer
        return info

    def update_info(self, id, info, committer):
        bas_res = False
        prj_res = False
        baseinfo = dict()
        projectinfo = dict()
        for item in info:
            if item in dict(self.YAML_TEMPLATE):
                projectinfo[item] = info[item]
            else:
                baseinfo[item] = info[item]
        prj_res = self.saveinfo(id, projectinfo,
                                "Update %s information."%id, committer)
        for storage in self.storages:
            if storage.exists(id):
                bas_res = storage.saveinfo(id, baseinfo,
                                           "Update %s information."%id, committer)
                break
        return prj_res or bas_res


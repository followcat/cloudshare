import ujson

import utils.companyexcel
import core.outputstorage
import services.company
import services.base.simulation
import extractor.information_explorer


class SimulationCO(services.base.simulation.Simulation,
                   services.company.Company):

    YAML_TEMPLATE = (
        ("relatedcompany",     list),
        ("position",           list),
        ("clientcontact",      list),
        ("caller",             list),
        ("progress",           list),
        ("updatednumber",      list),
    )

    list_item = {"relatedcompany", "position", "clientcontact",
                 "caller", "progress", "updatednumber"}
    fix_item  = {"id", "name"}
    customers_file = 'customers.json'

    def __init__(self, path, name, cvstorage, iotype='git'):
        super(SimulationCO, self).__init__(path, name, cvstorage, iotype)
        self._customers = None

    def compare_excel(self, stream, committer):
        datas = list()
        output = list()
        excels = utils.companyexcel.convert(stream)
        for excel in excels:
            metadata = extractor.information_explorer.catch_coinfo(excel, excel['name'])
            data = core.basedata.DataObject(metadata, excel)
            datas.append(data)
        for key in self.list_item:
            for excel in excels:
                id = extractor.unique_id.company_id(excel['name'])
                caller = committer
                existvalues = list()
                if self.exists(id):
                    info = self.getyaml(id)
                    if excel['caller']:
                        caller = excel['caller'][0]
                    existvalues = [v['content'] for v in info[key]]
                for value in excel[key]:
                    if value in existvalues:
                        continue
                    existvalues.append(value)
                    output.append(('followup', (id, key, value, caller)))
        return output

    def addcustomer(self, id, user):
        result = False
        if id in self.customers or not self.exists(id):
            return result
        self.customers.add(id)
        self.interface.modify(self.customers_file,
                              ujson.dumps(sorted(self.customers), indent=4),
                              message="Add id: " + id + " to customers.\n",
                              committer=user)
        result = True
        return result

    def deletecustomer(self, id, user):
        result = False
        if id not in self.customers or not self.exists(id):
            return result
        self.customers.remove(id)
        self.interface.modify(self.customers_file,
                              ujson.dumps(sorted(self.customers), indent=4),
                              message="Delete id: " + id + " in customers.\n",
                              committer=user)
        result = True
        return result

    @property
    def customers(self):
        if self._customers is None:
            try:
                stream = self.interface.get(self.customers_file)
                self._customers = set(ujson.loads(stream))
            except IOError:
                self._customers = set()
                self.interface.add(self.customers_file,
                                   ujson.dumps(ujson.dumps(sorted(self._customers),
                                                           indent=4)))
        return self._customers

import ujson

import services.company
import services.base.simulation


class SimulationCO(services.base.simulation.Simulation,
                   services.company.Company):

    YAML_TEMPLATE = (
        ("position",           list),
        ("clientcontact",      list),
        ("caller",             list),
        ("progress",           list),
        ("updatednumber",      list),
    )

    list_item = {"position", "clientcontact", "caller", "progress", "updatednumber"}
    customers_file = 'customers.json'

    def __init__(self, path, name, cvstorage, iotype='git'):
        super(SimulationCO, self).__init__(path, name, cvstorage, iotype)
        self._customers = None

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

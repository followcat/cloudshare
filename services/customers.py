import os
import glob

import services.customer


class Customers(object):

    default_customer_name = 'default'

    def __init__(self, path, acc_repos, cv_repos, mult_peo):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.acc_repos = acc_repos
        self.cv_repos = cv_repos
        self.mult_peo = mult_peo
        self.customers = dict()
        for customer_path in glob.glob(os.path.join(self.path, '*')):
            if os.path.isdir(customer_path):
                name = os.path.split(customer_path)[1]
                customer = services.customer.Customer(acc_repos, cv_repos, mult_peo,
                                                      customer_path, name)
                customer.setup({'storageCV': 'cloudshare', 'storagePEO': 'peostorage'})
                self.customers[name] = customer
        self.load_default_customer()

    def load_default_customer(self):
        path = os.path.join(self.path, self.default_customer_name)
        customer = services.customer.DefaultCustomer(self.acc_repos,
                                                     self.cv_repos, self.mult_peo,
                                                     path, self.default_customer_name)
        customer.setup({'storageCV': 'cvindividual', 'storagePEO': 'peoindividual'})
        self.customers[self.default_customer_name] = customer

    def exists(self, name):
        return name in self.customers

    def create(self, name):
        assert not self.exists(name)
        path = os.path.join(self.path, name)
        customer = services.customer.Customer(self.acc_repos,
                                              self.cv_repos, self.mult_peo,
                                              path, name)
        customer.setup({'storageCV': 'cloudshare', 'storagePEO': 'peostorage'})
        self.customers[name] = customer

    def get(self, name):
        return self.customers[name]

    def use(self, name, id):
        result = self.customers[self.default_customer_name]
        if name:
            result = self.customers[name].use(id)
        return result

    def names(self):
        return self.customers.keys()

    def allprojects(self):
        result = dict()
        for each in self.customers:
            customer = self.customers[each]
            result.update(customer.projects)
        return result

    def backup(self, path):
        customers_path = os.path.join(path, "customers")
        os.mkdir(customers_path)
        for each in self.customers:
            customer = self.customers[each]
            customer.backup(customers_path)

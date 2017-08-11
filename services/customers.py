import os
import glob

import services.customer


class Customers(object):

    def __init__(self, path, acc_repos, co_repos, cv_repos, mult_peo):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.acc_repos = acc_repos
        self.co_repos = co_repos
        self.cv_repos = cv_repos
        self.mult_peo = mult_peo
        self.customers = dict()
        for customer_path in glob.glob(os.path.join(self.path, '*')):
            if os.path.isdir(customer_path):
                name = os.path.split(customer_path)[1]
                customer = services.customer.Customer(acc_repos, co_repos,
                                                      cv_repos, mult_peo,
                                                      customer_path, name)
                self.customers[name] = customer

    def exists(self, name):
        return name in self.customers

    def create(self, name):
        assert not self.exists(name)
        path = os.path.join(self.path, name)
        customer = services.customer.Customer(self.acc_repos, self.co_repos,
                                              self.cv_repos, self.mult_peo,
                                              path, name)
        self.customers[name] = customer

    def get(self, name):
        return self.customers[name]

    def use(self, name, id):
        return self.customers[name].use(id)

    def names(self):
        return self.customers.keys()

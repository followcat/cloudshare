import os
import glob

import services.customer


class Customers(object):

    def __init__(self, path, acc_repo, co_repo, cv_repo, mult_peo,):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.acc_repo = acc_repo
        self.co_repo = co_repo
        self.cv_repo = cv_repo
        self.mult_peo = mult_peo
        self.customers = dict()
        for customer_path in glob.glob(os.path.join(self.path, '*')):
            if os.path.isdir(customer_path):
                name = os.path.split(customer_path)[1]
                customer = services.customer.Customer(acc_repo, co_repo,
                                                      cv_repo, mult_peo,
                                                      customer_path, name)
                self.customers[name] = customer

    def exists(self, name):
        return name in self.customers

    def create(self, name):
        assert not self.exists(name)
        path = os.path.join(self.path, name)
        customer = services.customer.Customer(self.acc_repo, self.co_repo,
                                              self.cv_repo, self.mult_peo,
                                              self.customer_path, name)
        self.customers[name] = customer

    def get(self, name):
        return self.customers[name]

    def use(self, name, id):
        return self.customers.use(id)

    def names(self):
        return self.customers.keys()

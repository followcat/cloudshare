import os
import core.mining.lsimodel
import core.mining.lsisimilarity


class Mining(object):

    def __init__(self, path, svc_list, default_svc):
        self.sim = {}
        self.path = path
        self.lsi_model = None
        self.services = {
                'default': [default_svc],
                'all': svc_list
            }
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.make_lsi(self.services['default'])

    def setup(self, name):
        assert name in self.services
        self.add(self.services[name], name)
        return self.sim[name]

    def make_lsi(self, service):
        self.lsi_model = None
        lsi_path = os.path.join(self.path, 'model')
        lsi = core.mining.lsimodel.LSImodel(lsi_path)
        try:
            lsi.load()
        except IOError:
            if lsi.build(service):
                lsi.save()
        self.lsi_model = lsi

    def add(self, svc_list, name):
        assert self.lsi_model
        save_path = os.path.join(self.path, name)
        index = core.mining.lsisimilarity.LSIsimilarity(save_path, self.lsi_model)
        try:
            index.load()
        except IOError:
            if index.build(svc_list):
                index.save()
        self.sim[name] = index

    def update(self):
        self.lsi_model.update(self.services['default'])
        for name in self.sim:
            self.sim[name].update(self.services[name])

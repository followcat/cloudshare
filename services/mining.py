import os
import core.mining.lsimodel


class Mining(object):

    def __init__(self, path, svc_list, default_svc):
        self.lsi = {}
        self.path = path
        self.lssvc = svc_list
        self.defaultsvc = default_svc
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.add_default()
        self.add_all()

    def add_default(self):
        self.add([self.defaultsvc], 'default')

    def add_all(self):
        self.add(self.lssvc, 'all')

    def add(self, svc_list, name):
        lsi_path = os.path.join(self.path, name)
        lsi = core.mining.lsimodel.LSImodel(lsi_path)
        try:
            lsi.load()
        except IOError:
            if lsi.build(svc_list):
                lsi.save()
        self.lsi[name] = lsi
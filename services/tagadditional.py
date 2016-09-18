import os

import utils.builtin
import core.outputstorage


class TagsCurriculumVitae(object):

    config_file = 'config.json'
    ids_file = 'names.json'

    def __init__(self, name, path, additionals):
        self.name = name
        self.path = os.path.join(path, name)
        self.additionals = additionals
        self.cvids = dict()
        self.config = dict()
        try:
            self.load()
        except IOError:
            pass

    def setup(self, additionals, selected):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.additionals = dict([(a.name, a) for a in additionals])
        self.config['additionals'] = set(self.additionals.keys())
        self.config['selected'] = selected
        self.update()

    def load(self):
        self.config = utils.builtin.load_json(self.path, self.config_file)
        self.cvids = utils.builtin.load_json(self.path, self.ids_file)

    def save(self):
        utils.builtin.save_json(self.config, self.path, self.config_file)
        utils.builtin.save_json(self.cvids, self.path, self.ids_file)

    def update(self):
        for name in self.config['additionals']:
            svc_cv = self.additionals[name]
            for yamlname in svc_cv.yamls():
                if not self.exists(yamlname):
                    yamlinfo = svc_cv.getyaml(yamlname)
                    key = self.config['selected']['key']
                    values_set = self.config['selected']['value']
                    if key in yamlinfo:
                        keyset = set()
                        for each in yamlinfo[key].values():
                            keyset.update(each)
                        if keyset.intersection(values_set):
                            self._add(yamlname, name)
        self.save()

    def exists(self, name):
        id = core.outputstorage.ConvertName(name)
        return id in self.cvids

    def _add(self, name, svccv_name):
        id = core.outputstorage.ConvertName(name).base
        self.cvids[id] = svccv_name

    def yamls(self):
        for id in self.cvids:
            yield core.outputstorage.ConvertName(id).yaml

    def names(self):
        for id in self.cvids:
            yield core.outputstorage.ConvertName(id).md

    def id_svccv(self, name):
        id = core.outputstorage.ConvertName(name).base
        svccv_name = self.cvids[id]
        if svccv_name not in self.additionals:
            raise Exception('Not loaded db: %s.' % svccv_name)
        return self.additionals[svccv_name]

    def getmd(self, name):
        svccv = self.id_svccv(name)
        return svccv.getmd(name)

    def getyaml(self, name):
        svccv = self.id_svccv(name)
        return svccv.getyaml(name)

    def gethtml(self, name):
        svccv = self.id_svccv(name)
        return svccv.gethtml(name)

    def datas(self):
        for id in self.cvids:
            svccv = self.id_svccv(name)
            text = svccv.getmd(id)
            yield name, text

    @property
    def NUMS(self):
        return len(self.cvids)

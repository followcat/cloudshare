import os

import utils.builtin
import core.outputstorage


class TagsCurriculumVitae(object):

    config_file = 'config.json'
    ids_file = 'names.json'

    def __init__(self, name, path, cvstorage):
        self.name = name
        self.path = os.path.join(path, name)
        self.cvids = dict()
        self.config = dict()
        self.cvstorage = cvstorage
        try:
            self.load()
        except IOError:
            pass

    def setup(self, selected):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.config['selected'] = selected
        self.update()

    def load(self):
        self.config = utils.builtin.load_json(self.path, self.config_file)
        self.cvids = set(utils.builtin.load_json(self.path, self.ids_file))

    def save(self):
        utils.builtin.save_json(self.config, self.path, self.config_file)
        utils.builtin.save_json(self.cvids, self.path, self.ids_file)

    def update(self):
        for yamlname in self.cvstorage.yamls():
            if not self.exists(yamlname):
                yamlinfo = self.cvstorage.getyaml(yamlname)
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
        self.cvids.add(id)

    def yamls(self):
        for id in self.cvids:
            yield core.outputstorage.ConvertName(id).yaml

    def names(self):
        for id in self.cvids:
            yield core.outputstorage.ConvertName(id).md

    def getmd(self, name):
        return self.cvstorage.getmd(name)

    def getyaml(self, name):
        return self.cvstorage.getyaml(name)

    def gethtml(self, name):
        return self.cvstorage.gethtml(name)

    def datas(self):
        for name in self.names():
            text = self.cvstorage.getmd(name)
            yield name, text

    @property
    def NUMS(self):
        return len(self.cvids)

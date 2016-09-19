import os

import utils.builtin
import core.outputstorage


class SimulationCV(object):

    config_file = 'config.json'
    ids_file = 'names.json'

    def __init__(self, name, path, cvstorage):
        self.name = name
        self.path = os.path.join(path, name)
        self.cvids = set()
        self.config = dict()
        self.cvstorage = cvstorage
        try:
            self.load()
        except IOError:
            pass

    def setup(self):
        pass

    def update(self):
        pass

    def load(self):
        self.config = utils.builtin.load_json(self.path, self.config_file)
        self.cvids = set(utils.builtin.load_json(self.path, self.ids_file))

    def save(self):
        utils.builtin.save_json(self.config, self.path, self.config_file)
        utils.builtin.save_json(self.cvids, self.path, self.ids_file)

    def exists(self, name):
        id = core.outputstorage.ConvertName(name)
        return id in self.cvids

    def _add(self, name):
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

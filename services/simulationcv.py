import os

import utils.builtin
import core.outputstorage


class SimulationCV(object):

    ids_file = 'names.json'

    YAML_TEMPLATE = (
        ("committer",           list),
        ("comment",             list),
        ("tag",                 list),
        ("tracking",            list),
    )

    def __init__(self, savedir, path, cvstorage):
        self.path = os.path.join(path, savedir)
        self.cvids = set()
        self.cvstorage = cvstorage
        try:
            self.load()
        except IOError:
            pass

    def load(self):
        self.cvids = set(utils.builtin.load_json(self.path, self.ids_file))

    def save(self):
        utils.builtin.save_json(sorted(self.cvids), self.path, self.ids_file,
                                indent=4)

    def generate_info_template(self):
        info = {}
        for each in self.YAML_TEMPLATE:
            info[each[0]] = each[1]()
        return info

    def exists(self, name):
        id = core.outputstorage.ConvertName(name).base
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
        if not self.exists(name):
            return None
        return self.cvstorage.getmd(name)

    def getyaml(self, name):
        if not self.exists(name):
            return None
        return self.cvstorage.getyaml(name)

    def gethtml(self, name):
        if not self.exists(name):
            return None
        return self.cvstorage.gethtml(name)

    def datas(self):
        for name in self.names():
            text = self.cvstorage.getmd(name)
            yield name, text

    @property
    def NUMS(self):
        return len(self.cvids)
